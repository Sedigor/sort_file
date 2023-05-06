import os
import shutil

def sort_files_by_extension(directory):
    # створюємо словник для зберігання файлів за розширенням
    extensions = {}

    # проходимося по всіх файлах у папці
    for filename in os.listdir(directory):
        # отримуємо повний шлях до файлу
        path = os.path.join(directory, filename)

        # перевіряємо, чи є файл
        if os.path.isfile(path):
            # отримуємо розширення файлу
            extension = os.path.splitext(filename)[1]

            # створюємо каталог, якщо його ще немає
            if extension not in extensions:
                os.makedirs(os.path.join(directory, extension))
                extensions[extension] = os.path.join(directory, extension)

            # переміщуємо файл до відповідного каталогу
            shutil.move(path, extensions[extension])

    # видаляємо порожні каталоги та підкаталоги з необмеженою кількістю вкладеності
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)