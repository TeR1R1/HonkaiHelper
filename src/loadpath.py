import os

def list_files(path, level=0):
    print("| " * level + "+--", os.path.basename(path) + "/")

    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isdir(file_path):
            list_files(file_path, level+1)
        else:
            print("| " * (level+1) + "+--", file_name)

if __name__ == '__main__':
    directory = './src'
    list_files(directory)