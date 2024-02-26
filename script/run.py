# Ce fichier devrait prendre en entrée un fichier conll et ressortir en sortie un fichier conll glosé
import argparse
import os
import sys
import importlib
import subprocess

def main():
    while True:
        command = input("Entrez votre commande (store/attach/exit) : ").strip().lower()
        if command == "exit":
            print("Exit")
            break
        elif command == "store":
            commande11=['python3','store_char.py','Gloss1.txt']
            commande12=['python3','store_word2.py','Gloss2.txt']
            commande13=['python3','store_word3.py','Gloss3.txt']
            consource = input("Entrez le conll que vous voulez appliquer, il doit se trouver dans le dossier conll (ex. chinese-beginner.A1.mSUD.conllu) :")
            commande11.append(consource)
            commande12.append(consource)
            commande13.append(consource)
            subprocess.run(commande11,check=True)
            subprocess.run(commande12,check=True)
            subprocess.run(commande13,check=True)
            subprocess.run(['python3','store.py'],check=True)
            print('Vos dicos se trouveront dans le dossier dico.')
            print('\n')

        elif command == "attach":
            commande2=['python3','attach.py']
            source = input("Entrez le conll que vous voulez appliquer, il doit se trouver dans le dossier conll (ex. chinese-beginner.A1.mSUD.conllu) :")
            outconll = input("Entrez le nom de votre résultat conll (ex. outA1.conll) : ")
            commande2.append(source)
            commande2.append(outconll)
            subprocess.run(commande2,check=True)
            print('Votre résultat conll se trouvera dans le dossier result.')
            print('\n')

        else:
            print("Commande invalide.")

if __name__ == "__main__":
    main()

