# from datetime import datetime
import asyncio

import aiohttp
import aiosqlite
from vkbottle import Bot
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink, BaseStateGroup, EMPTY_KEYBOARD
from vkbottle import PhotoMessageUploader
from vkbottle import VKAPIError
from vkbottle.bot import Message

from API_SJ_SQLUPDATE import *

global BOT
bot = Bot(token=sql_get_token_group_vk())
BOT = bot
photo_uploader = PhotoMessageUploader(bot.api)

async def bot_loop():
    bot = BOT
    photo_uploader = PhotoMessageUploader(bot.api)
    # обьявление переменных для маршрута сбора пользовательской инфы
    class SUBSDSATA(BaseStateGroup):
        CITY = 0
        PROF = 1
        PAY = 2
        GO = 4
        MENU = 5
        GET = 6
        CONT = 7
        NAME=8
        NAMEACCEPT=9

    # получение id usera
    async def iduserget(message: Message):
        users = await bot.api.users.get(message.from_id)
        id = users[0].id
        return id

    # 0 этап Добро пожаловать
    # ----------------------------------------------
    #
    #  в случае перезапуска админ рассылает сам пока что сообщение
    @bot.on.message(text="/restart")
    async def bot_restart_handler(message: Message):
        # проверяем, что отправитель является администратором
        admin = await iduserget(message)
        if int(admin) == int(230352030):
            idusers = sql_idusers_get()
            keyboard = (Keyboard(inline=False)
                        .add(Text('Начать', {"command": "start"}))
                        )
            for user in idusers:
                try:
                    await bot.api.messages.send(
                        message=f"По техническим причинам бот был перезапущен. Нажмите 'Начать', чтобы продолжить.",
                        peer_id=user, keyboard=keyboard, random_id=0)
                except VKAPIError[901]:
                    print(f"не могу отправить сообщение пользователю id {user}  из-за настроек приватности ", )
                    # admin_id = 230352030  # замените на ID администратора бота
                    # await bot.api.messages.send(
                    #     message=f"Не удалось отправить сообщение пользователям, VKAPIError_901",
                    #     peer_id=admin_id, random_id=0)
                    # continue
                    continue
        else:
            # отправляем сообщение об ошибке доступа
            await message.answer('Вы не администратор бота')


    # @bot.on.message(text=['Photo','photo'])
    # async def handler9(message):
    #     print(message.peer_id)
    #     photka = generate_image_with_qr_code_and_text('Полный рабочий день','https://www.superjob.ru/clients/s3-189142/vacancies.html')
    #     photo = await photo_uploader.upload(
    #         file_source=photka,
    #         peer_id=message.peer_id,
    #     )
    #     await message.answer(attachment=photo)














    @bot.on.message(state=None, payload={"command": "start"})  # от SUPERJOB💚
    @bot.on.message(text=['Начать', 'начать'])
    async def starthandler(message: Message):

        users = await bot.api.users.get(message.from_id)
        keyboard = (Keyboard(inline=False, one_time=True)
                    .add(Text('Найти работу', {'cmd': 'reg'}), color=KeyboardButtonColor.POSITIVE)
                    )

        await message.answer(f'Привет, {users[0].first_name}! \n На связи бот вакансий от SuperJob.'
                             '\n Я ищу предложения о работе по следующим параметрам:\n — Город \n — Профессия \n — Заработная плата\nЖми на кнопку «Найти работу»👀',
                             keyboard=keyboard)

    # поиск пользователя в базе
    @bot.on.message(payload={"cmd": "reg"})  # от SUPERJOB💚
    async def Infouser_handler(message: Message):
        iduser = await iduserget(message)
        name = await bot.api.users.get(message.from_id)
        name = name[0].first_name
        check = sql_get_user_info(iduser)

        keyboard0 = (Keyboard(inline=False, one_time=True)
                     .add(Text('На главное меню', {'cmd': 'menu'}))

                     )
        keyboard1 = (Keyboard(inline=False, one_time=True)
                     .add(Text('Начать', {'cmd': 'changes'})))

        if check is not None:
            profession, city, salary = sql_get_user_info(iduser)
            checksubs = sql_allinfo_subscribe_status_get(iduser)
            print(checksubs,100000000000)
            if checksubs is not None:
                iduser2, status2, salary2, city2, profession2, lastid2 = sql_allinfo_subscribe_status_get(iduser)
                if status2!=None and salary2!=None and city2!=None and profession2!=None and lastid2!=None:
                    if city2 == "Спб":
                        city = 'Санкт-Петербург'
                    # active = 9
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
                                         f"Зарплата от: {salary2} ₽\n"
                                         f"Активна: {active}\n\n", )
                    await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
                    await  asyncio.sleep(0.5)
                    await Menu_handler(message)

                else:

                    if city == "Спб":
                        city = 'Санкт-Петербург'
                    await message.answer(f'Смотри, мы нашли твои параметры:\n\n'
                                         f"Ваши параметры для поиска:\n"
                                         f"Город: {city}\n"
                                         f"Профессия: {profession}\n"
                                         f"Зарплата от: {salary} ₽\n\n")
            else:

                    if city == "Спб":
                        city = 'Санкт-Петербург'
                    await message.answer(f'Смотри, мы нашли твои параметры:\n\n'
                                         f"Ваши параметры для поиска:\n"
                                         f"Город: {city}\n"
                                         f"Профессия: {profession}\n"
                                         f"Зарплата от: {salary} ₽\n\n")
                    await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
                    await  asyncio.sleep(0.5)
                    await Menu_handler(message)
        if check is None:
            # await message.answer(f"{name}, ты впервые у нас"
            #                      " скорее выбирай свои параметры и\n будем подбирать тебе вакансии", keyboard=keyboard1)
            # await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CITY)
            await asyncio.sleep(0.5)
            await city_handler(message)

    # 1 этап получение инфы о городе
    # ---------------------------------------
    @bot.on.message(state=SUBSDSATA.CONT, payload={'cmd': 'changes'})
    async def city_handler(message: Message):

        keyboard = (
            Keyboard(inline=True)
            .add(Text('Москва'))
            .add(Text('Сочи'))
            .add(Text("Пермь"))
            .row()
            .add(Text('Омск'))
            .add(Text('Самара'))
            .add(Text('Казань'))
            .row()
            .add(Text('Санкт-Петербург'))
            .row()
            .add(Text('Новосибирск'))
            .row()
            .add(Text('Екатеринбург'))
            .row()
            .add(Text('Краснодар'))

        )

        # photo1= await photo_upd.upload('logo1.jpg')
        await message.answer("Выбери город из списка или напиши сам 🏬",
                             keyboard=keyboard, attachment='photo-217363563_457239040')
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.PROF)

    # 2 этап получение инфы о професии
    # ---------------------------------------------
    @bot.on.message(state=SUBSDSATA.PROF)
    async def prof_handler(message: Message):
        city=message.text
        if message.text=='Санкт-Петербург':
           city='Спб'
        if sql_access_cities(city)==1:
            sql_save_info_city(await iduserget(message), city.capitalize())
            keyboarad = (Keyboard(inline=True)
                         .add(Text('Разработчик'))
                         .add(Text('Дизайнер'))
                         .row()
                         .add(Text('Инженер'))
                         .add(Text('Архитектор'))
                         .row()
                         .add(Text('Экономист'))
                         .add(Text('Юрист'))
                         .row()
                         .add(Text('HR-менеджер'))
                         .row()
                         .add(Text('Product-менеджер'))
                         .row()
                         .add(Text('SEO'))
                         .add(Text('Аналитик '))
                         )

            await message.answer('Теперь определись с профессией или напиши свой вариант‍🚀', keyboard=keyboarad,
                                 attachment='photo-217363563_457239042')
            await bot.state_dispenser.set(message.peer_id, SUBSDSATA.PAY)
        else:
           await message.answer('Мы не нашли такого города, введите еще раз ')
           await city_handler(message)


    # 3 этап получение инфы о желаемом заработке
    # --------------------------------------------
    @bot.on.message(state=SUBSDSATA.PAY)
    async def pay_handler(message: Message):

        keyboarad0 = (Keyboard(inline=True)
                      .add(Text('от 10 000₽', {'cmd': 'edit'}))
                      .add(Text('от 20 000₽', {'cmd': 'edit'}))
                      .row()
                      .add(Text('от 30 000₽', {'cmd': 'edit'}))
                      .add(Text('от 50 000₽', {'cmd': 'edit'}))
                      .row()
                      .add(Text('от 80 000₽', {'cmd': 'edit'}))
                      .add(Text('от 100 000₽', {'cmd': 'edit'}))
                      .row()
                      .add(Text('от 150 000₽', {'cmd': 'edit'}))
                      .add(Text('от 200 000₽', {'cmd': 'edit'})))
        sql_save_info_prof(await iduserget(message), message.text)

        await message.answer('Какой уровень зарплаты ты рассматриваешь? Выбери или напиши сам💸', keyboard=keyboarad0,attachment='photo-217363563_457239041')
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)

    # обработка и выдача Результата
    # ------------------------------------------
    @bot.on.message(state=SUBSDSATA.CONT, payload={'cmd': 'edit'})
    async def initial_handler(message: Message):
        iduser = await iduserget(message)
        print(iduser)
        pay = message.text
        if '000₽' in str(pay):
            pay = message.text
            pay = pay.rstrip('₽').lstrip('от').replace(' ', '')
            sql_save_info_salary(iduser, pay)
            sql_change_position(iduser, 0)
        # sql_subscribe_status_set(iduser,'0')
        keyboardstart = (Keyboard(one_time=True, inline=False)
                         .add(Text('Получить', {'cmd': 'get'}), color=KeyboardButtonColor.POSITIVE)
                         .add(Text('Изменить', {'cmd': 'changes'}), color=KeyboardButtonColor.PRIMARY)
                         .row()
                         .add(Text('Назад', {'cmd': 'menu'}), color=KeyboardButtonColor.SECONDARY)
                         )
        keyboardcontin = (Keyboard(one_time=True, inline=False)
                          .add(Text('Получить', {'cmd': 'get'}), color=KeyboardButtonColor.POSITIVE)
                          .add(Text('Изменить', {'cmd': 'changes'}), color=KeyboardButtonColor.PRIMARY)
                          .row()
                          .add(Text('Назад', {'cmd': 'menu'}), color=KeyboardButtonColor.SECONDARY)
                          )
        profession, city, salary = sql_get_user_info(iduser)
        if city=="Спб":
            city='Санкт-Петербург'
        pos = sql_position_giving_vacancies(iduser)
        # await message.answer(sql_position_giving_vacancies(await iduserget(message)))
        if int(pos) != 0:
            await message.answer(f"🖇 Выбраны параметры:\n"
                                 f"Город : {city}\n"
                                 f"Профессия: {profession}\n"
                                 f"Зарплата от: {salary}₽\n\n"
                                 f'👌 Всё верно — жми «Получить».\n'
                                 f'Для выбора других параметров жми «Изменить»', keyboard=keyboardcontin)
        elif int(pos) == 0:
            await message.answer(f"🖇 Выбраны параметры:\n"
                                 f"Город : {city}\n"
                                 f"Профессия: {profession}\n"
                                 f"Зарплата от: {salary}₽\n\n"
                                 f'👌Всё верно — жми «Получить».\n'
                                 f'Нужна корректировка — жми «Изменить»'
                                 , keyboard=keyboardstart)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)

    # выдача 5 вакансий и переход в меню
    @bot.on.message(state=SUBSDSATA.CONT, payload={'cmd': 'get'})
    async def confirm_handler(message: Message):
        iduser = await iduserget(message)
        keyboard0 = (Keyboard(one_time=True)
                     .add(Text('Подписаться на рассылку', {'cmd': 'subsstart'}))
                     .row()
                     .add(Text('Главное меню', {'cmd': 'menu'}))


                     )
        keyboard1 = (Keyboard(one_time=False)
                     .add(Text('Поищем другое', {'cmd': 'edit'}), color=KeyboardButtonColor.PRIMARY)
                     .row()
                     .add(Text('Подписаться на рассылку', {'cmd': 'subsstart'}))
                     .add(Text('Главное меню', {'cmd': 'menu'}))
                     )

        # запрос и сохранение ответа апи!проработка варианта действий
        # при недействительном токене! с блоком вакансий и колвом вакансий
        # ---------------------------------------
        profession, city, salary = sql_get_user_info(iduser)
        if city == 'Спб':
            city = "Санкт-Петербург"

        newvacancy = await get_vacancy_objects(profession, city, salary)
        while newvacancy is None:
            newvacancy = await get_vacancy_objects(profession, city, salary)

        lenlist = len(newvacancy)


        sql_position_limit_set(iduser, lenlist)

        # # разбивка
        # # -----------------------------------------------
        if sql_position_limit_get(iduser) != 0:
            sql_change_position(iduser, 0)
            try:
                iduser = await iduserget(message)
                while sql_position_giving_vacancies(iduser) < 5 and sql_position_giving_vacancies(
                        iduser) < sql_position_limit_get(iduser):
                    pst = sql_position_giving_vacancies(iduser)
                    # if profession in newvacancy[pst]['profession']:
                    profession = newvacancy[pst]['profession']
                    link = newvacancy[pst]['link']
                    lastid = newvacancy[pst]['id']
                    logolink = newvacancy[pst]['client_logo']
                    # logo = await resize_image_from_url(logolink, 1920, 1080)
                    if pst == 0 and lastid != sqlgetlastid(iduser):
                        sql_save_lastid_vcncy(iduser, lastid)
                    keyboard1 = (Keyboard(inline=True)
                                 .add(OpenLink(link, 'Открыть'))
                                 )
                    # print(newvacancy[pst]['payment_from'], ' ', newvacancy[pst]['payment_from'])
                    if int(newvacancy[pst]['payment_from']) != 0 and int(newvacancy[pst]['payment_to']) != 0:
                        payment = f"от {newvacancy[pst]['payment_from']}₽ до {newvacancy[pst]['payment_to']}₽"
                    elif int(newvacancy[pst]['payment_from']) == 0 and int(newvacancy[pst]['payment_to']) != 0:
                        payment = f" до {newvacancy[pst]['payment_to']}₽"

                    elif int(newvacancy[pst]['payment_from']) != 0 and int(newvacancy[pst]['payment_to']) == 0:
                        payment = f" от {newvacancy[pst]['payment_from']}₽"
                    elif int(newvacancy[pst]['payment_from']) == 0 and int(newvacancy[pst]['payment_from']) == 0:
                        payment = 'По договоренности'
                    else:
                        payment = 'Не указана'
                    company = f'{newvacancy[pst]["firm_name"]}'
                    time.sleep(2)
                    qrcode=generate_image_with_qr_code_and_text(profession,link)
                    await message.answer(
                        message=f"Вакансия: {profession} \nКомпания:{company} \n Условия оплаты: {payment} \nИзучить требования и откликнуться:",
                        keyboard=keyboard1)
                    sql_change_position(iduser, 1)
                await message.answer(
                    'Хочешь получать новые вакансии по мере их появления — подпишись на бесплатную рассылку 📩',
                    keyboard=keyboard0,attachment='photo-217363563_457239043')
                await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
            except IndexError:
                await message.answer('🙆 Сейчас вакансий с такими параметрами нет.\nПолучай свежие вакансии — подпишись на бесплатную рассылку 📩', keyboard=keyboard1,attachment='photo-217363563_457239043')
                await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
        else:
            await message.answer('🙆 Сейчас вакансий с такими параметрами нет.\nПолучай свежие вакансии — подпишись на бесплатную рассылку 📩', keyboard=keyboard1)
            await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)

    # Главное меню
    @bot.on.message(state=SUBSDSATA.CONT, payload={'cmd': 'menu'})
    async def Menu_handler(message: Message):
        iduser = await iduserget(message)
        profession, city, salary = sql_get_user_info(iduser)
        if city == 'Cпб':
            city = 'СПБ'
        # print(profession, city, salary)
        # print(type(city))
        sql_create_link(iduser, profession, salary, city)
        mainlink = sql_savelink_user_get(iduser)
        # await  message.answer(mainlink)
        keyboard0 = (Keyboard(one_time=False)
                     .add(OpenLink(mainlink, 'Перейти на сайт'))
                     .add(Text('Смотреть еще', {'cmd': 'add'}))
                     .row()
                     .add(Text('Параметры поиска', {'cmd': 'edit'}))
                     .add(Text('Подписаться на рассылку', {'cmd': 'subsstart'}))
                     )
        keyboard1 = (Keyboard(one_time=False)
                     .add(OpenLink(mainlink, 'Перейти на сайт'))
                     .add(Text('Смотреть еще', {'cmd': 'add'}))
                     .row()
                     .add(Text('Параметры поиска', {'cmd': 'edit'}))
                     .row()
                     .add(Text('Изменить подписку', {'cmd': 'subsstart'}))
                     .row()
                     .add(Text('Отписаться от рассылки', {'cmd': 'subscancel'})))
        keyboard2 = (Keyboard(one_time=False)
                     .add(OpenLink(mainlink, 'Перейти на сайт'))
                     .add(Text('Смотреть еще', {'cmd': 'add'}))
                     .row()
                     .add(Text('Параметры поиска', {'cmd': 'edit'}))
                     .row()
                     .add(Text('Подписаться на рассылку', {'cmd': 'subsstart'})))
        # print(sql_allinfo_subscribe_status_get(iduser),567)
        print(8888888888)
        checksubs=sql_allinfo_subscribe_status_get(iduser)
        if checksubs is None:
            await message.answer("Ты в главном меню", keyboard=keyboard0)
        else:
            iduser2, status2, salary2, city2, profession2, lastid2 = sql_allinfo_subscribe_status_get(iduser)
            if status2 == None and salary2 == None and city2 == None and profession2 == None and lastid2 == None:
                await message.answer("Ты в главном меню", keyboard=keyboard0)

        if sql_subscribe_status_get(iduser) == 1:
                    await message.answer("Ты в главном меню", keyboard=keyboard1)
        elif sql_subscribe_status_get(iduser) == 0:
                    await message.answer("Ты в главном меню", keyboard=keyboard2)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)

    # доп выдача
    @bot.on.message(state=SUBSDSATA.CONT, payload={'cmd': 'add'})
    async def ADD_handler(message: Message):

        iduser = await iduserget(message)
        mainlink = sql_savelink_user_get(iduser)
        keyboard2 = (Keyboard(inline=True)
                     .add(OpenLink(mainlink, 'Открыть'))
                     )
        keyboard0 = (Keyboard(inline=True)

                     .add(Text('Подписаться на рассылку', {'cmd': 'subsstart'}))
                     )
        try:
            if sql_position_giving_vacancies(iduser) + 5 <= sql_position_limit_get(iduser):
                profession, city, salary = sql_get_user_info(iduser)
                if city == 'Спб':
                    city = "Санкт-Петербург"
                newvacancy = await get_vacancy_objects(profession, city, salary)
                for next in range(1, 6):

                    pst = sql_position_giving_vacancies(iduser)
                    # if profession in newvacancy[pst]['profession']:
                    profession = newvacancy[pst]['profession']
                    link = newvacancy[pst]['link']
                    lastid = newvacancy[pst]['id']
                    if pst == 0 and lastid != sqlgetlastid(iduser):
                        sql_save_lastid_vcncy(iduser, lastid)
                    keyboard1 = (Keyboard(inline=True)
                                 .add(OpenLink(link, 'Открыть'))
                                 )

                    if int(newvacancy[pst]['payment_from']) != 0 and int(newvacancy[pst]['payment_to']) != 0:

                        payment = f"от {newvacancy[pst]['payment_from']}₽ до {newvacancy[pst]['payment_to']}₽"
                    elif int(newvacancy[pst]['payment_from']) == 0 and int(newvacancy[pst]['payment_to']) != 0:

                        payment = f" до {newvacancy[pst]['payment_to']}₽"

                    elif int(newvacancy[pst]['payment_from']) != 0 and int(newvacancy[pst]['payment_to']) == 0:

                        payment = f" от {newvacancy[pst]['payment_from']}₽"
                    elif int(newvacancy[pst]['payment_from']) == 0 and int(newvacancy[pst]['payment_from']) == 0:

                        payment = 'По договоренности'
                    else:
                        payment = 'Не указана'
                    company = f'{newvacancy[pst]["firm_name"]}'
                    await message.answer(
                        f"Вакансия: {profession} \nКомпания:{company} \n Условия оплаты: {payment} \nИзучить требования и откликнуться:",
                        keyboard=keyboard1)
                    sql_change_position(iduser, 1)

                # await message.answer(keyboard=keyboard0)
                await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
            elif sql_position_giving_vacancies(iduser) + 5 >= sql_position_limit_get(iduser):
                sql_change_position(iduser, 0)
                await message.answer(
                    '💁 Сейчас это все доступные вакансии с выбранными параметрами.\nПолучай свежие вакансии — подпишись на бесплатную рассылку 📩',
                    keyboard=keyboard0)
                await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
                await asyncio.sleep(0.5)
                await Menu_handler(message)
        except IndexError:
                await message.answer('🙆 Сейчас вакансий с такими параметрами нет.\nПолучай свежие вакансии — подпишись на бесплатную рассылку 📩', keyboard=keyboard0,attachment='photo-217363563_457239043')
                await asyncio.sleep(0.5)
                await Menu_handler(message)

    # Оформление подписки
    # --------------------------------------------------
    @bot.on.message(state=SUBSDSATA.CONT, payload={'cmd': 'subsstart'})
    async def subs_confirm_handler(message: Message):
        keyboard0 = (Keyboard(one_time=False)
                     .add(Text('Подписка по заданным параметрам', {'cmd': 'subsname'}))
                     .row()
                     .add(Text('Задать новые параметры для подписки', {'cmd': 'edit'}))
                     .row()
                     .add(Text('Назад', {'cmd': 'menu'}))
                     )
        keyboard1 = (Keyboard(one_time=False)
                     .add(Text('Подписка по заданным параметрам', {'cmd': 'subsname'}))
                     .row()
                     .add(Text('Задать новые параметры для подписки', {'cmd': 'edit'}))

                     .row()
                     .add(Text('Назад', {'cmd': 'menu'}))
                     )
        keyboard2 = (Keyboard(one_time=False)
                     .add(Text('Подписка по заданным параметрам', {'cmd': 'subsfinish'}))
                     .row()
                     .add(Text('Задать новые параметры для подписки', {'cmd': 'edit'}))
                     .row()
                     .add(Text('Изменить название подписки', {'cmd': 'subsnaming'}))
                     .row()
                     .add(Text('Назад', {'cmd': 'menu'}))
                     )
        iduser = await iduserget(message)
        # print(iduser,type(iduser))
        profession, city, salary = sql_get_user_info(iduser)

        if city == 'Спб':
            city = "Санкт-Петербург"
        print(1.1)
        checksubs=sql_allinfo_subscribe_status_get(iduser)
        if checksubs is None:
            await message.answer(f'Создать подписку на основе этих параметров для поиска?\n\n'
                                 f"Ваши параметры для поиска:\n"
                                 f"Город: {city}\n"
                                 f"Профессия: {profession}\n"
                                 f"Зарплата от: {salary} ₽\n\n"
                                 f'Если запросы изменились - Задать новые параметры для подписки ', keyboard=keyboard0)
        elif checksubs is not None:
                iduser2, status2, salary2, city2, profession2, lastid2 = sql_allinfo_subscribe_status_get(iduser)
                if status2 == None and salary2 == None and city2 == None and profession2 == None and lastid2 == None:
        # if sql_allinfo_subscribe_status_get(iduser) is None:
                    print(1.2)
                    await message.answer(f'Создать подписку на основе этих параметров для поиска?\n\n'
                                 f"Ваши параметры для поиска:\n"
                                 f"Город: {city}\n"
                                 f"Профессия: {profession}\n"
                                 f"Зарплата от: {salary} ₽\n\n"
                                 f'Если запросы изменились - Задать новые параметры для подписки ', keyboard=keyboard0)

                print(1.3)
                iduser2, status2, salary2, city2, profession2, lastid2 = sql_allinfo_subscribe_status_get(iduser)
                if city2 == 'Спб':
                    city2 = "Санкт-Петербург"
                active = 9
                if status2 == 1:
                    active = 'Да'
                elif status2 == 0 or status2==None:
                    active = 'Нет'
                subsname=sql_subs_name_get(iduser)
                print(subsname)
                if subsname is not None:
                    print(1.4)
                    await message.answer(f'Изменить подписку на основе парметров для поиска?\n\n'
                                     f"Ваши параметры для поиска:\n"
                                     f"Город: {city}\n"
                                     f"Профессия: {profession}\n"
                                     f"Зарплата от: {salary}₽\n\n"
                                     
                                     f"Заменят ваши параметры рассылки\n\n"
                                     f"Название рассылки: {subsname}\n"
                                     f"Город : {city2}\n"
                                     f"Профессия: {profession2}\n"
                                     f"Зарплата от: {salary2} ₽\n"
                                     f"Активна: {active}\n\n"
                                     f'1.Если запросы изменились - Задать новые параметры для подписки \n'
                                     f'2.Изменить только название - Изменить название подписки \n'
                                     f'3.Обновить только параметры - Подписка по уже заданным параметрам \n', keyboard=keyboard2)
                if subsname is None:
                        print(1.5)
                        await message.answer(f'Изменить подписку на основе парметров для поиска?\n\n'
                                             f"Ваши параметры для поиска:\n"
                                             f"Город: {city}\n"
                                             f"Профессия: {profession}\n"
                                             f"Зарплата от: {salary}₽\n\n"
                                             
                                             f"Заменят ваши параметры рассылки:\n\n"
                                             f"Название рассылки: без названия \n"
                                             f"Город : {city2}\n"
                                             f"Профессия: {profession2}\n"
                                             f"Зарплата от: {salary2} ₽\n"
                                             f"Активна: {active}\n\n"
                                             f'1.Если запросы изменились - Задать новые параметры для подписки\n\n'
                                             f'2.Добавить только название - Изменить название подписки ', keyboard=keyboard1)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
        # вставка имени подписки
    @bot.on.message(state=SUBSDSATA.CONT, payload={'cmd': 'subsname'})
    async def subs_naming_handler(message: Message):

            await message.answer(f'Напиши название для подписки 🖇',keyboard=EMPTY_KEYBOARD)
            await bot.state_dispenser.set(message.peer_id, SUBSDSATA.NAME)
            # await subs_finish0_handler

    @bot.on.message(state=SUBSDSATA.CONT, payload={'cmd': 'subsnaming'})
    async def subs_naming1_handler(message: Message):

        await message.answer(f'Напиши название для подписки 🖇', keyboard=EMPTY_KEYBOARD)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.NAMEACCEPT)
    @bot.on.message(state=SUBSDSATA.NAME)
    async def subs_finish0_handler(message: Message):
        keyboard0 = (Keyboard(one_time=False)
                     .add(Text('На главное меню', {'cmd': 'menu'}))
                     )
        keyboard1 = (Keyboard(one_time=False)
                     .add(Text('Подтвердить', {'cmd': 'subsfinish'}))
                     )
        iduser = await iduserget(message)
        subsname = message.text
        sql_subs_name_set(iduser, subsname)
        # subsname = sql_subs_name_get(iduser)
        profession, city, salary = sql_get_user_info(iduser)
        iduser2, status2, salary2, city2, profession2, lastid2 = sql_allinfo_subscribe_status_get(iduser)
        await message.answer(f"Получились следующие параметры  вышей рассылки:\n\n"
                             f"Название рассылки: {subsname} \n"
                             f"Город : {city}\n"
                             f"Профессия: {profession}\n"
                             f"Зарплата от: {salary} ₽\n"
                             f'Если все верно - жми подтвердить', keyboard=keyboard1)
        # path = sql_subscribe_status_set(iduser, 1)

        # await message.answer(f'Название подписки: {subsname}',keyboard=keyboard1)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)


    @bot.on.message(state=SUBSDSATA.NAMEACCEPT)
    async def subs_finish1_handler(message: Message):
            iduser = await iduserget(message)
            subsname = message.text
            sql_subs_name_set(iduser, subsname)
            await message.answer('Название подписки изменено')
            await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
            await Menu_handler(message)

    # Изменение статуса подписки
    @bot.on.message(state=SUBSDSATA.CONT,payload={'cmd': 'subsfinish'})
    async def subs_finish2_handler(message: Message):
        iduser = await iduserget(message)


        path = sql_subscribe_status_set(iduser, 1)
        keyboard0 = (Keyboard(one_time=False)
                     .add(Text('На главное меню', {'cmd': 'menu'}))
                     )
        if path == 1:
            await message.answer('Данные подписки успешно обновлены')
        elif path == 2:
            await message.answer('Вы уже подписаны на рассылку с такими параметрами')
        elif path == 3:
            await message.answer('Подписка по прежним параметры возоблена')
        elif path == 4:
            await message.answer('Подписка активна, свойства обновлены')
        elif path == 6:
            await message.answer('Поздравляем, вы подписались на рассылку!')
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
        print('++++++')
        await Menu_handler(message)
    #  отмена подписки
    @bot.on.message(state=SUBSDSATA.CONT, payload={'cmd': 'subscancel'})
    async def subs_cancel_handler(message: Message):
        iduser = await iduserget(message)
        subsname=sql_subs_name_get(iduser)
        path = sql_subscribe_status_set(iduser, 0)
        keyboard0 = (Keyboard(one_time=False)
                     .add(Text('На главное меню', {'cmd': 'menu'}))
                     )
        keyboard1 = (Keyboard(one_time=False, inline=True)
                     .add(Text('Подписаться', {'cmd': 'subsstart'}))
                     )
        if path == 5:
            await message.answer(f'Рассылка {subsname} приостановлена')
            await message.answer('Если не хотите пропустить свежие вакансии\n'
                                 '-подпишись на бесплатную рассылку 📩', keyboard=keyboard1,attachment='photo-217363563_457239043')
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
        await Menu_handler(message)

    await bot.run_polling()


# ----------------------------------------------------------------------
async def check_new_vacancies_for_users():
    async def get_users_data():
        async with aiosqlite.connect('sjbase0.db') as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT * FROM sjsubscript WHERE status = 1') as cursor:
                rows = await cursor.fetchall()
                users_data = [dict(row) for row in rows]
                print(users_data)
        return users_data

    async def get_user_vacancy_objects(user_data):
        # print(user_data['iduser'])
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
        # print(2)
        lastid = user_data['lastid']
        if 'objects' in vacancy_objects and vacancy_objects['objects'] != []:
            # print(user_data)
            # print(vacancy_objects)
            first_vacancy = vacancy_objects['objects'][0]
            first_vacancy_id = first_vacancy['id']

            # print('id', user_data['iduser'], ' ', first_vacancy_id, ' - ', lastid)

            if first_vacancy_id != lastid:
                # print('send')
                # Обновляем lastid в базе данных
                async with aiosqlite.connect('sjbase0.db') as db:
                    await db.execute('UPDATE sjsubscript SET lastid = ? WHERE iduser = ?',
                                     (first_vacancy_id, user_data['iduser']))
                    await db.commit()
                    profession = first_vacancy['profession']
                    link = first_vacancy['link']
                    keyboard1 = (Keyboard(inline=True)
                                 .add(OpenLink(link, 'Открыть'))
                                 )
                if int(first_vacancy['payment_from']) != 0 and int(first_vacancy['payment_to']) != 0:

                    payment = f"от {first_vacancy['payment_from']}₽ до {first_vacancy['payment_to']}₽"
                elif int(first_vacancy['payment_from']) == 0 and int(first_vacancy['payment_to']) != 0:

                    payment = f" до {first_vacancy['payment_to']}₽"

                elif int(first_vacancy['payment_from']) != 0 and int(first_vacancy['payment_to']) == 0:

                    payment = f" от {first_vacancy['payment_from']}₽"
                elif int(first_vacancy['payment_from']) == 0 and int(first_vacancy['payment_from']) == 0:

                    payment = 'По договоренности'
                else:
                    payment = 'Не указана'
                company = f'|{first_vacancy["firm_name"]}|'
                subsname=sql_subs_name_get(user_data['iduser'])
                text = \
                    f"Новая вакансия по подписке {subsname}]" \
                     \
                    f" Вакансия: {profession} \n Компания: {company} \n Условия оплаты: {payment}\n\n🤝 Изучить требования и откликнуться:"
                await BOT.api.messages.send(peer_id=user_data['iduser'], message=text, random_id=0, keyboard=keyboard1,attachment='photo-217363563_457239044')
                # await bot.api.messages.send(message=f'{p}', peer_id=user_data['vk_id'], random_id=0)
            else:
                print('equal')
        else:
            if sql_subscribe_status_get(user_data['iduser']) != 1:
                keyboard = (Keyboard(one_time=False, inline=True)
                            .add(Text('Изменить', {'cmd': 'edit'}))
                            )
                await BOT.api.messages.send(peer_id=user_data['iduser'],
                                            message='По заданным параметрам подписки вакансий не найдено( Попробуйте выбрать другие параметры ',
                                            random_id=0, keyboard=keyboard)
                null_objects_status_change(user_data['iduser'], 0)
                print('не найдено вакансий')
            pass

    while True:
        await asyncio.sleep(900)
        users_data = await get_users_data()
        tasks = []
        for user_data in users_data:
            task = asyncio.create_task(get_user_vacancy_objects(user_data))
            tasks.append(task)

        vacancy_objects_list = await asyncio.gather(*tasks)

        for user_data, vacancy_objects in zip(users_data, vacancy_objects_list):
            await process_user_vacancy_objects(user_data, vacancy_objects)


async def main():
    keyboard = (Keyboard(inline=False)
                .add(Text('Начать', {'cmd': 'menu'}))
                )
    idusers = sql_idusers_get()
    # for user in idusers:
    #
    #     # try:
    #     #     await bot.api.messages.send(
    #     #         message=f"По техническим причинам бот был перезапущен. Нажмите 'Начать', чтобы продолжить.",
    #     #         peer_id=user, keyboard=keyboard, random_id=0)
    #     # except VKAPIError[901]:
    #     #     print(f"не могу отправить сообщение пользователю id {user}  из-за настроек приватности ", )
    #     #     admin_id = 230352030  # замените на ID администратора бота
    #     #     await bot.api.messages.send(
    #     #         message=f"Не удалось отправить сообщение пользователям, VKAPIError_901",
    #     #         peer_id=admin_id, random_id=0)


    task1 = asyncio.create_task(check_new_vacancies_for_users())
    task2 = asyncio.create_task(bot_loop())
    await asyncio.gather(task1, task2)


if __name__ == "__main__":
    asyncio.run(main())
