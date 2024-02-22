import sys
import re
from tqdm import tqdm

from extract_gloss_word import out_mot3

def store_gloss3(dico_file,conll_file):
    # Initialize a set to store already added words
    added_words = set()
    with open(dico_file, 'r') as file:
        dico = file.readlines()
        added_words = set(ele.split(' ')[0] for ele in dico)
    
    with open(conll_file, 'r') as file:
        t = file.read()
        text = [conll for conll in t.split("\n\n")]
        with open("../dico/tmp3.txt", "w") as output_file:
            for conll in tqdm(text, desc="Processing", unit="conll"):
                conlist = [l for l in conll.split("\n") if not l.startswith('#')]
                con = '\n'.join(conlist)
                chin_list = [l.split('\t')[1] for l in conlist if l]
                glo_li3 = out_mot3(con)

                for k in range(len(glo_li3)):
                    if glo_li3[k] != '_' and (chin_list[k] + chin_list[k+1] + chin_list[k+2]) not in added_words:
                        # Add the word to the set
                        added_words.add(chin_list[k] + chin_list[k+1] + chin_list[k+2])
                        # Write to output file
                        print(chin_list[k] + chin_list[k+1] + chin_list[k+2], glo_li3[k], file=output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python store_word3.py Gloss3.txt conll_file")
        sys.exit(1)

    dico_file = "../dico/" + sys.argv[1]
    conll_file = sys.argv[2]
    store_cara_gloss(dico_file, conll_file)

