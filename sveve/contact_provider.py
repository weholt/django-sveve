import abc
from typing import Iterable, Protocol

from .models import Contact


class ContactBase(Protocol):
    first_name: str
    last_name: str
    mobile_phone: str


class ContactProviderBase(abc.ABC):
    """ """

    @abc.abstractmethod
    def get_contacts(self) -> Iterable[ContactBase]:
        pass

    def sync_contacts(self) -> None:
        for contact in self.get_contacts():
            Contact.objects.update_or_create(first_name=contact.first_name, last_name=contact.last_name, defaults={"mobile_phone": contact.mobile_phone})
