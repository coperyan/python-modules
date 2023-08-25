import os
import pathlib
from azure.storage.blob import ContainerClient

from .config import *

# from .constants import *


class AzureCloudStorage:
    def __init__(
        self, conn_str: str = CONNECTION_STR, container_name: str = CONTAINER_NAME
    ):
        self._set_container_client(conn_str, container_name)

    def _set_container_client(self, conn_str: str, container_name: str):
        self.container_client = ContainerClient.from_connection_string(
            conn_str=conn_str, container_name=container_name
        )

    def upload_blob(self, file: str, prefix: str = None, purge_local: bool = False):
        if prefix:
            remote_file = f"{prefix}/{file}"
        else:
            remote_file = file
        blob_client = self.container_client.get_blob_client(blob=remote_file)
        with open(file, "rb") as data:
            blob_client = self.container_client.upload_blob(
                name=remote_file, data=data, overwrite=True
            )
        if purge_local:
            os.remove(file)
        return remote_file

    def upload_blobs(
        self, files: list, prefix: str = None, purge_local: bool = False
    ) -> list:
        uploaded_files = []
        for local_file in files:
            iter_file = self._upload_blob(
                file=local_file, prefix=prefix, purge_local=purge_local
            )
            uploaded_files.append(iter_file)

        return uploaded_files
