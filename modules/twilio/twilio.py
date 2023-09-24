from .config import *
from twilio.rest import Client


def send_twilio_message(message: str, to_phone: str = TO_PHONE):
    """Sends a text message via Twilio API

    Parameters
    ----------
        message : str
            Message you'd like to send
        to_phone (str, optional): str, default TO_PHONE
            Recipient phone number (10 digit)
    """
    twilio_client = Client(SID, TOKEN)
    message = twilio_client.messages.create(to=to_phone, from_=FROM_PHONE, body=message)
