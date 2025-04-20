import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import db
import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Здесь можно проголосовать, чем сегодня пахнет в Гатчине: свалкой или говном.\n\n" \
        "Используй /svalka или /govno, чтобы проголосовать. Голосовать можно только один раз в день.\n" \
        "Статистика: /stats — за сегодня, /history — за 7 дней."
    )

@dp.message(Command("svalka"))
async def cmd_svalka(message: Message):
    user_id = message.from_user.id
    voted = await db.has_voted_today(user_id)
    if voted:
        await message.answer("Вы уже голосовали сегодня!")
        return
    await db.save_vote(user_id, "svalka")
    await message.answer("Ваш голос за свалку засчитан!")

@dp.message(Command("govno"))
async def cmd_govno(message: Message):
    user_id = message.from_user.id
    voted = await db.has_voted_today(user_id)
    if voted:
        await message.answer("Вы уже голосовали сегодня!")
        return
    await db.save_vote(user_id, "govno")
    await message.answer("Ваш голос за говно засчитан!")

@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    svalka, govno = await db.get_today_stats()
    await message.answer(f"Сегодня:\nСвалка: {svalka}\nГовно: {govno}")

@dp.message(Command("history"))
async def cmd_history(message: Message):
    history = await db.get_history(7)
    text = "Статистика за 7 дней:\n"
    for day, svalka, govno in history:
        text += f"{day}: свалка — {svalka}, говно — {govno}\n"
    await message.answer(text)

async def main():
    await db.init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
