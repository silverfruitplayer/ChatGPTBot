from pyrogram import Client, idle
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from random import choice
from pyrogram import Client, filters
from aiohttp import ClientSession
from json import loads
from pyrogram.types import Message as message
import asyncio
import openai
import requests

openai.api_key = "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"

app = Client("test1", bot_token="5808857616:AAEhIze6UIe-BnN8_S9Iu5tIT2owsBTOJdA", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("running.")
    

"""
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
"""
@app.on_message(filters.command("ask"))
async def message_handler(_, message):
    if message.text.split(None, 1)[1]:
        # Send message to notify user that response is being generated
        generating_message = await message.reply("generating response...")

        # Get the message text
        message_text = message.text.strip().replace("/ask","",1).strip()

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
                    await message.reply(e)

        if len(response) > 4096:
            filename = "sex.txt"
            evaluation = "Success"

            with open(filename, "w+", encoding="utf8") as out_file:
                out_file.write(str(evaluation.strip()))
                await message.reply_document(
                    document=filename,
                    caption="ok",
                    disable_notification=True,
                    reply_to_message_id=reply_to_id,
                )
                os.remove(filename)
        else:
            await message.reply(response)
            await generating_message.delete()

app.start()
idle()     
