# Generated by Django 4.2.6 on 2024-02-07 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commissions', '0005_remove_commission_rule_commission_percentage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='commissions', to=settings.AUTH_USER_MODEL),
        ),
    ]
