import abc
from typing import Iterable, Protocol

from django.db import transaction

from .models import Contact


class ContactBase(Protocol):
    first_name: str
    last_name: str
    mobile_phone: str
    source: str = ""


class ContactProviderBase(abc.ABC):
    """ """

    @abc.abstractmethod
    def get_contacts(self) -> Iterable[ContactBase]:
        pass

    def sync_contacts(self) -> None:
        with transaction.atomic():
            Contact.objects.all().update(active=False)
            for contact in self.get_contacts():
                if contact.mobile_phone.isdigit():
                    Contact.objects.update_or_create(
                        first_name=contact.first_name,
                        last_name=contact.last_name,
                        defaults={"mobile_phone": contact.mobile_phone, "active": True, "source": contact.source},
                    )
