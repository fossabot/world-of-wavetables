def remove_prefix(string: str, prefix: str):
    if string.startswith(prefix):
        return string[len(prefix):]
    return string

def strip_symbols_from_path_name(string: str):
    new_string = remove_prefix(string, "\\")
    new_string = remove_prefix(new_string, "/")
    new_string = remove_prefix(new_string, ".\\")
    new_string = remove_prefix(new_string, ".")
    return new_string