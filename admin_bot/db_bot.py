import pymysql
from pymysql.cursors import DictCursor


def get_conn():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='admin_bot',
        charset='utf8mb4',
        cursorclass=DictCursor
    )
    return connection


def input_pre_registration_data(row, values):
    connection = get_conn()
    try:
        sql = 'INSERT INTO adm_pre_registration_data(%s, name, surname, email, company, position, number, ' \
              'data_processing, status_user, login_bitrix, password_bitrix) VALUES ("%s", "0", "0", "0", "0", "0", ' \
              '"0", "0", "0", "0", "0")' % (row, values)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return 200, 'Ваша заявка принята, ожидайте подтверждения.'
    except:
        connection.close()
        return 400


def input_registr_data(row, values, id_tg):
    connection = get_conn()
    try:
        sql = 'UPDATE adm_pre_registration_data SET %s = "%s" WHERE id_tg = %s' % (row, values, id_tg)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return 200, 'Ваша заявка принята, ожидайте подтверждения.'
    except:
        connection.close()
        return 400, 'Ошибка записи в базу данных, попробуйте снова или обратитесь в поддержку.'


def get_admin(id_tg):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM adm_admin_profile WHERE id_tg = %s' % id_tg
        cursor.execute(sql)
        data = cursor.fetchone()
        sql_2 = 'SELECT name FROM adm_organization WHERE id = %s' % data['company_id']
        cursor.execute(sql_2)
        company = cursor.fetchone()['name']
        connection.close()
        return data['id_tg'], data['FIO'], company, data['rang']
    except:
        connection.close()
        return 400


def get_info_anket(company):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM adm_pre_registration_data WHERE company = "%s" AND status_user = "Обработка"' % company
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.close()
        return data
    except:
        return None


def get_info_anket_admin2():
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM adm_pre_registration_data WHERE status_user = "Обработка"'
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.close()
        return data
    except:
        return None


def edit_status(status, id_tg):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'UPDATE adm_pre_registration_data SET status_user = "%s" WHERE id_tg = "%s" AND status_user != "%s"' % (
        status, id_tg, status)
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return 200
    except:
        connection.close()
        return 400


def get_name(id_tg):
    try:
        connection = get_conn()
        cursor = connection.cursor()
        sql = 'SELECT * FROM adm_pre_registration_data WHERE id_tg = "%s"' % id_tg
        cursor.execute(sql)
        data = cursor.fetchone()
        connection.close()
        return data['surname'] + ' ' + data['name'], data['email']
    except:
        pass


def check_account(id_tg):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM adm_pre_registration_data WHERE id_tg = "%s"' % id_tg
        cursor.execute(sql)
        data = cursor.fetchone()
        connection.close()
        return data['id_tg']
    except:
        return None


def get_organization_info():
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM adm_organization'
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.close()
        return data
    except:
        return None


def get_user_company(company):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM adm_pre_registration_data WHERE company = "%s"' % company
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.close()
        return data
    except:
        return None


def edit_password_company_user(password, id_tg):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'UPDATE adm_pre_registration_data SET password_bitrix="%s" WHERE id_tg = %s' % (password, id_tg)
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return 200
    except:
        connection.close()
        return 400


def get_full_info_user(id_tg):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM adm_pre_registration_data WHERE id_tg = %s' % id_tg
        cursor.execute(sql)
        data = cursor.fetchone()
        connection.close()
        return data
    except:
        connection.close()
        return None


def set_login_password_user_in_bitrix(login, password, id_tg):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'UPDATE adm_pre_registration_data SET login_bitrix="%s" WHERE id_tg = %s' % (login, id_tg)
        cursor.execute(sql)
        connection.commit()
        sql = 'UPDATE adm_pre_registration_data SET password_bitrix="%s" WHERE id_tg = %s' % (password, id_tg)
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return 200
    except:
        connection.close()
        return 400


def get_id_tg_all_user():
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT id_tg FROM adm_pre_registration_data'
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.close()
        return data
    except:
        return None


def get_organization_info_select_company(company):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM adm_organization WHERE name = "%s"' % company
        cursor.execute(sql)
        data = cursor.fetchone()
        connection.close()
        return data
    except:
        return None