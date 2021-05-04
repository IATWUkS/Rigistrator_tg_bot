import random

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import admin_bot.db_bot as db_bot
import AUTH_DATA

TOKEN = AUTH_DATA.TG_TOKEN
bot = telebot.TeleBot(TOKEN)


class data_admin:
    company = {}
    accept_list = []
    cancel_list = []
    list_user_company = []
    list_id_edit_password = []
    list_id_edit_status = []
    list_id_send_message = []
    list_edit_status_on_the_accept = []
    list_edit_status_on_the_ban = []
    list_all_data_company = []


@bot.message_handler(commands=['start'])
def message_handler(message):
    check_profile = db_bot.get_admin(message.from_user.id)
    try:
        if int(check_profile[0]) == message.from_user.id:
            # Интерфейс админа 1 уровня, своей организации.
            if int(check_profile[3]) == 1:
                kb = InlineKeyboardMarkup()
                view = InlineKeyboardButton('Просмотреть заявки', callback_data='view_anket')
                kb.add(view)
                bot.send_message(message.chat.id,
                                 'Привет, ' + check_profile[1] + '.\nВы администратор компании: ' + check_profile[2],
                                 reply_markup=kb)
                data_admin.company[str(message.from_user.id)] = check_profile[2]
            # Интерфейс главного админа, может обработать любые заявки.
            if int(check_profile[3]) == 2:
                kb = InlineKeyboardMarkup()
                view = InlineKeyboardButton('Просмотреть заявки', callback_data='view_anket_adm2')
                view_organization = InlineKeyboardButton('Просмотреть список организаций',
                                                         callback_data='view_organization')
                mailing = InlineKeyboardButton('Рассылка', callback_data='mailing')
                kb.add(view, view_organization)
                kb.add(mailing)
                bot.send_message(message.chat.id,
                                 'Привет, ' + check_profile[1] + '.\nВы администратор верхнего уровня.',
                                 reply_markup=kb)
    except:
        pass
    if check_profile == 400:
        kb = InlineKeyboardMarkup()
        start = InlineKeyboardButton('Заполнить', callback_data='registration')
        kb.add(start)
        photo = open('data/06_about.png', 'rb')
        bot.send_photo(message.chat.id, photo=photo,
                       caption='Добрый день, я администратор корпоративного портала "Портал".\nДля регистрации прошу '
                               'заполнить информацию о себе:', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # Регистрация нового пользователя
    if call.data == 'registration':
        check = db_bot.check_account(call.message.chat.id)
        if check == call.message.chat.id:
            bot.send_message(call.message.chat.id, 'У вас уже есть оставленная заявка.')
        else:
            db_bot.input_pre_registration_data('id_tg', call.message.chat.id)
            msg = bot.send_message(call.message.chat.id, 'Введите ваше имя:')
            bot.register_next_step_handler(msg, surname_input)
    if call.data == 'accept_data_processing':
        db_bot.input_registr_data('status_user', 'Обработка', call.message.chat.id)
        answer = db_bot.input_registr_data('data_processing', 'Согласен', call.message.chat.id)
        if answer[0] == 401:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer[1])
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer[1])
    # Работа с заявками админа своей организации
    if call.data == 'view_anket':
        data = db_bot.get_info_anket(data_admin.company[str(call.message.chat.id)])
        if str(data) == '()':
            bot.send_message(call.message.chat.id, 'У вас пока нет больше активных заявок.')
        try:
            for data_anket in data:
                kb = InlineKeyboardMarkup()
                accept = InlineKeyboardButton('Принять', callback_data='accept_' + str(data_anket['id_tg']))
                cancel = InlineKeyboardButton('Отклонить', callback_data='cancel_' + str(data_anket['id_tg']))
                data_admin.accept_list.append('accept_' + str(data_anket['id_tg']))
                data_admin.cancel_list.append('cancel_' + str(data_anket['id_tg']))
                kb.add(accept, cancel)
                bot.send_message(call.message.chat.id,
                                 'Имя: ' + data_anket['name'] + '\nФамилия: ' + data_anket['surname'] + '\nПочта: ' +
                                 data_anket['email'] + '\nКомпания: ' + data_anket['company'] + '\nДолжность: ' +
                                 data_anket['position'] + '\nТелефон: ' + data_anket['number'], reply_markup=kb)
        except:
            bot.send_message(call.message.chat.id, 'У вас пока нет больше активных заявок.')
    if call.data in data_admin.accept_list:
        id_tg = call.data.split('_')[1]
        status = db_bot.edit_status('Утверждён', id_tg)
        name_user = db_bot.get_name(id_tg)
        if status == 200:
            login_bitrix = name_user[1].split('@')[0]
            password_bitrix = str(random.randint(1000000, 99999999))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Пользователь ' + name_user[0] + ' был успешно утверждён.')
            bot.send_message(id_tg, 'Ваша учетная запись активирована, ссылка для входа: '
                                    'https://проект24.онлайн\nЛогин: ' + login_bitrix + '\nПароль: ' +
                             password_bitrix + '\nВ случае возникновения вопросов сообщите на '
                                               'почту: ваша почта.')
            db_bot.set_login_password_user_in_bitrix(login_bitrix, password_bitrix, id_tg)
        if status == 400:
            bot.send_message(call.message.chat.id, 'Ошибка утверждения пользователя ' + name_user[0])
    if call.data in data_admin.cancel_list:
        id_tg = call.data.split('_')[1]
        status = db_bot.edit_status('Исключён', id_tg)
        name_user = db_bot.get_name(id_tg)
        if status == 200:
            bot.send_message(call.message.chat.id, 'Пользователь ' + name_user[0] + ' был успешно исключён.')
        if status == 400:
            bot.send_message(call.message.chat.id, 'Ошибка исключенния пользователя ' + name_user[0])
    # Работа с анкетами главного админа
    if call.data == 'view_anket_adm2':
        data = db_bot.get_info_anket_admin2()
        if str(data) == '()':
            bot.send_message(call.message.chat.id, 'У вас пока нет больше активных заявок.')
        try:
            for data_anket in data:
                kb = InlineKeyboardMarkup()
                accept = InlineKeyboardButton('Принять', callback_data='accept_' + str(data_anket['id_tg']))
                cancel = InlineKeyboardButton('Отклонить', callback_data='cancel_' + str(data_anket['id_tg']))
                data_admin.accept_list.append('accept_' + str(data_anket['id_tg']))
                data_admin.cancel_list.append('cancel_' + str(data_anket['id_tg']))
                kb.add(accept, cancel)
                bot.send_message(call.message.chat.id,
                                 'Имя: ' + data_anket['name'] + '\nФамилия: ' + data_anket['surname'] + '\nПочта: ' +
                                 data_anket['email'] + '\nКомпания: ' + data_anket['company'] + '\nДолжность: ' +
                                 data_anket['position'] + '\nТелефон: ' + data_anket['number'], reply_markup=kb)
        except:
            bot.send_message(call.message.chat.id, 'У вас пока нет больше активных заявок.')
    if call.data in data_admin.accept_list:
        id_tg = call.data.split('_')[1]
        status = db_bot.edit_status('Утверждён', id_tg)
        name_user = db_bot.get_name(id_tg)
        if status == 200:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Пользователь ' + name_user[0] + ' был успешно утверждён.')
            bot.send_message(id_tg, 'Ваша учетная запись активирована, ссылка для входа: '
                                    'https://проект24.онлайн\nЛогин: ' + name_user[1].split('@')[0] + '\nПароль: ' +
                             str(random.randint(1000000, 99999999)) + '\nВ случае возникновения вопросов сообщите на '
                                                                      'почту: ваша почта.')
        if status == 400:
            bot.send_message(call.message.chat.id, 'Ошибка утверждения пользователя ' + name_user[0])
    if call.data in data_admin.cancel_list:
        id_tg = call.data.split('_')[1]
        status = db_bot.edit_status('Исключён', id_tg)
        name_user = db_bot.get_name(id_tg)
        if status == 200:
            bot.send_message(call.message.chat.id, 'Пользователь ' + name_user[0] + ' был успешно исключён.')
        if status == 400:
            bot.send_message(call.message.chat.id, 'Ошибка исключенния пользователя ' + name_user[0])
    # Интерфейс просмотра списка организаций и их участников.
    if call.data == 'view_organization':
        info_organization = db_bot.get_organization_info()
        for info in info_organization:
            kb = InlineKeyboardMarkup()
            accept = InlineKeyboardButton('Просмотреть список пользователей', callback_data=info['name'])
            data_admin.list_user_company.append(info['name'])
            kb.add(accept)
            bot.send_message(call.message.chat.id, 'Названия организации: ' + info['name'] + '\nФИО Директора: ' + info[
                'FIO_director'] + '\nАдрес: ' + info['adress'] + '\nНомер телефона: ' + info['number'] + '\nEMAIL: ' +
                             info['email'], reply_markup=kb)
    if call.data in data_admin.list_user_company:
        user_company_data = db_bot.get_user_company(call.data)
        try:
            if str(user_company_data) != '()':
                for data_anket in user_company_data:
                    kb = InlineKeyboardMarkup()
                    edit_status = InlineKeyboardButton('Изменить статус',
                                                       callback_data='edit_status_' + str(data_anket['id_tg']))
                    edit_password = InlineKeyboardButton('Изменить пароль',
                                                         callback_data='edit_password_' + str(data_anket['id_tg']))
                    send_message = InlineKeyboardButton('Отправить сообщение',
                                                        callback_data='send_message_' + str(data_anket['id_tg']))
                    data_admin.list_id_edit_status.append('edit_status_' + str(data_anket['id_tg']))
                    data_admin.list_id_edit_password.append('edit_password_' + str(data_anket['id_tg']))
                    data_admin.list_id_send_message.append('send_message_' + str(data_anket['id_tg']))
                    kb.add(edit_status, edit_password)
                    kb.add(send_message)
                    bot.send_message(call.message.chat.id,
                                     'Имя: ' + data_anket['name'] + '\nФамилия: ' + data_anket[
                                         'surname'] + '\nПочта: ' +
                                     data_anket['email'] + '\nКомпания: ' + data_anket['company'] + '\nДолжность: ' +
                                     data_anket['position'] + '\nТелефон: ' + data_anket['number'], reply_markup=kb)
            else:
                bot.send_message(call.message.chat.id, 'У этой компании нет пользователей.')
        except:
            bot.send_message(call.message.chat.id, 'У этой компании нет пользователей.')
    # Отправка сообщения пользователю по id
    if call.data in data_admin.list_id_send_message:
        id_tg = call.data.split('_')[2]
        msg = bot.send_message(call.message.chat.id, 'Введите сообщение для отправки(без ссылки или фото):')
        bot.register_next_step_handler(msg, send_message_company_user, id_tg)
    # Изменения пароля пользователю
    if call.data in data_admin.list_id_edit_password:
        id_tg = call.data.split('_')[2]
        msg = bot.send_message(call.message.chat.id, 'Введите новый пароль:')
        bot.register_next_step_handler(msg, edit_password_company_user, id_tg)
    # Изменения статуса пользователя
    if call.data in data_admin.list_id_edit_status:
        id_tg = call.data.split('_')[2]
        data_user = db_bot.get_full_info_user(id_tg)
        kb = InlineKeyboardMarkup()
        edit_status_on_the_accept = InlineKeyboardButton('Сменить на утверждён', callback_data=str(
            data_user['id_tg']) + '_' + 'edit_status_on_the_accept')
        edit_status_on_the_ban = InlineKeyboardButton('Сменить на исключён',
                                                      callback_data=str(
                                                          data_user['id_tg']) + '_' + 'edit_status_on_the_ban')
        kb.add(edit_status_on_the_accept, edit_status_on_the_ban)
        data_admin.list_edit_status_on_the_accept.append(str(data_user['id_tg']) + '_' + 'edit_status_on_the_accept')
        data_admin.list_edit_status_on_the_ban.append(str(data_user['id_tg']) + '_' + 'edit_status_on_the_ban')
        bot.send_message(call.message.chat.id, 'Имя пользователя: ' + data_user['name'] + '\nФамилия: ' + data_user[
            'surname'] + '\nВ данный момент у пользователя статус: ' + data_user['status_user'], reply_markup=kb)
    # Изменения статуса на Утверждён
    if call.data in data_admin.list_edit_status_on_the_accept:
        kb = InlineKeyboardMarkup()
        back = InlineKeyboardButton('Назад', callback_data='view_organization')
        kb.add(back)
        id_tg = call.data.split('_')[0]
        status = 'Утверждён'
        answer = db_bot.edit_status(status, id_tg)
        if answer == 200:
            name_user = db_bot.get_full_info_user(id_tg)
            login_bitrix = name_user['email'].split('@')[0]
            password_bitrix = str(random.randint(1000000, 99999999))
            bot.send_message(id_tg, 'Ваша учетная запись активирована, ссылка для входа: '
                                    'https://проект24.онлайн\nЛогин: ' + login_bitrix + '\nПароль: ' +
                             password_bitrix + '\nВ случае возникновения вопросов сообщите на '
                                               'почту: ваша почта.')
            db_bot.set_login_password_user_in_bitrix(login_bitrix, password_bitrix, id_tg)
            bot.send_message(call.message.chat.id,
                             'Статус для пользователя ' + str(id_tg) + ' был изменён на "Утверждён".', reply_markup=kb)
        if answer == 400:
            bot.send_message(call.message.chat.id, 'Статус для пользователя ' + str(
                id_tg) + ' не был изменён. Т.к он уже имеет данный статус.', reply_markup=kb)
    # Изменения статуса на Исключён
    if call.data in data_admin.list_edit_status_on_the_ban:
        kb = InlineKeyboardMarkup()
        back = InlineKeyboardButton('Назад', callback_data='view_organization')
        kb.add(back)
        id_tg = call.data.split('_')[0]
        status = 'Исключён'
        answer = db_bot.edit_status(status, id_tg)
        if answer == 200:
            bot.send_message(id_tg, 'Вас исключили с компании.')
            bot.send_message(call.message.chat.id,
                             'Статус для пользователя ' + str(id_tg) + ' был изменён на "Исключён".', reply_markup=kb)
        if answer == 400:
            bot.send_message(call.message.chat.id, 'Статус для пользователя ' + str(
                id_tg) + ' не был изменён. Т.к он уже имеет данный статус.', reply_markup=kb)
    if call.data == 'mailing':
        kb = InlineKeyboardMarkup()
        all_user = InlineKeyboardButton('Всем участникам', callback_data='all_user')
        mailing_organiz = InlineKeyboardButton('По организации', callback_data='mailing_organiz')
        kb.add(all_user, mailing_organiz)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите способ '
                                                                                                     'рассылки:',
                              reply_markup=kb)
    if call.data == 'all_user':
        msg = bot.send_message(call.message.chat.id, 'Введите текст сообщения:')
        bot.register_next_step_handler(msg, mailing_all_user)
    if call.data == 'mailing_organiz':
        list_all_data_company = db_bot.get_organization_info()
        for names in list_all_data_company:
            kb = InlineKeyboardMarkup()
            select = InlineKeyboardButton('Выбрать', callback_data=names['name'])
            data_admin.list_all_data_company.append(names['name'])
            kb.add(select)
            bot.send_message(call.message.chat.id, 'Названия организации: ' + names['name'] + '\nФИО Директора: ' + names[
                'FIO_director'] + '\nАдрес: ' + names['adress'] + '\nНомер телефона: ' + names['number'] + '\nEMAIL: ' +
                             names['email'], reply_markup=kb)
    if call.data in data_admin.list_all_data_company:
        name_organization = call.data
        msg = bot.send_message(call.message.chat.id, 'Введите сообщение:')
        bot.register_next_step_handler(msg, mailing_organization, name_organization)


def mailing_organization(message, name_organization):
    message_text = message.text
    list_id_tg_company = db_bot.get_user_company(name_organization)
    try:
        for index_id_tg in list_id_tg_company:
            bot.send_message(index_id_tg['id_tg'], message_text)
    except:
        pass
    bot.send_message(message.chat.id, 'Рассылка успешно завершена.')


def mailing_all_user(message):
    message_text = message.text
    data_list_id_tg = db_bot.get_id_tg_all_user()
    try:
        for index_id_tg in data_list_id_tg:
            bot.send_message(index_id_tg['id_tg'], message_text)
    except:
        pass
    bot.send_message(message.chat.id, 'Рассылка успешно завершена.')


def edit_password_company_user(message, id_tg):
    kb = InlineKeyboardMarkup()
    back = InlineKeyboardButton('Назад', callback_data='view_organization')
    kb.add(back)
    try:
        answer = db_bot.edit_password_company_user(password=message.text, id_tg=id_tg)
        if answer == 200:
            bot.send_message(id_tg, 'Администратор сменил пароль вашей учетной записи.\nВаш новый пароль: ' + str(
                message.text))
            bot.send_message(message.chat.id, 'Пароль для пользователя ' + str(id_tg) + ' был изменен.',
                             reply_markup=kb)
        if answer == 400:
            bot.send_message(message.chat.id, 'Пароль для пользователя ' + str(id_tg) + 'не был изменен. Ошибка '
                                                                                        'записи в базу данных',
                             reply_markup=kb)
    except:
        bot.send_message(message.chat.id, 'Пароль не удалось изменить.', reply_markup=kb)


def send_message_company_user(message, id_tg):
    message_text = message.text
    kb = InlineKeyboardMarkup()
    back = InlineKeyboardButton('Назад', callback_data='view_organization')
    kb.add(back)
    msg = bot.send_message(message.chat.id, 'Добавьте ссылку(если ссылка не нужна введите 0):')
    bot.register_next_step_handler(msg, send_message_company_user_url, id_tg, message_text)


def send_message_company_user_url(message, id_tg, message_text):
    url = message.text
    msg = bot.send_message(message.chat.id, 'Добавьте фото(если фото не нужно введите 0):')
    bot.register_next_step_handler(msg, send_message_company_user_photo, id_tg, url, message_text)


@bot.message_handler(content_types=['document', 'audio', 'photo'])
def send_message_company_user_photo(message, id_tg, url, message_text):
    if message.content_type == 'photo':
        raw = message.photo[2].file_id
        name = raw + ".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('data/photo_message_user/' + name, 'wb') as new_file:
            new_file.write(downloaded_file)
        img = open('data/photo_message_user/' + name, 'rb')
        if url != "0" and url is not None:
            kb = InlineKeyboardMarkup()
            back = InlineKeyboardButton('Назад', callback_data='view_organization')
            kb.add(back)
            kb_2 = InlineKeyboardMarkup()
            url_button = InlineKeyboardButton('Перейти по ссылке', url=url)
            kb_2.add(url_button)
            try:
                bot.send_photo(id_tg, img, message_text, reply_markup=kb_2)
                bot.send_message(message.chat.id, 'Сообщение успешно отправлено!', reply_markup=kb)
            except:
                bot.send_message(message.chat.id, 'Сообщение не удалось отправить.', reply_markup=kb)
        else:
            kb = InlineKeyboardMarkup()
            back = InlineKeyboardButton('Назад', callback_data='view_organization')
            kb.add(back)
            try:
                bot.send_photo(id_tg, img, message_text)
                bot.send_message(message.chat.id, 'Сообщение успешно отправлено!', reply_markup=kb)
            except:
                bot.send_message(message.chat.id, 'Сообщение не удалось отправить.', reply_markup=kb)
    else:
        if url != "0":
            kb = InlineKeyboardMarkup()
            back = InlineKeyboardButton('Назад', callback_data='view_organization')
            kb.add(back)
            kb_2 = InlineKeyboardMarkup()
            url_button = InlineKeyboardButton('Перейти по ссылке', url=url)
            kb_2.add(url_button)
            try:
                bot.send_message(id_tg, message_text, reply_markup=kb_2)
                bot.send_message(message.chat.id, 'Сообщение успешно отправлено!', reply_markup=kb)
            except:
                bot.send_message(message.chat.id, 'Сообщение не удалось отправить.', reply_markup=kb)
        else:
            kb = InlineKeyboardMarkup()
            back = InlineKeyboardButton('Назад', callback_data='view_organization')
            kb.add(back)
            try:
                bot.send_message(id_tg, message_text)
                bot.send_message(message.chat.id, 'Сообщение успешно отправлено!', reply_markup=kb)
            except:
                bot.send_message(message.chat.id, 'Сообщение не удалось отправить.', reply_markup=kb)


def surname_input(message):
    db_bot.input_registr_data('name', message.text, message.from_user.id)
    msg = bot.send_message(message.chat.id, 'Введите вашу фамилию:')
    bot.register_next_step_handler(msg, email_input)


def email_input(message):
    db_bot.input_registr_data('surname', message.text, message.from_user.id)
    msg = bot.send_message(message.chat.id, 'Введите ваш EMAIL:')
    bot.register_next_step_handler(msg, company_input)


def company_input(message):
    db_bot.input_registr_data('email', message.text, message.from_user.id)
    msg = bot.send_message(message.chat.id, 'Введите название вашей компании:')
    bot.register_next_step_handler(msg, position_input)


def position_input(message):
    db_bot.input_registr_data('company', message.text, message.from_user.id)
    msg = bot.send_message(message.chat.id, 'Введите вашу должность:')
    bot.register_next_step_handler(msg, number_input)


def number_input(message):
    db_bot.input_registr_data('position', message.text, message.from_user.id)
    msg = bot.send_message(message.chat.id, 'Введите ваш номер телефона:')
    bot.register_next_step_handler(msg, data_processing_input)


def data_processing_input(message):
    kb = InlineKeyboardMarkup()
    start = InlineKeyboardButton('Согласен', callback_data='accept_data_processing')
    kb.add(start)
    db_bot.input_registr_data('number', message.text, message.from_user.id)
    bot.send_message(message.chat.id, 'Согласны на обработку ваших данных?', reply_markup=kb)


bot.polling(none_stop=True)