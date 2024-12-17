# Generated by Django 5.1.2 on 2024-11-25 22:39

import colorfield.fields
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import netfields.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64, unique=True)),
                ("description", models.TextField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name="Machin",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                ("username", models.CharField(max_length=64)),
                ("password", models.CharField(max_length=64)),
                ("history_save", models.BooleanField(default=True)),
                ("log_save", models.BooleanField(default=True)),
                ("ip", netfields.fields.InetAddressField(max_length=39)),
                (
                    "port",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(65535),
                            django.core.validators.MinValueValidator(1),
                        ]
                    ),
                ),
                ("user_monitor_permision", models.BooleanField(default=False)),
                ("user_user_permision", models.BooleanField(default=False)),
                ("group_monitor_permision", models.BooleanField(default=False)),
                ("group_user_permision", models.BooleanField(default=False)),
                ("other_monitor_permision", models.BooleanField(default=False)),
                ("other_user_permision", models.BooleanField(default=False)),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="API.group"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Log",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "history",
                    models.FileField(auto_created=True, editable=False, upload_to=""),
                ),
                (
                    "log",
                    models.FileField(auto_created=True, editable=False, upload_to=""),
                ),
                ("time_save", models.DateTimeField(auto_now_add=True)),
                (
                    "machin",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="API.machin"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Machin_Group",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64, unique=True)),
                (
                    "machin",
                    models.ManyToManyField(
                        related_name="machin_group", to="API.machin"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "login",
                    models.CharField(
                        blank=True, max_length=150, unique=True, verbose_name="login"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                ("is_observer", models.BooleanField(default=False)),
                ("history_save", models.BooleanField(default=True)),
                ("history", models.FileField(upload_to="")),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Machine_request_one_comand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "color",
                    colorfield.fields.ColorField(
                        default="#FFFFFF", image_field=None, max_length=25, samples=None
                    ),
                ),
                ("request_file_path", models.FileField(editable=False, upload_to="")),
                (
                    "machin",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="API.machin"
                    ),
                ),
                (
                    "machin_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="API.machin_group",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="machin",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="group",
            name="users",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
