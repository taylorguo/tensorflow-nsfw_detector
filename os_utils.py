#! usr/bin/env python
# coding: utf-8
# Python 3.6.3

import os 

def get_file_list(file_dir):
    files_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if (not file.startswith(".")) and (os.path.splitext(file)[1] == ".jpe" or ".jpeg" or ".png"):
                files_list.append(os.path.join(root,file))
    return files_list

if __name__ == "__main__":
    print("\nfile_name: ",get_file_list("dataset"))