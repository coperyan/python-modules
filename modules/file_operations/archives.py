import os
import shutil


def create_archive(source_path: str = None, format: str = "zip", base_name: str = None):
    """Create RAR/ZIP archive 

    Parameters
    ----------
        source_path (str, optional): str, default None
            os path to zip -- defaults to current dir if None
        format (str, optional): str, default zip
            archive extension
        base_name (str, optional): str, default None
            name of archive file
                (defaults to last folder in path if None

    """
    if not base_name:
        if os.path.isdir(source_path):
            base_name = f"{os.path.basename(source_path)}"
        else:
            base_name = f"{os.path.splitext(os.path.basename(source_path))[0]}"
    shutil.make_archive(base_name, format, source_path)
