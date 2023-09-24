from .config import *
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def _build_message(message: str, users: list = None, code: str = None) -> str:
    """Builds a message string for the `message_slack_channel` function

    Parameters
    ----------
        message : str
            Body of message
        users (list, optional): list, default None
            List of users to mention in the message
                Note: must have `config.py` setup with the `USERS` dictionary like so:
                    `{User: ID}`
        code (str, optional): str, default None
            Code block to add to message

    Returns
    -------
        str
            Message string
    """
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
    """Send a message to a slack channel

    Parameters
    ----------
        message : str
            Body of message
        channel (str, optional): str, default CHANNEL
            Channel name ex `#channelname`
        code (str, optional): str, default None
            Code block for message string
        file (str, optional): str, default None
            Local path to file
        mention_users (list, optional): list, default None
            List of users to mention in the message
                Note: must have `config.py` setup with the `USERS` dictionary like so:
                    `{User: ID}`
    """
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
