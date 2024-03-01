import argparse
import os
import sys
import importlib
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Glosser un fichier CoNLL")
    parser.add_argument("command", choices=["store", "attach", "exit"], help="Commande à exécuter")
    parser.add_argument("--conll-file", help="Fichier CoNLL à utiliser")
    parser.add_argument("--out-conll", help="Nom du fichier de sortie pour la commande 'attach'")

    args = parser.parse_args()

    if args.command == "store":
        commande11 = ['python3', 'store_char.py', 'Gloss1.txt']
        commande12 = ['python3', 'store_word2.py', 'Gloss2.txt']
        commande13 = ['python3', 'store_word3.py', 'Gloss3.txt']
        
        if not args.conll_file:
            print("Vous devez spécifier un fichier CoNLL avec --conll-file pour la commande 'store'.")
            sys.exit(1)

        commande11.append(args.conll_file)
        commande12.append(args.conll_file)
        commande13.append(args.conll_file)
        subprocess.run(commande11, check=True)
        subprocess.run(commande12, check=True)
        subprocess.run(commande13, check=True)
        subprocess.run(['python3', 'store.py'], check=True)
        print('Vos dictionnaires se trouveront dans le dossier dico.')
        print('\n')

    elif args.command == "attach":
        if not args.conll_file:
            print("Vous devez spécifier un fichier CoNLL avec --conll-file pour la commande 'attach'.")
            sys.exit(1)
        if not args.out_conll:
            print("Vous devez spécifier un nom de fichier de sortie avec --out-conll pour la commande 'attach'.")
            sys.exit(1)
        
        commande2 = ['python3', 'attach.py', args.conll_file, args.out_conll]
        subprocess.run(commande2, check=True)
        print('Votre fichier CoNLL résultant se trouvera dans le dossier result.')
        print('\n')

    else:
        print("Commande invalide.")

if __name__ == "__main__":
    main()
    
    
#### Exemple : 
# python3 run.py store --conll-file chinese-beginner.A1.mSUD.conllu
# python3 run.py attach --conll-file chinese-beginner.A1.mSUD.conllu --out-conll outA1.conll


