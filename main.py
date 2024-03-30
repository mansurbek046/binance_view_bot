import logging
from pyrogram import Client, filters
from binance.spot import Spot
import requests
import json

api_id='20619129'
api_hash='b4edb93608b3fc73cfa412ce538d4882'

bot_token='7074408130:AAHrKKZend7i3PUBjI3sr2bW4iVPDZvFJ18'

app=Client('binance_view_bot',api_hash=api_hash,api_id=api_id,bot_token=bot_token)
spot=Spot()

@app.on_message(filters.command('start'))
async def start(client,message):
  await client.send_message(chat_id=message.chat.id,text="Send me coin name..")

@app.on_message()
async def handler(client,message):
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
        
        symbol=data['symbol']
        price = data['lastPrice']
        change_percentage = data['priceChangePercent']
        high_price = data['highPrice']
        low_price = data['lowPrice']
        volume = data['volume']
        
        gift_text=f"{symbol} Market\n\n💰 Price: {price:,.2f}\n🫰 24H Change: {change_percentage:.2}%\n⬆ High: {high_price:,.2f}\n⬇️ Low: {low_price:,.2f}\n📊 24H Volume: {volume:,.2f}"

      await client.send_message(chat_id=message.chat.id,text=gift_text)


if __name__=="__main__":
  app.run()



