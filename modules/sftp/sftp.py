from .config import *

import os
import pysftp


def get_conn(host: str = HOST, username: str = USER, password: str = PASSWORD):
    pysftp.Connection(host=host, username=username, password=password)


def list_files(
    host: str,
    username: str,
    password: str,
    path: str = None,
    exclude_dirs: bool = True,
    exclude_files: list = None,
    exclude_ext: list = None,
) -> list:
    files = []

    with get_conn(host, username, password) as svc:
        for f in svc.listdir(path):
            files.append(os.path.join(path, f))

    if exclude_dirs:
        files = [f for f in files if not os.path.isdir(f)]

    if exclude_files:
        files = [f for f in files if os.path.basename(f) not in exclude_files]

    if exclude_ext:
        files = [f for f in files if os.path.splitext(f)[1] not in exclude_ext]

    return files


def get_file(
    host: str, username: str, password: str, remote_path: str, local_path: str = None
):
    with get_conn(host, username, password) as svc:
        svc.get(
            remote_path, (local_path if local_path else os.path.basename(remote_path))
        )


def put_file(
    host: str, username: str, password: str, local_path: str, remote_path: str = None
):
    with get_conn(host, username, password) as svc:
        svc.get(
            local_path, (remote_path if remote_path else os.path.basename(local_path))
        )
