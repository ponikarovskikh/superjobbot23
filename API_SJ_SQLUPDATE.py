import requests
import json
import  time
import sqlite3
from urllib.parse import *

#  Api-БЛОК Superjob
# ======================================================================================================

def update_api_keys():
    access_token, refresh_token, client_secret, client_id, token_group = sql_get_api_keys_info()
    params = {
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }
    url = "https://api.superjob.ru/2.0/oauth2/refresh_token/"
    response = requests.get(url, params=params)
    resjson = response.json()
    access_token = resjson['access_token']
    sql_update_api_keys(access_token)
    # with open('tokens.json', 'r') as f:
    #     dict = json.load(f)
    # dict['access_token']=acc
    # with open('tokens.json', 'w') as f:
    #     json.dump(dict, f)
    return  access_token



def get_vacancy_objects(keyword, town, payment):
        # идентификация
        # ======================================================
        # with open('tokens.json', 'r') as f:
        #     dict = json.load(f)
        # api_key=dict['access_token']
        # app_id=dict['client_secret']
        access_token, refresh_token, client_secret, client_id, token_group=sql_get_api_keys_info()
        # --------------------------------------------------------
        params = {
            'payment_from': f'{payment}',
            "sort_new": time.time(),
            "keyword": f"{keyword}",
            "town": f'{town}'
        }
        headers = {
            'X-Api-App-Id': client_secret,
            'Authorization': f"Bearer {access_token}"
        }
        url = "https://api.superjob.ru/2.0/vacancies/"
        response = requests.get(url, headers=headers, params=params ).json()
        resjson_form = json.dumps(response, ensure_ascii=False, indent=2)
        # ===========================================================
        if 'error' in resjson_form:
            if response['error']['code'] == 410:  # обработка ошибки 410
                update_api_keys()  # функция для получения нового ключа
                get_vacancy_objects(keyword, town, payment)
        elif 'objects' in resjson_form:
            pyform = json.loads(resjson_form)
            newvacancy=pyform['objects']
            return newvacancy



#
#


















                                                        # SQL-БЛОК
# =====================================================================================================================
# ||||                         КЛЮЧИ                             |||||||
# ----------------------------------------------------------------
# создание таблицы со всеми ключами для api
def sqlkeysbaseinfo():
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    # Создаем таблицу "users", если ее еще нет в базе данных
    cursor.execute("""CREATE TABLE IF NOT EXISTS sj_keyss (
                                 access_token TEXT ,
                                 refresh_token TEXT,
                                 client_secret TEXT,
                                 client_id TEXT,
                                 token_group TEXT)""")
    conn.commit()
    with open('tokens.json', 'r') as f:
        dict = json.load(f)
    access_token = dict['access_token']
    client_secret = dict['client_secret']
    refresh_token=dict['refresh_token']
    client_id=dict['client_id']
    token_group=dict['token_group']
    query = f"INSERT INTO sj_keyss (access_token, refresh_token, client_secret, client_id,token_group) VALUES ('{access_token}', '{refresh_token}', '{client_secret}', '{client_id}','{token_group}')"
    cursor.execute(query)
    conn.commit()

# получение актуальной информации о ключах к апи и группе
def sql_get_api_keys_info():
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"SELECT access_token, refresh_token, client_secret, client_id,token_group FROM sj_keyss WHERE client_id='{2100}'"
    cursor.execute(query)
    data = cursor.fetchone()
    return data




# занесение в базу после обновления ключа access_token
def sql_update_api_keys(access_token):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"UPDATE sj_keyss SET access_token = '{access_token}' WHERE client_id='{2100}'"
    cursor.execute(query)
    conn.commit()





    # if access_token==True and client_secret==True:
    #     access_token, refresh_token, client_secret, client_id, token_group=data
    #     return access_token,client_secret
    # Печатаем данные
    # if data is not None:
    #     access_token, refresh_token, client_secret, client_id,token_group = data
    #     print(f"access_token:{access_token}, refresh_token:{refresh_token}, client_secret:{client_secret},client_id:{client_id},token_group:{token_group}")
    #
# получение токена группы из базы данных
def sql_get_token_group_vk():
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"SELECT token_group FROM sj_keyss WHERE client_id='{2100}'"
    cursor.execute(query)
    data = cursor.fetchone()
    idgroup = data
    return idgroup

# --------------------------------------------------------------------------------------------------------






# -----------------------------------------------------------
# БД Пользователей                                      |||||
# -----------------------------------------------------------
# создание таблицы для хранения инфы о пользвателях
def conn_to_dbifousers():
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    # Создаем таблицу "users", если ее еще нет в базе данных
    cursor.execute("""CREATE TABLE IF NOT EXISTS sj_table0 (
                             id INTEGER ,
                             prof TEXT,
                             city TEXT,
                             salary TEXT)""")
    conn.commit()




def e45():
    # подключаемся к базе данных
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()

    # добавляем колонку "статус подписки"
    cursor.execute('ALTER TABLE sj_subs_users ADD COLUMN latestid TEXT;')

    # добавляем колонку "позиция"
    cursor.execute('ALTER TABLE sj_subs_users ADD COLUMN maxposition INTEGER;')

    # сохраняем изменения в базе данных
    conn.commit()

    # закрываем соединение
    conn.close()













# созданик таблицы для хранения информации о юзерах
def createtableusers():
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    # Создаем таблицу "users", если ее еще нет в базе данных
    cursor.execute("""CREATE TABLE IF NOT EXISTS sj_subs_users (
                                     iduser TEXT ,
                                     city TEXT,
                                     profession TEXT,
                                     salary TEXT,
                                    status TEXT, position INTEGER,
                                    latestid TEXT,
                                    maxposition INTEGER)""")

    conn.commit()

# забив сначала id и города(включая проверку на наличие ифнормации по id)
def sql_save_info_city(iduser,city):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()

    # Проверяем наличие информации в БД по id
    query = f"SELECT city FROM sj_subs_users WHERE iduser = '{iduser}'"
    cursor.execute(query)
    result = cursor.fetchone()

    # Если информация уже есть, то обновляем ее, иначе создаем новую запись
    if result is not None:
        query = f"UPDATE sj_subs_users SET city = '{city}' WHERE iduser = '{iduser}'"
        cursor.execute(query)
    else:
        query = f"INSERT INTO sj_subs_users (iduser, city) VALUES ('{iduser}', '{city}')"
        cursor.execute(query)
    conn.commit()

# вставка професии
def sql_save_info_prof(iduser,prof):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"UPDATE sj_subs_users SET profession = '{prof}' WHERE iduser = '{iduser}' "
    cursor.execute(query)
    conn.commit()

# вставка зарплаты
def sql_save_info_salary(iduser,sal):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"UPDATE sj_subs_users SET salary = '{sal}' WHERE iduser = '{iduser}' "
    cursor.execute(query)
    conn.commit()

# выгрузка данных по id пользователя
def sql_get_user_info(iduser):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"SELECT profession, city, salary FROM sj_subs_users WHERE iduser='{iduser}'"
    cursor.execute(query)
    data = cursor.fetchone()
    profession, city, salary = data
    return  profession, city, salary


# сохранение лимита на прокрутку вакансий (длина массива)
def sql_position_limit_set(iduser,maxposition):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"SELECT maxposition FROM sj_subs_users WHERE iduser='{iduser}'"
    cursor.execute(query)
    data = cursor.fetchone()
    if "None" in data or "None" not in data:
        query = f"UPDATE sj_subs_users SET maxposition = '{maxposition}' WHERE iduser = '{iduser}' "
        cursor.execute(query)
        conn.commit()

# полуение длины списка вакансий
def sql_position_limit_get(iduser):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"SELECT maxposition FROM sj_subs_users WHERE iduser='{iduser}'"
    cursor.execute(query)
    data = cursor.fetchone()
    limit = data
    return limit[0]

# получение текущего местоположения пользователя на списке выдачи вакансий
def sql_position_giving_vacancies(iduser):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"SELECT position FROM sj_subs_users WHERE iduser='{iduser}'"
    cursor.execute(query)
    data = cursor.fetchone()
    # query = f"INSERT INTO sj_subs_users (iduser, position) VALUES ('{iduser}', '{0}')"
    if "None" in data:
        query = f"UPDATE sj_subs_users SET position = '0' WHERE iduser = '{iduser}' "
    cursor.execute(query)
    conn.commit()
    # if  data[0]>5:
    #     query = f"UPDATE sj_subs_users SET position = '0' WHERE iduser = '{iduser}' "
    #     cursor.execute(query)
    #     conn.commit()
    query = f"SELECT position FROM sj_subs_users WHERE iduser='{iduser}'"
    cursor.execute(query)
    data = cursor.fetchone()
    position=data
    return position[0]

# переход пользователя по списку выдачи выкансий по запросу
def sql_change_position(iduser,inkrem):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    if inkrem !=0:
        query = f"UPDATE sj_subs_users SET position = '{sql_position_giving_vacancies(iduser)+inkrem}' WHERE iduser = '{iduser}'"
        cursor.execute(query)
        conn.commit()
    if inkrem==0:
        query = f"UPDATE sj_subs_users SET position = '{inkrem}' WHERE iduser = '{iduser}'"
        cursor.execute(query)
        conn.commit()




# БЛОК ПОДПИСКИ
# ---------------------------------------------------------------------------------
# установление статуса подписки
def sql_subscribe_status_set(iduser,status):
    # подключение к базе данных
    conn = sqlite3.connect('sjbase0.db')
    # создание объекта-курсора
    cursor = conn.cursor()
    # SQL-запрос для получения списка всех названий колонок в таблице
    query = f"UPDATE sj_subs_users SET status = '{status}' WHERE iduser = '{iduser}'"
    cursor.execute(query)
    conn.commit()


# проверка на подписку
def sql_subscribe_status_get(iduser):
    # подключение к базе данных
    conn = sqlite3.connect('sjbase0.db')
    # создание объекта-курсора
    cursor = conn.cursor()
    query = f"SELECT status FROM sj_subs_users WHERE iduser='{iduser}'"
    cursor.execute(query)
    data = cursor.fetchone()
    return data[0]



def subspost():
    access_token, refresh_token, client_secret, client_id, token_group = sql_get_api_keys_info()
    params = {
        'name':'чзх',
        "payment_from": 10000,
        # "sort_new": time.time(),
        "keyword": "Водитель",
        "town": "Москва"

    }
    headers = {
        'X-Api-App-Id': client_secret,
        'Authorization': f"Bearer {access_token}"
    }
    url = "https://api.superjob.ru/2.0/subscriptions/"
    url_encoded_params = urlencode(params)
    response = requests.post(url, headers=headers, params=url_encoded_params).json()
    print(response)

#
# print(subspost())


def subsdelete():
    access_token, refresh_token, client_secret, client_id, token_group = sql_get_api_keys_info()

    headers = {
        'X-Api-App-Id': client_secret,
        'Authorization': f"Bearer {access_token}"
    }
    url = "https://api.superjob.ru/2.0/subscriptions/56323207"
    response = requests.delete(url, headers=headers).json()

    print(response)

# print(subsdelete())


def subs_get_check():
    access_token, refresh_token, client_secret, client_id, token_group = sql_get_api_keys_info()

    headers = {
        'X-Api-App-Id': client_secret,
        'Authorization': f"Bearer {access_token}"
    }
    url = "https://api.superjob.ru/2.0/subscriptions/56323243"
    response = requests.get(url, headers=headers).json()

    print(response)
# print(subs_get_check())


#56323213 56323213 56323207
































# БЛОК ПЕРЕХОДА НА САЙТ
# --------------------------------------------------------------------------
def sql_city_ids(city):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    if city == 'Санкт-Петербург':
        query = f"SELECT id FROM idcity WHERE title='Санкт-Петербург'"
        cursor.execute(query)
        data = cursor.fetchone()
        return data[0]
    elif city == 'Ростов-на-Дону':
        query = f"SELECT id FROM idcity WHERE title='Ростов-на-Дону'"
        cursor.execute(query)
        data = cursor.fetchone()
        return data[0]
    else:
        query = f"SELECT id FROM idcity WHERE title='{city}'"
        cursor.execute(query)
        data = cursor.fetchone()
        return data[0]
print(sql_city_ids('Санкт-Петербург'))
#забить таблицу для перехода на сайт
# создание и сохранение ссылки в бд ссылки на сайт согласно нашим параметрам
def sql_create_link(iduser,prof,sal,city):
    base_url = 'https://www.superjob.ru/vacancy/search/'

    idcity=sql_city_ids(city) #получение id города
    print(idcity)
    params = {'keywords': prof, 'geo[t][0]':idcity, 'payment_from': f'{sal}'}
    url = base_url + '?' + urlencode(params)
    sql_savelink_user_set(iduser,url)

def sql_savelink_user_set(iduser,link):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    # Выполняем SQL-запрос для создания новой колонны
    query=f"UPDATE sj_subs_users SET link = '{link}' WHERE iduser = '{iduser}'"
    cursor.execute(query)
    # Сохраняем изменения в базе данных
    conn.commit()
    # Закрываем соединение
    conn.close()

# получение сылки пользоват
def sql_savelink_user_get(iduser):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"SELECT link FROM sj_subs_users WHERE iduser='{iduser}'"
    cursor.execute(query)
    data = cursor.fetchone()
    link = data
    return link[0]


# загузка городов из апи в базу данных
def cityall():
    req=requests.get('https://api.superjob.ru/2.0/towns/?all=1&id_country=1')
    resjson = req.json()
    objects=resjson['objects']
    # print(resjson['objects'][0]['id'],resjson['objects'][0]['title'])
    conn = sqlite3.connect('sjbase0.db')
    for obj in objects:
        conn.execute("INSERT INTO idcity (id, title) VALUES (?, ?)", (obj["id"], obj["title"]))

    # Сохранение изменений
    conn.commit()


# print(sql_create_link('Водитель',10000,'Пермь'))


# ------------------------------------------------------------------------------





# увидеть все элементы
def t65():
    # # подключение к базе данных
    # conn = sqlite3.connect('sjbase0.db')
    #
    # # создание объекта-курсора
    # cursor = conn.cursor()
    #
    # # SQL-запрос для очистки таблицы
    # query = "DELETE FROM sj_subs_users"
    # cursor.execute(query)
    #
    # # подтверждение изменений
    # conn.commit()
    #
    # # закрытие соединения
    # conn.close()
    # подключение к базе данныхsj_subs_users
    conn = sqlite3.connect('sjbase0.db')

    # создание объекта-курсора
    cursor = conn.cursor()

    # SQL-запрос для получения всех строк из таблицы
    query = "SELECT * FROM idcity"
    cursor.execute(query)

    # получение всех строк
    rows = cursor.fetchall()

    # вывод всех строк
    for row in rows:
        print(row)

    # закрытие соединения
    conn.close()









