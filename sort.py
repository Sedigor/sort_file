import sys
import os
import shutil
from pathlib import Path


extensions = {
    "images": ['JPEG', 'PNG', 'JPG', 'SVG'],
    "documents": ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    "audio": ['MP3', 'OGG', 'WAV', 'AMR'],
    "video": ['AVI', 'MP4', 'MOV', 'MKV'],
    "archives": ['ZIP', 'GZ', 'TAR']
}


def make_trans_dict():
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    return TRANS


def get_folder_path():
    return " ".join(sys.argv[1:])


def create_folders(folder_path, f_extensions):
    for folder in f_extensions.keys():
        if not os.path.exists(f"{folder_path}\\{folder}"):
            os.mkdir(f"{folder_path}\\{folder}")


def dict_split(some_dict):
    key_list = []
    value_list = []
    for k, v in some_dict.items():
        key_list.append(k)
        value_list.append(v)
    return key_list, value_list


def normalize(file_name):
    trans_map = make_trans_dict()
    new_name = file_name.translate(trans_map)
    new_file_name = ""
    for symbol in new_name:
        symbol.translate(trans_map)
        if not symbol.isalpha():
            new_file_name += "_"
            continue
        new_file_name += symbol
    return new_file_name
            

def sort_files(folder_path, f_extensions):
    dest_folders = dict_split(f_extensions)[0]
    ext_check = dict_split(f_extensions)[1]
    for f in os.listdir(folder_path):
        file_path = os.path.join(folder_path, f)
        if os.path.isfile(file_path):
            f_extension = Path(file_path).suffix
            for i in range(len(dest_folders)):
                if f_extension[1:].upper() in ext_check[i]:
                    try:
                        shutil.move(file_path, f"{main_path}\\{dest_folders[i]}")
                    except:
                        os.remove(file_path)
        else:
            sort_files(file_path, extensions)
            
            
def remove_empty_folders(folder_path):
    for sub_dir in os.listdir(folder_path):
        sub_path = os.path.join(folder_path, sub_dir)
        if os.path.isdir(sub_path):
            if not os.listdir(sub_path):
                os.rmdir(sub_path)
            else:
                remove_empty_folders(sub_path)
                

def rename_files_and_folders(folder_path):
    for f in os.listdir(folder_path):
        f_path = os.path.join(folder_path, f)
        f_name = Path(f_path).name.split(".")[0]
        f_extension = Path(f_path).suffix
        new_name = normalize(f_name)
        os.rename(f_path, f"{folder_path}\\{new_name}{f_extension}")
    for new_f in os.listdir(folder_path):
        f_new_path = os.path.join(folder_path, new_f)
        if os.path.isdir(f_new_path):
            rename_files_and_folders(f_new_path)
                
                
def archive_to_folder(folder_path):
    for archive in os.listdir(f"{folder_path}\\archives"):
        file_path = f"{folder_path}\\archives\\{archive}"
        if os.path.isfile(file_path):
            archive_name = Path(file_path).name.split(".")[0]
            shutil.unpack_archive(file_path, f"{folder_path}\\archives\\{archive_name}")
            os.remove(file_path)
                

if __name__ == "__main__":
    # main_path = get_folder_path()
    main_path = "D:\\sort_folder"
    create_folders(main_path, extensions)
    sort_files(main_path, extensions)
    rename_files_and_folders(main_path)
    archive_to_folder(main_path)
    remove_empty_folders(main_path)