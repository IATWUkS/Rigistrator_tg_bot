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
        verbose_name = 'аккаунт'
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
        verbose_name = 'компанию'
        verbose_name_plural = 'Компании'


class Admin_profile(models.Model):
    id_tg = models.TextField(verbose_name='ID телеграмма')
    FIO = models.TextField(verbose_name='ФИО админа')
    company = models.ForeignKey(to='Organization', verbose_name='Компания', on_delete=models.CASCADE)
    rang = models.TextField(verbose_name='Уровень администратора(1,2)')

    class Meta:
        verbose_name = 'админа группы'
        verbose_name_plural = 'Админы группы'

    def __str__(self):
        return self.FIO


class logging_message(models.Model):
    id_chat = models.TextField(verbose_name='ID чата')
    id_user = models.TextField(verbose_name='ID пользователя')
    message = models.TextField(verbose_name='Сообщение')
    date = models.DateTimeField(verbose_name='Дата отправки сообщения')
    name_chat = models.TextField(verbose_name='Названия чата')
    name_user = models.TextField(verbose_name='Имя пользователя')

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.id_chat


class support_messenger(models.Model):
    number_anket = models.TextField(verbose_name='Номер заявки')
    id_user = models.TextField(verbose_name='ID пользователя')
    message = models.TextField(verbose_name='Сообщение')
    status = models.TextField(verbose_name='Статус')
    id_admin = models.TextField(verbose_name='ID админа обрабатывающего заявку')

    class Meta:
        verbose_name = 'чат поддержки'
        verbose_name_plural = 'Поддержка'

    def __str__(self):
        return self.number_anket


class edit_hello_message(models.Model):
    hello_message = models.TextField(verbose_name='Начальное сообщение')

    class Meta:
        verbose_name = 'Изменения текста сообщений'
        verbose_name_plural = 'Изменения текста сообщений'