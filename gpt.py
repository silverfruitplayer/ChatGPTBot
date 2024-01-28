import html
from random import choice
from pyrogram import Client, filters, idle, enums
from aiohttp import ClientSession
from httpx import AsyncClient, Timeout
import asyncio
import requests
import logging
import os
import os
#import PIL.Image
from PIL import Image
import google.generativeai as genai

GOOGLEAI_KEY = "" # Please Get From https://makersuite.google.com/app/apikey #

genai.configure(api_key=GOOGLEAI_KEY)


model = genai.GenerativeModel("gemini-pro-vision")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

app = Client("geminiai", bot_token="", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")


#session = ClientSession()
#session.close()
"""
fetch = AsyncClient(
    http2=True,
    verify=False,
    headers={
        "Accept-Language": "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42",
    },
    timeout=Timeout(20),
)
"""
@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(f"Hi {message.from_user.mention}, Ask any question to start over.\nYou can search images too (NSFW content not allowed)")


@app.on_message(filters.sticker | filters.photo)
async def say(_, message):
    try:
        x = await message.reply_text("Please Wait...")

        if message.sticker:
            sticker_path = await app.download_media(message.sticker.file_id)
            image = Image.open(sticker_path)
            jpeg_path = sticker_path.replace(".webp", ".jpeg")
            image.convert("RGB").save(jpeg_path, "JPEG")
            #photo = jpeg_path
            response0 = model.generate_content(jpeg_path)
            await message.reply_photo("jpeg_path")
            await x.edit_text(
                f"**Details Of Sticker You Provided:** {response0.parts[0].text}", parse_mode=enums.ParseMode.MARKDOWN
            )    
            os.remove(sticker_path)
        else:
            if message.photo:
                base_img = await message.download()
                img = Image.open(base_img)
                response = model.generate_content(img)
                await x.edit_text(
                    f"**Details Of Photo You Provided:** {response.parts[0].text}", parse_mode=enums.ParseMode.MARKDOWN
                )
                os.remove(base_img)
    except Exception as e:
        print(e)

@app.on_message(filters.text)
async def gemini_chatbot(_, message):
    if not GOOGLEAI_KEY:
        return await message.reply_text("GOOGLEAI_KEY env is missing!!!")
    msg = await message.reply_text("Wait a moment...")
    try:
        params = {
            'key': GOOGLEAI_KEY,
        }
        json_data = {
            'contents': [
                {
                    'parts': [
                        {
                            'text': message.text,
                        },
                    ],
                },
            ],
        }
        response = requests.post(
            'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
            params=params,
            json=json_data,
            timeout=20.0,
        )
        if not response.json().get("candidates"):
            return await msg.edit_text("Your question contains slang or foul languages that has been blocked for security reasons.")
        await msg.edit_text(
            f"**Your Question was:**\n{message.text}\n\n**Your Answer is:**\n{html.escape(response.json()['candidates'][0]['content']['parts'][0]['text'])}"
        )    
    except Exception as e:
        print(e)
app.start()
idle()
