import logging
from pyrogram import Client, filters
from binance.spot import Spot
import requests
import json
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from pyrogram.errors import UserNotParticipant
import asyncio
from datetime import datetime, timedelta
import random

#const vars
api_id='20619129'
api_hash='b4edb93608b3fc73cfa412ce538d4882'
bot_token='7074408130:AAHrKKZend7i3PUBjI3sr2bW4iVPDZvFJ18'
CHANNEL_ID=-1002143083883
owner=6045995371

#main
app=Client('binance_view_bot',api_hash=api_hash,api_id=api_id,bot_token=bot_token)
spot=Spot()

#repetatives
nonadmin="<b>🙅 Permission denied!</b>"

#functions
def get_date(days_to_add):
    current_date = datetime.now()
    future_date = current_date + timedelta(days=days_to_add)
    future_date_str = future_date.strftime('%d.%m.%Y')
    return future_date_str

async def price_alert(symbol, type_, price, chat_id, client):
  await client.send_message(chat_id=chat_id, text=f"✅ <b>Alert added</b>:\n{symbol.upper()} {price} USDT {get_add()}")
  while True:
    
    if not symbol.endswith('USDT'):
      symbol+='USDT'
    
    price=float(str(price).replace(',',''))
    type_=type_.lower()
    
    url=f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    
    res=requests.get(url)
    
    if res.status_code==200:
      data=res.json()
      
      if type_=="long" and float(data["price"])>=price:
        await client.send_message(chat_id=chat_id, text=f"<b>⚠ Alert</b>\n{data['symbol']}: {float(data['price']):,.2f} {get_add()}")
        break
      if type_=="short" and float(data["price"])<=price:
        await client.send_message(chat_id=chat_id, text=f"<b>⚠ Alert</b>\n{data['symbol']}: {float(data['price']):,.2f} {get_add()}")
        break
      if type_=="" and float(data["price"])==price:
        await client.send_message(chat_id=chat_id, text=f"<b>⚠ Alert</b>\n{data['symbol']}: {float(data['price']):,.2f} {get_add()}")
        break

    await asyncio.sleep(20)

def add_ad(user_id,view_count,ad_content,link="@test123"):
  with open("ads.json", "w+") as file:
    file.seek(0)
    data=json.load(file)
    ad={
      "user_id":user_id,
      "view_count":view_count,
      "ad_content":ad_content,
      "link":link
    }
    data[len(data)+1]=ad
    if data:
      json.dump(data, file)
    else:
      json.dump({}, file)

def rm_ad(channel):
  with open("ads.json", "w+") as file:
    file.seek(0)
    my_obj=json.load(file)
    field_to_check = "link"
    value_to_check = channel
    for key, inner_obj in list(my_obj.items()):  # Using list() to create a snapshot for modification
        if field_to_check in inner_obj and inner_obj[field_to_check] == value_to_check:
            del my_obj[key]
    if my_obj:
      json.dump(my_obj, file)
    else:
      json.dump({}, file)
    return True
  return False

def get_add():
  ad_text={}
  with open("ads.json", "w+") as file:
      file.seek(0)
      data=json.load(file)
      key=random.choice(data.keys())
      ad_obj=data[key]
      ad_text=f"\n\n<pre>{ad_obj['ad_content']}</pre>\n{ad_obj['link']}"
      data[key]["view_count"]=int(data[key]["view_count"])-1
      if data:
        json.dump(data, file)
      else:
        json.dump({}, file)

  return ad_text

def list_ads():
  list_ads_text=""
  count=0
  with open("ads.json", "r") as file:
        data=json.load(file)
        for key, value in data.items():
          link=value["link"]
          if link.startswith("@") or link.startswith("t.me/"):
            list_ads_text+=link+"\n"
            count+=1
  return f"{list_ads_text}\nChannel count: {count}"

#on_message
@app.on_message(filters.command('start'))
async def start(client,message):
  try:
    member=await client.get_chat_member(CHANNEL_ID, message.from_user.id)
    if not member.status!="ChatMemberStatus.MEMBER":
      await message.reply_text("Please join our channel and /start again to use bot.")
    else:
      await client.send_message(chat_id=message.chat.id,text="Send me coin name..")
  except UserNotParticipant:
    await message.reply_text("Please join our channel and /start again to use bot.")

@app.on_message(filters.command('alert'))
async def set_alert(client,message):
  message_text=message.text.split(' ')
  if len(message_text)==4:
    asyncio.create_task(price_alert(message_text[1].upper(),message_text[2],message_text[3],message.chat.id,client))
  else:
    await client.send_message(chat_id=message.chat.id,text="❌ Wrong using! {get_add()}")

@app.on_message(filters.command('ad'))
async def ad(client,message):
  if message.from_user.id==owner:
    message_text=message.text.split("@#$")
    
    add_ad(message_text[0],message_text[1],message_text[2],message_text[3])
    await client.send_message(chat_id=message.chat.id, text="✅ Ad added!")
  else:
    await client.send_message(chat_id=message.chat.id, text=f"{nonadmin}{get_add()}")

@app.on_message(filters.command('rm'))
async def ad(client,message):
  if message.from_user.id==owner:
    message_text=message.text.split(" ")
    rm=rm_ad(message_text[1])
    if rm:
      await client.send_message(chat_id=message.chat.id,text="✅ Ad deleted!")
  else:
    await client.send_message(chat_id=message.chat.id, text=f"{nonadmin}{get_add()}")

@app.on_message(filters.command('ads'))
async def ad(client,message):
  if message.from_user.id==owner:
    await client.send_message(chat_id=message.chat.id,text=list_ads())
  else:
    await client.send_message(chat_id=message.chat.id, text=f"{nonadmin}{get_add()}")

@app.on_message()
async def handler(client,message):
  try:
    member=await client.get_chat_member(CHANNEL_ID, message.from_user.id)
    
    if not member.status!="ChatMemberStatus.MEMBER":
      await message.reply_text("Please join our channel and /start again to use bot.")
    else:
      message_text=message.text
      gift_text=""
      if message_text:
        message_text=message_text.split()
        if message_text[0]:
          currency=message_text[0].upper()
          if not currency.endswith('USDT'):
            currency+='USDT'
          
          if len(message_text)>=2:
            timeframe=message_text[1]
          else:
            timeframe='1h'

          url = f'https://api.binance.com/api/v3/ticker/24hr?symbol={currency}'
    
          res=requests.get(url)
          if res.status_code==200:
            data=res.json()
            up="📈"
            down="📉"
        
            symbol = data['symbol']
            price = float(data['lastPrice'])
            change_percentage = float(data['priceChangePercent'])
            high_price = float(data['highPrice'])
            low_price = float(data['lowPrice'])
            volume = float(data['volume'])
            
            status_icon=up
            if change_percentage<0:
              status_icon=down
    
            gift_text = f"<b>{symbol} Market\n\n💰 Price: {price:,.2f}\n{status_icon} 24H Change: {change_percentage:.2f}%\n⬆ High: {high_price:,.2f}\n⬇️ Low: {low_price:,.2f}\n📊 24H Volume: {volume:,.2f}</b>"

            reply_markup=InlineKeyboardMarkup([[
              InlineKeyboardButton("💰 Binance", web_app=WebAppInfo(url=f"https://www.binance.com/en/trade/{currency}")),
              InlineKeyboardButton("TradingView 📊", web_app=WebAppInfo(url=f"https://www.tradingview.com/symbols/{currency}"))
              ]])
    
            await client.send_message(chat_id=message.chat.id,text=gift_text+get_add(),reply_markup=reply_markup)

  except UserNotParticipant:
    await message.reply_text("Please join our channel and /start again to use bot.")

if __name__=="__main__":
  app.run()
