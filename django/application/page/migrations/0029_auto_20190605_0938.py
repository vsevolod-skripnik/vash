# Generated by Django 2.1.7 on 2019-06-05 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0028_auto_20190604_1856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='clean_meta',
        ),
        migrations.RemoveField(
            model_name='page',
            name='meta',
        ),
    ]