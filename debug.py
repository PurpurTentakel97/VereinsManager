# Purpur Tentakel
# 21.01.2022
# VereinsManager / SQLite


def debug(item, keyword, message) -> None:
    print(f"+++++ Debug.LOG  // {item} // {keyword} // {message} +++++")


def error(item, keyword, message) -> None:
    print(f"+++++ ERROR.LOG // {item} // {keyword} // {message} +++++")


def info(item, keyword, message) -> None:
    print(f"+++++ Info.LOG // {item} // {keyword} // {message} +++++")
