# Generated by Django 3.1.4 on 2020-12-25 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saebyuk', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookinfo',
            old_name='book_info',
            new_name='book',
        ),
    ]