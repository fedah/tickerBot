from pprint import PrettyPrinter
import yfinance as yf
import finviz as fz
from finviz.screener import Screener

def try_fz():
    # filters = ['exch_nasd']
    # list = ["AIMD", "NYMX"]
    # stocks = Screener(list)

    msft =  fz.get_stock('ZZZZZZZZ')
    for entry in msft:
        key, value = entry
        print(f'{key} : {value}')
        count +=1 
        if count > 10:
            break

def try_yf():
    ticker_symbol = "MSFT"
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    stats = ["ask", "bid", "preMarketPrice", "shortRatio"]
    data = f"{ticker_symbol}\n"

    for stat in stats:
        data += f"{stat} : {info[stat]}\n"
    print(data)

if __name__ == "__main__":
    # ticker_symbol = "MSFT"
    # ticker = yf.Ticker(ticker_symbol)
    # info = ticker.info
    # print(info.keys())

    try_fz()

