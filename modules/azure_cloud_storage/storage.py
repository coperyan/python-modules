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
        """Initialize Azure Storage Blob (Container Client) for uploads

        Parameters
        ----------
            conn_str : str
                connection string for container
            container_name : str
                container name
        """
        self.container_client = ContainerClient.from_connection_string(
            conn_str=conn_str, container_name=container_name
        )

    def upload_blob(
        self, file: str, prefix: str = None, purge_local: bool = False
    ) -> str:
        """Upload Single Blob to Azure Storage Container

        Parameters
        ----------
            file : str
                local_path to file
            prefix (str, optional): str, default None
                destination path within azure container
                ex. `containerFolder/containerSubFolder` resolves to
                `container/containerFolder/containerSubFolder/file`
            purge_local (bool, optional): bool, default False
                whether to delete local file after successful upload

        Returns
        -------
            str
                remote file path
        """
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
        """Upload blobs to Azure Storage Container

        Parameters
        ----------
            files : list
                list of files to upload
            prefix (str, optional): str, default None
                destination path within azure container
                ex. `containerFolder/containerSubFolder` resolves to
                `container/containerFolder/containerSubFolder/file`
            purge_local (bool, optional): bool, default False
                whether to delete local files after successful upload

        Returns
        -------
            list
                remote path(s) to files
        """
        uploaded_files = []
        for local_file in files:
            iter_file = self._upload_blob(
                file=local_file, prefix=prefix, purge_local=purge_local
            )
            uploaded_files.append(iter_file)

        return uploaded_files
