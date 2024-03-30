import logging
from pyrogram import Client, filters
from binance.spot import Spot
import requests
import json
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from pyrogram.errors import UserNotParticipant

api_id='20619129'
api_hash='b4edb93608b3fc73cfa412ce538d4882'

bot_token='7074408130:AAHrKKZend7i3PUBjI3sr2bW4iVPDZvFJ18'

app=Client('binance_view_bot',api_hash=api_hash,api_id=api_id,bot_token=bot_token)
spot=Spot()

CHANNEL_ID=-1002143083883

@app.on_message(filters.command('start'))
async def start(client,message):
  try:
    member=await client.get_chat_member(CHANNEL_ID, message.from_user.id)
    if not member.status in ["member", "administrator"]:
      await message.reply_text("Please join our channel and /start again to use bot.")
    else:
      await client.send_message(chat_id=message.chat.id,text="Send me coin name..")
  except UserNotParticipant:
    await message.reply_text("Please join our channel and /start again to use bot.")


@app.on_message()
async def handler(client,message):
  try:
    member=await client.get_chat_member(CHANNEL_ID, message.from_user.id)
    print(member)
    if not member.status!="ChatMemberStatus.MEMBER":
      await message.reply_text("Please join our channel and /start again to use bot.")
    else:
      message_text=message.text
      gift_text=""
      if message_text:
        # await client.send_message(chat_id=message.chat.id,text=spot.time())
        message_text=message_text.split()
        if message_text[0]:
          currency=message_text[0].upper()
          if not currency.endswith('USDT'):
            currency+='USDT'
          
          if len(message_text)>=2:
            timeframe=message_text[1]
          else:
            timeframe='1h'
          
          # gift_text=spot.klines(currency,timeframe)
          
          url = f'https://api.binance.com/api/v3/ticker/24hr?symbol={currency}'
    
          res=requests.get(url)
          if res.status_code==200:
            data=res.json()
            # gift_text=json.dumps(data, indent=2)
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
    
            gift_text = f"{symbol} Market\n\n💰 Price: {price:,.2f}\n{status_icon} 24H Change: {change_percentage:.2f}%\n⬆ High: {high_price:,.2f}\n⬇️ Low: {low_price:,.2f}\n📊 24H Volume: {volume:,.2f}"
    
            reply_markup=InlineKeyboardMarkup([[
              InlineKeyboardButton("💰 Binance", web_app=WebAppInfo(url=f"https://www.binance.com/en/trade/{currency}")),
              InlineKeyboardButton("TradingView 📊", web_app=WebAppInfo(url=f"https://www.tradingview.com/symbols/{currency}"))
              ]])
    
            await client.send_message(chat_id=message.chat.id,text=gift_text,reply_markup=reply_markup)

  except UserNotParticipant:
    await message.reply_text("Please join our channel and /start again to use bot.")

if __name__=="__main__":
  app.run()


