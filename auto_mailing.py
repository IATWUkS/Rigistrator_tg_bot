from time import sleep
import admin_bot.db_bot as db_bot


class Status_enable:
    enable = 0
    enable_company = {}


def mailing_all(bot, message, time):
    while Status_enable.enable == 1:
        id_tg_all_user = db_bot.get_id_tg_all_user()
        for data in id_tg_all_user:
            bot.send_message(data['id_tg'], message)
        sleep(time)


def auto_mailing_company(bot, message, time, company):
    while Status_enable.enable_company[company] == 1:
        id_tg_all_user = db_bot.get_user_company(company)
        for data in id_tg_all_user:
            bot.send_message(data['id_tg'], message)
        sleep(time)
