# Generated by Django 4.2.16 on 2024-11-26 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("API", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="machin",
            name="group_monitor_permision",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="machin",
            name="group_user_permision",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="machin",
            name="other_monitor_permision",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="machin",
            name="other_user_permision",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="machin",
            name="user_monitor_permision",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="machin",
            name="user_user_permision",
            field=models.BooleanField(default=True),
        ),
    ]
