from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render

from .models import Contact, Group
from .services import send_group_message, send_message


def send_message_to_contact(request, recipient_phone_number):
    queryset = Contact.objects.filter(mobile_phone=recipient_phone_number)
    if "apply" in request.POST:
        message_text = request.POST.get("message").strip()
        msg = send_message(request.user, settings.SVEVE_SENDER_TEXT, message_text, queryset)
        messages.add_message(request, messages.SUCCESS, msg.status_message)
        return redirect("admin:sveve_contact_changelist")
    return render(request, "admin/send_message_to_contact.html", context={"contact": Contact.objects.get(mobile_phone=recipient_phone_number)})


def send_message_to_group(request, group_id):
    queryset = Group.objects.filter(id=group_id)
    group = queryset.first()
    if "apply" in request.POST:
        message_text = request.POST.get("message").strip()
        msg = send_group_message(request, message_text, queryset)
        messages.add_message(request, messages.SUCCESS, msg.status_message)
        return redirect("admin:sveve_group_changelist")
    return render(request, "admin/send_message_to_group.html", context={"group": group})
