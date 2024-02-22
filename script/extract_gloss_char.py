import re
import requests
from bs4 import BeautifulSoup


def before_punct(string, punct):
    for char in string:
        if char in punct:
            return string.split(char)[0]
    return string


def remove_non_word(input_string):
    non_word_chars_pattern = re.compile(r'\W+')

    match = re.search(r'\w+', input_string)

    if match:
        start, end = match.start(), match.end()

        # Remove non-word characters before and after the word
        cleaned_string = non_word_chars_pattern.sub('', input_string[start:end])

        return cleaned_string
    else:
        return input_string

def underline(mot):
    # Replace spaces with underscores
    mot = re.sub(' ', '_', mot)

    # Keep only the part of the word before the first non-ASCII character
    mot = re.split('[^\x00-\x7F]', mot)[0]

    # Remove consecutive underscores at the beginning and end
    mot = re.sub('^_+|_+$', '', mot)

    return remove_non_word(mot)


def get_cara_gloss(chinese_character):
    punct = [',', ';', '.', '?', ':', '!']
    letter_pattern = re.compile(r'^[a-zA-Z]$')

    if letter_pattern.match(chinese_character):
        return chinese_character

    search_url = f"https://en.wiktionary.org/wiki/{chinese_character}"

    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        definitions_section = soup.find('span', {'id': 'Definitions'})
        ety_section = soup.find('span',{'id':'Etymology_1'})
        extra_section=soup.find('table',{'class','wikitable mw-collapsible mw-collapsed'})
        
        
        if definitions_section:   
            gloss_section = definitions_section.find_next('ol')
            reference = definitions_section.find_next("table") 
            # pages which have direct glose
        
            if gloss_section and not gloss_section.text.strip().startswith("Alternative"):
                first_li = gloss_section.find('li')
                #print(first_li)
                gloss_def = ''
                
                for ele in first_li:
                    #print(ele)
                    if ele.name == 'dl' or ele.name=='ul':
                        break
                    gloss_def += str(ele)
                                    
                if gloss_def :
                    pattern1 = r'<[^>]+>'
                    result1 = re.sub(pattern1, '', gloss_def)
                    pattern2 = r'\([^)]*\)'
                    result = re.sub(pattern2, '', result1)
                    result = before_punct(result,punct)
                    return underline(result)

            # pages which have "-see" reference for glose
            elif reference: 
                reference = definitions_section.find_next("table")
                gloss_sect2 = [b for b in soup.find_all("b") if "see" in b.text][0].text
                #print(gloss_sect2)
                match = re.search(r'“(.*?)”', gloss_sect2)

                if match:
                    gloss_p = match.group(1)
                    result2 = gloss_p.split(';')[0].strip()   
                    result2 = before_punct(result2,punct)
                    return underline(result2)
                
        #pages without "Definitions" but "Etymology_1,2..."
        elif ety_section:
            reference = ety_section.find_next("table")
            gloss_sect3 = [b for b in soup.find_all("b") if "see" in b.text][0].text
            #print(gloss_sect2)
            match = re.search(r'“(.*?)”', gloss_sect3)

            if match:
                gloss_p = match.group(1)
                result3 = gloss_p.split(';')[0].strip()
                result3 = before_punct(result3,punct)
                return underline(result3)
        elif extra_section:
            gloss_sect2 = [b for b in soup.find_all("b") if "see" in b.text][0].text
            #print(gloss_sect2)
            match = re.search(r'“(.*?)”', gloss_sect2)

            if match:
                gloss_p = match.group(1)
                result2 = gloss_p.split(';')[0].strip()   
                result2 = before_punct(result2,punct)
                return underline(result2)

            
    return "_"

def get_chinese_gloss(result):
    punct_pattern = re.compile(r'^\W+$')
    if 'This_term_needs_a' in get_cara_gloss(result) or 'Only_used_in' in get_cara_gloss(result):
        return '_'
    elif punct_pattern.match(result):
        return result
    else:
        return get_cara_gloss(result)

#chinese_character = "Q"
#chinese_gloss = get_chinese_gloss(chinese_character)
#print(f"{chinese_character}的第一个释义内容：{chinese_gloss}")


