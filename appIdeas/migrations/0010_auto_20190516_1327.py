# Generated by Django 2.1.7 on 2019-05-16 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appIdeas', '0009_persission'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Persission',
            new_name='Permission',
        ),
    ]