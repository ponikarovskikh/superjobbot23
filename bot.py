
from vkbottle.bot import Bot,Message
from vkbottle import Keyboard,KeyboardButtonColor,Text,OpenLink,BaseStateGroup,CtxStorage
from vkbottle import PhotoMessageUploader

import requests
import time
import json
bot=Bot(token='vk1.a.gC18gjaTqfcql01jYmAv87GwsY7azlNlgGH2dEQVR06UXYCaEkSZSeXEhsom4wBYHNWkNcBp1T7SdGMD8E7ZPEWnT2TNnMBHG0CuaDAfwe4imZ757iMsCQmnuVkqWGJAIW62IW9bxs4JliThV_krBJPBz6scsVZUZ44hBAgfx8RGfEkhLUjeWuN3X-YWyE_zmVDYjepPxfYHrvFUNe5ptQ')
ctx=CtxStorage()


# обьявление переменных для сбора пользовательской инфы
# ------------------------------------------------------
class SUBSDSATA(BaseStateGroup):
    CITY=0
    PROF=1
    PAY=2
    FINISH=4
    GET = 3



# API запрос к SJ
#--------------------------------------------------------------
def getinfo(keyword,town,payment):
                    params = {
                    'payment_from':f'{payment}',
                    "sort_new": time.time(),
                    "keyword":f"{keyword}",
                    "town":f'{town}'
                    }
                    headers={
                    'X-Api-App-Id': "v3.r.130155215.a338c216d6fb51385312670e906c0b708b7c3e2b.3be37d75e69e47c96e6e44000d613035b9d07b00",
                    'Authorization': "Bearer v3.r.130155215.eab298d92cb901aced882c514dc818cf46f86c12.ce283e8e18c56e10028a9b45c87d9bcc6b98959d"
                     }
                    endpoint = "https://api.superjob.ru/2.0/vacancies/"
                    response = requests.get(endpoint, headers=headers, params=params,).json()
                    resjson_form = json.dumps(response, ensure_ascii=False, indent=2)
                    pyform = json.loads(resjson_form)
                    newvacancy=pyform['objects']
                    ctx.set('newvacancy',newvacancy)
                    return newvacancy



# 0 этап главное меню
# ----------------------------------------------
@bot.on.message(payload={'cmd':'start'})
@bot.on.message(text=['Начать','начать'])
async def starthandler(message:Message):
    flag=False

    keyboard=(Keyboard(inline=False,one_time=True)
              .add(Text('Искать работу',{'cmd':'reg'}), color=KeyboardButtonColor.POSITIVE)
              )
    await message.answer('Это бот вакансий от SUPERJOB💚'
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
    await message.answer("Найти вакансии? Я это могу! Приступим? Выбирай город из списка или пиши вручную 🧭🌁", keyboard=keyboard)
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

    await message.answer('Теперь определись с профессией или напиши свой вариант‍🚀',keyboard=keyboarad)
    await bot.state_dispenser.set(message.peer_id,SUBSDSATA.PAY)

# 3 этап получение инфы о желаемом заработке
# --------------------------------------------

@bot.on.message(state=SUBSDSATA.PAY)
async def pay_handler(message:Message):


    ctx.set('prof',message.text)
    keyboarad = (Keyboard(inline=True)
                 .add(Text('10 000₽'))
                 .add(Text('20 000₽'))
                 .row()
                 .add(Text('30 000₽'))
                 .add(Text('50 000₽'))
                 .row()
                 .add(Text('80 000₽'))
                 .add(Text('100 000₽'))
                 .row()
                 .add(Text('150 000₽'))
                 .add(Text('200 000₽'))
                 .row()
                 .add(Text('300 000₽'))
                 .add(Text('400 000₽'))   )
    await message.answer('Сколько денег хочешь зарабатывать? Выбери или напиши вручную 💵', keyboard=keyboarad)
    await bot.state_dispenser.set(message.peer_id, SUBSDSATA.GET)
# обработка и выдача Результата
# ------------------------------------------


@bot.on.message(state=SUBSDSATA.GET)
async def initial_handler(message:Message):
    pay = message.text
    pay = pay.rstrip('₽').replace(' ', '')
    ctx.set('pay', pay)


    keyboard = (Keyboard(one_time=False)
                .add(Text('Искать🔍',{'cmd':'reg'}),color=KeyboardButtonColor.PRIMARY)
                )
    # keyboard1 = (Keyboard(one_time=True)
    #             .add(Text('Искать🔎', {'cmd': 'reg'}), color=KeyboardButtonColor.PRIMARY)
    #             )
    # запрос и сохранение ответа апи!роработка варианта действий  при недействительном токене! с блоком вакансий и колвом вакансий
    # ---------------------------------------
    newvacancy = getinfo(ctx.get('prof'), ctx.get('city'), ctx.get('pay'))




















    lenlist=len(newvacancy)
    ctx.set('newvacancy', newvacancy)
    ctx.set('len',lenlist)
    u=message.payload
    # разбивка
    # ------------------------------------------------
    d=0
    await message.answer(f"Ваши параметры🎲:\nГород 🌁:{ctx.get('city')}\nПрофессия👨‍💻:{ctx.get('prof')}\nЗарплата💲 от: {ctx.get('pay')}\n Ожидайте выдачу🕒",keyboard=keyboard)
    ctx.set('num', 0)
    # await message.answer('🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢')
    time.sleep(1)
    try:
        while d <= 5 and d<=ctx.get("len") :
                # if ctx.get("len") ==0:
                #     await message.answer('Извините, мы не нашли вакансий согласно вашим параметрам\n Напишите "Начать"',keyboard=keyboard)
                #     break
                # elif ctx.get("len") < 5 and ctx.get("len")!=0:
                #     await message.answer(f'Вакансия {ctx.get("num")+1} из {ctx.get("len")}:')
                # else:
                #     await message.answer(f'Вакансия {ctx.get("num")+1} из {5}:')
                profession = newvacancy[ctx.get("num")]['profession']
                link = newvacancy[ctx.get("num")]['link']
                # s = pyshorteners.Shortener()
                # link = s.tinyurl.short(
                #     f"{link}")
                keyboard1=(Keyboard(inline=True)
                           .add(OpenLink(link,'Открыть🚀'))
                           )

                payment = f"{newvacancy[ctx.get('num')]['payment_from']} - {newvacancy[ctx.get('num')]['payment_to']}"
                if payment=='0 - 0':
                    payment='После собеседования'
                company = newvacancy[ctx.get('num')]["firm_name"]

                ctx.set('num', d)
                await message.answer (f"💼Вакансия: {profession} \n 🏙Компания:{company} \n 💲Условия оплаты: {payment} \n 🔜Оставить заявку и узнать подробне о вакансии:",keyboard=keyboard1)

                time.sleep(1)
                d += 1
        ctx.set('num', 0)
        await message.answer('Пока всё✔ Нажмите "Искать🔍"',keyboard=keyboard)
    except IndexError:

        await message.answer('Извините, мы не нашли вакансий согласно вашим параметрам\n Напишите "Искать🔍"',keyboard=keyboard)


#
# @bot.on.message(text='Вперед')
# async def scrolltoward(message:Message):
#     keyboard = (Keyboard(one_time=True)
#                 .add(Text('Назад',{'cmd':'back'}))
#                 .add(Text('Отменить подписку❎',{'cmd':'reg'}))
#                 .add(Text("Вперед ", {'cmd': 'next2'})))
#
#
#     newvacancy = ctx.get('newvacancy')
#     profession = newvacancy[ctx.get("num")]['profession']
#     link = newvacancy[ctx.get("num")]['link']
#     payment = f"{newvacancy[ctx.get('num')]['payment_from']} - {newvacancy[ctx.get('num')]['payment_to']}"
#     company = newvacancy[ctx.get('num')]["firm_name"]
#
#     time.sleep(2)
#     await message.answer(f'Вакансия {ctx.get("num")+1} из {ctx.get("len")}:')
#     await message.answer( f"💼Вакансия: {profession} \n 🏙Компания:{company} \n 💲Условия оплаты: {payment} \n 🔜Оставить заявку и узнать подробне о вакансии:\n {link} ",keyboard=keyboard)
#

# @bot.on.message(payload={'cmd':'next2'})
# async def scrolltoward(message:Message):
#
#     keyboard = (Keyboard(one_time=True)
#                 .add(Text('Назад',{'cmd':'back'}))
#                 .add(Text('Отменить подписку❎',{'cmd':'reg'}))
#                 .add(Text("Вперед ", {'cmd': 'next1'})))
#
#     i=ctx.get('num')
#     i =i+1
#     ctx.set('num', i)
#     newvacancy = ctx.get('newvacancy')
#     profession = newvacancy[ctx.get("num")]['profession']
#     link = newvacancy[ctx.get("num")]['link']
#     payment = f"{newvacancy[ctx.get('num')]['payment_from']} - {newvacancy[ctx.get('num')]['payment_to']}"
#     company = newvacancy[ctx.get('num')]["firm_name"]
#
#     await message.answer(f'Вакансия {ctx.get("num")+1} из {ctx.get("len")}:')
#     await message.answer(f"💼Вакансия: {profession} \n 🏙Компания:{company} \n 💲Условия оплаты: {payment} \n 🔜Оставить заявку и узнать подробне о вакансии:\n {link} ", keyboard=keyboard)
#
#









# @bot.on.message(payload={'cmd':'back'})
# async def scrollbackward(message:Message):
#     keyboard = (Keyboard(one_time=True)
#                     .add(Text('Назад', {'cmd':'back'}))
#                     .add(Text('Отменить подписку❎',{'cmd':'reg'}))
#                     .add(Text("Вперед", {'cmd':'next'}))
#                     )
#     i = ctx.get('num')
#     i =i-1
#     ctx.set('num', i)
#     newvacancy = ctx.get('newvacancy')
#     profession = newvacancy[ctx.get("num")]['profession']
#     link = newvacancy[ctx.get("num")]['link']
#     payment = f"{newvacancy[ctx.get('num')]['payment_from']} - {newvacancy[ctx.get('num')]['payment_to']}"
#     company = newvacancy[ctx.get('num')]["firm_name"]
#     time.sleep(2)
#     await message.answer(f'Вакансия {ctx.get("num") + 1} из {ctx.get("len")}:')
#     await message.answer(f"💼Вакансия: {profession} \n 🏙Компания:{company} \n 💲Условия оплаты: {payment} \n 🔜Оставить заявку и узнать подробне о вакансии:\n {link} ",keyboard=keyboard)










bot.run_forever()













