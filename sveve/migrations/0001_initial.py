# Generated by Django 4.1.5 on 2023-01-19 20:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("mobile_phone", models.CharField(max_length=100)),
            ],
            options={
                "ordering": ["last_name", "first_name"],
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sender_text", models.CharField(blank=True, max_length=11, null=True)),
                ("text", models.TextField(max_length=1071)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("status", models.CharField(choices=[("sent", "Sent"), ("not-sent", "Not sent")], default="sent", max_length=20)),
                ("status_message", models.TextField(blank=True, null=True)),
                ("recipients", models.ManyToManyField(to="sveve.contact")),
                ("sender", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Group",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("members", models.ManyToManyField(blank=True, related_name="groups", to="sveve.contact")),
            ],
            options={
                "ordering": ["name"],
            },
        ),
    ]