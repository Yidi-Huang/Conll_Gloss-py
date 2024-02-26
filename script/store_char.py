import sys
import re
from tqdm import tqdm
from extract_gloss_char import get_chinese_gloss


def store_cara_gloss(dico_file, conll_file):
    # Initialize a set to store already added words
    added_words = set()
    with open(dico_file, 'r') as file:
        dico = file.readlines()
        added_words = set(ele.split(' ')[0] for ele in dico)
    
    with open(conll_file, 'r') as file:
        t = file.read()
        text = [conll for conll in t.split("\n\n")]
        with open("../dico/tmp1.txt", "w") as output_file:
            for conll in tqdm(text, desc="Processing", unit="conll"):
                conlist = [l for l in conll.split("\n") if not l.startswith('#')]
                chin_list = [l.split('\t')[1] for l in conlist if l]
                for i in range(len(chin_list)):
                    if chin_list[i] not in added_words:
                        # Add the word to the set
                        added_words.add(chin_list[i])
                        # Write to output file
                        print(chin_list[i], get_chinese_gloss(chin_list[i]), file=output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python store_char.py Gloss1.txt conll_file")
        sys.exit(1)

    dico_file = "../dico/" + sys.argv[1]
    conll_file = "../conll/"+sys.argv[2]
    store_cara_gloss(dico_file, conll_file)

