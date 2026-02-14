import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# === Переменные окружения ===
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
STRING_SESSION = os.environ.get("STRING_SESSION")
HANDLER = os.environ.get("HANDLER", ".saveit")

# === Создаём клиент через STRING_SESSION ===
client = TelegramClient(
    StringSession(STRING_SESSION),
    API_ID,
    API_HASH
)


@client.on(events.NewMessage(pattern=f"^{HANDLER}$"))
async def handler(event):
    if not event.is_reply:
        await event.reply("Ответь на сообщение с медиа.")
        return

    reply = await event.get_reply_message()

    if not reply.media:
        await event.reply("В этом сообщении нет медиа.")
        return

    try:
        file = await reply.download_media()
        await client.send_file("me", file)
        await event.reply("Сохранено в Избранное ✅")
        os.remove(file)
    except Exception as e:
        await event.reply(f"Ошибка: {e}")


async def main():
    print("Saveit запущен...")
    await client.start()
    print("Успешно подключено к Telegram ✅")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
