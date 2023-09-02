import os
import json
import time
import base64
import random
import requests
from msgraph.core import GraphClient

from .config import *
from .constants import *

# from .client import MSGraphClient


class MSGraphMessage:
    def __init__(
        self,
        client: GraphClient,
        mailbox: str,
        to_recipients: list = None,
        cc_recipients: list = None,
        bcc_recipients: list = None,
        subject: str = "",
        body: str = "",
        body_type: str = "Text",
        file_attachments: list = None,
        img_attachments: list = None,
        importance: str = "normal",
    ):
        self.client = client
        self.mailbox = mailbox.lower()
        self.to_recipients = to_recipients
        self.cc_recipients = cc_recipients
        self.bcc_recipients = bcc_recipients
        self.subject = subject
        self.body = body
        self.body_type = body_type
        self.file_attachments = file_attachments
        self.img_attachments = img_attachments
        self.importance = importance
        self.body_json = None
        self.message_id = None
        self._validate_mailbox()
        self._validate_recipients()
        self._validate_imgs()
        self.send()

    def _validate_mailbox(self, mailbox: str):
        if mailbox not in VALID_MAILBOXES:
            raise ValueError("Invalid mailbox string passed!")

    def _validate_recipients(self):
        if not any([self.to_recipients, self.cc_recipients, self.bcc_recipients]):
            raise ValueError(
                "Must have one of the following recipient lists populated.."
            )

    def _validate_imgs(self):
        if self.body_type == "str" and self.img_attachments is not None:
            raise Exception("Passed str as body type with img attachments..")

    def _recipient_list_to_json(self, l: list) -> list:
        return [{"emailAddress": {"address": e}} for e in l]

    def _get_attachment_info(self, attachment: str, img: bool = False) -> dict:
        with open(attachment, "rb") as f:
            content = f.read()

        return {
            "name": os.path.basename(attachment),
            "path": attachment,
            "size": len(content),
            "content": base64.b64encode(content) if img else content,
        }

    def _build_message_body(self) -> dict:
        body = {
            "subject": self.subject,
            "body": {"contentType": self.body_type, "content": self.body},
            "importance": self.importance,
            "from": {"emailAddress": {"address": self.mailbox}},
        }
        if self.to_recipients:
            body["toRecipients"] = self._recipient_list_to_json(self.to_recipients)
        if self.cc_recipients:
            body["ccRecipients"] = self._recipient_list_to_json(self.cc_recipients)
        if self.bcc_recipients:
            body["bccRecipients"] = self._recipient_list_to_json(self.bcc_recipients)

        return body

    def _create_message(self) -> str:
        resp = self.client.post(
            url=f"/users/{self.mailbox}/messages",
            headers={"Content-Type": "application/json"},
            data=json.dumps(self.body_json),
        )

        if resp.status_code == 429:
            num_tries = 1
            while num_tries < 3 and resp.status_code == 429:
                iter_sleep = resp.headers["retry-after"]
                time.sleep(iter_sleep)
                resp = self.client.post(
                    url=f"/users/{self.mailbox}/messages",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(self.body_json),
                )
                num_tries += 1

        if resp.status_code != 201:
            raise Exception(f"{resp.status_code}: {resp.text}")
        else:
            return resp.json().get("id")

    def _create_upload_session(self, attachment: dict) -> str:
        resp = self.client.post(
            url=f"/users/{self.mailbox}/messages/{self.message_id}/attachments/createUploadSession",
            headers={"Content-Type": "application/json"},
            data=json.dumps(
                {
                    "AttachmentItem": {
                        "attachmentType": "file",
                        "name": attachment.get("name"),
                        "size": attachment.get("size"),
                    }
                }
            ),
        )

        if resp.status_code != 201:
            raise Exception(f"{resp.status_code}: {resp.text}")
        else:
            return resp.json().get("uploadUrl")

    def _chunk_attachment_upload(self, attachment: dict, url: str):
        complete = False
        num_tries = 0
        while not complete:
            resp = requests.put(
                url,
                headers={
                    "Content-Length": f"{len(attachment.get('content'))}",
                    "Content-Range": f"bytes 0-{len(attachment.get('content'))-1}/{len(attachment.get('content'))}",
                    "Content-Type": "application/json",
                },
                data=attachment.get("content"),
            )

            if resp.status_code == 201:
                complete = True
                return

            if num_tries > 2:
                raise Exception(f"Failed to upload attachment:{resp.status_code}")

            if resp.status_code == 429:
                iter_sleep = int(resp.headers["retry-after"]) + random.randint(4, 9)
                time.sleep(iter_sleep)
                num_tries += 1

            if resp.status_code != 201:
                raise Exception(f"{resp.status_code}: {resp.text}")

    def _img_attachment_upload(self, img: dict):
        resp = self.client.post(
            f"/users/{self.mailbox}/messages/{self.message_id}/attachments",
            data=json.dumps(
                {
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": img.get("name"),
                    "contentBytes": img.get("content").decode("utf-8"),
                    "isInline": "true",
                }
            ),
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code != 201:
            raise Exception(f"Request failed: {resp.text}")

    def _send_message(self):
        resp = self.client.post(
            f"/users/{self.mailbox}/messages/{self.message_id}/send",
            headers={"Content-Type": "application/json"},
        )

        num_tries = 1
        while resp.status_code == 429 and num_tries < 3:
            time.sleep(resp.headers["retry-after"])
            resp = self.client.post(
                f"/users/{self.mailbox}/messages/{self.message_id}/send",
                headers={"Content-Type": "application/json"},
            )
            num_tries += 1
        if resp.status_code != 201:
            raise Exception(f"{resp.status_code}: {resp.text}")

    def send(self):
        self.body_json = self._build_message_body()
        self.message_id = self._create_message()

        for attachment in self.file_attachments:
            attachment_info = self._get_attachment_info(attachment)
            url = self._create_upload_session(attachment_info)
            self._chunk_attachment_upload(attachment, url)

        for img in self.img_attachments:
            attachment_info = self._get_attachment_info(img, True)

        self._send_message()
