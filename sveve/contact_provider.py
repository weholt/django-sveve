import abc
from dataclasses import dataclass
from typing import Iterable


@dataclass
class ContactBase:
    first_name: str
    last_name: str
    mobile_phone: str


class ContactProviderBase(abc.ABC):
    """ """

    @abc.abstractmethod
    def get_contacts(self) -> Iterable[ContactBase]:
        pass


class TestContactProvider(ContactProviderBase):
    """ """

    def get_contacts(self) -> Iterable[ContactBase]:
        return [ContactBase(first_name="Thomas", last_name="Weholt", mobile_phone="90866360")]
