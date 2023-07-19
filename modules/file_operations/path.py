import os


def list_files(
    path: str,
    contains: str = None,
    recursive: bool = False,
    exclude_files: list = None,
    exclude_dirs: bool = True,
    exclude_ext: list = None,
) -> list:
    """List files in directory
    Params:
        path: str of relative path
        contains: keyword that must be contained in filename
        recursive: search within subfolders, dirs, etc
        exclude_files: file (basenames) to exclude
        exclude_dirs: file (subdirs) to exclude
        exclude_ext: file (extensions) to exclude
    Returns:
        list of full filenames
    """
    files = []
    if recursive:
        for root, dirs, files in os.walk(path):
            for f in files:
                files.append(os.path.join(root, f))
    else:
        for f in os.listdir(path):
            files.append(os.path.join(path, f))

    if contains:
        files = [f for f in files if contains in os.path.basename(f)]

    if exclude_dirs:
        files = [f for f in files if not os.path.isdir(f)]

    if exclude_files:
        files = [f for f in files if os.path.basename(f) not in exclude_files]

    if exclude_ext:
        files = [f for f in files if os.path.splitext(f)[1] not in exclude_ext]

    return files
