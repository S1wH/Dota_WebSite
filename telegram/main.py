import logging
import asyncio
from datetime import date
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from connection import make_request, get_token, BASE_URL

API_TOKEN = '6404033562:AAFFUFrDwtt59l9_ON_An2npr2ZnMRr6WQ4'

TOKEN = None
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Текущие матчи", "Текущие турниры"]
    keyboard.add(*buttons)
    await message.answer("Что хотите найти?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Текущие матчи"))
async def get_current_matches(message: types.Message):
    response = await make_request(BASE_URL + 'matches/v1.0/api/matches/?status=O', TOKEN)
    if response is None:
        await message.answer('Please authorize to use bot')
    else:
        if response:
            result = ''
            for i in range(0, 5):
                result += 'Match between ' +\
                          str(response[i]['team1']) +\
                          ' and ' + str(response[i]['team2']) + '\n'
            await message.answer(result)
        else:
            await message.answer('No current matches')


@dp.message_handler(Text(equals="Текущие турниры"))
async def get_current_tournaments(message: types.Message):
    current_date = date.today()
    response = await make_request(BASE_URL +
                                  f'tournaments/api/tournaments/?'
                                  f'start_date__lte={current_date}'
                                  f'&end_date__gte={current_date}', TOKEN)
    if response == 'NO':
        await message.answer('Please authorize to use bot')
    else:
        if response:
            result = ''
            for i in range(len(response)):
                result += f'{response[i]["name"]}\n'
            await message.answer(result)
        else:
            await message.answer('No current tournaments')


@dp.message_handler(commands=["team"])
async def get_team(message: types.Message):
    cur_team = message.text[message.text.find(' ') + 1::]
    res = message.text.find(' ')
    if res != -1:
        response = await make_request(BASE_URL + 'teams_and_players/api/teams/', TOKEN)
        if response:
            for team in response:
                if cur_team.lower() in team["name"].lower():
                    await message.answer(
                        f'Победы: {team["win_matches"]}\n'
                        f'Поражения: {team["lose_matches"]}\n'
                        f'Ничьи: {team["draw_matches"]}\n'
                        f'Страна: {team["country"]}\n'
                        f'Призовые: {team["prize"]}\n'
                    )
                    return
        await message.answer("Команда не была найдена")
    else:
        await message.answer("Введите корректное название команды")


@dp.message_handler(commands=["player"])
async def get_player(message: types.Message):
    cur_player = message.text[message.text.find(' ') + 1::]
    res = message.text.find(' ')
    if res != -1:
        response = await make_request(BASE_URL + 'teams_and_players/api/players/', TOKEN)
        if response:
            for player in response:
                if cur_player.lower() in player["name"].lower() \
                        or cur_player.lower() in player["nickname"].lower():
                    team = None
                    for period in player["player_career"]:
                        if not period["end_date"]:
                            team = period["team"]
                    await message.answer(
                        f'Имя: {player["name"]}\n'
                        f'Никнейм: {player["nickname"]}\n'
                        f'Возраст: {player["age"]}\n'
                        f'Страна: {player["country"]}\n'
                        f'Текущая команда: {team}\n'
                        f'Описание: {player["biography"]}\n'
                    )
                    return
        await message.answer("Игрок не был найдена")
    else:
        await message.answer("Введите корректный никнейм или имя игрока")


@dp.message_handler(commands=["tournament"])
async def get_tournament(message: types.Message):
    cur_tournament = message.text[message.text.find(' ') + 1::]
    res = message.text.find(' ')
    if res != -1:
        response = await make_request(BASE_URL + 'tournaments/api/tournaments/', TOKEN)
        if response:
            for tournament in response:
                if cur_tournament.lower() in tournament["name"].lower():
                    teams = "\n".join(tournament["teams"])
                    await message.answer(
                        f'Название: {tournament["name"]}\n'
                        f'Местро проведения: {tournament["place"]}\n'
                        f'Призовой фонд: {tournament["prize"]}\n'
                        f'Состав участников:\n{teams}\n'
                    )
                    return
        await message.answer("Турнир не был найдена")
    else:
        await message.answer("Введите корректное название")


async def main():
    global TOKEN
    TOKEN = await get_token()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
