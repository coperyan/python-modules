from .config import *
from .constants import *

import os
from google.cloud import storage

storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB


class GoogleCloudStorage:
    def __init__(self, project: str = PROJECT, bucket: str = BUCKET):
        """Initializes client object"""
        self.host_project = project
        self.client = storage.Client(project=project)
        self.bucket = self.client.bucket(bucket)

    def _bucket_exists(self) -> bool:
        return True if self.bucket else False

    def _bucket_name(self) -> str:
        return self.bucket.name if self._bucket_exists() else None

    def _validate_bucket(self, bucket):
        if not self._bucket_name() == bucket:
            self.bucket = self.client.bucket(bucket)

    def upload_file(
        self, bucket: str, file_path: str, gcs_path: str, chunk_size: int = CHUNK_SIZE
    ):
        self._validate_bucket(bucket=bucket)
        blob = self.bucket.blob(gcs_path, chunk_size=chunk_size)
        blob.upload_from_filename(file_path, timeout=300)

    def download_file(self, bucket: str, gcs_path: str, local_path: str):
        self._validate_bucket(bucket=bucket)
        blob = self.bucket.blob(gcs_path)
        if os.path.isdir(local_path):
            local_path = os.path.join(local_path, os.path.basename(gcs_path))
        blob.download_to_filename(local_path)

    def copy_file(
        self, from_bucket: str, to_bucket: str, from_path: str, to_path: str = None
    ):
        if not to_path:
            from_path = to_path
        from_bucket = self.client.bucket(from_bucket)
        to_bucket = self.client.bucket(to_bucket)
        from_blob = from_bucket.blob(from_path)
        blob_copy = from_bucket.copy_blob(from_blob, to_bucket, if_generation_match=0)

    def list_files(self, bucket: str, path: str, ext: list = None) -> list:
        files = self.client.list_blobs(bucket, prefix=path)
        if ext:
            files = [f.name for f in files if os.path.splitext(f.name)[1] in ext]
        return files
