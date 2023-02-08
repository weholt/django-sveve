# django-sveve

Adds support for sending SMS using Sveve.no's API using a reusable django app.

* [Sveve.no](http://sveve.no/)
* [API documentation](https://sveve.no/apidok/)

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

Install [django-environ](http://django-environ/) to separate your account information from the settings.py file:

Add django-environ to your settings.py, something like this or go by the django-environ documentation:
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

Create an .env file for your account information:
```
SVEVE_API_URL="https://sveve.no/SMS/SendMessage"
SVEVE_USERNAME="<your username at seve>"
SVEVE_PASSWORD="<your password at sveve>"
SVEVE_SENDER_TEXT="<the title of each sms you send. NB! Make it short>"
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

### Optional Configuration

* TODO: document the contacts-provider section.

A more
## Version history

0.1.0 :
 - Initial MVP - release
