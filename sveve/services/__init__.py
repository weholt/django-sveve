import importlib
import inspect
import json
from typing import Iterable, List  # Optional, Tuple,

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import gettext as _

from sveve.contact_provider import ContactProviderBase
from sveve.models import Contact, Group, Message

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
            response = json.loads(r.content)
            if "fatalError" in response.get("response"):
                msg.status = "not-sent"
                msg.status_message = _("Status code: %s. Fatal error: %s" % (r.status_code, response.get("response", {}).get("fatalError")))
            else:
                sentOk = response.get("response", {}).get("msgOkCount")
                msg.status_message = _("Sent %s message(s)" % sentOk)
                for recipient in recipients:
                    msg.recipients.add(recipient)
        else:
            msg.status = "not-sent"
            msg.status_message = _("Status code: %s" % r.status_code)
    except Exception as ex:
        msg.status = "not-sent"
        msg.status_message = str(ex)
    return msg


def get_contact_providers() -> Iterable[ContactProviderBase]:
    result = []
    for provider_text in settings.SVEVE_CONTACTS_PROVIDERS:
        provider = importlib.import_module(provider_text)
        for c in dir(provider):
            p = getattr(provider, c)
            try:
                if inspect.isclass(p) and issubclass(p, ContactProviderBase) and p.__name__ != "ContactProviderBase":
                    result.append(p)
            except Exception as ex:
                print("ex", ex)

    return result


def send_group_message(request: HttpRequest, message: str, groups: Iterable[Group]) -> Message:
    recipients = Contact.objects.filter(groups__in=[group.id for group in groups])
    return send_message(request.user, settings.SVEVE_SENDER_TEXT, message, list(set(recipients)))
