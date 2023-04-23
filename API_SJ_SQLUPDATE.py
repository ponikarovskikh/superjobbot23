import requests
import json
import  time
import sqlite3
from urllib.parse import *
import aiosqlite
import aiohttp


# =====================================================================================================================
#                                            КЛЮЧИ                                                      #
# ------------------------------------------------------------------------------------------------------#
# 0.1.создание таблицы со всеми ключами для api
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

# 1.1получение актуальной информации о ключах к апи и группе
async def sql_get_api_keys_info():
    conn = await aiosqlite.connect('sjbase0.db')
    async with conn.execute(f"SELECT access_token, refresh_token, client_secret, client_id, token_group FROM sj_keyss WHERE client_id='{2100}'") as cursor:
        data = await cursor.fetchone()
    await conn.close()
    return data

# 1.1.занесение в базу после обновления ключа access_token
def sql_update_api_keys(access_token):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"UPDATE sj_keyss SET access_token = '{access_token}' WHERE client_id='{2100}'"
    cursor.execute(query)
    conn.commit()

# 1.2.олучение токена группы из базы данных
def sql_get_token_group_vk():
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"SELECT token_group FROM sj_keyss WHERE client_id='{2100}'"
    cursor.execute(query)
    data = cursor.fetchone()
    idgroup = data
    return idgroup


















                                            #  Api-БЛОК Superjob
# ======================================================================================================
# обновление ключа access_token
async def update_api_keys():
        access_token, refresh_token, client_secret, client_id, token_group = await sql_get_api_keys_info()

        params = {
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret
        }
        url = "https://api.superjob.ru/2.0/oauth2/refresh_token/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                resjson = await response.json()
        access_token = resjson['access_token']
        sql_update_api_keys(access_token)
        return access_token

# выдача вакансий единым массивом
async def get_vacancy_objects(keyword, town, payment):
    access_token, refresh_token, client_secret, client_id, token_group = await sql_get_api_keys_info()
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
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            resjson_form = await response.json()
    # ===========================================================
    if 'error' in resjson_form:
        if resjson_form['error']['code'] == 410: # обработка ошибки 410
            await update_api_keys() # функция для получения нового ключа
            await get_vacancy_objects(keyword, town, payment)
    elif 'objects' in resjson_form:
            newvacancy = resjson_form['objects']
            return newvacancy





                                                        # SQL-БЛОК


# ---------------------------------------------------------------------------------------------------------#
#                                 БД Пользователей и выдача вакансий                                       #
# ---------------------------------------------------------------------------------------------------------#

# 0.1 создание таблицы для хранения информации о юзерах
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
                                    lastid INTEGER,
                                    maxposition INTEGER)""")

    conn.commit()

# 1.1забив сначала id и города(включая проверку на наличие ифнормации по id)
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

# 1.2.вставка професии
def sql_save_info_prof(iduser,prof):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"UPDATE sj_subs_users SET profession = '{prof}' WHERE iduser = '{iduser}' "
    cursor.execute(query)
    conn.commit()

# 1.3.вставка зарплаты
def sql_save_info_salary(iduser,sal):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"UPDATE sj_subs_users SET salary = '{sal}' WHERE iduser = '{iduser}' "
    cursor.execute(query)
    conn.commit()

# 2.1.выгрузка данных по id пользователя
def sql_get_user_info(iduser):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"SELECT profession, city, salary FROM sj_subs_users WHERE iduser='{iduser}'"
    cursor.execute(query)
    data = cursor.fetchone()
    profession, city, salary = data
    return  profession, city, salary

# 2.2.сохранение лимита на прокрутку вакансий (длина массива)
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

# 2.3.полуение длины списка вакансий
def sql_position_limit_get(iduser):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"SELECT maxposition FROM sj_subs_users WHERE iduser='{iduser}'"
    cursor.execute(query)
    data = cursor.fetchone()
    limit = data
    return limit[0]

# 2.4.получение текущего местоположения каретки просмотра пользователя на списке выдачи вакансий
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

# 2.5.переход каретки просмотра пользователя по списку выдачи выкансий по запросу
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

# сохранение первой вакансии по выдачи с 0 адресом для дальнейшей подписки
def sql_save_lastid_vcncy(iduser,lastid):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"UPDATE sj_subs_users SET lastid = '{lastid}' WHERE iduser = '{iduser}'"
    cursor.execute(query)
    conn.commit()


# -------------------------------------------------------------------------------------------------------#
#                               БЛОК ПЕРЕХОДА НА САЙТ                                                    #
# -------------------------------------------------------------------------------------------------------#
def sql_city_ids(city):#проблема с питером
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    if city=='CПБ':
        city='Спб'
    query = f"SELECT id,title FROM idcity WHERE title LIKE '{city}'"

    cursor.execute(query)
    data = cursor.fetchone()
    return data[0]

# print(sql_city_ids('Спб'))
#забить таблицу для перехода на сайт
# создание и сохранение ссылки в бд ссылки на сайт согласно нашим параметрам
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
def sql_create_link(iduser,prof,sal,city):
    base_url = 'https://www.superjob.ru/vacancy/search/'

    idcity=sql_city_ids(city) #получение id города
    print(idcity)
    params = {'keywords': prof, 'geo[t][0]':idcity, 'payment_from': f'{sal}'}
    url = base_url + '?' + urlencode(params)
    sql_savelink_user_set(iduser,url)

# получение сылки пользоват
def sql_savelink_user_get(iduser):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"SELECT link FROM sj_subs_users WHERE iduser='{iduser}'"
    cursor.execute(query)
    data = cursor.fetchone()
    link = data
    return link[0]
# 0.1.загузка городов из апи в базу данных
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
def ng():
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()

# ---------------------------------------------------------------------------------------------------------#
#                                                БЛОК ПОДПИСКИ                                             #
# ---------------------------------------------------------------------------------------------------------#
def sqlcreatetablesubs():
    # Создаем подключение к базе данных
    conn = sqlite3.connect('sjbase0.db')

    # Создаем объект "курсор"
    cursor = conn.cursor()

    # Создаем таблицу
    cursor.execute('''CREATE TABLE sjsubscript (
                    id INTEGER,
                    city TEXT,
                    salary INTEGER,
                    profession TEXT,
                    status INTEGER,
                    subscriptions INTEGER,
                    lastid INTEGER
                    )''')

    # Сохраняем изменения
    conn.commit()

    # Закрываем соединение
    conn.close()
# print(sqlcreatetablesubs())


# перегон параметров в бд sjsubscript и дальнейшее установление статуса подписки(1 или 0)
def sql_subscribe_status_set(iduser,status):
    #
    # загрузка инфы из бд subsusers
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"SELECT profession, city, salary,lastid FROM sj_subs_users WHERE iduser='{iduser}'"
    cursor.execute(query)
    data = cursor.fetchone()
    profession1, city1, salary1,lastid1=data

    # Проверяем наличие информации в БД sjsubscript по id
    query = f"SELECT status,salary,city,profession,lastid FROM sjsubscript WHERE iduser = '{iduser}'"
    cursor.execute(query)
    result = cursor.fetchone()
    # Если информация уже есть, то обновляем ее, иначе создаем новую запись
    # если создаем подписку
    if result is not None:
        print(1)
        status2, salary2, city2, profession2,lastid2 = result
        if status==1 and status2==1:
            print(1.1)
            if salary2 is not None and city2 is not None and profession2 is not None and lastid2 is not None:
                print(1.2)
                # print(profession1, profession2 ,city1,city2 ,type(salary1),type(salary2))
                if profession1!=profession2 or city1!=city2 or int(salary1)!=int(salary2) :
                    print(1.3)
                    query = f"UPDATE sjsubscript SET status='{status}',city = '{city1}',lastid = '{lastid1}',salary = '{salary1}',profession='{profession1}'WHERE iduser = '{iduser}'"
                    cursor.execute(query)
                    conn.commit()
                    # print('Данные подписки успешно обновлены')
                    return 1
                elif profession1 == profession2 and city1 == city2 and int(salary1) == int(salary2):
                    # print(1.4)
                    # query = f"UPDATE sjsubscript SET status='{status}' WHERE iduser = '{iduser}'"
                    # cursor.execute(query)
                    # conn.commit()
                    # print('Извините,Вы уже подписались на рассылку с такими параметрами')
                    return 2
        elif status == 1 and status2 == 0:
            print(2.1)
            if salary2 is not None and city2 is not None and profession2 is not None and lastid2 is not None:
                print(2.2)
                if profession1 == profession2 and city1 == city2 and int(salary1) == int(salary2):
                    query = f"UPDATE sjsubscript SET status='{status}' WHERE iduser = '{iduser}'"
                    cursor.execute(query)
                    conn.commit()
                    # print('Подписка по прежним параметры возоблена')
                    return 3
                elif profession1 != profession2 or city1 != city2 or int(salary1) != salary2:
                    print(2.3)
                    query = f"UPDATE sjsubscript SET status='{status}',city = '{city1}',lastid = '{lastid1}',salary = '{salary1}',profession='{profession1}'WHERE iduser = '{iduser}'"
                    cursor.execute(query)
                    conn.commit()
                    # print('Подписка активна, свойства обновлены')
                    return 4
        # если хотим отменить подписку
        elif status==0 and status2==1:
            print(3.1)
            query = f"UPDATE sjsubscript SET status='{status}' WHERE iduser = '{iduser}'"
            cursor.execute(query)
            conn.commit()
            # print('Рассылка отменена( \nВы всегда можете снова подписаться')
            return 5

    elif result is None:
        print(4)
        query = f"INSERT INTO sjsubscript (status,salary,iduser,city,profession,lastid) VALUES" \
                f" ('{status}', '{salary1}','{iduser}', '{city1}','{profession1}','{lastid1}')"
        cursor.execute(query)
        conn.commit()
        # print('Вы подписались на рассылку!\nДанные зарегистрированы')
        return 6

    # мой айди вк 230352030



# проверка на подписку
def sql_subscribe_status_get(iduser):
    # подключение к базе данных
    conn = sqlite3.connect('sjbase0.db')
    # создание объекта-курсора
    cursor = conn.cursor()
    query = f"SELECT iduser,status,salary,city,profession,lastid FROM sjsubscript WHERE iduser = '{iduser}'"
    cursor.execute(query)
    result = cursor.fetchone()
    # status2, salary2, city2, proffession2, subscriptions2, lastid2 = result
    return result[1]
# получение всей инфы о подписке из отдела sjscript
def sql_allinfo_subscribe_status_get(iduser):
    # подключение к базе данных
    conn = sqlite3.connect('sjbase0.db')
    # создание объекта-курсора
    cursor = conn.cursor()
    query = f"SELECT iduser,status,salary,city,profession,lastid FROM sjsubscript WHERE iduser = '{iduser}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:

        # status2, salary2, city2, proffession2, subscriptions2, lastid2 = result
        return None
    else:
        return result
# print(sql_allinfo_subscribe_status_get(230352030))

















# Функциональные запросы для работы с БД
#===========================================
# увидеть заголовки элементов sj_subs_users
def all_titles_check():
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    sql = f"PRAGMA table_info(sj_subs_users)"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
# print(all_titles_check())


# колонки талицы sj_subs_users
# iduser
# city
# profession
# salary
# position
# maxposition
# link
# lastid

# колонки sjsubscript
# city
# salary
# profession
# status
# subscriptions
# lastid
# iduser

#idcity города и коды

# удалить столбец
def deletecolumn():
        conn = sqlite3.connect('sjbase0.db')
        cursor = conn.cursor()
# # Выполняем SQL-запрос на удаление столбцов
        cursor.execute('ALTER TABLE sjsubscript DROP COLUMN id')
        conn.commit()
# print(deletecolumn())

#добавить столбцы
def createcolums():
    # подключаемся к базе данных
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()

    # добавляем колонку "статус подписки"
    cursor.execute('ALTER TABLE sjsubscript ADD COLUMN iduser INTEGER;')

    # добавляем колонку "позиция"
    # cursor.execute('ALTER TABLE sj_subs_users ADD COLUMN maxposition INTEGER;')

    # сохраняем изменения в базе данных
    conn.commit()

    # закрываем соединение
    conn.close()
# print(createcolums())



def sqlgetlastid(iduser):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"SELECT lastid FROM sj_subs_users WHERE iduser={iduser}"

    cursor.execute(query)
    data = cursor.fetchone()
    lasid=data
    return lasid[0]
# print(sqlgetlastid(230352030))

























# print(t65())


def t64():
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    # Выполняем SQL-запрос для создания новой колонны
    query = f"UPDATE idcity SET title = 'Спб' WHERE id = '{14}'"
    cursor.execute(query)
    # Сохраняем изменения в базе данных
    conn.commit()
    # Закрываем соединение
    conn.close()

# print(t64())
