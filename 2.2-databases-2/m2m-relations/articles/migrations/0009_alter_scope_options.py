# Generated by Django 4.2 on 2023-05-13 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_alter_tag_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scope',
            options={'ordering': ['is_main']},
        ),
    ]
