# Generated by Django 3.2 on 2021-05-06 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0012_support_messenger'),
    ]

    operations = [
        migrations.AddField(
            model_name='support_messenger',
            name='status',
            field=models.TextField(default='Обработка', verbose_name='Статус'),
            preserve_default=False,
        ),
    ]
