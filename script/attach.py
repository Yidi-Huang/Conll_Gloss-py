import sys
import os


def attach_gloss1(source, conll, output_file):
    """
    Attach gloss from source to CONLL file and save the result to the output_file.
    """
    glossdico = {}

    # Read gloss dictionary from the source file
    with open(source, 'r') as file:
        dico = file.readlines()

        for ele in dico:
            parts = ele.split(' ')
            word = parts[0]
            gloss = parts[1][:-1]
            glossdico[word] = gloss

    # Process the CONLL file
    with open(conll, 'r') as file2:
        t = file2.read()
        text = [conll for conll in t.split("\n\n")]

        # Open output file for writing
        with open(output_file, 'w') as output:
            for conll in text:
                conlist = [l for l in conll.split("\n")]
                for l in conlist:
                    if not l.startswith('#') and ('Gloss' not in l) and l:
                        conlone = l.split('\t')
                        # Update the last column with the Gloss value from the dictionary
                        conlone[-1] = f'Gloss={glossdico[conlone[1]]}|' + conlone[-1]
                        nl = ('\t'.join(conlone))
                    else:
                        nl = l

                    # Write the modified line to the output file
                    output.write(''.join(nl) + '\n')

                # Add an empty line after each CONLL block
                output.write('\n')


def attach_gloss3(source, conll, output_file):
    """
    Attach gloss from source to CONLL file and save the result to the output_file.
    """
    glossdico = {}

    # Read gloss dictionary from the source file
    with open(source, 'r') as file:
        dico = file.readlines()

        for ele in dico:
            parts = ele.split(' ')
            word = parts[0]
            gloss = parts[1][:-1]
            glossdico[word] = gloss

    # Process the CONLL file
    with open(conll, 'r') as file2:
        t = file2.read()
        text = [conll for conll in t.split("\n\n")]

        # Open output file for writing
        with open(output_file, 'w') as output:
            for conll in text:
                tokenlist = []
                conlist = [l for l in conll.split("\n")]
                glosslist = []
                colones = []

                for l in conlist:
                    if not l.startswith('#') and ('Word_gloss' not in l) and l:
                        colones.append(l)
                        token = l.split('\t')[1]
                        tokenlist.append(token)

                counter1 = len(conlist) - len(colones)

                for i in range(len(tokenlist) - 2):
                    m3 = ''.join(tokenlist[i:i + 3])
                    if m3 in glossdico:
                        glosslist.append(glossdico[m3])
                    else:
                        glosslist.append("_")

                for j in range(len(glosslist)):
                    colone = colones[j].split('\t')

                    if glosslist[j] != '_' and 'Word_gloss' not in colone[-1] and 'Inword' not in colone[-1]:
                        colone[-1] += f'|Word_gloss={glosslist[j]}'
                        conlist[counter1 + j] = '\t'.join(colone)

                for k in range(len(conlist)):
                    if 'Word_gloss' in conlist[k]:
                        conlist[k + 1] += '|Inword=Yes'
                        conlist[k + 2] += '|Inword=Yes'

                output.write('\n'.join(conlist) + '\n\n')


def attach_gloss2(source, conll, output_file):
    """
    Attach gloss from source to CONLL file and save the result to the output_file.
    """
    glossdico = {}

    # Read gloss dictionary from the source file
    with open(source, 'r') as file:
        dico = file.readlines()

        for ele in dico:
            parts = ele.split(' ')
            word = parts[0]
            gloss = parts[1][:-1]
            glossdico[word] = gloss

    # Process the CONLL file
    with open(conll, 'r') as file2:
        t = file2.read()
        text = [conll for conll in t.split("\n\n")]

        # Open output file for writing
        with open(output_file, 'w') as output:
            for conll in text:
                tokenlist = []
                conlist = [l for l in conll.split("\n")]
                glosslist = []
                colones = []

                for l in conlist:
                    if not l.startswith('#') and l:
                        colones.append(l)
                        token = l.split('\t')[1]
                        tokenlist.append(token)

                counter1 = len(conlist) - len(colones)

                for i in range(len(tokenlist) - 1):

                    m3 = ''.join(tokenlist[i:i + 2])
                    if m3 in glossdico:
                        glosslist.append(glossdico[m3])
                    else:
                        glosslist.append("_")

                for j in range(len(glosslist)):
                    colone = colones[j].split('\t')

                    if glosslist[j] != '_' and 'Word_gloss' not in colone[-1] and 'Inword' not in colone[-1]:
                        colone[-1] += f'|Word_gloss2={glosslist[j]}'
                        if j + 1 < len(colones):
                            next_colone = colones[j + 1].split('\t')
                            next_colone[-1] += '|Inword=Yes'
                            colones[j + 1] = '\t'.join(next_colone)

                    conlist[counter1 + j] = '\t'.join(colone)

                for j in range(len(glosslist)):
                    colone = colones[j].split('\t')

                    if (
                        glosslist[j] != '_' and
                        'Word_gloss' not in colone[-1] and
                        'Inword' not in colone[-1] and
                        'Inword' not in conlist[counter1 + j + 1]
                    ):
                        colone[-1] += f'|Word_gloss2={glosslist[j]}'
                        conlist[counter1 + j] = '\t'.join(colone)

                for k in range(len(conlist)):
                    if 'Word_gloss2' in conlist[k]:
                        conlist[k + 1] += '|Inword=Yes'

                output.write('\n'.join(conlist))
                # Add an empty line after each CONLL block
                output.write('\n\n')


def replace_word_in_file(old_file, target_file):
    """
    Replace occurrences of 'Word_gloss2' with 'Word_gloss' in the specified file.
    """
    try:
        # Open the input file
        with open(old_file, 'r') as file:
            data = file.read()

        # Replace all occurrences of the old word with the new word
        data = data.replace('Word_gloss2', 'Word_gloss')

        # Write the modified data back to the file
        with open(target_file, 'w') as file:
            file.write(data)

    except FileNotFoundError:
        print(f"Error: File '{old_file}' not found.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 attach.py original_conll result_conll")
        sys.exit(1)

    original_conll = "../conll/"+sys.argv[1]
    

    source_directory = "../dico/"
    destination_directory = "../result/"
    
    result_conll = destination_directory+sys.argv[2]


    process1_conll = os.path.join(destination_directory, 'process1.conllu')
    process3_conll = os.path.join(destination_directory, 'process3.conllu')
    process2_conll = os.path.join(destination_directory, 'process2.conllu')

    attach_gloss1(os.path.join(source_directory, 'Gloss1.txt'), original_conll, process1_conll)
    attach_gloss3(os.path.join(source_directory, 'Gloss3.txt'), process1_conll, process3_conll)
    attach_gloss2(os.path.join(source_directory, 'Gloss2.txt'), process3_conll, process2_conll)

    replace_word_in_file(process2_conll, result_conll)

# Example usgae : python3 attach.py chinese-beginner.A1.mSUD.conllu outA1.conllu
