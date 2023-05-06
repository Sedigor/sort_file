import sys
import os
import shutil
import pathlib


extensions = {
    "images": ['JPEG', 'PNG', 'JPG', 'SVG'],
    "documents": ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    "audio": ['MP3', 'OGG', 'WAV', 'AMR'],
    "video": ['AVI', 'MP4', 'MOV', 'MKV'],
    "archives": ['ZIP', 'GZ', 'TAR'],
    "other": []
}

a = Path(sys.argv[1])

def get_folder_path():
    
    """this function gets path to folder for sort"""
    
    f_path = Path(sys.argv[1])
    
    return sys.argv[1]


def create_folders(folder_path, f_extensions):
    
    """this function create folders from dict"""
    
    for folder in f_extensions.keys():
        if not os.path.exists(f"{folder_path}\\{folder}"):
            os.mkdir(f"{folder_path}\\{folder}")


def get_subfolder_path(folder_path):

    """this function gets subfolder path"""
    
    subfolder_paths = []
    for folder in os.scandir(folder_path):
        if folder.is_dir():
            subfolder_paths.append(folder.path)
    return subfolder_paths


def get_file_paths(folder_path):
    
    """this function gets path to file"""
        
    file_paths = []
    for f in os.scandir(folder_path):
        if f.is_file():
            file_paths.append(f.path)
    return file_paths


def dict_split(some_dict):
    key_list = []
    value_list = []
    for k, v in some_dict.items():
        key_list.append(k)
        value_list.append(v)
    return (key_list, value_list)


def sort_files(folder_path, f_extensions):
    dest_folders, ext_check = dict_split(f_extensions)
    for f in os.listdir(folder_path):
        file_path = os.path.join(folder_path, f)
        if os.path.isfile(file_path):
            f_extension = file_path.rsplit(".")[-1]
            for i in range(len(dest_folders)):
                if f_extension.upper() in ext_check[i]:
                    try:
                        shutil.move(file_path, f"{main_path}\\{dest_folders[i]}")
                    except:
                        os.remove(file_path)
            if os.path.exists(file_path):
                shutil.move(file_path, f"{main_path}\\other")
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
                

if __name__ == "__main__":
    #main_path = "D:\\folder for sort"
    main_path = get_folder_path()
    print(main_path)
    create_folders(main_path, extensions)
    sort_files(main_path, extensions)
    remove_empty_folders(main_path)