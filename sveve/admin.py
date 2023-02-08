from django import forms
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.html import mark_safe

from .models import Contact, Group, Message
from .services import send_group_message, send_message


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class CreateGroupForm(forms.Form):
    name = forms.CharField()


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["last_name", "first_name", "mobile_phone", "send_message_to_contact"]
    change_list_template = "admin/contact_changelist.html"
    search_fields = ["last_name", "first_name", "mobile_phone"]
    actions = ["send_message", "create_group"]

    @admin.action(description="Sends a message to the selected contacts")
    def send_message(self, request, queryset):
        if "apply" in request.POST:  # or 'action' in request.POST:
            message_text = request.POST.get("message").strip()
            if message_text:
                msg = send_message(request.user, settings.SVEVE_SENDER_TEXT, message_text, queryset)
                if msg.status == "sent":
                    self.message_user(request, "Sent message to {} contacts".format(queryset.count()))
                else:
                    self.message_user(request, "Failed to send messag: %s" % msg.status_message)
                return redirect(reverse("admin:sveve_contact_changelist"))

        return render(request, "admin/send_message.html", context={"orders": queryset})

    @admin.action(description="Creates a new group from the selected contacts")
    def create_group(self, request, queryset):
        if "apply" in request.POST:
            group_name = request.POST.get("name", "").strip()
            if group_name:
                group = Group.objects.create(name=group_name)
                for contact in queryset:
                    group.members.add(contact)

            return redirect(reverse("admin:sveve_contact_changelist"))

        return render(request, "admin/create_group.html", context={"orders": queryset, "form": CreateGroupForm()})

    def send_message_to_contact(self, obj):
        return mark_safe('<a href="%s">Send SMS</a>' % (reverse("sveve:contact-send-message", args=[obj.mobile_phone.strip()])))

    send_message_to_contact.short_description = "Send SMS"
    send_message_to_contact.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            for line in request.FILES["csv_file"].read().decode("utf-8").split("\n"):
                try:
                    first_name, last_name, mobile_phone = line.split(",")
                    Contact.objects.update_or_create(first_name=first_name, last_name=last_name, defaults={"mobile_phone": mobile_phone})
                except Exception as ex:
                    print("Error parsing '%s': %s" % (line, ex))
            self.message_user(request, "Your csv file has been imported")
            return redirect(reverse("admin:sveve_contact_changelist"))
        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["name", "send_message_to_group"]
    search_fields = ["name"]
    formfield_overrides = {
        models.ManyToManyField: {"widget": forms.CheckboxSelectMultiple},
    }
    actions = ["send_message"]

    @admin.action(description="Sends a message to contacts in the selected groups")
    def send_message(self, request, queryset):
        if "apply" in request.POST:  # or 'action' in request.POST:
            message_text = request.POST.get("message").strip()
            msg = send_group_message(request, message_text, queryset)
            self.message_user(
                request, msg.status == "sent" and "Sent message to {} contacts".format(queryset.count()) or "Failed to send messag: %s" % msg.status_message
            )
            return redirect(reverse("admin:sveve_group_changelist"))
        return render(request, "admin/send_message.html", context={"orders": queryset})

    def send_message_to_group(self, obj):
        return mark_safe('<a href="%s">Send SMS</a>' % (reverse("sveve:group-send-message", args=[obj.id])))

    send_message_to_group.short_description = "Send SMS"
    send_message_to_group.allow_tags = True


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["sender", "sender_text", "created", "status"]
    list_filter = ["status"]
    date_hierarchy = "created"
    readonly_fields = ["created"]
