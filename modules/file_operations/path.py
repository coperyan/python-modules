import os


def list_files(
    path: str,
    recursive: bool = False,
    exclude_files: list = None,
    exclude_dirs: bool = True,
    exclude_ext: list = None,
) -> list:
    files = []
    if recursive:
        for root, dirs, files in os.walk(path):
            for f in files:
                files.append(os.path.join(root, f))
    else:
        for f in os.listdir(path):
            files.append(os.path.join(path, f))

    if exclude_dirs:
        files = [f for f in files if not os.path.isdir(f)]

    if exclude_files:
        files = [f for f in files if os.path.basename(f) not in exclude_files]

    if exclude_ext:
        files = [f for f in files if os.path.splitext(f)[1] not in exclude_ext]

    return files
