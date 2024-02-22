import sys
import re
from tqdm import tqdm

from extract_gloss_word import out_mot2

def store_gloss2(dico_file,conll_file):
    # Initialize a set to store already added words
    added_words = set()
    with open(dico_file, 'r') as file:
        dico = file.readlines()
        added_words = set(ele.split(' ')[0] for ele in dico)
    
    with open(conll_file, 'r') as file:
        t = file.read()
        text = [conll for conll in t.split("\n\n")]
        with open("../dico/tmp2.txt", "w") as output_file:
            for conll in tqdm(text, desc="Processing", unit="conll"):
                conlist = [l for l in conll.split("\n") if not l.startswith('#')]
                con = '\n'.join(conlist)
                chin_list = [l.split('\t')[1] for l in conlist if l]
                glo_li2 = out_mot2(con)
                for i in range(len(glo_li2)):
                    if glo_li2[i] != '_' and (chin_list[i] + chin_list[i+1]) not in added_words:
                        # Add the word to the set
                        added_words.add(chin_list[i] + chin_list[i+1])
                        # Write to output file
                        print(chin_list[i] + chin_list[i+1], glo_li2[i], file=output_file)


if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python store_word2.py Gloss2.txt conll_file")
        sys.exit(1)

    dico_file = "../dico/" + sys.argv[1]
    conll_file = sys.argv[2]
    store_cara_gloss(dico_file, conll_file)

