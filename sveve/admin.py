from django.conf import settings
from django.contrib import admin

from .models import Contact, Group, Message
from .services import send_message

# from django.utils.html import mark_safe


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["last_name", "first_name", "mobile_phone"]
    actions = ["send_message"]

    @admin.action(description="Sends a message to the selected contacts")
    def send_message(self, request, queryset):
        msg = send_message(request.user, settings.SVEVE_SENDER_TEXT, "Sms virker gitt.", queryset)
        print(msg)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["sender", "sender_text", "created", "status"]
    list_filter = ["status"]
    date_hierarchy = "created"
    readonly_fields = ["created"]
    # def create_from_template(self, obj):
    #     return mark_safe("<a href='%s'>Add performance
    # report</a>" % reverse("airgunperformanceindex:performance-report-create-from-template", args=[obj.uuid]))

    # create_from_template.short_description = "Add performance report from template"
    # create_from_template.allow_tags = True
