from django.urls import path

from .views import send_message_to_contact, send_message_to_group

app_name = "sveve"

urlpatterns = [
    path("sveve/contact/send_sms/<str:recipient_phone_number>", send_message_to_contact, name="contact-send-message"),
    path("sveve/group/send_sms/<int:group_id>", send_message_to_group, name="group-send-message"),
]
