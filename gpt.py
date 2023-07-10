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
#from uvloop import install

openai.api_key = ""

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

app = Client("gptbot", bot_token="", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(f"Hi {message.from_user.mention}, Ask any question to start over.\nYou can search images too (NSFW content not allowed)")
    
@app.on_message(filters.regex("^/image"))
async def message_handler(_, message):
    if message.text:
        generating_message = await message.reply("Generating response for image...")

        message_text = message.text    

        while True:
            try:
                response1 = openai.Image.create(
                   prompt=f"{message_text}\n",
                   n=2,
                   size="1024x1024"
                )
                x =  response1["data"][0]["url"]
                await message.reply_photo(x)
                await generating_message.delete()
                break   
                
            except openai.error.Timeout as e:
                await message.reply(f"The what!?\n!!error start!!\n{e}\n!!!error end!!!")
                break
            
            except openai.error.RateLimitError as e:
                print(f"OpenAI API request exceeded rate limit: {e}")
                break
            
            except openai.error.InvalidRequestError as e:
                await message.reply(f"The what!?\n!!error start!!\n{e}\n!!!error end!!!")
                break                                      
                
                  


@app.on_message(filters.text)
async def message_handler(_, message):
    if message.text:

        cmd = ("/")

        fst_word = message.text.strip().split(None, 1)[0]

        if fst_word in cmd:
            return
        
        generating_message = await message.reply("Generating response...")

        message_text = message.text    

    
        while True:
            try:
                # Pass event object to callback function
                response = openai.Completion.create(
                    engine="text-davinci-003",
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
                    reply_to_message_id=reply_to_message.message.id,
                )
                os.remove(filename)
        else:
            await message.reply(response["choices"][0]["text"])
            await generating_message.delete()

app.start()
idle()
