# Generated by Django 4.2.6 on 2023-12-11 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='formula',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
