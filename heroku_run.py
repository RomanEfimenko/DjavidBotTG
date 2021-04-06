#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from aiogram import Bot, types, md
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
import random
import asyncio
import aiohttp
from PIL import Image, ImageChops, ImageDraw, ImageFont

TOKEN = os.environ.get('TOKEN')
ID_TRENER = os.environ.get('ID_TRENER')

WEBHOOK_HOST = 'https://djavidbot.herokuapp.com/'  # name your app
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
newmemes_count = [0]

def check_admin_id(from__user__id) :
    if from__user__id == ID_TRENER :
        return True
    else :
        return False

def get_array_words(stringii) :
    my_array_w = stringii.split(' ');
    return my_array_w

def get_array_strings(stringii,lenght_odnoj_string,font_fs) :
    my_array_w = stringii.split(' ');
    return_array_strs = [my_array_w[0]]
    i = 1
    row_index = 0
    while i < len(my_array_w) :
        size_new_str_in_pxls = font_fs.getsize(return_array_strs[row_index]+' '+my_array_w[i])
        #print('\nwidth : '+str(size_new_str_in_pxls[0])+'\n')
        if(size_new_str_in_pxls[0] < lenght_odnoj_string) :
            return_array_strs[row_index] = return_array_strs[row_index] + ' ' + my_array_w[i]
        else :
            row_index = row_index + 1
            return_array_strs.append(my_array_w[i])
        i = i + 1
    return return_array_strs

async def create_david_mem(typo_text__citati) :
    newmemes_count[0] = newmemes_count[0] + 1;
    if newmemes_count[0] > 20 :
        newmemes_count[0] = 1
    font = ImageFont.truetype("times.ttf", size=32)
    try:
        my_img = Image.open("img/ava_horiz_270.jpg")
    except:
        print("Unable to load image")
    idraw = ImageDraw.Draw(my_img)
    #text = typo_text__citati
    array_text = get_array_strings(typo_text__citati,520,font)
    visota = 33
    i = 0
    for text_one_stringi in array_text :
         idraw.text((275, 20+(visota*i)), array_text[i], font=font)
         i = i + 1
    my_img_new_name = 'mem'+str(newmemes_count[0])+'.png'
    my_img.save(my_img_new_name)
    return my_img_new_name

async def get_citata() :
    text_citati = ""
    session = aiohttp.ClientSession()
    my_querty_post_ = {'method':'getQuote','key':'457653','format':'json','lang':'ru'}
    async with session.post('http://api.forismatic.com/api/1.0/', data=my_querty_post_) as resp :
        my_json = await resp.json()
        text_citati = my_json['quoteText']
        print(await resp.json())
    await session.close()
    return text_citati

#-- Команди для плєбєїв
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if check_admin_id(message.from_user.id) :
        await bot.send_message(message.from_user.id, "/help\n/debsd\n/testq\n\t\tАхуєнний Код Давінчі")
    else :
        await bot.send_message(message.from_user.id, "Djavid Commands:\n/help\n/mydroch\n/autor")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await bot.send_message(message.chat.id, "/mydroch - форсовано змусити мене сказати шось разумне.\n(c) Djavid")

@dp.message_handler(commands=['autor'])
async def process_help_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Зробив LS. кантакт @romanefimen")

@dp.message_handler(commands=['debsd'])
async def process_debsd_command(message: types.Message):
    if check_admin_id(message.from_user.id) :
        print(str(message))

@dp.message_handler(commands=['testq'])
async def process_testq_command(message: types.Message):
    if check_admin_id(message.from_user.id) :
        lol = await get_citata()
        img_path = await create_david_mem(lol)
        #await bot.send_message(message.chat.id, lol+'\n(c) Джавид')
        await bot.send_photo(message.from_user.id, open(img_path,'rb'))
        #print("Citat\n"+lol+'\n')

@dp.message_handler(commands=['mydroch'])
async def process_mydrost_command(message: types.Message):
    citata_text = await get_citata()
    img_path = await create_david_mem(citata_text)
    await bot.send_photo(message.chat.id, open(img_path,'rb'))

#-- My commands vsyo
'''
@dp.message_handler(commands='start')
async def welcome(message: types.Message):
    await bot.send_message(
        message.chat.id,
        f'Приветствую! Это демонтрационный бот\n'
        f'Подробная информация на '
        f'{md.hlink("github", "https://github.com/deploy-your-bot-everywhere/heroku")}',
        parse_mode=types.ParseMode.HTML,
        disable_web_page_preview=True)
@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)
'''

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.send_message(ID_TRENER, "Я лежу пизда мен1")
    pass

if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=WEBAPP_HOST, port=WEBAPP_PORT)
