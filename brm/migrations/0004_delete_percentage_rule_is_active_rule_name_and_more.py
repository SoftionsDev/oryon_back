# Generated by Django 4.2.6 on 2023-12-14 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brm', '0003_percentage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Percentage',
        ),
        migrations.AddField(
            model_name='rule',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='rule',
            name='name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rule',
            name='percentage',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
    ]
