__users = {
    'admin': '$2b$12$ZzB/puhiBTdzqPEXdKz2BujOkaoGMBeKpyEA/M3T/TwDx67RJ8VNm',
    'test': '$2b$12$fbq1pd5sc0dWTv8LraJFheXH0mpTk0ylMou8RzKwDn0XjCsdthbiu'
}


def get_user(login: str):
    try:
        return type('', (object,), {'login': login, 'password': __users[login]})()
    except KeyError:
        return None
