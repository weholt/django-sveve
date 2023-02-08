# django-sveve

A reusable django app for sending SMS using Sveve.no's API.

* [Sveve.no](http://sveve.no/)
* [API documentation](https://sveve.no/apidok/)

## The state of this MVP ([Minimum viable product](https://en.wikipedia.org/wiki/Minimum_viable_product))

 * It can send SMS to multiple recipients.
 * You can define groups of contacts and send a SMS to several groups at a time.
 * Contacts can be imported from a spreadsheet/Excel/CSV file.
 * Contacts can be imported/exported by implementing a Contact Provider (documentation of that feature is coming soon).

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

### Optional Configuration

* TODO: document the contacts-provider section.

## Version history

0.1.0 :
 - Initial MVP - release
