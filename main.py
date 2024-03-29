import logging
from pyrogram import Client, filters
from binance.spot import Spot

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
  if message_text:
    await client.send_message(chat_id=message.chat.id,text=spot.time())
    gift_text=spot.klines(message_text,'1h')
    await client.send_message(chat_id=message.chat.id,text=gift_text)  


if __name__=="__main__":
  app.run()



