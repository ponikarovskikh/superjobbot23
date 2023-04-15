
from vkbottle.bot import Bot,Message
from vkbottle import Keyboard,KeyboardButtonColor,Text,OpenLink,BaseStateGroup,CtxStorage,EMPTY_KEYBOARD

from API_SJ_SQLUPDATE import *
from datetime import datetime






bot=Bot(token=sql_get_token_group_vk())
ctx=CtxStorage()

# обьявление переменных для логиского маршрута
# сбора пользовательской инфы
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


# 0 этап главное меню
# ----------------------------------------------
@bot.on.message(state=None,payload={"command":"start"})
@bot.on.message(text=['Начать','начать'])
async def starthandler(message:Message):

    users = await bot.api.users.get(message.from_id)
    keyboard=(Keyboard(inline=False,one_time=True)
              .add(Text('Искать работу',{'cmd':'reg'}), color=KeyboardButtonColor.POSITIVE)
              )
    await message.answer(f'Приветствуем тебя,{users[0].first_name}! \n Это бот вакансий от SUPERJOB💚'
                         '\n Поможем найти новые вакансии по вашим параметрам:\n Город | Профессия | Заработная плата📝\nНажмите кнопку "Искать работу"🔔',keyboard=keyboard)



# 1 этап получение инфы о городе
# ---------------------------------------
@bot.on.message(payload={'cmd':'reg'})
@bot.on.message(lev='/reg')
async def city_handler(message:Message):

    keyboard = (
            Keyboard(inline=True)
            .add(Text('Москва'))
            .add(Text('Казань'))
            .row()
            .add(Text('Cанкт-Петербург'))
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

    await message.answer('Теперь определись с профессией или напиши свой вариант‍🚀',keyboard=keyboarad,attachment='photo-217363563_457239025')
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

    await message.answer('Сколько денег хочешь зарабатывать? Выбери или напиши вручную 💵', keyboard=keyboarad0,attachment='photo-217363563_457239026')
    await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)


# обработка и выдача Результата
# ------------------------------------------


@bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'edit'})
async def initial_handler(message:Message):
    iduser= await iduserget(message)
    pay= message.text
    if '₽' in str(pay):
        pay = message.text
        pay = pay.rstrip('₽').replace(' ', '')
        sql_save_info_salary(iduser,pay)
        sql_change_position(iduser, 0)
        sql_subscribe_status_set(iduser,'0')
    keyboardstart = (Keyboard(one_time=True,inline=False)
                .add(Text('Получить',{'cmd':'get'}), color=KeyboardButtonColor.POSITIVE)
                .add(Text('Изменить', {'cmd': 'reg'}), color=KeyboardButtonColor.PRIMARY)
                )
    keyboardcontin = (Keyboard(one_time=True, inline=False)

                     .add(Text('Изменить', {'cmd': 'reg'}), color=KeyboardButtonColor.PRIMARY)
                     .row()
                     .add(Text('Назад', {'cmd': 'menu'}), color=KeyboardButtonColor.SECONDARY)
                     )
    profession, city, salary=sql_get_user_info(iduser)


    # attachment='photo-217363563_457239027'
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
                         f'Если Запросы изменились - Изменить ',keyboard=keyboardstart)
    await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)

        # await message.answer(f"Ваши параметры🎲:\nГород :{ctx.get('city')}"
        #                      f"\nПрофессия:{ctx.get('prof')}\nЗарплата от: {ctx.get('pay')}"
        #                      f'\n\n'
        #                      f'Если Запросы изменились - Изменить ', keyboard=keyboardcont,
        #                      attachment='photo-217363563_457239027')222



#выдача 5 вакансий и переход в меню
@bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'get'})
async def confirm_handler(message: Message):
    iduser = await iduserget(message)
    keyboard0 = (Keyboard(one_time=True)
                # .add(Text('Перейти на сайт \n (В разработке)'))
                # .add(Text('Давай еще',{'cmd':'add'}))
                # .add(Text('Мои параметры',{'cmd':'edit'}))
                # .row()

                 .add(Text('Далее', {'cmd':'menu'}))
                 )

    keyboard1=(Keyboard(one_time=False)
                .add(Text('Изменить',{'cmd':'edit'}), color=KeyboardButtonColor.PRIMARY))

# запрос и сохранение ответа апи!проработка варианта действий
# при недействительном токене! с блоком вакансий и колвом вакансий
# ---------------------------------------
    profession, city, salary = sql_get_user_info(iduser)
    newvacancy = get_vacancy_objects(profession, city, salary)
    # print(newvacancy)
    lenlist=len(newvacancy)
    sql_position_limit_set(iduser,lenlist)
    print(sql_position_limit_get(iduser))


    # ctx.set('newvacancy', newvacancy)
    # ctx.set('len',lenlist)
#
# # разбивка
# # -----------------------------------------------

    sql_change_position(iduser, 0)
    # await message.answer(sql_position_giving_vacancies(await iduserget(message)))
    try:
            iduser = await iduserget(message)
            while sql_position_giving_vacancies(iduser) < 5 and sql_position_giving_vacancies(iduser) < sql_position_limit_get(await iduserget(message))   :

                print(sql_position_giving_vacancies(iduser))
                profession = newvacancy[sql_position_giving_vacancies(iduser)]['profession']
                link = newvacancy[sql_position_giving_vacancies(iduser)]['link']
                keyboard1=(Keyboard(inline=True)
                           .add(OpenLink(link,'Открыть🚀'))
                           )
                if int(newvacancy[sql_position_giving_vacancies(iduser)]['payment_from'])<int(salary) and int(newvacancy[sql_position_giving_vacancies(iduser)]['payment_from'])!=0 :
                    payment = f"{salary} - {newvacancy[sql_position_giving_vacancies(iduser)]['payment_to']}"
                else:
                    payment = f"{newvacancy[sql_position_giving_vacancies(iduser)]['payment_from']} - {newvacancy[sql_position_giving_vacancies(iduser)]['payment_to']}"
                if payment=='0 - 0':
                    payment='После собеседования'
                company = newvacancy[sql_position_giving_vacancies(iduser)]["firm_name"]
                sql_change_position(iduser,1)
                await message.answer (f"💼Вакансия: {profession} \n 🏙Компания:{company} \n 💲Условия оплаты: {payment} \n🔜Оставить заявку и узнать подробне о вакансии:",keyboard=keyboard1)
            await message.answer('Что дальше?',keyboard=keyboard0)
            await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
    except IndexError:
        await message.answer('Извините, мы не нашли вакансий согласно вашим параметрам\n Давайте изменим "',keyboard=keyboard1)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)

#Главное меню
@bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'menu'})
async def Menu_handler(message: Message):
    iduser = await iduserget(message)
    profession, city, salary = sql_get_user_info(iduser)
    print(profession, city, salary )
    sql_create_link(iduser,profession,salary,city)
    mainlink=sql_savelink_user_get(iduser)
    # await  message.answer(mainlink)
    keyboard0 = (Keyboard(one_time=False)

                 .add(OpenLink(mainlink, 'Перейти на сайт'))
                 .add(Text('Получить еще', {'cmd': 'add'}))
                 .row()
                 .add(Text('Мои параметры',{'cmd':'edit'}))
                 .add(Text('Создать подписку',{'cmd':'subs'}))
                      )
    keyboard1 = (Keyboard(one_time=False)
                 .add(OpenLink(mainlink, 'Перейти на сайт'))
                 .add(Text('Давай еще', {'cmd': 'add'}))
                 .row()
                 .add(Text('Мои параметры',{'cmd':'edit'}))
                 .add(Text('Отменить подписку', {'cmd': 'subs'})))
    if sql_subscribe_status_get(iduser)=='1':
        await message.answer("Главное меню",keyboard=keyboard1)
    if sql_subscribe_status_get(iduser)=='0':
        await message.answer("Главное меню",keyboard=keyboard0)

    await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)

#доп выдача
@bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'add'})
async def ADD_handler(message:Message):

    keyboard0 = (Keyboard(one_time=False)
                 .add(Text('Давай еще', {'cmd': 'add'}))
                 .add(Text('Назад',{'cmd': 'menu'}))
                 )
    keyboard2 = (Keyboard(one_time=False)
               .add(Text('Назад', {'cmd': 'menu'}))
                 )
    iduser = await iduserget(message)
    if sql_position_giving_vacancies(iduser)+5 <= sql_position_limit_get(iduser):
        profession, city, salary = sql_get_user_info(iduser)
        newvacancy = get_vacancy_objects(profession, city, salary)
        for next in range(1,6):
                pos=sql_position_giving_vacancies(iduser)
                profession = newvacancy[pos]['profession']
                link = newvacancy[pos]['link']
                keyboard1=(Keyboard(inline=True)
                           .add(OpenLink(link,'Открыть🚀'))
                           )
                if int(newvacancy[pos]['payment_from'])<int(salary) and int(newvacancy[pos]['payment_from'])!=0 :
                    payment = f"{salary} - {newvacancy[pos]['payment_to']}"
                else:
                    payment = f"{newvacancy[pos]['payment_from']} - {newvacancy[pos]['payment_to']}"
                if payment=='0 - 0':
                    payment='После собеседования'
                company = newvacancy[pos]["firm_name"]
                sql_change_position(iduser,1)
                await message.answer (f"💼Вакансия: {profession} \n 🏙Компания:{company} \n 💲Условия оплаты: {payment} \n🔜Оставить заявку и узнать подробне о вакансии:",keyboard=keyboard1)
        await message.answer(keyboard=keyboard0)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
    elif sql_position_giving_vacancies(iduser) + 5 > sql_position_limit_get(iduser):
            sql_change_position(iduser, 0)
            await message.answer('Упс, вакансий не осталось',keyboard=keyboard2)
            await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)



#Оформление подписки
@bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'subs'})
async def subs_handler(message: Message):
    keyboard0=(Keyboard(one_time=False)
                 .add(Text('Подтвердить', {'cmd': 'menu'}))
                 )
    iduser = await iduserget(message)
    if sql_subscribe_status_get(iduser)=='0':
        sql_subscribe_status_set(iduser, '1')
        await message.answer('Подписка создана', keyboard=keyboard0)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
    elif sql_subscribe_status_get(iduser)=='1':
        sql_subscribe_status_set(iduser, '0')
        await message.answer('Подписка отменена',keyboard=keyboard0)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)

















bot.run_forever()













