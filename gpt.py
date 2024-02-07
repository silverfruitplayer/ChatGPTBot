
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from random import choice
from pyrogram import Client, filters, idle
from aiohttp import ClientSession
from json import loads
from pyrogram.types import Message as message
import asyncio
import openai
from openai import OpenAI

client = OpenAI(api_key="")
import requests
import logging
import os
import uvloop


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

app = Client("gptbot", bot_token="", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")

last_question = ""
follow_up_question = ""

@app.on_message(filters.command("start"))
async def start(_, message):
    global last_question, follow_up_question
    last_question = ""
    follow_up_question = ""
    await message.reply_text(f"Hi {message.from_user.mention}, Ask any question to start over.\nYou can search images too (NSFW content not allowed)")

@app.on_message(filters.regex("^/image"))
async def image_handler(_, message):
    global last_question, follow_up_question
    if message.text:
        generating_message = await message.reply("Generating response for image...")

        message_text = message.text

        while True:
            try:
                response1 = client.images.generate(prompt=f"{message_text}\n",
                n=2,
                size="1024x1024")
                x = response1.data[0].url
                await message.reply_photo(x)
                await generating_message.delete()
                last_question = message_text  # Store the last question
                follow_up_question = ""  # Clear the follow-up question
                break

            except openai.Timeout as e:
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
    global last_question, follow_up_question
    if message.text:
        cmd = ("/")

        fst_word = message.text.strip().split(None, 1)[0]

        if fst_word in cmd:
            return

        generating_message = await message.reply("Generating response...")

        message_text = message.text

        if message_text.lower() == "/cancel":
            last_question = ""  # Clear the last question
            follow_up_question = ""  # Clear the follow-up question
            await message.reply("Follow-up question cancelled. Please ask a new question.")
            return

        if follow_up_question:
            # Use the follow-up question as part of the prompt
            prompt = f"{last_question}\n{follow_up_question}\n{message_text}\n"
            follow_up_question = ""  # Clear the follow-up question
        elif last_question:
            # Ask for a follow-up question
            prompt = f"{last_question}\nWould you like a follow-up answer?\n{message_text}\n"
            follow_up_question = message_text
        else:
            prompt = message_text

        if message_text:
            try:
                response = client.completions.create(engine="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=2048,
                temperature=0.5)
        
        
            except Exception as e:
                print(e)

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
            await message.reply(response.choices[0].text)
            await generating_message.delete()

        last_question = message_text  # Store the current question

async def main():
    # Set uvloop as the event loop policy
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # Start both app.start() and idle() concurrently
    tasks = [app.start(), idle()]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
