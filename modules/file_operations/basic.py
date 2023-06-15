import os
import shutil


def delete_file(file_path: str) -> None:
    os.remove(file_path)


def copy_file(old_path: str, new_path: str) -> None:
    shutil.copy(old_path, new_path)


def read_file(file_path: str, **kwargs) -> str:
    with open(file_path, "r") as f:
        fstr = "".join([x for x in f.read()])
    fstr = fstr.format_map(kwargs)
    return fstr
