import os
import shutil


def delete_file(file_path: str) -> None:
    """Removes file from OS"""
    os.remove(file_path)


def copy_file(old_path: str, new_path: str) -> None:
    """Copies file from old->new path"""
    shutil.copy(old_path, new_path)


def read_file(file_path: str, replace_str: dict, **kwargs) -> str:
    """Reads file w/ kwargs or replace str if needed
    Params:
        file_path
        replace_str: dict of instances to replace
        kwargs: apply to file params
    """
    with open(file_path, "r") as f:
        fstr = "".join([x for x in f.read()])
    for k, v in replace_str.items():
        fstr = fstr.replace(k, v)
    fstr = fstr.format_map(kwargs)
    return fstr


def get_file_size_mb(file_path):
    """Get file size in MB"""
    return round(os.path.getsize(file_path) / 1024.00 / 1024.00, 2)
