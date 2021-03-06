# Generated by Django 3.2 on 2021-05-05 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0008_auto_20210503_2333'),
    ]

    operations = [
        migrations.CreateModel(
            name='logging_message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_chat', models.TextField(verbose_name='ID чата')),
                ('id_user', models.TextField(verbose_name='ID пользователя')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('date', models.TextField(verbose_name='Дата отправки сообщения')),
                ('name_chat', models.TextField(verbose_name='Названия чата')),
            ],
            options={
                'verbose_name': 'Сообщения',
                'verbose_name_plural': 'Сообщения',
            },
        ),
    ]
