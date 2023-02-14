# django-sveve

A reusable django app for sending SMS using [Sveve.no's API](https://sveve.no/apidok/send).

* [Sveve.no](http://sveve.no/)
* [API documentation](https://sveve.no/apidok/)

## The state of this MVP ([Minimum viable product](https://en.wikipedia.org/wiki/Minimum_viable_product))

 * It can send SMS to multiple recipients.
 * You can define groups of contacts and send a SMS to several groups at a time.
 * Contacts can be imported from a spreadsheet/Excel/CSV file.
 * Contacts can be synchronized with other sources by implementing a custom contacts provider, documented below.

## Installation

```
pip install -e git+git://github.com/weholt/django-sveve.git#egg=opengraph
```

Add 'sveve' to your INSTALLED_APPS before 'django.contrib.admin':
```
INSTALLED_APPS = [
    "sveve",
    "django.contrib.admin",
    ...
    "django.contrib.staticfiles",
]
```

Add the sveve urls to your global urls.py:
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    ...
    path("", include("sveve.urls"))
]
```

Create an .env file for your account information:
```
SVEVE_API_URL="https://sveve.no/SMS/SendMessage"
SVEVE_USERNAME="<your username at seve>"
SVEVE_PASSWORD="<your password at sveve>"
SVEVE_SENDER_TEXT="<the title of each sms you send. NB! Make it short>"
```
The .env file should be located in the same folder as django's manage.py.

Install [django-environ](http://django-environ/) to separate your account information from the settings.py file:
Configure django-environ to read your .env file inyour settings.py, something like this or go by the django-environ documentation:
```
import environ

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
```

Add the following to the end of settings.py:
```
SVEVE_API_URL = env("SVEVE_API_URL")
SVEVE_USERNAME = env("SVEVE_USERNAME")
SVEVE_PASSWORD = env("SVEVE_PASSWORD")
SVEVE_SENDER_TEXT = env("SVEVE_SENDER_TEXT")
```

Execute any migrations to add the Sveve specific models:
```
 $ python manage.py migrate
```

Create a superuser to access the django admin:
```
$ python manage.py createsuperuser
```

Start the webserver and go to the admin pages:
```
$ python manage.py runserver
```

## Run the example project
This assumes you already have Python 3.9+ installed:
```
$ git clone http://github.com/weholt/django-sveve.git
$ cd django-sveve
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```
Visit http://localhost:8000 in your browser.

### Providing contacts from another source than file

*This section assumes knowledge of python programming, python modules and packages.*

Consider this example of a custom contacts provider, snipped from the test.py file in the sveve app:
```
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
            # lots of more contacts generated
            ("Arne", "Weholt", "90866360"),
        ]:
            yield CustomContact(first_name=first_name, last_name=last_name, mobile_phone=mobile_phone)
```
By implementing a class like the TestContactProvider above you'll be able to synch the contacts with whatever comes out of the custom provider class.
To make your custom contact provider available to use in the django admin, just add the string-representation of the file containing your provider
in the SVEVE_CONTACTS_PROVIDERS list. For instance, if your providers are available in a file called mycustomproviders inside a module called providers

```
SVEVE_CONTACTS_PROVIDERS = ["providers.mycustomproviders"]
```
On disk this would look like a folder called providers in the same folder as manage.py, with at least __init__.py inside it in addition to your file mycustomproviders.py. Hope that was clear enough.

If you've done everything correctly, you should click the "Synchronize contacts" inside the admin and see the contacts from your providers appear.


## Version history

0.1.0 :
 - Initial MVP - release.

 0.2.0 :
 - Code refactoring, better handling of exceptions on import of contacts from file.
 - Added character counting to sms message field.
 - Added example code for custom contacts provider and some documentation for it.

0.3.0:
 - Fixed a few bugs.
 - Added a source field to Contacts to indicate the source when provided by a custom contacts provider.