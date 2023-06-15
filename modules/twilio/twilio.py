from .config import *
from twilio.rest import Client


def send_twilio_message(message: str, to_phone: str = TO_PHONE):
    twilio_client = Client(SID, TOKEN)
    message = twilio_client.messages.create(to=to_phone, from_=FROM_PHONE, body=message)
