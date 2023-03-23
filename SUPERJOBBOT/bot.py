
from vkbottle.bot import Bot,Message
from vkbottle import Keyboard,KeyboardButtonColor,Text,OpenLink,BaseStateGroup,CtxStorage,EMPTY_KEYBOARD

from API_SJ_REQUEST import *
from datetime import datetime
bot=Bot(token='vk1.a.gC18gjaTqfcql01jYmAv87GwsY7azlNlgGH2dEQVR06UXYCaEkSZSeXEhsom4wBYHNWkNcBp1T7SdGMD8E7ZPEWnT2TNnMBHG0CuaDAfwe4imZ757iMsCQmnuVkqWGJAIW62IW9bxs4JliThV_krBJPBz6scsVZUZ44hBAgfx8RGfEkhLUjeWuN3X-YWyE_zmVDYjepPxfYHrvFUNe5ptQ')
ctx=CtxStorage()


# обьявление переменных для сбора пользовательской инфы
# ------------------------------------------------------
class SUBSDSATA(BaseStateGroup):
    CITY=0
    PROF=1
    PAY=2
    GO=4
    GET = 3
    CONT=5
    UPDATE=6
    BACK=7



# API запрос к SJ
#--------------------------------------------------------------




# 0 этап главное меню
# ----------------------------------------------
@bot.on.message(state=None,payload={"command":"start"})
@bot.on.message(text=['Начать','начать'])
async def starthandler(message:Message):

    users = await bot.api.users.get(message.from_id)
    keyboard=(Keyboard(inline=False,one_time=True)
              .add(Text('Искать работу',{'cmd':'reg'}), color=KeyboardButtonColor.POSITIVE)
              )
    await message.answer(f'Приветствуем тебя,{users[0].first_name} Это бот вакансий от SUPERJOB💚'
                         '\n Поможем найти новые вакансии по вашим параметрам:\n Город | Профессия | Заработная плата📝\nНажмите кнопку "Искать работу"🔔',keyboard=keyboard)


# 1 этап получение инфы о городе
# ---------------------------------------
@bot.on.message(payload={'cmd':'reg'})
@bot.on.message(lev='/reg')
async def city_handler(message:Message):
    keyboard = (
            Keyboard(inline=True)
            .add(Text('Москва'))
            .add(Text('Волгоград'))
            .row()
            .add(Text('Владивосток'))
            .add(Text('CПБ'))
            .row()
            .add(Text('Воронеж'))
            .add(Text('Казань'))
            .row()
            .add(Text("Калуга"))
            .add(Text('Краснодар'))
            .row()
            .add(Text("Пермь"))
            .add(Text('Ростов'))

        )
    # photo1= await photo_upd.upload('logo1.jpg')
    await message.answer("Найти вакансии? Я это могу! Приступим? Выбирай город из списка или пиши вручную 🧭🌁", keyboard=keyboard,attachment='photo-217363563_457239024')
    await bot.state_dispenser.set(message.peer_id,SUBSDSATA.PROF)




# 2 этап получение инфы о професии
#---------------------------------------------
@bot.on.message(state=SUBSDSATA.PROF)
async def prof_handler(message:Message):
    if message.text == "СПБ":
        ctx.set('city','Cанкт-Петербург')
    else:
        ctx.set('city', message.text)
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
    ctx.set('prof',message.text)
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
    ctx.set('pay', None)
    ctx.set('keystart',True)
    await message.answer('Сколько денег хочешь зарабатывать? Выбери или напиши вручную 💵', keyboard=keyboarad0,attachment='photo-217363563_457239026')
    await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)


# обработка и выдача Результата
# ------------------------------------------


@bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'edit'})
async def initial_handler(message:Message):
    if ctx.get('pay') ==None:
        pay = message.text
        pay = pay.rstrip('₽').replace(' ', '')
        ctx.set('pay', pay)

    keyboardstart = (Keyboard(one_time=True,inline=False)
                .add(Text('Получить',{'cmd':'get'}), color=KeyboardButtonColor.POSITIVE)
                .add(Text('Изменить', {'cmd': 'reg'}), color=KeyboardButtonColor.PRIMARY)
                )
    keyboardcont = (Keyboard(one_time=True, inline=False)

                .add(Text('Изменить', {'cmd': 'reg'}), color=KeyboardButtonColor.PRIMARY)

                .add(Text('Назад', {'cmd': 'menu'}), color=KeyboardButtonColor.SECONDARY)
                )
    if ctx.get('keystart')==True:
        await message.answer(f"Ваши параметры🎲:\nГород :{ctx.get('city')}"
                         f"\nПрофессия:{ctx.get('prof')}\nЗарплата от: {ctx.get('pay')}"
                         f'\n\n Посмотреть вакансии - "Получить"\n'
                         f'Если Запросы изменились - Изменить ',keyboard=keyboardstart,attachment='photo-217363563_457239027')
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.GO)
    elif ctx.get('keystart')==False:
        await message.answer(f"Ваши параметры🎲:\nГород :{ctx.get('city')}"
                             f"\nПрофессия:{ctx.get('prof')}\nЗарплата от: {ctx.get('pay')}"
                             f'\n\n'
                             f'Если Запросы изменились - Изменить ', keyboard=keyboardcont,
                             attachment='photo-217363563_457239027')



#выдача 5 вакансий и переход в меню
@bot.on.message(state=SUBSDSATA.GO,payload={'cmd':'get'})
async def confirm_handler(message: Message):
    keyboard0 = (Keyboard(one_time=False)
                .add(Text('Перейти на сайт'))
                .add(Text('Давай еще',{'cmd':'add'}))
                .add(Text('Мои параметры',{'cmd':'edit'}))
                .row()
                .add(Text('В главное меню', {'cmd': 'menu'}))
                 )

    keyboard1=(Keyboard(one_time=False)
                .add(Text('Изменить',{'cmd':'edit'}), color=KeyboardButtonColor.PRIMARY))

# запрос и сохранение ответа апи!проработка варианта действий
# при недействительном токене! с блоком вакансий и колвом вакансий
# ---------------------------------------
    newvacancy = getinfo(ctx.get('prof'), ctx.get('city'), ctx.get('pay'))
    lenlist=len(newvacancy)
    ctx.set('newvacancy', newvacancy)
    ctx.set('len',lenlist)

# разбивка
# -----------------------------------------------
    ctx.set('keystart', False)
    ctx.set('num', 0)
    ctx.set('subs', False)
    try:
            while ctx.get("num") < 5 and ctx.get("num")<=ctx.get("len") :
                if ctx.get("num") == 0:
                    with open('tokens.json', 'r') as f:
                        dict = json.load(f)
                    if int(dict['date_published']) < int(newvacancy[ctx.get("num")]['date_published']):
                        dict['date_published'] = newvacancy[ctx.get("num")]['date_published']
                        ctx.set('datpub0',newvacancy[ctx.get("num")]['date_published'])
                    with open('tokens.json', 'w') as f:
                        json.dump(dict, f)
                await message.answer(f'Вакансия {ctx.get("num")+1} из {5}:')
                profession = newvacancy[ctx.get("num")]['profession']
                time=int(newvacancy[ctx.get("num")]['date_published'])

                link = newvacancy[ctx.get("num")]['link']
                keyboard1=(Keyboard(inline=True)
                           .add(OpenLink(link,'Открыть🚀'))
                           )
                if int(newvacancy[ctx.get('num')]['payment_from'])<int(ctx.get('pay')) and int(newvacancy[ctx.get('num')]['payment_from'])!=0 :
                    payment = f"{ctx.get('pay')} - {newvacancy[ctx.get('num')]['payment_to']}"
                else:
                    payment = f"{newvacancy[ctx.get('num')]['payment_from']} - {newvacancy[ctx.get('num')]['payment_to']}"
                if payment=='0 - 0':
                    payment='После собеседования'
                company = newvacancy[ctx.get('num')]["firm_name"]
                ctx.set('num', ctx.get('num')+1)
                await message.answer (f"💼Вакансия: {profession} \n 🏙Компания:{company} \n 💲Условия оплаты: {payment} \n🔜Оставить заявку и узнать подробне о вакансии:",keyboard=keyboard1)
            await message.answer('Что дальше?',keyboard=keyboard0)
            await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
    except IndexError:
        await message.answer('Извините, мы не нашли вакансий согласно вашим параметрам\n Давайте изменим "',keyboard=keyboard1)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)

#Главное меню
@bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'menu'})
async def Menu_handler(message: Message):
    ctx.set('keystart', False)
    keyboard0 = (Keyboard(one_time=False)
                 .add(Text( 'Перейти на сайт'))
                 .add(Text('Давай еще', {'cmd': 'add'}))
                 .row()
                 .add(Text('Мои параметры',{'cmd':'edit'}))
                 .add(Text('Создать подписку',{'cmd':'subs'}))
                      )
    keyboard1 = (Keyboard(one_time=False)
                 .add(Text('Перейти на сайт'))
                 .add(Text('Давай еще', {'cmd': 'add'}))
                 .row()
                 .add(Text('Мои параметры',{'cmd':'edit'}))
                 .add(Text('Отменить подписку', {'cmd': 'subs'})))
    if ctx.get('subs')==False:
        await message.answer('Вы в главном меню',keyboard=keyboard0)

    elif ctx.get('subs')==True:
        await message.answer('Вы в главном меню', keyboard=keyboard1)
    await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)

#доп выдача
@bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'add'})
async def ADD_handler(message: Message):
    finish=ctx.get("num")
    keyboard0 = (Keyboard(one_time=False)
                 .add(Text('Давай еще', {'cmd': 'add'}))
                 .add(Text('Назад',{'cmd': 'menu'}))
                 )
    keyboard2 = (Keyboard(one_time=False)
                 .add(Text('Назад', {'cmd': 'menu'}))
                 )
    if finish+5<=ctx.get("len"):
        while  ctx.get("num") < finish+5 and finish+5 <= ctx.get("len"):
            await message.answer(f'Вакансия {ctx.get("num") + 1} из {finish+5}:')
            profession = ctx.get('newvacancy')[ctx.get("num")]['profession']
            time = int(ctx.get('newvacancy')[ctx.get("num")]['date_published'])
            date = datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
            link = ctx.get('newvacancy')[ctx.get("num")]['link']
            company = ctx.get('newvacancy')[ctx.get('num')]["firm_name"]
            keyboard1 = (Keyboard(inline=True)
                     .add(OpenLink(link, 'Открыть🚀'))
                     )
            payment = f"{ctx.get('newvacancy')[ctx.get('num')]['payment_from']} - {ctx.get('newvacancy')[ctx.get('num')]['payment_to']}"
            if payment == '0 - 0':
                payment = 'После собеседования'
            ctx.set('num', ctx.get("num")+1)
            await message.answer(
            f"💼Вакансия: {profession} \n 🏙Компания:{company} \n 💲Условия оплаты: {payment}\n🔜Оставить заявку и узнать подробне о вакансии:",
            keyboard=keyboard1)
        await message.answer(keyboard=keyboard0)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
    if finish + 5 > ctx.get("len"):
        await message.answer('Упс, вакансий не осталось',keyboard=keyboard2)
        ctx.set('num',0)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)



#Оформление подписки
@bot.on.message(state=SUBSDSATA.CONT,payload={'cmd':'subs'})
async def subs_handler(message: Message):
    keyboard0=(Keyboard(one_time=False)
                 .add(Text('Назад', {'cmd': 'menu'}))
                 )
    if ctx.get('subs')==False:
        ctx.set('subs',True)
        await message.answer('Подписка создана', keyboard=keyboard0)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
    elif ctx.get('subs') == True:
        ctx.set('subs', False  )
        await message.answer('Подписка отменена',keyboard=keyboard0)
        await bot.state_dispenser.set(message.peer_id, SUBSDSATA.CONT)
















bot.run_forever()













