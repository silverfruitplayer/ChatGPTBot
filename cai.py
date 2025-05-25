import asyncio
from pyrogram import Client, filters
from PyCharacterAI import Client as CAIClient

# === CONFIGURATION ===
API_ID = 123456  # your Telegram API ID
API_HASH = "your_api_hash"  # your Telegram API hash
BOT_TOKEN = "your_bot_token"  # your bot token from @BotFather

CHARACTER_ID = ""  # CharacterAI character ID
CAI_TOKEN = ""        # Your CharacterAI token

user_sessions = {}

app = Client("cai_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def get_or_create_session(user_id: int):
    if user_id in user_sessions:
        return user_sessions[user_id]

    cai_client = CAIClient()
    await cai_client.authenticate(CAI_TOKEN)
    chat = await cai_client.create_or_continue_chat(CHARACTER_ID)

    user_sessions[user_id] = {
        "client": cai_client,
        "chat": chat
    }
    return user_sessions[user_id]

# === COMMAND HANDLERS ===
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await message.reply_text("Hey! Just send me a message and I’ll pass it to the character for you 😊")

# === CHAT HANDLER ===
@app.on_message(filters.text & filters.private & ~filters.command(["start"]))
async def chat_with_character(client, message):
    user_id = message.from_user.id
    user_input = message.text

    try:
        session = await get_or_create_session(user_id)
        cai_chat = session["chat"]

        response = await cai_chat.send_message(user_input)
        character_reply = response.text

        await message.reply_text(f"{response.src_character_name}: {character_reply}")
    except Exception as e:
        await message.reply_text("⚠️ Something went wrong. Please try again later.")
        print(f"Error: {e}")

# === RUN BOT ===
async def main():
    await app.start()
    print("Bot is running...")
    await idle()
    await app.stop()

from pyrogram.idle import idle
asyncio.run(main())
