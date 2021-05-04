from django.db import models


class pre_registration_data(models.Model):
    id_tg = models.IntegerField(verbose_name='ID телеграм пользователя')
    name = models.TextField(verbose_name='Имя', max_length=24)
    surname = models.TextField(verbose_name='Фамилия', max_length=24)
    email = models.TextField(verbose_name='EMAIL')
    company = models.TextField(verbose_name='Компания')
    position = models.TextField(verbose_name='Должность')
    number = models.TextField(verbose_name='Номер телефона')
    data_processing = models.TextField(verbose_name='Согласия на обработку данных')
    status_user = models.TextField(verbose_name='Статус аккаунта пользователя', max_length=24)
    login_bitrix = models.TextField(verbose_name='Логин пользователя в BitRix')
    password_bitrix = models.TextField(verbose_name='Пароль пользователя в Bitrix')

    def __str__(self):
        return f'[{self.id_tg}] {self.surname} {self.name}'

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'


class Organization(models.Model):
    name = models.TextField(verbose_name='Названия компании')
    INN = models.TextField(verbose_name='ИНН')
    KPP = models.TextField(verbose_name='КПП')
    OGRN = models.TextField(verbose_name='ОГРН')
    adress = models.TextField(verbose_name='Юр.Адрес')
    Mailing_address = models.TextField(verbose_name='Почтовый адрес')
    FIO_director = models.TextField(verbose_name='ФИО Директора')
    email = models.TextField(verbose_name='EMAIL')
    id_tg = models.TextField(verbose_name='Телеграмм аккаунт')
    number = models.TextField(verbose_name='Номер телефона')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Admin_profile(models.Model):
    id_tg = models.TextField(verbose_name='ID телеграмма')
    FIO = models.TextField(verbose_name='ФИО админа')
    company = models.ForeignKey(to='Organization', verbose_name='Компания', on_delete=models.CASCADE)
    rang = models.TextField(verbose_name='Уровень администратора(1,2)')

    class Meta:
        verbose_name = 'Админ группы'
        verbose_name_plural = 'Админы группы'

    def __str__(self):
        return self.FIO