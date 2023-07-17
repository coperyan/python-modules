import os
import shutil


def create_archive(source_path: str = None, format: str = "zip", base_name: str = None):
    """Creates archive file from folder
    Params:
        source_path: folder to zip
        format: zip, rar, etc
        base_name: name of file
    """
    if not base_name:
        if os.path.isdir(source_path):
            base_name = f"{os.path.basename(source_path)}"
        else:
            base_name = f"{os.path.splitext(os.path.basename(source_path))[0]}"
    shutil.make_archive(base_name, format, source_path)
