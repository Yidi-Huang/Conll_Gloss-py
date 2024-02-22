import requests
from bs4 import BeautifulSoup
import re

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

def get_mc_gloss(chinese_mc):
    punct = [',', ';', '.', '?', ':', '!']

    search_url = f"https://en.wiktionary.org/wiki/{chinese_mc}"

    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        reference = soup.find('table', {'class': 'wikitable mw-collapsible mw-collapsed'})
        hint_section = soup.find('strong', {'class': 'Hani headword'})
            
        if hint_section:
            gloss_section = hint_section.find_next('ol')
            if gloss_section:
                first_li = gloss_section.find('li')
                while first_li and not first_li.text.strip():
                    # If the first li has no content, search for the next one
                    first_li = first_li.find_next('li')

                if first_li:
                    gloss_def = ''

                
                for ele in first_li:
                    if ele.name == 'dl' or ele.name=='ul':
                        break
                    gloss_def += str(ele)
                                    
                if gloss_def:
                    pattern1 = r'<[^>]+>'
                    result1 = re.sub(pattern1, '', gloss_def)
                    pattern2 = r'\([^)]*\)'
                    result = re.sub(pattern2, '', result1)
                    result = before_punct(result,punct)
                    return underline(result)
        elif reference: 
            gloss_sect2 = [b for b in soup.find_all("b") if "see" in b.text][0].text
            #print(gloss_sect2)
            match = re.search(r'“(.*?)”', gloss_sect2)

            if match:
                gloss_p = match.group(1)
                result2 = gloss_p.split(';')[0].strip()   
                result2 = before_punct(result2,punct)
                result2 = re.sub(' ', '_', result2)
                return result2
    return "_"


def out_mot3(output1):
    lines = output1.split('\n')
    lwg=[]
    if lines!=['']:
    #get each character in the phrase
        lm=[line.split('\t')[1] for line in lines]
        

        # if it is a word with 3 characters
        for i in range(len(lm)-2):
            m3 = ''.join(lm[i:i+3])
            wordgloss=get_mc_gloss(m3)
            lwg.append(wordgloss)
            
    return lwg
    
def out_mot2(output2):
    lines = output2.split('\n')
    lwg2=[]
    #get each character in the phrase
    if lines!=['']:
        lm=[line.split('\t')[1] for line in lines]
        

        # if it is a word with 2 characters
        for k in range(len(lm)-1):
            m2 = ''.join(lm[k:k+2])
            if 'Inword' not in lines[k] and 'Gloss_word' not in lines[k]: # to avoid overlaps like "对不起" and "不起"
                wordgloss=get_mc_gloss(m2)
            else:
                wordgloss='_'
            lwg2.append(wordgloss)
    return lwg2
