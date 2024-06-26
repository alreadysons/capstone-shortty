# Generated by Django 5.0.3 on 2024-05-09 17:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_category_message_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages",
                to="main.category",
            ),
        ),
    ]
