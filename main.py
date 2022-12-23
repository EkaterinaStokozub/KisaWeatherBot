import json
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import aioschedule

import requests

API_TOKEN = None
with open("token.txt") as f:
    API_TOKEN = f.read().strip()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

buttons=[[types.KeyboardButton(text='Сейчас')],[types.KeyboardButton(text='Утром'),types.KeyboardButton(text='Днём')],
         [types.KeyboardButton(text='Вечером'),types.KeyboardButton(text='Ночью')]]

chat_id = {}
global lat
global lon

conditions = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
                  'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
                  'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
                  'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
                  'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
                  'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
                  'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
                  }
wind_dir = {'nw': 'северо-западное', 'n': 'северное', 'ne': 'северо-восточное', 'e': 'восточное',
                'se': 'юго-восточное', 's': 'южное', 'sw': 'юго-западное', 'w': 'западное', 'с': 'штиль'}

def req(lat,lon):
      url_yandex = f'https://api.weather.yandex.ru/v2/forecast/?lat={lat}&lon={lon}&[lang=ru_RU]'
      token_yandex = 'e935f5fe-68ba-4040-acc0-1490d5ffead6'
      yandex_req = requests.get(url=url_yandex, headers={'X-Yandex-API-Key': token_yandex})
      data=json.loads(yandex_req.text)
      return data



@dp.message_handler(commands=['start'])
async def say_hello(message: types.Message):
      await message.answer('Привет! Я KisaWeatherBot и я здесь для того, чтобы ты узнал погоду. Пришли мне геометку и я '
                           'скажу тебе прогноз погоды!')


@dp.message_handler(content_types=['location'])
async def get_location(message: types.Message):
      markup=types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
      chat_id[message.from_user.id] = message.from_user
      global lat
      global lon
      lat = message.location.latitude
      lon = message.location.longitude

      await message.answer(text='Спасибо! Выберите прогноз погоды',reply_markup=markup)


@dp.message_handler(regexp='Сейчас')
async def weather_now(message: types.Message):
      data=req(lat,lon)
      await message.answer(f"Давление: {data['info']['def_pressure_mm']}мм.рт.\n"
                           f"Давление: {data['info']['def_pressure_pa']}Па\n"
                           f"Температура: {data['fact']['temp']}°C\n"
                           f"Ощущается: {data['fact']['feels_like']}°C\n"
                           f"На небе: {conditions[data['fact']['condition']]}\n"
                           f"Скорость ветра: {data['fact']['wind_speed']}м/с\n"
                           f"Направление ветра: {wind_dir[data['fact']['wind_dir']]}\n"
                           f"Восход: {data['forecasts'][0]['sunrise']}\n"
                           f"Закат: {data['forecasts'][0]['sunset']}")

@dp.message_handler(regexp='Утром')
async def weather_morning(message: types.Message):
      data=req(lat,lon)
      morning = data['forecasts'][0]['parts']['morning']
      await message.answer(f"Давление: {morning['pressure_mm']}мм.рт.\n"
                           f"Давление: {morning['pressure_pa']}Па\n"
                           f"Температура: {morning['temp_avg']}°C\n"
                           f"Ощущается: {morning['feels_like']}°C\n"
                           f"На небе: {conditions[morning['condition']]}\n"
                           f"Скорость ветра: {morning['wind_speed']}м/с\n"
                           f"Направление ветра: {wind_dir[morning['wind_dir']]}\n")

@dp.message_handler(regexp='Днём')
async def weather_day(message: types.Message):
      data=req(lat,lon)
      day = data['forecasts'][0]['parts']['day']
      await message.answer(f"Давление: {day['pressure_mm']}мм.рт.\n"
                           f"Давление: {day['pressure_pa']}Па\n"
                           f"Температура: {day['temp_avg']}°C\n"
                           f"Ощущается: {day['feels_like']}°C\n"
                           f"На небе: {conditions[day['condition']]}\n"
                           f"Скорость ветра: {day['wind_speed']}м/с\n"
                           f"Направление ветра: {wind_dir[day['wind_dir']]}\n")

@dp.message_handler(regexp='Вечером')
async def weather_evening(message: types.Message):
      data=req(lat,lon)
      evening = data['forecasts'][0]['parts']['evening']
      await message.answer(f"Давление: {evening['pressure_mm']}мм.рт.\n"
                           f"Давление: {evening['pressure_pa']}Па\n"
                           f"Температура: {evening['temp_avg']}°C\n"
                           f"Ощущается: {evening['feels_like']}°C\n"
                           f"На небе: {conditions[evening['condition']]}\n"
                           f"Скорость ветра: {evening['wind_speed']}м/с\n"
                           f"Направление ветра: {wind_dir[evening['wind_dir']]}\n")

@dp.message_handler(regexp='Ночью')
async def weather_night(message: types.Message):
      data=req(lat,lon)
      night = data['forecasts'][0]['parts']['night']
      await message.answer(f"Давление: {night['pressure_mm']}мм.рт.\n"
                           f"Давление: {night['pressure_pa']}Па\n"
                           f"Температура: {night['temp_avg']}°C\n"
                           f"Ощущается: {night['feels_like']}°C\n"
                           f"На небе: {conditions[night['condition']]}\n"
                           f"Скорость ветра: {night['wind_speed']}м/с\n"
                           f"Направление ветра: {wind_dir[night['wind_dir']]}\n")


async def periodic():
    data = req(lat, lon)
    for id in chat_id:
        await bot.send_message(id, f"Давление: {data['info']['def_pressure_mm']}мм.рт.\n"
                           f"Давление: {data['info']['def_pressure_pa']}Па\n"
                           f"Температура: {data['fact']['temp']}°C\n"
                           f"Ощущается: {data['fact']['feels_like']}°C\n"
                           f"На небе: {conditions[data['fact']['condition']]}\n"
                           f"Скорость ветра: {data['fact']['wind_speed']}м/с\n"
                           f"Направление ветра: {wind_dir[data['fact']['wind_dir']]}\n"
                           f"Восход: {data['forecasts'][0]['sunrise']}\n"
                           f"Закат: {data['forecasts'][0]['sunset']}", disable_notification=True)

async def scheduler():
    aioschedule.every().day.at("23:27").do(periodic)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(10)

async def on_startup(_):
    asyncio.create_task(scheduler())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)

