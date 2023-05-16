import asyncio
import json
import  time
import sqlite3
from urllib.parse import *
import aiosqlite
import aiohttp
import requests
from io import BytesIO
from PIL import Image
import urllib.parse
import matplotlib.pyplot as plt


import requests
from io import BytesIO
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
import webbrowser

















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

def sql1_get_api_keys_info():
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()

    cursor.execute("SELECT access_token, refresh_token, client_secret, client_id, token_group FROM sj_keyss WHERE client_id='2100'")
    data = cursor.fetchone()

    cursor.close()
    conn.close()

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
            print(resjson_form)
    # ===========================================================
    if 'error' in resjson_form:
        if resjson_form['error']['code'] == 410: # обработка ошибки 410
            await update_api_keys() # функция для получения нового ключа
            await get_vacancy_objects(keyword, town, payment)
    elif 'objects' in resjson_form:
            newvacancy = resjson_form['objects']
            return newvacancy


# print(get_vacancy_objects('программист','Санкт-Петербург',10000))
# asyncio.run(get_vacancy_objects('программист','Санкт-Петербург',10000))




import io

def generate_image_with_qr_code_and_text(text, qr_code_link):
    # Создание полотна размером 600x400
    canvas = Image.new("RGB", (600, 400), "white")

    # Создание объекта для рисования на полотне
    draw = ImageDraw.Draw(canvas)

    # Загрузка шрифта
    font = ImageFont.truetype("arial.ttf", size=24)

    # Создание QR-кода
    qr_code = qrcode.QRCode()
    qr_code.add_data(qr_code_link)
    qr_code_image = qr_code.make_image(fill="black", back_color="white")

    # Размещение QR-кода в левом верхнем углу
    canvas.paste(qr_code_image, (0, 0))

    # Размещение текста справа от QR-кода
    text_x = qr_code_image.width + 10
    text_y = 0
    draw.text((text_x, text_y), text, font=font, fill="black")

    # Создание временного буфера для сохранения изображения в памяти
    image_buffer = io.BytesIO()

    # Сохранение изображения в формате JPEG во временный буфер
    canvas.save(image_buffer, format="JPEG")

    # Перемещение указателя буфера в начало
    image_buffer.seek(0)

    # Чтение содержимого буфера и создание изображения в виде переменной
    image_variable = image_buffer.read()

    # Возврат изображения в виде переменной
    return image_variable

# Пример использования функции


# image_variable = generate_image_with_qr_code_and_text(text, qr_code_link)






























def generate_api_url(keywords):
    access_token, refresh_token, client_secret, client_id, token_group =  sql1_get_api_keys_info()
    base_url = 'https://api.superjob.ru/2.0/vacancies/'
    params = {'keywords[1][srws]': '1'}
    headers = {
        'X-Api-App-Id': client_secret,
        'Authorization': f"Bearer {access_token}"
    }

    # Добавляем ключевые слова в параметры запроса
    for i, keyword in enumerate(keywords):
        params[f'keywords[1][keys][{i}]'] = keyword

    # Генерируем URL-адрес API-запроса с параметрами
    url = base_url + '?' + urllib.parse.urlencode(params)
    # Возвращаем URL-адрес и заголовки
    return url, headers

# Пример использования функции
keywords = ['php', 'javascript']
api_url, headers = generate_api_url(keywords)

# Выполнение запроса к API
response = requests.get(api_url, headers=headers)

print(response)


































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
# print(sql_save_info_city(493371147,'Краснодар'))

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
    print(data)
    if data is None:
        return data
    else:

        profession, city, salary = data
        return  profession, city, salary

# print(sql_get_user_info(230352030))

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
def sql_city_ids(city):#проблема с питером #а если такого нет
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    if city=='CПБ':
        city='Спб'
    query = f"SELECT id,title FROM idcity WHERE title LIKE '%{city}%'"

    cursor.execute(query)
    data = cursor.fetchone()
    if data is None:
        return None
    else:
        return data[0]


def sql_access_cities(city):#проблема с питером #а если такого нет
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    # if city=='CПБ':
    #     city='Спб'
    query = f"SELECT title FROM idcity "

    cursor.execute(query)
    data = cursor.fetchall()
    cities=[]
    for d in data:
        print(d[0])
        d0=d[0].lower()
        cities.append(d0)
    city=city.lower()
    for object in cities:
        if city in object:
            print(object,city)
            return 1
            break
    else:
        return 0
# print(sql_access_cities('Донеeeeк'))





















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
    req= requests.get('https://api.superjob.ru/2.0/towns/?all=1&id_country=1')
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
    iduser2, status2, salary2, city2, profession2, lastid2 = sql_allinfo_subscribe_status_get(iduser)
    if status2 != None and salary2 != None and city2 != None and profession2 != None and lastid2 != None:

        print(1)
        status2, salary2, city2, profession2,lastid2 = result
        print(status2, salary2, city2, profession2,lastid2)
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

    elif  status2 == None and salary2 == None and city2 == None and profession2 == None and lastid2 == None:
        print(4)
        query = f"UPDATE sjsubscript SET status='{status}',city = '{city1}',lastid = '{lastid1}',salary = '{salary1}',profession='{profession1}'WHERE iduser = '{iduser}'"
        cursor.execute(query)
        conn.commit()
        # print('Вы подписались на рассылку!\nДанные зарегистрированы')
        iduser2, status2, salary2, city2, profession2, lastid2 = sql_allinfo_subscribe_status_get(iduser)
        print('c 0 оз', iduser2, status2, salary2, city2, profession2, lastid2)
        return 6

    # мой айди вк 230352030


def null_objects_status_change(iduser,status):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"UPDATE sjsubscript SET status='{status}' WHERE iduser = '{iduser}'"
    cursor.execute(query)
    conn.commit()

# вставка имени подписки
def sql_subs_name_set(iduser,subsname):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"SELECT subscriptname1 FROM sjsubscript WHERE iduser = '{iduser}'"
    cursor.execute(query)
    result = cursor.fetchone()
    print(result)
    if result is not None:
        query = f"UPDATE sjsubscript SET subscriptname1='{subsname}' WHERE iduser = '{iduser}'"
    else:
        query = f"INSERT INTO sjsubscript (iduser, subscriptname1) VALUES ('{iduser}', '{subsname}')"
    cursor.execute(query)
    conn.commit()
# print(sql_subs_name_set(230352030,'jne'))
def sql_subs_name_get(iduser):
    # подключение к базе данных
    conn = sqlite3.connect('sjbase0.db')
    # создание объекта-курсора
    cursor = conn.cursor()
    query = f"SELECT subscriptname1 FROM sjsubscript WHERE iduser = '{iduser}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return None
    else:

        return result[0]
# print(sql_subs_name_get(1))




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
    # print(result)
    # print(result[0], 1)
    if result is None:

        # status2, salary2, city2, proffession2, subscriptions2, lastid2 = result
        return None
    else:

        return result
# print(sql_allinfo_subscribe_status_get(492583722))

















# Функциональные запросы для работы с БД
#===========================================



# лого компаний

async def resize_image_from_url(url, width, height):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            img_bytes = await response.read()
            img = Image.open(BytesIO(img_bytes))
            img_resized = img.resize((width, height), Image.ANTIALIAS)
            return img_resized

# print(resize_image_from_url('https://www.mirf.ru/wp-content/uploads/2015/11/Alien-Tech.jpg',1920,1080))


















# увидеть заголовки элементов sj_subs_users
def all_titles_check():
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    sql = f"PRAGMA table_info(sjsubscript)"
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





def f78():
# Установите соединение с базой данных
    conn = sqlite3.connect('sjbase0.db')

    # Создайте курсор
    cursor = conn.cursor()

    # Выполните запрос SQL
    cursor.execute("SELECT * FROM sjsubscript")

    # Получите все строки результата
    rows = cursor.fetchall()

    # Выведите информацию
    for row in rows:
        print(row)

    # Закройте курсор и соединение с базой данных
    cursor.close()
    conn.close()

# print(f78())




def sql_zabivinf0(id):
    conn = sqlite3.connect('sjbase0.db')
    # Создайте курсор
    cursor = conn.cursor()
    # Выполните запрос SQL для удаления строки
    cursor.execute("DELETE FROM sjsubscript WHERE iduser = ?", (id,))

    # Подтвердите изменения в базе данных
    conn.commit()

    # Закройте курсор и соединение с базой данных
    cursor.close()
    conn.close()
# print(sql_zabivinf0(230352030))

# print(f78())
# ('Новосибирск', 10000, 'HR-менеджер', 1, None, 46057918, 230352030, None, None, 'Шмшрршрш')
# ('Москва', 50000, 'Педагог', 1, None, 37918050, 492583722, None, None, 'Подписка по уже заданным параметрам')
# ('Москва', 10000, 'Разработчик', 0, None, 46136762, 718624833, None, None, 'Подписка по уже заданным параметрам')
# (None, None, None, None, None, None, 1, None, 'CHE000 0 0 0', 'CHE000 0 0 0')
# (None, None, None, None, None, None, 552771990, None, None, None)
# (None, None, None, None, None, None, 317349044, None, None, 'Event')
# (None, None, None, None, None, None, 715877690, None, None, 'Менеджер Махачкала')
# None




# удалить столбец
def deletecolumn():
        conn = sqlite3.connect('sjbase0.db')
        cursor = conn.cursor()
# # Выполняем SQL-запрос на удаление столбцов
        cursor.execute('ALTER TABLE sjsubscript DROP COLUMN subsname')
        conn.commit()
# print(deletecolumn())

#добавить столбцы
def createcolums():
    # подключаемся к базе данных
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()

    # добавляем колонку "статус подписки"
    cursor.execute('ALTER TABLE sjsubscript ADD COLUMN subscriptname1 TEXT;')

    # добавляем колонку "позиция"
    # cursor.execute('ALTER TABLE sj_subs_users ADD COLUMN maxposition INTEGER;')

    # сохраняем изменения в базе данных
    conn.commit()

    # закрываем соединение
    conn.close()
# print(createcolums())




# def addcolumn():
#     conn = sqlite3.connect('sjbase0.db')
#     cursor = conn.cursor()
#
#     # Добавляем новую колонку refresh со значением 0
#     cursor.execute('ALTER TABLE sj_subs_users ADD COLUMN refresh INTEGER DEFAULT 0')
#
#     conn.commit()
#     conn.close()
# print(addcolumn())







# def sql_refresh_value(user_id):
#     conn = sqlite3.connect('my_database.db')
#     c = conn.cursor()
#     # Проверяем текущее значение refresh для пользователя
#     c.execute(f"SELECT refresh FROM my_table WHERE user_id={user_id}")
#     current_value = c.fetchone()[0]
#     # Инвертируем значение refresh
#     new_value = 0 if current_value == 1 else 1
#     # Обновляем значение refresh в таблице
#     c.execute(f"UPDATE my_table SET refresh={new_value} WHERE user_id={user_id}")
#     conn.commit()
#     conn.close()










#  в зависимости от бд ласт ид
def sqlgetlastid(iduser):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"SELECT lastid FROM sj_subs_users WHERE iduser={iduser}"

    cursor.execute(query)
    data = cursor.fetchone()
    lasid=data
    return lasid[0]
# print(sqlgetlastid(230352030))




def sqlsetlastid1(lastid1,iduser):
    conn = sqlite3.connect('sjbase0.db')
    cursor = conn.cursor()
    query = f"UPDATE sjsubscript SET lastid = '{lastid1}' WHERE iduser = '{iduser}'"
    cursor.execute(query)
    conn.commit()
# print(sqlsetlastid1(1,718624833))










# id 230352030   46097756  -  46097756
# equal
# id 492583722   45350823  -  45350823
# equal
# id 718624833   34243086  -  34243086
# equal










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

def deleteusers():
    conn = sqlite3.connect('sjbase0.db')

    # Создаем курсор для работы с базой данных
    cur = conn.cursor()

    # Выполняем запрос на удаление элемента с указанным iduser
    cur.execute(f"DELETE FROM sj_subs_users WHERE iduser ={230352030} ")

    # Сохраняем изменения в базе данных
    conn.commit()
    # cur.execute("DELETE FROM sjsubscript WHERE iduser = ?", (2303520301,))
    #
    # # Сохраняем изменения в базе данных
    # conn.commit()
    # Закрываем соединение с базой данных
    conn.close()

# print(deleteusers())


def sql_idusers_get():
    # подключение к базе данных
    conn = sqlite3.connect('sjbase0.db')
    c = conn.cursor()

    # выбираем все значения столбца "iduser"
    c.execute("SELECT iduser FROM sj_subs_users")

    # создаем список "idusers"
    idusers = [row[0] for row in c.fetchall()]

    # закрываем подключение к базе данных
    conn.close()
    print(idusers)
    return idusers


# print(sql_idusers_get())