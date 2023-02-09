from dataclasses import dataclass
from typing import Iterable

from django.test import TestCase

from .contact_provider import ContactBase, ContactProviderBase
from .models import Contact


@dataclass
class CustomContact:
    first_name: str
    last_name: str
    mobile_phone: str


class TestContactProvider(ContactProviderBase):
    """ """

    def get_contacts(self) -> Iterable[ContactBase]:
        for first_name, last_name, mobile_phone in [
            ("Thomas", "Weholt", "90866360"),
            ("Tore", "Weholt", "90866360"),
            ("Emrik", "Weholt", "90866360"),
            ("Mari", "Weholt", "90866360"),
            ("Tom", "Weholt", "90866360"),
            ("Arne", "Weholt", "90866360"),
        ]:
            yield CustomContact(first_name=first_name, last_name=last_name, mobile_phone=mobile_phone)


class CustomContactProviderTestCase(TestCase):
    def test_custom_contact_provider(self):
        provider = TestContactProvider()
        provider.sync_contacts()
        self.assertEqual(Contact.objects.all().count(), 6)
