import pandas as pd


def create_excel_message_all_company(names_chats, content_message, date_message):
    df = pd.DataFrame({
        'Название группы:': names_chats,
        'Сообщение': content_message,
        'Дата публикации': date_message
    })
    df.to_excel('all_message_company.xlsx')
