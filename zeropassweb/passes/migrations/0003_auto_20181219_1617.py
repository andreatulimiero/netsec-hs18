# Generated by Django 2.1.4 on 2018-12-19 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0002_pass_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pass',
            old_name='name',
            new_name='key',
        ),
    ]