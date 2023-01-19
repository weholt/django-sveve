import importlib
import inspect
from typing import List  # Optional, Tuple,

import requests
from django.conf import settings
from django.contrib.auth import get_user_model

from sveve.contact_provider import ContactProviderBase
from sveve.models import Contact, Message

User = get_user_model()


def send_message(sender: User, sender_text: str, message: str, recipients: List[Contact]) -> Message:
    """
    Sends a message from user to a bunch of recipients
    """
    msg = Message.objects.create(sender=sender, sender_text=sender_text, text=message)
    try:
        r = requests.post(
            settings.SVEVE_API_URL,
            json={
                "user": settings.SVEVE_USERNAME,
                "passwd": settings.SVEVE_PASSWORD,
                "to": ", ".join([contact.mobile_phone for contact in recipients]),
                "msg": message,
                "from": sender_text,
                "f": "json",
            },
        )
        if r.status_code == 200:
            for recipient in recipients:
                msg.recipients.add(recipient)
        else:
            msg.status = "not-sent"
            msg.status_message = "Status code: %s" % r.status_code
    except Exception as ex:
        msg.status = "not-sent"
        msg.status_message = str(ex)
    return msg


def get_contacts():
    for provider_text in settings.SVEVE_CONTACTS_PROVIDERS:
        provider = importlib.import_module(provider_text)
        for c in dir(provider):
            p = getattr(provider, c)
            try:
                if inspect.isclass(p) and issubclass(p, ContactProviderBase) and p.__name__ != "ContactProviderBase":
                    for contact in p().get_contacts():
                        yield contact
            except Exception as ex:
                print("ex", ex)
