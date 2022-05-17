# Purpur Tentakel
# 17.05.2022
# VereinsManager / Count

from os import listdir
from os.path import isfile, join

files_count: int = 0
lines_count: int = 0
words_count: int = 0
characters_count: int = 0

files: list = [
    "debug.py",
    "main.py",
    "transition.py",
    "count.py",
]

directories: list = [
    "config",
    "helpers",
    "logic",
    "logic/data_handler",
    "logic/main_handler",
    "logic/pdf_handler",
    "logic/sqlite",
    "ui",
    "ui/dialog",
    "ui/frames",
    "ui/windows",
    "ui/windows/member_windows",
]

error_files: list = [
    "config/default_icon.png",
]


def _count_files(files: list) -> None:
    global files_count
    global lines_count
    global words_count
    global characters_count

    for f in files:
        if f in error_files:
            continue

        files_count += 1
        with open(f, "r") as file:
            for line in file:
                lines_count += 1
                words: list = line.split()
                words_count += len(words)
                characters_count += sum(len(word) for word in words)


if __name__ == "__main__":
    _count_files(files=files)

    for directory in directories:
        current_files: list = [f"{directory}/{f}" for f in listdir(directory) if isfile(join(directory, f))]
        _count_files(current_files)

    print("VereinsManager:")
    print(f"files: {files_count}")
    print(f"lines: {lines_count}")
    print(f"words: {words_count}")
    print(f"characters: {characters_count}")
