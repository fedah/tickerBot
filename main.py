import os
from dotenv import load_dotenv, find_dotenv
import discord
import yfinance as yf
import finviz as fz
from finviz.screener import Screener

client = discord.Client()
commands = """\n```TickerBot - Look up stocks data in Discord : )

- $ticker             :  print bot commands
- $ticker info ABC    :  print price information about ticker ABC
- $ticker chart ABC   :  print ticker ABC technical chart
- $ticker tech ABC    :  print RSI, SMA(20/50/200) and Change for ticker ABC```
"""
no_ticker_warning = "you have to provide a ticker in all caps"


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    msg = message.content
    channel = message.channel
    print("Got the message!")

    if message.author == client.user:
        return

    if msg == "$ticker":
        await channel.send(commands)

    if msg.startswith('$ticker chart'):
        if len(msg.split()) != 3:
            await channel.send("""```fix
            To use the command "$ticker chart" + {no_ticker_warning}```
            """)
        else:
            ticker_symbol = msg.split()[2]
            ticker = None

            try:
                ticker = Screener([ticker_symbol])
            except:
                await channel.send(f"""```fix
                The ticker symbol {ticker_symbol} seems to not exist```
                """)

            if ticker != None:
                ticker.get_charts(period='d', chart_type='c', size='l', ta='1')

                chart = None
                for root, dir, files in os.walk("charts"):
                    for filename in files:
                        if filename.startswith(ticker_symbol):
                            chartPath = os.path.join(root, filename)
                            chart = discord.File(chartPath, filename=filename)
                            break
                
                embed = discord.Embed()
                embed.set_image(url=f"attachment://{chart.filename}")

                data = f"**Ticker {ticker_symbol} - Chart**\n"

                data = f">>> {data}"
                await channel.send(data, file=chart, embed=embed)
                os.remove(chartPath)
            
    if msg.startswith('$ticker info'):
        if len(msg.split()) != 3:
            await channel.send("""```fix
            To use the command "$ticker info" + {no_ticker_warning}```
            """)
        else:
            ticker_symbol = msg.split()[2]
            tickerInfo = None
            
            try:
                ticker = yf.Ticker(ticker_symbol);
                tickerInfo = ticker.info
            except:
                await channel.send(f"""```fix
                The ticker symbol {ticker_symbol} seems to not exist```
                """)

            if tickerInfo != None:
                stats = ["ask", "bid", "currentPrice", "shortRatio"]
                data = f"**Ticker {ticker_symbol} - Info**\n"

                for stat in stats:
                    if stat in tickerInfo.keys():
                        data += f"**{stat}** : {tickerInfo[stat]}\n"

                data = f">>> {data}"
                await channel.send(data)

    if msg.startswith('$ticker tech'):
            if len(msg.split()) != 3:
                await channel.send("""```fix
                To use the command "$ticker tech" + {no_ticker_warning}```
                """)
            else:
                ticker_symbol = msg.split()[2]
                ticker = None

                try:
                    ticker = fz.get_stock(ticker_symbol)
                except:
                    await channel.send(f"""```fix
                    The ticker symbol {ticker_symbol} seems to not exist```
                    """)

                if ticker != None:
                    stats = ["RSI (14)", "SMA20", "SMA50", "SMA200" "Change"]
                    data = f"**Ticker {ticker_symbol} - Technical**\n"

                    for stat in stats:
                        if stat in ticker.keys():
                            data += f"**{stat}** : {ticker[stat]}\n"

                    data = f">>> {data}"
                    await channel.send(data)

    if msg == "$clear":
        async for message in channel.history(limit=200):
            await message.delete()

load_dotenv(find_dotenv())
client.run(os.getenv('TOKEN'))

