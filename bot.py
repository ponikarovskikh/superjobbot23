
from vkbottle.bot import Bot,Message
from vkbottle import Keyboard,KeyboardButtonColor,Text,OpenLink,BaseStateGroup
from API_SJ_SQLUPDATE import *
from datetime import datetime
import asyncio
import aiosqlite
import aiohttp

global bot

async def bot_loop():
    bot=Bot(token=sql_get_token_group_vk())
    x=1
    x=3
# обьявление переменных для маршрута сбора пользовательской инфы
    class SUBSDSATA(BaseStateGroup):
        CITY=0
        PROF=1
        PAY=2
        GO=4
        MENU = 5
        GET = 6
        CONT=7
# получение id usera
    async def iduserget(message:Message):
        users = await bot.api.users.get(message.from_id)
        id = users[0].id
        return id

# 0 этап Добро пожаловать
# ----------------------------------------------
    @bot.on.message(state=None,payload={"command":"start"})#от SUPERJOB💚
    @bot.on.message(text=['Начать','начать'])
    async def starthandler(message:Message):

        users = await bot.api.users.get(message.from_id)
        keyboard=(Keyboard(inline=False,one_time=True)
              .add(Text('Искать работу',{'cmd':'reg'}), color=KeyboardButtonColor.POSITIVE)
              )

        await message.answer(f'Привет, {users[0].first_name}! \n Это бот вакансий.'
                         '\n Поможем найти новые вакансии по вашим параметрам:\n Город | Профессия | Заработная плата📝\nНажмите кнопку "Искать работу"🔔',keyboard=keyboard)

    # поиск пользователя в базе
    @bot.on.message(payload={"cmd":"reg"})#от SUPERJOB💚
    async def starthandler(message:Message):
        iduser = await iduserget(message)
        check=sql_get_user_info(iduser)

        keyboard0=(Keyboard(inline=False,one_time=True)
               .add(Text('Главное меню', {'cmd': 'menu'}))

              )
        keyboard1 = (Keyboard(inline=False, one_time=True)
                 .add(Text('Начать', {'cmd': 'change'}))

                 )

        if check is not None:
            profession, city, salary = sql_get_user_info(iduser)
            checksubs=sql_allinfo_subscribe_status_get(iduser)
            if checksubs is not None:
                iduser2, status2, salary2, city2, profession2, lastid2 = sql_allinfo_subscribe_status_get(iduser)

                active = 9
                if status2 == 1:
                    active = 'Да'
                elif status2 == 0:
                    active = 'Нет'
                await message.answer(f'Смотри, мы нашли твои параметры:\n\n'
                             f"Ваши параметры для поиска:\n"
                             f"Город: {city}\n"
                             f"Профессия: {profession}\n"
                             f"Зарплата от: {salary}₽\n\n"
                             f"Ваши параметры для рассылки:\n"
                             f"Город : {city2}\n"
                             f"Профессия: {profession2}\n"
                             f"Зарплата от: {salary2}₽\n"
                             f"Активна: {active}\n\n"
                             f'Если запросы изменились - Изменить ', keyboard=keyboard0)
                await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
            if checksubs is None:
                await message.answer(f'Смотри, мы нашли твои параметры:\n\n'
                                     f"Ваши параметры для поиска:\n"
                                     f"Город: {city}\n"
                                     f"Профессия: {profession}\n"
                                     f"Зарплата от: {salary}₽\n\n" , keyboard=keyboard0)
                await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
        if check is None:
            await message.answer("О,друг, ты впервые у нас!"
                             " Выбирай скорее свои параметры и\n будем подберать тебе вкусные вакансии", keyboard=keyboard1)
            await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
# 1 этап получение инфы о городе
# ---------------------------------------
    @bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'change'})
    async def city_handler(message:Message):

        keyboard = (
            Keyboard(inline=True)
            .add(Text('Москва'))
            .add(Text('Казань'))
            .row()
            .add(Text('CПБ'))
            .row()
            .add(Text('Воронеж'))
            .add(Text("Калуга"))
            .row()
            .add(Text('Ростов-на-Дону'))
            .row()
            .add(Text('Волгоград'))
            .add(Text('Краснодар'))
            .row()
            .add(Text('Владивосток'))

                 )



    # photo1= await photo_upd.upload('logo1.jpg')
        await message.answer("Найти вакансии? Я это могу! Приступим? Выбирай город из списка или пиши вручную 🧭🌁", keyboard=keyboard,attachment='photo-217363563_457239024')
        await bot.state_dispenser.set(message.peer_id,SUBSDSATA.PROF)
# 2 этап получение инфы о професии
#---------------------------------------------
    @bot.on.message(state=SUBSDSATA.PROF)
    async def prof_handler(message:Message):
        sql_save_info_city(await iduserget(message),message.text) #поправить питер чето сьехал
        keyboarad=(Keyboard(inline=True)
            .add(Text('Программист'))
            .add(Text('Директор'))
            .row()
            .add(Text('Тестировщик'))
            .add(Text('Дизайнер'))
            .row()
            .add(Text('Администратор'))
            .add(Text('Юрист'))
            .row()
            .add(Text('Подработка'))
            .add(Text('Водитель'))
            .row()
            .add(Text('Менеджер'))
            .add(Text('Продавец'))
               )

        await message.answer('Теперь определись с профессией или напиши свой вариант‍🚀',keyboard=keyboarad,attachment='photo-217363563_457239032')
        await bot.state_dispenser.set(message.peer_id,SUBSDSATA.PAY)
# 3 этап получение инфы о желаемом заработке
# --------------------------------------------
    @bot.on.message(state=SUBSDSATA.PAY)
    async def pay_handler(message:Message):

        keyboarad0 = (Keyboard(inline=True)
                 .add(Text('10 000₽',{'cmd':'edit'}))
                 .add(Text('20 000₽',{'cmd':'edit'}))
                 .row()
                 .add(Text('30 000₽',{'cmd':'edit'}))
                 .add(Text('50 000₽',{'cmd':'edit'}))
                 .row()
                 .add(Text('80 000₽',{'cmd':'edit'}))
                 .add(Text('100 000₽',{'cmd':'edit'}))
                 .row()
                 .add(Text('150 000₽',{'cmd':'edit'}))
                 .add(Text('200 000₽',{'cmd':'edit'}))
                 .row()
                 .add(Text('300 000₽',{'cmd':'edit'}))
                 .add(Text('400 000₽',{'cmd':'edit'}))   )
        sql_save_info_prof(await iduserget(message),message.text)

        await message.answer('Сколько денег хочешь зарабатывать? Выбери или напиши вручную 💵', keyboard=keyboarad0,attachment='photo-217363563_457239028')
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)



# обработка и выдача Результата
# ------------------------------------------
    @bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'edit'})
    async def initial_handler(message:Message):
        iduser= await iduserget(message)
        print(iduser)
        pay= message.text
        if '₽' in str(pay):
            pay = message.text
            pay = pay.rstrip('₽').replace(' ', '')
            sql_save_info_salary(iduser,pay)
            sql_change_position(iduser, 0)
         # sql_subscribe_status_set(iduser,'0')
        keyboardstart = (Keyboard(one_time=True,inline=False)
                .add(Text('Получить',{'cmd':'get'}), color=KeyboardButtonColor.POSITIVE)
                .add(Text('Изменить', {'cmd': 'change'}), color=KeyboardButtonColor.PRIMARY)
                .add(Text('Назад', {'cmd': 'menu'}), color=KeyboardButtonColor.SECONDARY)
                )
        keyboardcontin = (Keyboard(one_time=True, inline=False)

                     .add(Text('Изменить', {'cmd': 'change'}), color=KeyboardButtonColor.PRIMARY)
                     .row()
                     .add(Text('Назад', {'cmd': 'menu'}), color=KeyboardButtonColor.SECONDARY)
                     )
        profession, city, salary=sql_get_user_info(iduser)
        pos=sql_position_giving_vacancies(iduser)
        # await message.answer(sql_position_giving_vacancies(await iduserget(message)))
        if int (pos) != 0:
            await message.answer(f"Ваши параметры🎲:\nГород : {city}"
                         f"\nПрофессия: {profession}\n"
                         f"Зарплата от: {salary}"
                         f'\n\n Посмотреть вакансии - "Получить"\n'
                         f'Если Запросы изменились - Изменить ',keyboard=keyboardcontin)
        elif int(pos)==0:
            await message.answer(f"Ваши параметры🎲:\nГород : {city}"
                         f"\nПрофессия: {profession}\n"
                         f"Зарплата от: {salary}"
                         f'\n\n Посмотреть вакансии - "Получить"\n'
                      ,keyboard=keyboardstart)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
#выдача 5 вакансий и переход в меню
    @bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'get'})
    async def confirm_handler(message: Message):
        iduser = await iduserget(message)
        keyboard0 = (Keyboard(one_time=True)
                 .add(Text('Главное меню', {'cmd':'menu'}))
                 .add(Text('Подписаться на рассылку', {'cmd': 'subsstart'}))
                 )
        keyboard1=(Keyboard(one_time=False)
                .add(Text('Поищем другое',{'cmd':'edit'}), color=KeyboardButtonColor.PRIMARY)
                .add(Text('Главное меню', {'cmd': 'menu'}))
               )

# запрос и сохранение ответа апи!проработка варианта действий
# при недействительном токене! с блоком вакансий и колвом вакансий
# ---------------------------------------
        profession, city, salary = sql_get_user_info(iduser)
        newvacancy = await get_vacancy_objects(profession, city, salary)

        lenlist=len(newvacancy)
        sql_position_limit_set(iduser,lenlist)

# # разбивка
# # -----------------------------------------------
        if sql_position_limit_get(iduser)!=0:
            sql_change_position(iduser, 0)
            try:
                iduser = await iduserget(message)
                while sql_position_giving_vacancies(iduser) < 5 and sql_position_giving_vacancies(iduser) < sql_position_limit_get(iduser)   :
                        pst=sql_position_giving_vacancies(iduser)
                    # if profession in newvacancy[pst]['profession']:
                        profession = newvacancy[pst]['profession']
                        link = newvacancy[pst]['link']
                        lastid=newvacancy[pst]['id']
                        if pst==0 and lastid!=sqlgetlastid(iduser):
                            sql_save_lastid_vcncy(iduser,lastid)
                        keyboard1=(Keyboard(inline=True)
                                .add(OpenLink(link,'Открыть🚀'))
                                )
                        if int(newvacancy[pst]['payment_from'])!=0 and int(newvacancy[pst]['payment_from'])!=0 :
                         payment = f"до {newvacancy[pst]['payment_to']}₽"

                        elif int(newvacancy[pst]['payment_from'])==0:
                         payment = f" до {newvacancy[pst]['payment_to']}"

                        elif int(newvacancy[pst]['payment_to']) == 0:
                         payment = f" до {newvacancy[pst]['payment_to']}"
                        else:
                         payment = f"{newvacancy[pst]['payment_from']} - {newvacancy[pst]['payment_to']}"
                        if payment=='0 - 0':
                            payment='После собеседования'
                        company = f'{newvacancy[pst]["firm_name"]}'
                        await message.answer(
                        f"💼Вакансия: {profession} \n 🏙Компания:{company} \n 💲Условия оплаты: {payment} \n🔜Оставить заявку и узнать подробне о вакансии:",
                        keyboard=keyboard1)
                        sql_change_position(iduser,1)
                await message.answer('Понравилис вакансии жми подписаться на рассылку и получай свежии вакансии первым',keyboard=keyboard0)
                await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
            except IndexError:
                await message.answer('Извините, мы не нашли вакансий согласно вашим параметрам\n',keyboard=keyboard1)
                await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
        else:
            await message.answer('Мы не нашли вакансий согласно вашим параметрам',keyboard=keyboard1)
            await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
#Главное меню
    @bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'menu'})
    async def Menu_handler(message: Message):
        iduser = await iduserget(message)
        profession, city, salary = sql_get_user_info(iduser)
        if city == 'Cпб':
            city='СПБ'
        print(profession, city, salary )
        print(type(city))
        sql_create_link(iduser,profession,salary,city)
        mainlink=sql_savelink_user_get(iduser)
        # await  message.answer(mainlink)
        keyboard0 = (Keyboard(one_time=False)
                     .add(OpenLink(mainlink, 'Перейти на сайт'))
                     .add(Text('Смотреть еще', {'cmd': 'add'}))
                     .row()
                     .add(Text('Параметры поиска',{'cmd':'edit'}))
                     .add(Text('Создать подписку на рассылку',{'cmd':'subsfinish'}))
                       )
        keyboard1 = (Keyboard(one_time=False)
                     .add(OpenLink(mainlink, 'Перейти на сайт'))
                     .add(Text('Смотреть еще', {'cmd': 'add'}))
                     .row()
                     .add(Text('Параметры поиска',{'cmd':'edit'}))
                     .row()
                     .add(Text('Изменить подписку',{'cmd':'subsstart'}))
                     .row()
                     .add(Text('Отписаться от рассылки', {'cmd': 'subscancel'})))
        keyboard2 = (Keyboard(one_time=False)
                     .add(OpenLink(mainlink, 'Перейти на сайт'))
                     .add(Text('Смотреть еще', {'cmd': 'add'}))
                     .row()
                     .add(Text('Параметры поиска', {'cmd': 'edit'}))
                     .row()
                     .add(Text('Получать рассылку', {'cmd': 'subsfinish'})))
        if sql_allinfo_subscribe_status_get(iduser) is None:
                await message.answer("Главное меню",keyboard=keyboard0)
        elif sql_subscribe_status_get(iduser) is not None:
            if sql_subscribe_status_get(iduser)==1:
                await message.answer("Главное меню",keyboard=keyboard1)
            elif sql_subscribe_status_get(iduser)==0:
                await message.answer("Главное меню", keyboard=keyboard2)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
#доп выдача
    @bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'add'})
    async def ADD_handler(message:Message):
        # keyboard0 = (Keyboard(one_time=False)
        #              .add(Text('Давай еще', {'cmd': 'add'}))
        #              .add(Text('Назад',{'cmd': 'menu'}))
        #              )
        keyboard2 = (Keyboard(one_time=False)
                   .add(Text('Назад', {'cmd': 'menu'}))
                     )
        iduser = await iduserget(message)
        if sql_position_giving_vacancies(iduser)+5 <= sql_position_limit_get(iduser):
            profession, city, salary = sql_get_user_info(iduser)
            newvacancy = await get_vacancy_objects(profession, city, salary)
            for next in range(1,6):

                        pst = sql_position_giving_vacancies(iduser)
                    # if profession in newvacancy[pst]['profession']:
                        profession = newvacancy[pst]['profession']
                        link = newvacancy[pst]['link']
                        lastid = newvacancy[pst]['id']
                        if pst == 0 and lastid != sqlgetlastid(iduser):
                            sql_save_lastid_vcncy(iduser, lastid)
                        keyboard1 = (Keyboard(inline=True)
                                     .add(OpenLink(link, 'Открыть🚀'))
                                     )
                        if int(newvacancy[pst]['payment_from']) != 0 and int(newvacancy[pst]['payment_from']) != 0:
                            payment = f"до {newvacancy[pst]['payment_to']}₽"

                        elif int(newvacancy[pst]['payment_from']) == 0:
                            payment = f" до {newvacancy[pst]['payment_to']}"

                        elif int(newvacancy[pst]['payment_to']) == 0:
                            payment = f" до {newvacancy[pst]['payment_to']}"
                        else:
                            payment = f"{newvacancy[pst]['payment_from']} - {newvacancy[pst]['payment_to']}"
                        if payment == '0 - 0':
                            payment = 'После собеседования'
                        company = f'{newvacancy[pst]["firm_name"]}'
                        await message.answer(
                            f"💼Вакансия: {profession} \n 🏙Компания:{company} \n 💲Условия оплаты: {payment} \n🔜Оставить заявку и узнать подробне о вакансии:",
                            keyboard=keyboard1)
                        sql_change_position(iduser,1)
            # await message.answer(keyboard=keyboard0)
            await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
        elif sql_position_giving_vacancies(iduser) + 5 > sql_position_limit_get(iduser):
                sql_change_position(iduser, 0)
                await message.answer('Упс, вакансий не осталось',keyboard=keyboard2)
                await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)


#Оформление подписки
# --------------------------------------------------
    @bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'subsstart'})
    async def subs_confirm_handler(message: Message):
        keyboard0=(Keyboard(one_time=False)
                    .add(Text('Создать', {'cmd': 'subsfinish'}))
                    .row()
                    .add(Text('Назад', {'cmd': 'menu'}))
                     )
        keyboard1 = (Keyboard(one_time=False)
                     .add(Text('Изменить и подписаться', {'cmd': 'subsfinish'}))
                     .row()
                     .add(Text('Назад', {'cmd': 'menu'}))
                     )
        iduser = await iduserget(message)
        print(iduser,type(iduser))
        profession, city, salary = sql_get_user_info(iduser)
        iduser2, status2, salary2, city2, profession2, lastid2=sql_allinfo_subscribe_status_get(iduser)
        active=9
        if status2==1:
            active='Да'
        elif status2==0:
            active='Нет'
        if sql_allinfo_subscribe_status_get(iduser) is None:
            await message.answer(f'Создать подписку на основе этих параметров для поиска?\n\n'
                                 f"Ваши параметры для поиска:\n"
                                 f"Город: {city}\n"
                                 f"Профессия: {profession}\n"
                                 f"Зарплата от: {salary}₽\n\n"
                                 f'Если запросы изменились - Изменить ', keyboard=keyboard0)

        elif sql_allinfo_subscribe_status_get(iduser) is not None:
            await message.answer(f'Изменить подписку на основе парметров для поиска?\n\n'
                                 f"Ваши параметры для поиска:\n"
                                 f"Город: {city}\n"
                                 f"Профессия: {profession}\n"
                                 f"Зарплата от: {salary}₽\n\n"
                                 f"Ваши параметры рассылки:\n"
                                 f"Город : {city2}\n"
                                 f"Профессия: {profession2}\n"
                                 f"Зарплата от: {salary2}₽\n"
                                 f"Активна: {active}\n\n"
                                 f'Если запросы изменились - Изменить ', keyboard=keyboard1)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
# Изменение статуса подписки
    @bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'subsfinish'})
    async def subs_finish_handler(message: Message):
        iduser=await iduserget(message)
        path=sql_subscribe_status_set(iduser,1)
        keyboard0 = (Keyboard(one_time=False)
                     .add(Text('На главное меню', {'cmd': 'menu'}))
                     )
        if path == 1:
            await message.answer('Данные подписки успешно обновлены', keyboard=keyboard0)
        elif path==2:
            await message.answer('Извините,Вы уже подписались на рассылку с такими параметрами', keyboard=keyboard0)
        elif path == 3:
            await message.answer('Подписка по прежним параметры возоблена', keyboard=keyboard0)
        elif path == 4:
            await message.answer('Подписка активна, свойства обновлены', keyboard=keyboard0)
        elif path==6:
            await message.answer('Поздравляем, вы подписались на рассылку!', keyboard=keyboard0)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
#  отмена подписки
    @bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'subscancel'})
    async def subs_finish_handler(message: Message):
        iduser=await iduserget(message)
        path=sql_subscribe_status_set(iduser,0)
        keyboard0 = (Keyboard(one_time=False)
                     .add(Text('На главное меню', {'cmd': 'menu'}))
                     )
        keyboard1 = (Keyboard(one_time=False,inline=True)
                     .add(Text('Подписаться🍍', {'cmd': 'subsstart'}))
                     )
        if path==5:
            await message.answer('Рассылка приостановлена', keyboard=keyboard0)
            await message.answer('Если не хотите пропустить привлекательные вакансии,\n'
                                 'советуем снова подписаться',keyboard=keyboard1)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
    await bot.run_polling()
# ----------------------------------------------------------------------
async def check_new_vacancies_for_users():


    async def get_users_data():
            async with aiosqlite.connect('sjbase0.db') as db:
                db.row_factory = aiosqlite.Row
                async with db.execute('SELECT * FROM sjsubscript WHERE status = 1') as cursor:
                    rows = await cursor.fetchall()
                    users_data = [dict(row) for row in rows]
            return users_data



    async def get_user_vacancy_objects(user_data):
            access_token, refresh_token, client_secret, client_id, token_group = await sql_get_api_keys_info()
            params = {
                'payment_from': user_data['salary'],
                'sort_new': time.time(),
                'keyword': user_data['profession'],
                'town': user_data['city'],
            }
            headers = {
                'X-Api-App-Id': client_secret,
                'Authorization': f'Bearer {access_token}',
            }
            url = 'https://api.superjob.ru/2.0/vacancies/'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    response_json = await response.json()
                    return response_json




    async def process_user_vacancy_objects(user_data, vacancy_objects):
            lastid = user_data['lastid']
            if 'objects' in vacancy_objects and len(vacancy_objects)!=0:
                first_vacancy = vacancy_objects['objects'][0]
                first_vacancy_id = first_vacancy['id']
                if first_vacancy_id != lastid:
                    # Обновляем lastid в базе данных
                    async with aiosqlite.connect('sjbase0.db') as db:
                        await db.execute('UPDATE sjsubscript SET lastid = ? WHERE iduser = ?', (first_vacancy_id, user_data['iduser']))
                        await db.commit()
                        profession = first_vacancy['profession']
                        link = first_vacancy['link']
                        keyboard1 = (Keyboard(inline=True)
                                 .add(OpenLink(link, 'Открыть🚀'))
                                 )
                    if int(first_vacancy['payment_from']) != 0 and int(first_vacancy['payment_from']) != 0:
                        payment = f"до {first_vacancy['payment_to']}₽"

                    elif int(first_vacancy['payment_from']) == 0:
                        payment = f" до {first_vacancy['payment_to']}"

                    elif int(first_vacancy['payment_to']) == 0:
                        payment = f" до {first_vacancy['payment_to']}"
                    else:
                        payment = f"{first_vacancy['payment_from']} - {first_vacancy['payment_to']}"
                    if payment == '0 - 0':
                        payment = 'После собеседования'
                    company = f'{first_vacancy["firm_name"]}'
                    text= f"💼 Новая Вакансия: {profession} \n 🏙Компания:{company} \n 💲Условия оплаты: {payment} \n🔜Оставить заявку и узнать подробне о вакансии:"
                    await bot.api.messages.send(peer_id=user_data['iduser'], message=text, random_id=0,keyboard=keyboard1)
                    # await bot.api.messages.send(message=f'{p}', peer_id=user_data['vk_id'], random_id=0)



    while True:
        await asyncio.sleep(300)
        users_data = await get_users_data()
        tasks = []
        for user_data in users_data:
            task = asyncio.create_task(get_user_vacancy_objects(user_data))
            tasks.append(task)

        vacancy_objects_list = await asyncio.gather(*tasks)

        for user_data, vacancy_objects in zip(users_data, vacancy_objects_list):
            await process_user_vacancy_objects(user_data, vacancy_objects)

async def main():
    task1 = asyncio.create_task(check_new_vacancies_for_users())
    task2 = asyncio.create_task(bot_loop())
    await asyncio.gather(task1, task2)


if __name__ == "__main__":
    asyncio.run(main())










