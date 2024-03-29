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
      coin_info=spot.get_symbol_ticker(symbol=currency)
      
      price = coin_info['price']
      price_change_percentage = coin_info['priceChangePercent']
      high_price = coin_info['highPrice']
      low_price = coin_info['lowPrice']
      volume = coin_info['volume']
      
      gift_text = f"Price: {price}\n24H Change: {price_change_percentage}%\nHigh: {high_price}\nLow: {low_price}\n24H Vol: {volume}"
      await client.send_message(chat_id=message.chat.id,text=gift_text)


if __name__=="__main__":
  app.run()



