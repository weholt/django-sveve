from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Contact(models.Model):
    "A basic contact"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile_phone = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name} ({self.mobile_phone})"

    class Meta:
        ordering = ["last_name", "first_name"]


class Group(models.Model):
    "A basic group"

    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Contact, blank=True, related_name="groups")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


MESSAGE_STATUS_OPTIONS = (("sent", "Sent"), ("not-sent", "Not sent"))


class Message(models.Model):
    """
    The message sent to recipients
    """

    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sender_text = models.CharField(max_length=11, null=True, blank=True)
    text = models.TextField(max_length=1071)
    recipients = models.ManyToManyField(Contact)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.CharField(max_length=20, choices=MESSAGE_STATUS_OPTIONS, default="sent")
    status_message = models.TextField(null=True, blank=True)
