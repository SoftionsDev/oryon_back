# Generated by Django 4.2.6 on 2024-01-23 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_commercial_goal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.CharField(choices=[('MANAGER', 'gerente'), ('DIRECTOR', 'director'), ('ADVISER', 'asesor'), ('ASSISTANT', 'asistente')], max_length=100),
        ),
    ]
