import os
import requests


def download_file_from_url(url: str, save_path: str = "download") -> None:
    """Downloads/chunks file from URL

    Parameters
    ----------
        url : str
        save_path (str, optional): str, default "download"
            local directory to save file in
    """
    with requests.get(url, allow_redirects=True, stream=True) as r:
        r.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def download_zipped_file(url: str, headers: dict = None):
    return None
