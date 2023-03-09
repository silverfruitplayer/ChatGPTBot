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
import logging
import os

openai.api_key = "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"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

app = Client("test1", bot_token="5808857616:AAEhIze6UIe-BnN8_S9Iu5tIT2owsBTOJdA", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(f"Hi {message.from_user.mention}, Ask any question to start over.")
    

@app.on_message(filters.text)
async def message_handler(_, message):
    if message.text:
        generating_message = await message.reply("Generating response...")

        message_text = message.text

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
                
            except openai.error.Timeout as e:
                await message.reply(f"The what!?\n!!error start!!\n{e}\n!!!error end!!!")
                pass 
            
            except openai.error.RateLimitError as e:
                print(f"OpenAI API request exceeded rate limit: {e}")
                pass
            
            except openai.error.InvalidRequestError as e:
                await message.reply(f"The what!?\n!!error start!!\n{e}\n!!!error end!!!")
                pass                                       
                
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
            await message.reply(response["choices"][0]["text"])
            await generating_message.delete()

app.start()
idle()     
