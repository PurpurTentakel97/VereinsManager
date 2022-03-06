# Purpur Tentakel
# 21.01.2022
# VereinsManager / SQLite

is_debug: bool = True
is_debug_item: bool = False
debug_item: str = "MEMBERS WINDOW"
is_debug_keyword: bool = False
debug_keyword: str = "Phonenumbers"

is_info: bool = True
is_info_item: bool = False
info_item: str = "MEMBERS WINDOW"
is_info_keyword: bool = False
info_keyword: str = "Phonenumbers"


def debug(item, keyword, message) -> None:
    if is_debug:
        if is_debug_item and item == debug_item:
            print(f"+++++ Debug.LOG // {item} // {keyword} // {message} +++++")
        elif is_debug_keyword and keyword == debug_keyword:
            print(f"+++++ Debug.LOG // {item} // {keyword} // {message} +++++")
        elif not is_debug_keyword and not is_debug_item:
            print(f"+++++ Debug.LOG // {item} // {keyword} // {message} +++++")


def info(item, keyword, message) -> None:
    if is_info:
        if is_info_item and item == info_item:
            print(f"+++++ Info.LOG // {item} // {keyword} // {message} +++++")
        elif is_info_keyword and keyword == info_keyword:
            print(f"+++++ Info.LOG // {item} // {keyword} // {message} +++++")
        elif not is_info_keyword and not is_info_item:
            print(f"+++++ Info.LOG // {item} // {keyword} // {message} +++++")


def error(item, keyword, message) -> None:
    print(f"+++++ ERROR.LOG // {item} // {keyword} // {message} +++++")
