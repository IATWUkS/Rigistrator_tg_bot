# Generated by Django 3.2 on 2021-04-30 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0003_alter_pre_registration_data_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pre_registration_data',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adm.organization', verbose_name='Компания'),
        ),
    ]
