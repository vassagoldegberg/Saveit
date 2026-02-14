import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
STRING_SESSION = os.environ.get("STRING_SESSION")

client = TelegramClient(
    StringSession(STRING_SESSION),
    API_ID,
    API_HASH
)


@client.on(events.NewMessage(incoming=True))
async def auto_save(event):
    # Берём информацию о чате
    chat = await event.get_chat()

    # ✅ Оставляем только личные диалоги (не группы и не каналы)
    if not event.is_private:
        return

    # Игнорируем свои сообщения
    me = await client.get_me()
    if event.sender_id == me.id:
        return

    # Если нет медиа — игнорируем
    if not event.media:
        return

    try:
        file = await event.download_media()
        await client.send_file("me", file)
        os.remove(file)
    except Exception:
        pass


async def main():
    print("AutoSave (только личные чаты) запущен...")
    await client.start()
    print("Сохранение активно ✅")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
