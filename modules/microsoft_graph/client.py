import os

from azure.identity import ClientSecretCredential
from msgraph.core import GraphClient

from .config import *
from .constants import *
from .email import MSGraphMessage


class MSGraphClient:
    def __init__(self):
        self.credential = None
        self.client = None
        self._auth_and_create_client()

    def _auth_and_create_client(self):
        self.credential = ClientSecretCredential(
            tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET
        )
        self.client = GraphClient(credential=self.credential)

    def send_message(self, **kwargs) -> MSGraphMessage:
        return MSGraphMessage(self.client, **kwargs)
