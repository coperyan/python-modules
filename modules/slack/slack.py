from .config import *
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def _build_message(message: str, users: list = None, code: str = None):
    if users:
        message = (
            (", ".join([f"<@{USERS.get(usr)}>" for usr in users]))
            + f"\n"
            + f"{message}"
        )
    if code:
        message += f"\n```{code}```"

    return message


def message_slack_channel(
    message: str,
    channel: str = CHANNEL,
    code: str = None,
    file: str = None,
    mention_users: list = None,
):
    slack_client = WebClient(token=TOKEN)

    message = _build_message(message=message, users=mention_users, code=code)

    if file:
        resp = slack_client.files_upload(
            channels=channel,
            file=file,
            title=os.path.basename(file),
            initial_comment=message,
        )
    else:
        resp = slack_client.chat_postMessage(channel=channel, text=message)
