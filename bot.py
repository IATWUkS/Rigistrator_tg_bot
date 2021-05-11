import datetime
import random

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import admin_bot.db_bot as db_bot
import AUTH_DATA
import auto_mailing as am
import exc_write

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
    list_user_id = []
    list_next_page_cout = []
    list_last_page_cout = []
    list_next_page_cout_user = []
    list_last_page_cout_user = []
    list_auto_mailing_company = []
    company_stop_list = []
    company_start_list = []
    list_words_block = []
    list_id_anket = []
    list_callback_support_send = []
    list_callback_support_stop = []


with open('words.txt', 'r', encoding='utf-8') as f:
    string = f.readline()
    string_2 = string.split(',')
    for word in string_2:
        try:
            data_admin.list_words_block.append(word.split(' ')[1])
        except:
            pass


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
                auto_mailing = InlineKeyboardButton('Авто рассылка', callback_data='auto_mailing')
                support = InlineKeyboardButton('Поддержка', callback_data='support')
                kb.add(view, view_organization)
                kb.add(mailing, auto_mailing)
                kb.add(support)
                bot.send_message(message.chat.id,
                                 'Привет, ' + check_profile[1] + '.\nВы администратор верхнего уровня.',
                                 reply_markup=kb)
    except:
        pass
    if check_profile == 400:
        kb = InlineKeyboardMarkup()
        start = InlineKeyboardButton('Заполнить', callback_data='registration')
        help = InlineKeyboardButton('Помощь', callback_data='help')
        check = db_bot.check_account(message.chat.id)
        if check != message.chat.id:
            kb.add(start)
        kb.add(help)
        photo = open('data/06_about.png', 'rb')
        message_text = db_bot.get_hello_message()
        bot.send_photo(message.chat.id, photo=photo,
                       caption=message_text['hello_message'], reply_markup=kb)


@bot.message_handler(commands=['help'])
def message_handler(message):
    msg = bot.send_message(message.chat.id, 'Введите ваш вопрос:')
    bot.register_next_step_handler(msg, support_message)


@bot.message_handler(content_types=['text'])
def control_message(message):
    id_chat = message.chat.id
    id_user = message.from_user.id
    name_chat = message.chat.title
    date = datetime.datetime.now()
    name_user = message.from_user.first_name
    message_chat = message.text
    db_bot.insert_message(id_chat, id_user, message_chat, date, name_chat, name_user)
    message_worlds = message.text.split()
    for word in message_worlds:
        if word.lower() in data_admin.list_words_block:
            bot.reply_to(message, 'Пожалуйста воздержитесь от употребление мата.')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'help':
        msg = bot.send_message(call.message.chat.id, 'Введите ваш вопрос:')
        bot.register_next_step_handler(msg, support_message)
    if call.data == 'menu':
        check_profile = db_bot.get_admin(call.message.chat.id)
        try:
            if int(check_profile[0]) == call.message.chat.id:
                # Интерфейс админа 1 уровня, своей организации.
                if int(check_profile[3]) == 1:
                    kb = InlineKeyboardMarkup()
                    view = InlineKeyboardButton('Просмотреть заявки', callback_data='view_anket')
                    kb.add(view)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                    'Привет, ' + check_profile[1] + '.\nВы администратор компании: ' + check_profile[
                        2],
                                          reply_markup=kb)
                    data_admin.company[str(call.message.chat.id)] = check_profile[2]
                # Интерфейс главного админа, может обработать любые заявки.
                if int(check_profile[3]) == 2:
                    kb = InlineKeyboardMarkup()
                    view = InlineKeyboardButton('Просмотреть заявки', callback_data='view_anket_adm2')
                    view_organization = InlineKeyboardButton('Просмотреть список организаций',
                                                             callback_data='view_organization')
                    mailing = InlineKeyboardButton('Рассылка', callback_data='mailing')
                    auto_mailing = InlineKeyboardButton('Авто рассылка', callback_data='auto_mailing')
                    support = InlineKeyboardButton('Поддержка', callback_data='support')
                    kb.add(view, view_organization)
                    kb.add(mailing, auto_mailing)
                    kb.add(support)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                    'Привет, ' + check_profile[1] + '.\nВы администратор верхнего уровня.',
                                          reply_markup=kb)
        except:
            pass
    # Интерфейс поддержки
    if call.data == 'support':
        kb = InlineKeyboardMarkup()
        download_message_log = InlineKeyboardButton('Выгрузка сообщений', callback_data='download_message_log')
        support_messege_answer = InlineKeyboardButton('Ответить на вопросы', callback_data='support_messege_answer')
        menu = InlineKeyboardButton('Меню', callback_data='menu')
        kb.add(download_message_log, support_messege_answer)
        kb.add(menu)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите опцию',
                              reply_markup=kb)
    if call.data == 'support_messege_answer':
        kb2 = InlineKeyboardMarkup()
        menu = InlineKeyboardButton('меню', callback_data='menu')
        kb2.add(menu)
        data_anket = db_bot.get_support_anket()
        for anket in data_anket:
            status = db_bot.get_status_support(anket['number_anket'])
            if status['status'] == 'Обработка' and anket['id_admin'] == '0' or status['status'] == 'Обработка' and \
                    anket['id_admin'] == str(call.message.chat.id):
                kb = InlineKeyboardMarkup()
                check_message = InlineKeyboardButton('Ответить',
                                                     callback_data='check_message_' + anket['number_anket'] + '_' +
                                                                   anket['id_user'] + '_' + anket['id_admin'])
                kb.add(check_message)
                data_admin.list_id_anket.append(
                    'check_message_' + anket['number_anket'] + '_' + anket['id_user'] + '_' + anket['id_admin'])
                bot.send_message(call.message.chat.id,
                                 'Номер анкеты:\n%s\n\nСообщение:\n%s' % (anket['number_anket'], anket['message']),
                                 reply_markup=kb)
        bot.send_message(call.message.chat.id, '.', reply_markup=kb2)
    if call.data == 'download_message_log':
        kb = InlineKeyboardMarkup()
        download_message_chat_all = InlineKeyboardButton('По чату', callback_data='download_message_chat_all')
        download_message_chat_user = InlineKeyboardButton('По юзеру из чата',
                                                          callback_data='download_message_chat_user')
        all_upload_message = InlineKeyboardButton('Выгрузка всех сообщений', callback_data='all_upload_message')
        back = InlineKeyboardButton('Назад', callback_data='support')
        kb.add(download_message_chat_all, download_message_chat_user)
        kb.add(all_upload_message)
        kb.add(back)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите тип '
                                                                                                     'выгрузки',
                              reply_markup=kb)
    if call.data == 'all_upload_message':
        kb = InlineKeyboardMarkup()
        menu = InlineKeyboardButton('Меню', callback_data='menu')
        kb.add(menu)
        names_chats = []
        content_message = []
        date_message = []
        data = db_bot.get_data_history_message_all()
        if data is None or str(data) == '()':
            bot.send_message(call.message.chat.id, 'Такого пользователя нет.')
        else:
            for item in data:
                names_chats.append(item['name_chat'])
                content_message.append(item['message'])
                date_message.append(item['date'])
            exc_write.create_excel_message_all_company(names_chats, content_message, date_message)
            bot.send_document(call.message.chat.id, open('all_message_company.xlsx', 'rb'))
            bot.send_message(call.message.chat.id, 'Нажмите, чтоб перейти в меню', reply_markup=kb)
    if call.data == 'download_message_chat_user':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Введите имя пользователя:')
        bot.register_next_step_handler(msg, upload_history_message_user_step_1)
    if call.data == 'download_message_chat_all':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Введите названия компании:')

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
            kb = InlineKeyboardMarkup()
            menu = InlineKeyboardButton('меню', callback_data='menu')
            kb.add(menu)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='У вас пока '
                                                                                                         'нет больше '
                                                                                                         'активных '
                                                                                                         'заявок.',
                                  reply_markup=kb)
        try:
            for data_anket in data:
                kb = InlineKeyboardMarkup()
                accept = InlineKeyboardButton('Принять', callback_data='accept_' + str(data_anket['id_tg']))
                cancel = InlineKeyboardButton('Отклонить', callback_data='cancel_' + str(data_anket['id_tg']))
                menu = InlineKeyboardButton('Меню', callback_data='menu')
                data_admin.accept_list.append('accept_' + str(data_anket['id_tg']))
                data_admin.cancel_list.append('cancel_' + str(data_anket['id_tg']))
                kb.add(accept, cancel)
                kb.add(menu)
                bot.send_message(call.message.chat.id,
                                 'Имя: ' + data_anket['name'] + '\nФамилия: ' + data_anket['surname'] + '\nПочта: ' +
                                 data_anket['email'] + '\nКомпания: ' + data_anket['company'] + '\nДолжность: ' +
                                 data_anket['position'] + '\nТелефон: ' + data_anket['number'], reply_markup=kb)
        except:
            bot.send_message(call.message.chat.id, 'У вас пока нет больше активных заявок.')
    if call.data in data_admin.accept_list:
        kb = InlineKeyboardMarkup()
        menu = InlineKeyboardButton('Меню', callback_data='menu')
        kb.add(menu)
        id_tg = call.data.split('_')[1]
        status = db_bot.edit_status('Утверждён', id_tg)
        name_user = db_bot.get_name(id_tg)
        if status == 200:
            login_bitrix = name_user[1].split('@')[0]
            password_bitrix = str(random.randint(1000000, 99999999))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Пользователь ' + name_user[0] + ' был успешно утверждён.', reply_markup=kb)
            bot.send_message(id_tg, 'Ваша учетная запись активирована, ссылка для входа: '
                                    'https://проект24.онлайн\nЛогин: ' + login_bitrix + '\nПароль: ' +
                             password_bitrix + '\nВ случае возникновения вопросов сообщите на '
                                               'почту: ваша почта.')
            db_bot.set_login_password_user_in_bitrix(login_bitrix, password_bitrix, id_tg)
        if status == 400:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Ошибка утверждения пользователя ' + name_user[0], reply_markup=kb)
    if call.data in data_admin.cancel_list:
        kb = InlineKeyboardMarkup()
        menu = InlineKeyboardButton('Меню', callback_data='menu')
        kb.add(menu)
        id_tg = call.data.split('_')[1]
        status = db_bot.edit_status('Исключён', id_tg)
        name_user = db_bot.get_name(id_tg)
        if status == 200:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Пользователь ' + name_user[0] + ' был успешно исключён.', reply_markup=kb)
        if status == 400:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Ошибка исключенния пользователя ' + name_user[0], reply_markup=kb)
    # Работа с анкетами главного админа
    if call.data == 'view_anket_adm2':
        data = db_bot.get_info_anket_admin2()
        if str(data) == '()':
            kb = InlineKeyboardMarkup()
            menu = InlineKeyboardButton('Меню', callback_data='menu')
            kb.add(menu)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='У вас пока нет больше активных заявок.', reply_markup=kb)
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
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='У вас пока нет больше активных заявок.', reply_markup=kb)
    if call.data in data_admin.accept_list:
        kb = InlineKeyboardMarkup()
        menu = InlineKeyboardButton('Меню', callback_data='menu')
        kb.add(menu)
        id_tg = call.data.split('_')[1]
        status = db_bot.edit_status('Утверждён', id_tg)
        name_user = db_bot.get_name(id_tg)
        if status == 200:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Пользователь ' + name_user[0] + ' был успешно утверждён.', reply_markup=kb)
            bot.send_message(id_tg, 'Ваша учетная запись активирована, ссылка для входа: '
                                    'https://проект24.онлайн\nЛогин: ' + name_user[1].split('@')[0] + '\nПароль: ' +
                             str(random.randint(1000000, 99999999)) + '\nВ случае возникновения вопросов сообщите на '
                                                                      'почту: ваша почта.')
        if status == 400:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Ошибка утверждения пользователя ' + name_user[0], reply_markup=kb)
    if call.data in data_admin.cancel_list:
        kb = InlineKeyboardMarkup()
        menu = InlineKeyboardButton('Меню', callback_data='menu')
        kb.add(menu)
        id_tg = call.data.split('_')[1]
        status = db_bot.edit_status('Исключён', id_tg)
        name_user = db_bot.get_name(id_tg)
        if status == 200:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Пользователь ' + name_user[0] + ' был успешно исключён.', reply_markup=kb)
        if status == 400:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Ошибка '
                                                                                                         'исключенния'
                                                                                                         ' пользователя ' +
                                                                                                         name_user[0],
                                  reply_markup=kb)
    # Интерфейс просмотра списка организаций и их участников.
    if call.data == 'view_organization':
        id = str(random.randint(10000, 9999999))
        cout = 1
        kb = InlineKeyboardMarkup()
        menu = InlineKeyboardButton('меню', callback_data='menu')
        info_organization = db_bot.get_organization_info()
        for info in info_organization:
            accept = InlineKeyboardButton(info['name'], callback_data=info['name'])
            data_admin.list_user_company.append(info['name'])
            kb.add(accept)
            if cout == 10:
                break
            cout += 1
        data_admin.list_next_page_cout.append('next_page_' + str(cout) + '_' + id)
        data_admin.list_last_page_cout.append('last_page_' + str(cout) + '_' + id)
        next_page = InlineKeyboardButton('>', callback_data='next_page_' + str(cout) + '_' + id)
        last_page = InlineKeyboardButton('<', callback_data='last_page_' + str(cout) + '_' + id)
        kb.add(last_page, menu, next_page)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите '
                                                                                                     'организацию',
                              reply_markup=kb)
    # Интерфейс просмотра организаций след страница
    if call.data in data_admin.list_next_page_cout:
        id = call.data.split('_')[3]
        cout = int(call.data.split('_')[2]) + 10
        next_cout = int(call.data.split('_')[2])
        kb = InlineKeyboardMarkup()
        menu = InlineKeyboardButton('меню', callback_data='menu')
        info_organization = db_bot.get_organization_info()
        for info in info_organization[next_cout:next_cout + 10]:
            accept = InlineKeyboardButton(info['name'], callback_data=info['name'])
            data_admin.list_user_company.append(info['name'])
            kb.add(accept)
        next_page = InlineKeyboardButton('>', callback_data='next_page_' + str(cout) + '_' + id)
        last_page = InlineKeyboardButton('<', callback_data='last_page_' + str(cout) + '_' + id)
        data_admin.list_next_page_cout.append('next_page_' + str(cout) + '_' + id)
        data_admin.list_last_page_cout.append('last_page_' + str(cout) + '_' + id)
        kb.add(last_page, menu, next_page)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите '
                                                                                                     'организацию',
                              reply_markup=kb)
    # Интерфейс просмотра списка организаций прошлой стрнц
    if call.data in data_admin.list_last_page_cout:
        id = call.data.split('_')[3]
        cout = int(call.data.split('_')[2]) - 10
        next_cout = int(call.data.split('_')[2])
        print(next_cout)
        kb = InlineKeyboardMarkup()
        menu = InlineKeyboardButton('меню', callback_data='menu')
        info_organization = db_bot.get_organization_info()
        for info in info_organization[next_cout - 20:next_cout - 10]:
            accept = InlineKeyboardButton(info['name'], callback_data=info['name'])
            data_admin.list_user_company.append(info['name'])
            kb.add(accept)
        next_page = InlineKeyboardButton('>', callback_data='next_page_' + str(cout) + '_' + id)
        last_page = InlineKeyboardButton('<', callback_data='last_page_' + str(cout) + '_' + id)
        data_admin.list_next_page_cout.append('next_page_' + str(cout) + '_' + id)
        data_admin.list_last_page_cout.append('last_page_' + str(cout) + '_' + id)
        kb.add(last_page, menu, next_page)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите '
                                                                                                     'организацию',
                              reply_markup=kb)
    # Интерфейс просмотра списка юзеров в организаций
    if call.data in data_admin.list_user_company:
        id = str(random.randint(10000, 9999999))
        cout = 1
        kb = InlineKeyboardMarkup()
        menu = InlineKeyboardButton('меню', callback_data='menu')
        user_company_data = db_bot.get_user_company(call.data)
        data_company = db_bot.get_organization_info_select_company(call.data)
        for company_data in user_company_data:
            next_user = InlineKeyboardButton(company_data['name'] + ' ' + company_data['surname'],
                                             callback_data=str(call.data) + '_' + company_data['name'] + '_next_user')
            data_admin.list_user_id.append(str(call.data) + '_' + company_data['name'] + '_next_user')
            kb.add(next_user)
            if cout == 10:
                break
            cout += 1
        next_page = InlineKeyboardButton('>',
                                         callback_data='next_page_' + str(cout) + '_' + data_company['name'] + '_' + id)
        last_page = InlineKeyboardButton('<',
                                         callback_data='last_page_' + str(cout) + '_' + data_company['name'] + '_' + id)
        data_admin.list_next_page_cout_user.append('next_page_' + str(cout) + '_' + data_company['name'] + '_' + id)
        data_admin.list_last_page_cout_user.append('last_page_' + str(cout) + '_' + data_company['name'] + '_' + id)
        data_admin.list_auto_mailing_company.append('auto_mailing_' + data_company['name'])
        auto_mailing_company = InlineKeyboardButton('Авто рассылка',
                                                    callback_data='auto_mailing_' + data_company['name'])
        kb.add(last_page, menu, next_page)
        kb.add(auto_mailing_company)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Названия '
                                                                                                     'организации: '
                                                                                                     + data_company[
                                                                                                         'name'] +
                                                                                                     '\nФИО '
                                                                                                     'Директора: ' +
                                                                                                     data_company[
                                                                                                         'FIO_director'] + '\nАдрес: ' +
                                                                                                     data_company[
                                                                                                         'adress'] + '\nНомер телефона: ' +
                                                                                                     data_company[
                                                                                                         'number'] + '\nEMAIL: ' +
                                                                                                     data_company[
                                                                                                         'email'],
                              reply_markup=kb)
    if call.data in data_admin.list_next_page_cout_user:
        cout = int(call.data.split('_')[2]) + 10
        next_cout = int(call.data.split('_')[2])
        company_name = call.data.split('_')[3]
        id = call.data.split('_')[4]
        kb = InlineKeyboardMarkup()
        menu = InlineKeyboardButton('меню', callback_data='menu')
        user_company_data = db_bot.get_user_company(company_name)
        data_company = db_bot.get_organization_info_select_company(company_name)
        for company_data in user_company_data[next_cout:next_cout + 10]:
            next_user = InlineKeyboardButton(company_data['name'] + ' ' + company_data['surname'],
                                             callback_data=str(call.data) + '_' + company_data['name'] + '_next_user')
            data_admin.list_user_id.append(str(call.data) + '_' + company_data['name'] + '_next_user')
            kb.add(next_user)
        next_page = InlineKeyboardButton('>', callback_data='next_page_' + str(cout) + '_' + company_name + '_' + id)
        last_page = InlineKeyboardButton('<', callback_data='last_page_' + str(cout) + '_' + company_name + '_' + id)
        data_admin.list_next_page_cout_user.append('next_page_' + str(cout) + '_' + company_name + '_' + id)
        data_admin.list_last_page_cout_user.append('last_page_' + str(cout) + '_' + company_name + '_' + id)
        data_admin.list_auto_mailing_company.append('auto_mailing_' + company_name)
        auto_mailing_company = InlineKeyboardButton('Авто рассылка',
                                                    callback_data='auto_mailing_' + company_name)
        kb.add(last_page, menu, next_page)
        kb.add(auto_mailing_company)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Названия '
                                                                                                     'организации: '
                                                                                                     + data_company[
                                                                                                         'name'] +
                                                                                                     '\nФИО '
                                                                                                     'Директора: ' +
                                                                                                     data_company[
                                                                                                         'FIO_director'] + '\nАдрес: ' +
                                                                                                     data_company[
                                                                                                         'adress'] + '\nНомер телефона: ' +
                                                                                                     data_company[
                                                                                                         'number'] + '\nEMAIL: ' +
                                                                                                     data_company[
                                                                                                         'email'],
                              reply_markup=kb)
    if call.data in data_admin.list_last_page_cout_user:
        company_name = call.data.split('_')[3]
        id = call.data.split('_')[4]
        cout = int(call.data.split('_')[2]) - 10
        next_cout = int(call.data.split('_')[2])
        kb = InlineKeyboardMarkup()
        menu = InlineKeyboardButton('меню', callback_data='menu')
        user_company_data = db_bot.get_user_company(company_name)
        data_company = db_bot.get_organization_info_select_company(company_name)
        for company_data in user_company_data[next_cout - 20:next_cout - 10]:
            next_user = InlineKeyboardButton(company_data['name'] + ' ' + company_data['surname'],
                                             callback_data=str(call.data) + '_' + company_data['name'] + '_next_user')
            data_admin.list_user_id.append(str(call.data) + '_' + company_data['name'] + '_next_user')
            kb.add(next_user)
        next_page = InlineKeyboardButton('>', callback_data='next_page_' + str(cout) + '_' + company_name + '_' + id)
        last_page = InlineKeyboardButton('<', callback_data='last_page_' + str(cout) + '_' + company_name + '_' + id)
        data_admin.list_next_page_cout_user.append('next_page_' + str(cout) + '_' + company_name + '_' + id)
        data_admin.list_last_page_cout_user.append('last_page_' + str(cout) + '_' + company_name + '_' + id)
        data_admin.list_auto_mailing_company.append('auto_mailing_' + company_name)
        auto_mailing_company = InlineKeyboardButton('Авто рассылка',
                                                    callback_data='auto_mailing_' + company_name)
        kb.add(last_page, menu, next_page)
        kb.add(auto_mailing_company)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Названия '
                                                                                                     'организации: '
                                                                                                     + data_company[
                                                                                                         'name'] +
                                                                                                     '\nФИО '
                                                                                                     'Директора: ' +
                                                                                                     data_company[
                                                                                                         'FIO_director'] + '\nАдрес: ' +
                                                                                                     data_company[
                                                                                                         'adress'] + '\nНомер телефона: ' +
                                                                                                     data_company[
                                                                                                         'number'] + '\nEMAIL: ' +
                                                                                                     data_company[
                                                                                                         'email'],
                              reply_markup=kb)
    # Автоматическая рассылка по компании
    if call.data in data_admin.list_auto_mailing_company:
        company = call.data.split('_')[2]
        kb = InlineKeyboardMarkup()
        start_mailing_company = InlineKeyboardButton('Начать рассылку', callback_data='start_mailing_' + company)
        stop_mailing_company = InlineKeyboardButton('Остановить рассылку', callback_data='stop_mailing_' + company)
        kb.add(start_mailing_company, stop_mailing_company)
        data_admin.company_start_list.append('start_mailing_' + company)
        data_admin.company_stop_list.append('stop_mailing_' + company)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите действие.', reply_markup=kb)
    if call.data in data_admin.company_start_list:
        company = call.data.split('_')[2]
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Введите текст для рассылки:')
        bot.register_next_step_handler(msg, next_mailing_company_steps, company)
    if call.data in data_admin.company_stop_list:
        kb = InlineKeyboardMarkup()
        menu = InlineKeyboardButton('Меню', callback_data='menu')
        kb.add(menu)
        company = call.data.split('_')[2]
        am.Status_enable.enable_company[company] = 0
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Рассылка для компании остановлена.', reply_markup=kb)
    # Взаимодействия с данными пользователя компании
    if call.data in data_admin.list_user_id:
        user_company_data = db_bot.get_user_company(call.data.split('_')[0])
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
                    back = InlineKeyboardButton('Назад', callback_data='view_organization')
                    data_admin.list_id_edit_status.append('edit_status_' + str(data_anket['id_tg']))
                    data_admin.list_id_edit_password.append('edit_password_' + str(data_anket['id_tg']))
                    data_admin.list_id_send_message.append('send_message_' + str(data_anket['id_tg']))
                    kb.add(edit_status, edit_password)
                    kb.add(send_message)
                    kb.add(back)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                    'Имя: ' + data_anket['name'] + '\nФамилия: ' + data_anket[
                        'surname'] + '\nПочта: ' +
                    data_anket['email'] + '\nКомпания: ' + data_anket['company'] + '\nДолжность: ' +
                    data_anket['position'] + '\nТелефон: ' + data_anket['number'], reply_markup=kb)
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='У этой '
                                                                                                             'компании нет пользователей.')
        except:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='У этой '
                                                                                                         'компании '
                                                                                                         'нет '
                                                                                                         'пользователей.')
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
        menu = InlineKeyboardButton('Меню', callback_data='menu')
        edit_status_on_the_accept = InlineKeyboardButton('Сменить на утверждён', callback_data=str(
            data_user['id_tg']) + '_' + 'edit_status_on_the_accept')
        edit_status_on_the_ban = InlineKeyboardButton('Сменить на исключён',
                                                      callback_data=str(
                                                          data_user['id_tg']) + '_' + 'edit_status_on_the_ban')
        kb.add(edit_status_on_the_accept, edit_status_on_the_ban)
        kb.add(menu)
        data_admin.list_edit_status_on_the_accept.append(str(data_user['id_tg']) + '_' + 'edit_status_on_the_accept')
        data_admin.list_edit_status_on_the_ban.append(str(data_user['id_tg']) + '_' + 'edit_status_on_the_ban')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Имя пользователя: ' + data_user['name'] + '\nФамилия: ' + data_user[
                                  'surname'] + '\nВ данный момент у пользователя статус: ' + data_user['status_user'],
                              reply_markup=kb)
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
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
            'Статус для пользователя ' + str(id_tg) + ' был изменён на "Утверждён".', reply_markup=kb)
        if answer == 400:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Статус для пользователя ' + str(
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
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
            'Статус для пользователя ' + str(id_tg) + ' был изменён на "Исключён".', reply_markup=kb)
        if answer == 400:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Статус для пользователя ' + str(
                                      id_tg) + ' не был изменён. Т.к он уже имеет данный статус.', reply_markup=kb)
    # Рассылка
    if call.data == 'mailing':
        kb = InlineKeyboardMarkup()
        all_user = InlineKeyboardButton('Всем участникам', callback_data='all_user')
        mailing_organiz = InlineKeyboardButton('По организации', callback_data='mailing_organiz')
        menu = InlineKeyboardButton('Меню', callback_data='menu')
        kb.add(all_user, mailing_organiz)
        kb.add(menu)
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
            select = InlineKeyboardButton('Выбрать', callback_data='company_' + names['name'])
            menu = InlineKeyboardButton('Меню', callback_data='menu')
            data_admin.list_all_data_company.append('company_' + names['name'])
            kb.add(select)
            kb.add(menu)
            bot.send_message(call.message.chat.id,
                             'Названия организации: ' + names['name'] + '\nФИО Директора: ' + names[
                                 'FIO_director'] + '\nАдрес: ' + names['adress'] + '\nНомер телефона: ' + names[
                                 'number'] + '\nEMAIL: ' +
                             names['email'], reply_markup=kb)
    if call.data in data_admin.list_all_data_company:
        name_organization = call.data.split('_')[1]
        msg = bot.send_message(call.message.chat.id, 'Введите сообщение:')
        bot.register_next_step_handler(msg, mailing_organization, name_organization)
    # Ответы на заявки об помощи
    if call.data in data_admin.list_id_anket:
        data_anket = call.data.split('_')
        admin_answer_id = db_bot.get_admin_answer_message(data_anket[2])
        if admin_answer_id['id_admin'] == '0':
            db_bot.update_message_support_admin_id(data_anket[2], data_anket[4])
        admin_answer_id = db_bot.get_admin_answer_message(data_anket[2])
        if data_anket[4] == admin_answer_id['id_admin']:
            msg = bot.send_message(call.message.chat.id, 'Введите ответ:')
            bot.register_next_step_handler(msg, send_message_user_support, data_anket[3], data_anket[2])
        else:
            kb = InlineKeyboardMarkup()
            menu = InlineKeyboardButton('Меню', callback_data='menu')
            kb.add(menu)
            bot.send_message(call.message.chat.id, 'Заявка уже обрабатывается', reply_markup=kb)
    if call.data in data_admin.list_callback_support_send:
        kb = InlineKeyboardMarkup()
        menu = InlineKeyboardButton('Меню', callback_data='menu')
        kb.add(menu)
        data_anket = call.data.split('_')
        status = db_bot.get_status_support(data_anket[2])
        if status['status'] == 'Обработка':
            msg = bot.send_message(call.message.chat.id, 'Введите сообщение:')
            bot.register_next_step_handler(msg, send_message_user_support_repeat, data_anket[3], data_anket[2])
        else:
            msg = bot.send_message(call.message.chat.id, 'Заявка уже обработана.', reply_markup=kb)
    if call.data in data_admin.list_callback_support_stop:
        data_anket = call.data.split('_')
        db_bot.update_message_support_status(data_anket[2], "Закончен")
        bot.send_message(call.message.chat.id, 'Диалог завершен.')
    # Автоматическая рассылка
    if call.data == 'auto_mailing':
        kb = InlineKeyboardMarkup()
        all_mailing_auto = InlineKeyboardButton('Всем', callback_data='all_mailing_auto')
        kb.add(all_mailing_auto)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Настройка '
                                                                                                     'автоматической '
                                                                                                     'рассылки',
                              reply_markup=kb)
    if call.data == 'all_mailing_auto':
        kb = InlineKeyboardMarkup()
        start_all_mailing_auto = InlineKeyboardButton('Запустить авто рассылку', callback_data='start_all_mailing_auto')
        stop_all_mailing_auto = InlineKeyboardButton('Остановить авто рассылку', callback_data='stop_all_mailing_auto')
        menu = InlineKeyboardButton('Меню', callback_data='menu')
        kb.add(start_all_mailing_auto, stop_all_mailing_auto)
        kb.add(menu)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите опцию',
                              reply_markup=kb)
    if call.data == 'start_all_mailing_auto':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите '
                                                                                                           'сообщение:')
        bot.register_next_step_handler(msg, mailing_auto_enable)
    if call.data == 'stop_all_mailing_auto':
        kb = InlineKeyboardMarkup()
        menu = InlineKeyboardButton('меню', callback_data='menu')
        kb.add(menu)
        am.Status_enable.enable = 0
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Рассылка для '
                                                                                                     'всех '
                                                                                                     'пользователей '
                                                                                                     'отключена.',
                              reply_markup=kb)


def upload_history_message_user_step_1(message):
    kb = InlineKeyboardMarkup()
    menu = InlineKeyboardButton('меню', callback_data='menu')
    kb.add(menu)
    name_user = message.text
    names_chats = []
    content_message = []
    date_message = []
    data = db_bot.get_data_history_message_name_user(name_user)
    if data is None or str(data) == '()':
        bot.send_message(message.chat.id, 'Такого пользователя нет.', reply_markup=kb)
    else:
        for item in data:
            names_chats.append(item['name_chat'])
            content_message.append(item['message'])
            date_message.append(item['date'])
        exc_write.create_excel_message_all_company(names_chats, content_message, date_message)
        bot.send_document(message.chat.id, open('all_message_company.xlsx', 'rb'))
        bot.send_message(message.chat.id, 'Нажмите для перехода в меню', reply_markup=kb)


def upload_history_message(message):
    kb = InlineKeyboardMarkup()
    menu = InlineKeyboardButton('меню', callback_data='menu')
    kb.add(menu)
    names_chats = []
    content_message = []
    date_message = []
    name_company = message.text
    data = db_bot.get_data_history_message(name_company)
    if data is None or str(data) == '()':
        bot.send_message(message.chat.id, 'Такой компании нет.', reply_markup=kb)
    else:
        for item in data:
            names_chats.append(item['name_chat'])
            content_message.append(item['message'])
            date_message.append(item['date'])
        exc_write.create_excel_message_all_company(names_chats, content_message, date_message)
        bot.send_document(message.chat.id, open('all_message_company.xlsx', 'rb'))
        bot.send_message(message.chat.id, 'Нажмите для перехода в меню', reply_markup=kb)


def next_mailing_steps(message):
    message_send = message.text
    msg = bot.send_message(message.chat.id, 'Введите промежуток между отправкой сообщений(сек):')
    bot.register_next_step_handler(msg, mailing_auto_enable, message_send)


def next_mailing_company_steps(message, company):
    message_send = message.text
    msg = bot.send_message(message.chat.id, 'Введите промежуток между отправкой сообщений(сек):')
    bot.register_next_step_handler(msg, mailing_auto_enable_company, company, message_send)


def mailing_auto_enable(message, message_send):
    kb = InlineKeyboardMarkup()
    menu = InlineKeyboardButton('меню', callback_data='menu')
    kb.add(menu)
    am.Status_enable.enable = 1
    bot.send_message(message.chat.id, 'Рассылка в работе.', reply_markup=kb)
    am.mailing_all(bot, message_send, int(message.text))


def mailing_auto_enable_company(message, company, message_send):
    kb = InlineKeyboardMarkup()
    menu = InlineKeyboardButton('меню', callback_data='menu')
    kb.add(menu)
    am.Status_enable.enable_company[company] = 1
    bot.send_message(message.chat.id, 'Рассылка в работе.', reply_markup=kb)
    am.auto_mailing_company(bot, message_send, int(message.text), company)


def mailing_organization(message, name_organization):
    kb = InlineKeyboardMarkup()
    menu = InlineKeyboardButton('меню', callback_data='menu')
    kb.add(menu)
    message_text = message.text
    list_id_tg_company = db_bot.get_user_company(name_organization)
    try:
        for index_id_tg in list_id_tg_company:
            bot.send_message(index_id_tg['id_tg'], message_text)
    except:
        pass
    bot.send_message(message.chat.id, 'Рассылка успешно завершена.', reply_markup=kb)


def mailing_all_user(message):
    kb = InlineKeyboardMarkup()
    menu = InlineKeyboardButton('меню', callback_data='menu')
    kb.add(menu)
    message_text = message.text
    data_list_id_tg = db_bot.get_id_tg_all_user()
    try:
        for index_id_tg in data_list_id_tg:
            bot.send_message(index_id_tg['id_tg'], message_text)
    except:
        pass
    bot.send_message(message.chat.id, 'Рассылка успешно завершена.', reply_markup=kb)


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


@bot.message_handler(content_types=['document', 'audio', 'photo', 'voice'])
def send_message_user_support_repeat(message, id_tg, number_anket):
    if message.content_type == 'text':
        content_message = message.text
        db_bot.update_message_support(number_anket, content_message)
        bot.send_message(message.chat.id, 'Вашe сообщение отправлено.')
        id_admin = db_bot.get_admin_idtg()
        for ids in id_admin:
            kb = InlineKeyboardMarkup()
            check_message = InlineKeyboardButton('Ответить',
                                                 callback_data='check_message_' + number_anket + '_' + id_tg + '_' +
                                                               ids[
                                                                   'id_tg'])
            kb.add(check_message)
            bot.send_message(ids['id_tg'], 'У вас новое сообщение\n\nСообщение:\n' + content_message, reply_markup=kb)
    else:
        if message.content_type == 'photo':
            content_message = message.caption
            db_bot.update_message_support(number_anket, content_message)
            bot.send_message(message.chat.id, 'Вашe сообщение отправлено.')
            id_admin = db_bot.get_admin_idtg()
            raw = message.photo[0].file_id
            name = raw + ".jpg"
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            with open('data/photo_message_user/' + name, 'wb') as new_file:
                new_file.write(downloaded_file)
            img = open('data/photo_message_user/' + name, 'rb')
            for ids in id_admin:
                kb = InlineKeyboardMarkup()
                check_message = InlineKeyboardButton('Ответить',
                                                     callback_data='check_message_' + number_anket + '_' + id_tg + '_' +
                                                                   ids[
                                                                       'id_tg'])
                kb.add(check_message)
                bot.send_photo(ids['id_tg'], img, 'У вас новое сообщение\n\nСообщение:\n' + content_message,
                               reply_markup=kb)
        if message.content_type == 'document':
            content_message = message.caption
            db_bot.update_message_support(number_anket, content_message)
            bot.send_message(message.chat.id, 'Вашe сообщение отправлено.')
            id_admin = db_bot.get_admin_idtg()
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = 'data/photo_message_user/' + message.document.file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            document_send = open('data/photo_message_user/' + message.document.file_name, 'rb')
            for ids in id_admin:
                kb = InlineKeyboardMarkup()
                check_message = InlineKeyboardButton('Ответить',
                                                     callback_data='check_message_' + number_anket + '_' + id_tg + '_' +
                                                                   ids[
                                                                       'id_tg'])
                kb.add(check_message)
                bot.send_document(ids['id_tg'], document_send, 'У вас новое сообщение\n\nСообщение:\n' + content_message,
                               reply_markup=kb)
        if message.content_type == 'voice':
            content_message = message.caption
            db_bot.update_message_support(number_anket, content_message)
            bot.send_message(message.chat.id, 'Вашe сообщение отправлено.')
            id_admin = db_bot.get_admin_idtg()
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open('data/photo_message_user/' + message.voice.file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            voice_send = open('data/photo_message_user/' + message.voice.file_name, 'rb')
            for ids in id_admin:
                kb = InlineKeyboardMarkup()
                check_message = InlineKeyboardButton('Ответить',
                                                     callback_data='check_message_' + number_anket + '_' + id_tg + '_' +
                                                                   ids[
                                                                       'id_tg'])
                kb.add(check_message)
                bot.send_voice(ids['id_tg'], voice_send, 'У вас новое сообщение\n\nСообщение:\n' + content_message,
                               reply_markup=kb)


def send_message_user_support(message, id_tg, number_anket):
    if message.content_type == 'text':
        kb = InlineKeyboardMarkup()
        send_message = InlineKeyboardButton('Написать',
                                            callback_data='send_message_' + number_anket + '_' + str(message.chat.id))
        stop_message = InlineKeyboardButton('Закончить',
                                            callback_data='stop_message_' + number_anket + '_' + str(message.chat.id))
        kb.add(send_message, stop_message)
        data_admin.list_callback_support_send.append('send_message_' + number_anket + '_' + str(message.chat.id))
        data_admin.list_callback_support_stop.append('stop_message_' + number_anket + '_' + str(message.chat.id))
        bot.send_message(id_tg, "Ваша заявка " + number_anket + " обработана\nСообщение:\n\n" + message.text,
                         reply_markup=kb)
    else:
        if message.content_type == 'photo':
            kb = InlineKeyboardMarkup()
            send_message = InlineKeyboardButton('Написать',
                                                callback_data='send_message_' + number_anket + '_' + str(
                                                    message.chat.id))
            stop_message = InlineKeyboardButton('Закончить',
                                                callback_data='stop_message_' + number_anket + '_' + str(
                                                    message.chat.id))
            kb.add(send_message, stop_message)
            data_admin.list_callback_support_send.append('send_message_' + number_anket + '_' + str(message.chat.id))
            data_admin.list_callback_support_stop.append('stop_message_' + number_anket + '_' + str(message.chat.id))
            print(message.photo)
            raw = message.photo[0].file_id
            name = raw + ".jpg"
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            with open('data/photo_message_user/' + name, 'wb') as new_file:
                new_file.write(downloaded_file)
            img = open('data/photo_message_user/' + name, 'rb')
            bot.send_photo(id_tg, img, "Ваша заявка " + number_anket + " обработана\nСообщение:\n\n" + message.caption,
                           reply_markup=kb)
        if message.content_type == 'document':
            kb = InlineKeyboardMarkup()
            send_message = InlineKeyboardButton('Написать',
                                                callback_data='send_message_' + number_anket + '_' + str(
                                                    message.chat.id))
            stop_message = InlineKeyboardButton('Закончить',
                                                callback_data='stop_message_' + number_anket + '_' + str(
                                                    message.chat.id))
            kb.add(send_message, stop_message)
            data_admin.list_callback_support_send.append('send_message_' + number_anket + '_' + str(message.chat.id))
            data_admin.list_callback_support_stop.append('stop_message_' + number_anket + '_' + str(message.chat.id))
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = 'data/photo_message_user/' + message.document.file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            document_send = open('data/photo_message_user/' + message.document.file_name, 'rb')
            bot.send_document(id_tg, document_send,
                              "Ваша заявка " + number_anket + " обработана\nСообщение:\n\n" + message.caption,
                              reply_markup=kb)
        if message.content_type == 'voice':
            kb = InlineKeyboardMarkup()
            send_message = InlineKeyboardButton('Написать',
                                                callback_data='send_message_' + number_anket + '_' + str(
                                                    message.chat.id))
            stop_message = InlineKeyboardButton('Закончить',
                                                callback_data='stop_message_' + number_anket + '_' + str(
                                                    message.chat.id))
            kb.add(send_message, stop_message)
            data_admin.list_callback_support_send.append('send_message_' + number_anket + '_' + str(message.chat.id))
            data_admin.list_callback_support_stop.append('stop_message_' + number_anket + '_' + str(message.chat.id))
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open('data/photo_message_user/' + message.voice.file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            voice_send = open('data/photo_message_user/' + message.voice.file_name, 'rb')
            bot.send_voice(id_tg, voice_send,
                           "Ваша заявка " + number_anket + " обработана\nСообщение:\n\n" + message.caption,
                           reply_markup=kb)


def support_message(message):
    if message.content_type == 'text':
        number_anket = str(random.randint(100000, 999999999))
        content_message = message.text
        db_bot.insert_message_support(number_anket, message.chat.id, content_message)
        db_bot.update_message_support_status(number_anket, "Обработка")
        bot.send_message(message.chat.id, 'Ваша заявка отправлена.')
        id_admin = db_bot.get_admin_idtg()
        for ids in id_admin:
            kb = InlineKeyboardMarkup()
            check_message = InlineKeyboardButton('Ответить',
                                                 callback_data='check_message_' + number_anket + '_' + str(
                                                     message.chat.id) + '_' + ids['id_tg'])
            kb.add(check_message)
            data_admin.list_id_anket.append(
                'check_message_' + number_anket + '_' + str(message.chat.id) + '_' + ids['id_tg'])
            bot.send_message(ids['id_tg'], 'У вас новая заявка\n\nСообщение:\n' + content_message, reply_markup=kb)
    else:
        if message.content_type == 'photo':
            number_anket = str(random.randint(100000, 999999999))
            content_message = message.caption
            db_bot.insert_message_support(number_anket, message.chat.id, content_message)
            db_bot.update_message_support_status(number_anket, "Обработка")
            bot.send_message(message.chat.id, 'Ваша заявка отправлена.')
            id_admin = db_bot.get_admin_idtg()
            raw = message.photo[0].file_id
            name = raw + ".jpg"
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            with open('data/photo_message_user/' + name, 'wb') as new_file:
                new_file.write(downloaded_file)
            img = open('data/photo_message_user/' + name, 'rb')
            for ids in id_admin:
                kb = InlineKeyboardMarkup()
                check_message = InlineKeyboardButton('Ответить',
                                                     callback_data='check_message_' + number_anket + '_' + str(
                                                         message.chat.id) + '_' + ids['id_tg'])
                kb.add(check_message)
                data_admin.list_id_anket.append(
                    'check_message_' + number_anket + '_' + str(message.chat.id) + '_' + ids['id_tg'])
                bot.send_photo(ids['id_tg'], img, 'У вас новая заявка\n\nСообщение:\n' + content_message,
                               reply_markup=kb)
        if message.content_type == 'document':
            number_anket = str(random.randint(100000, 999999999))
            content_message = message.caption
            db_bot.insert_message_support(number_anket, message.chat.id, content_message)
            db_bot.update_message_support_status(number_anket, "Обработка")
            bot.send_message(message.chat.id, 'Ваша заявка отправлена.')
            id_admin = db_bot.get_admin_idtg()
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = 'data/photo_message_user/' + message.document.file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            document_send = open('data/photo_message_user/' + message.document.file_name, 'rb')
            for ids in id_admin:
                kb = InlineKeyboardMarkup()
                check_message = InlineKeyboardButton('Ответить',
                                                     callback_data='check_message_' + number_anket + '_' + str(
                                                         message.chat.id) + '_' + ids['id_tg'])
                kb.add(check_message)
                data_admin.list_id_anket.append(
                    'check_message_' + number_anket + '_' + str(message.chat.id) + '_' + ids['id_tg'])
                bot.send_document(ids['id_tg'], document_send, 'У вас новая заявка\n\nСообщение:\n' + content_message,
                                  reply_markup=kb)
        if message.content_type == 'voice':
            number_anket = str(random.randint(100000, 999999999))
            content_message = message.caption
            db_bot.insert_message_support(number_anket, message.chat.id, content_message)
            db_bot.update_message_support_status(number_anket, "Обработка")
            bot.send_message(message.chat.id, 'Ваша заявка отправлена.')
            id_admin = db_bot.get_admin_idtg()
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open('data/photo_message_user/' + message.voice.file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            voice_send = open('data/photo_message_user/' + message.voice.file_name, 'rb')
            for ids in id_admin:
                kb = InlineKeyboardMarkup()
                check_message = InlineKeyboardButton('Ответить',
                                                     callback_data='check_message_' + number_anket + '_' + str(
                                                         message.chat.id) + '_' + ids['id_tg'])
                kb.add(check_message)
                data_admin.list_id_anket.append(
                    'check_message_' + number_anket + '_' + str(message.chat.id) + '_' + ids['id_tg'])
                bot.send_voice(voice_send, ids['id_tg'], 'У вас новая заявка\n\nСообщение:\n' + content_message,
                               reply_markup=kb)


def send_message_company_user_photo(message, id_tg, url, message_text):
    try:
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
    except:
        pass


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
