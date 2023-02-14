from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

User = get_user_model()


class Contact(models.Model):
    "A basic contact"

    first_name = models.CharField(max_length=100, verbose_name=_("First name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last name"))
    mobile_phone = models.CharField(max_length=100, verbose_name=_("Mobile phone number"))
    source = models.CharField(max_length=50, null=True, verbose_name=_("Source"))
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name} ({self.mobile_phone})"

    class Meta:
        ordering = ["last_name", "first_name"]


class Group(models.Model):
    "A basic group"

    name = models.CharField(max_length=100, verbose_name=_("Group name"))
    members = models.ManyToManyField(Contact, blank=True, related_name="groups", verbose_name=_("members"))

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


MESSAGE_STATUS_OPTIONS = (("sent", _("Sent")), ("not-sent", _("Not sent")))


class Message(models.Model):
    """
    The message sent to recipients
    """

    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("Sender"))
    sender_text = models.CharField(max_length=11, null=True, blank=True, verbose_name=_("Sender Text"))
    text = models.TextField(max_length=1071, verbose_name=_("Text"))
    recipients = models.ManyToManyField(Contact, verbose_name=_("Recipients"))
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("Created"))
    status = models.CharField(max_length=20, choices=MESSAGE_STATUS_OPTIONS, default="sent", verbose_name=_("Status"))
    status_message = models.TextField(null=True, blank=True, verbose_name=_("Status message"))
