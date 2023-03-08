from pyrogram import Client, idle
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from random import choice
from pyrogram import Client, filters
from aiohttp import ClientSession
from json import loads
from pyrogram.types import Message as message
import asyncio

app = Client("test1", bot_token="5808857616:AAEhIze6UIe-BnN8_S9Iu5tIT2owsBTOJdA", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("running.")
    


@app.on_message(filters.text & ~filters.command("check"))
async def toggle(_, message):
    
    url = f"https://api.openai.com/v1/engines/davinci/completions"

    headers = {
            "Authorization": "Bearer {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}",
            "Content-Type": "application/json",
        }
    
    async with ClientSession() as session:
        await asyncio.sleep(0.5)
        async with session.get(url, headers=headers) as resp:
            await message.reply((await resp.json()))

@app.on_message(filters.text & ~filters.command("ask"))
async def message_handler(_, message):
    if message.strip().startswith("/ask"):
        # Send message to notify user that response is being generated
        generating_message = await message.reply("generating response...")

        # Get the message text
        message_text = message.strip().replace("/ask","",1).strip()

        while True:
            try:
                # Pass event object to callback function
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=f"{message_text}\n",
                    max_tokens=2048,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
                break
            except openai.exceptions.OpenAiError as e:
                if 'Usage Limit Exceeded' in str(e):
                    switch_api_key()
                else:
                    raise e

        link = handle_response(message, response)
        await message.reply(link)
        await generating_message.delete()

app.start()
idle()     
