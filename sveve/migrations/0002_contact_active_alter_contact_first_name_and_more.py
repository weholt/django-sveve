# Generated by Django 4.1.5 on 2023-02-12 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sveve", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="contact",
            name="active",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="contact",
            name="first_name",
            field=models.CharField(max_length=100, verbose_name="First name"),
        ),
        migrations.AlterField(
            model_name="contact",
            name="last_name",
            field=models.CharField(max_length=100, verbose_name="Last name"),
        ),
        migrations.AlterField(
            model_name="contact",
            name="mobile_phone",
            field=models.CharField(max_length=100, verbose_name="Mobile phone number"),
        ),
        migrations.AlterField(
            model_name="group",
            name="members",
            field=models.ManyToManyField(blank=True, related_name="groups", to="sveve.contact", verbose_name="members"),
        ),
        migrations.AlterField(
            model_name="group",
            name="name",
            field=models.CharField(max_length=100, verbose_name="Group name"),
        ),
        migrations.AlterField(
            model_name="message",
            name="created",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created"),
        ),
        migrations.AlterField(
            model_name="message",
            name="recipients",
            field=models.ManyToManyField(to="sveve.contact", verbose_name="Recipients"),
        ),
        migrations.AlterField(
            model_name="message",
            name="sender",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name="Sender"),
        ),
        migrations.AlterField(
            model_name="message",
            name="sender_text",
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name="Sender Text"),
        ),
        migrations.AlterField(
            model_name="message",
            name="status",
            field=models.CharField(choices=[("sent", "Sent"), ("not-sent", "Not sent")], default="sent", max_length=20, verbose_name="Status"),
        ),
        migrations.AlterField(
            model_name="message",
            name="status_message",
            field=models.TextField(blank=True, null=True, verbose_name="Status message"),
        ),
        migrations.AlterField(
            model_name="message",
            name="text",
            field=models.TextField(max_length=1071, verbose_name="Text"),
        ),
    ]
