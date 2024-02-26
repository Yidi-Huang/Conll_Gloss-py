import os


base_path = '../dico/'

# temporary dico to complete dico
files_to_copy = {
    'tmp1.txt': 'Gloss1.txt',
    'tmp2.txt': 'Gloss2.txt',
    'tmp3.txt': 'Gloss3.txt'
}

def main():
    for source_file, destination_file in files_to_copy.items():
        source_path = os.path.join(base_path, source_file)
        destination_path = os.path.join(base_path, destination_file)
        
        # 读取源文件内容
        with open(source_path, 'r') as source:
            content = source.read()
        
        # 将内容追加到目标文件
        with open(destination_path, 'a') as destination:
            destination.write(content)

if __name__ == "__main__":
    main()

