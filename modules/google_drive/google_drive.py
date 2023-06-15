from .constants import *

import os
import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def upload_file(file_path: str, folder_id: str):
    mimetype = EXT_TYPES.get(os.path.parsext(file_path)[1])

    creds = service_account.Credentials.from_service_account_file(
        "credentials.json", scopes=SCOPES
    )

    try:
        service = build("drive", "v3", credentials=creds)

        file_metadata = {
            "name": f"{os.path.basename(file_path)}",
            "parents": [folder_id],
        }
        media = MediaFileUpload(f"{file_path}", mimetype=mimetype, resumable=True)
        file = (
            service.files()
            .create(
                body=file_metadata,
                media_body=media,
                fields="id",
                supportsAllDrives=True,
            )
            .execute()
        )
        print(f'File ID: "{file.get("id")}".')
        return file.get("id")
    except HttpError as error:
        print(f"An error occurred: {error}")
