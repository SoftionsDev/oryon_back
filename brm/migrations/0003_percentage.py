# Generated by Django 4.2.6 on 2023-12-13 00:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('brm', '0002_rule_formula'),
    ]

    operations = [
        migrations.CreateModel(
            name='Percentage',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('field', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
