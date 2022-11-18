from curses import window
import pandas as pd
import ta
from binance import Client
from datetime import date, datetime, timedelta, date
import time
import numpy as np
import subprocess
import config
from tradingview_ta import TA_Handler, Interval, Exchange 
from subprocess import DEVNULL, STDOUT
from termcolor import colored

# Symbol Whatever
symbol = 'ADAUSDT'

# Path to your config
configs = 'configs/live/test/4.json'

# Wallet Exposure Long | Short
we_long = '1'                           
we_short = '1'

# Interval to Trade Whatever
interval = '1m'

# EMA
emafast = 50
emamiddle = 100
emaslow = 200

# Limit for EMA 200
limit = 200


class Bot_Stoch_RSI_EMA():

    def __init__(self, symbol, interval, limit):
        self.symbol = symbol
        self.interval = interval
        self.limit = limit

    def dfall(self, symbol, interval, limit):
        client = Client(
            api_key = config.API_KEY,
            api_secret = config.SECRET_KEY)
        
        bars = client.get_historical_klines(symbol, interval=interval, limit=limit)

        df = pd.DataFrame(bars) 
        df = df.iloc[:,0:5]
        df.columns = ['Time','Open','High','Low','Close']
        df.set_index('Time', inplace=True)
        df.index = pd.to_datetime(df.index, unit='ms')
        df = df.astype(float)

        df[f'EMA_'+str(emafast)] = ta.trend.ema_indicator(df.Close, window=emafast)
        df[f'EMA_'+str(emamiddle)] = ta.trend.ema_indicator(df.Close, window=emamiddle)
        df[f'EMA_'+str(emaslow)] = ta.trend.ema_indicator(df.Close, window=emaslow)
        df['stochrsi_k'] = ta.momentum.stochrsi_k(df.Close, window=10, smooth1=5, smooth2=5)
        df['stochrsi_d'] = ta.momentum.stochrsi_d(df.Close, window=10, smooth1=5, smooth2=5)
        df.dropna(inplace=True)

        #Long Signal
        df['Buy'] = (
        df.stochrsi_k <= 0.15) & (
        df.stochrsi_d <= 0.15) & (
        df.stochrsi_k > df.stochrsi_d) & (
        # df.Close > df[f'EMA_'+str(emafast)]) #& (
        # df.Close > df[f'EMA_'+str(emamiddle)]) & (
        df.Close > df[f'EMA_'+str(emaslow)]) # & (
        # df[f'EMA_'+str(emafast)] > df[f'EMA_'+str(emamiddle)]) & (
        # df[f'EMA_'+str(emafast)] > df[f'EMA_'+str(emaslow)]) & (
        # df[f'EMA_'+str(emamiddle)] > df[f'EMA_'+str(emaslow)]
        # )

        # #Sell Signal
        df['Sell'] = (
        df.stochrsi_k >= 0.85) & (
        df.stochrsi_d >= 0.85) & (
        df.stochrsi_k < df.stochrsi_d) & (
        # df.Close < df[f'EMA_'+str(emafast)]) #& (
        # df.Close < df[f'EMA_'+str(emamiddle)]) & (
        df.Close < df[f'EMA_'+str(emaslow)]) # & (
        # df[f'EMA_'+str(emafast)] < df[f'EMA_'+str(emamiddle)]) & (
        # df[f'EMA_'+str(emafast)] < df[f'EMA_'+str(emaslow)]) & (
        # df[f'EMA_'+str(emamiddle)] < df[f'EMA_'+str(emaslow)]
        # )
        pos_dict = {'in_position':False}

        # Start Passivbot
        if df.Buy.values:
            print(colored(f'Started Long on {self.symbol}...', 'blue'))
            startlong =  subprocess.Popen(['python3', 'passivbot.py', 'bybit_01', self.symbol, configs, '-lm', 'n', '-sm', 'gs', '-lw', we_long, '-sw', we_short], stdout=DEVNULL, stderr=STDOUT)
            time.sleep(45)
            startlong.kill()
            pos_dict['in_position'] = True

        elif df.Sell.values:
            print(colored(f'Start Short on {self.symbol}...', 'red'))
            startshort =  subprocess.Popen(['python3', 'passivbot.py', 'bybit_01', self.symbol, configs, '-lm', 'gs', '-sm', 'n', '-lw', we_long, '-sw', we_short], stdout=DEVNULL, stderr=STDOUT)
            time.sleep(45)
            startshort.kill()
            pos_dict['in_position'] = True

        else:
            print(colored(f'Waiting for entry on {self.symbol}...', 'yellow'))
            stopbot =  subprocess.Popen(['python3', 'passivbot.py', 'bybit_01', self.symbol, configs, '-lm', 'gs', '-sm', 'gs', '-lw', we_long, '-sw', we_short], stdout=DEVNULL, stderr=STDOUT)
            time.sleep(45)
            stopbot.kill()
            pos_dict['in_position'] = False

        return(df)


# UNCOMMENT TO TRADE

bot1 = Bot_Stoch_RSI_EMA('ADAUSDT','15m', 200)
# bot2 = Bot_Stoch_RSI_EMA('ALGOUSDT','15m', 200)
# bot3 = Bot_Stoch_RSI_EMA('ANKRUSDT','15m', 200)
# bot4 = Bot_Stoch_RSI_EMA('APTUSDT','15m', 200)
# bot5 = Bot_Stoch_RSI_EMA('ARUSDT','15m', 200)
# bot6 = Bot_Stoch_RSI_EMA('ATAUSDT','15m', 200)
# bot7 = Bot_Stoch_RSI_EMA('ATOMUSDT','15m', 200)
# bot8 = Bot_Stoch_RSI_EMA('AUDIOUSDT','15m', 200)
bot9 = Bot_Stoch_RSI_EMA('AVAXUSDT','15m', 200)
# bot10 = Bot_Stoch_RSI_EMA('AXSUSDT','15m', 200)
# bot11 = Bot_Stoch_RSI_EMA('BAKEUSDT','15m', 200)
# bot12 = Bot_Stoch_RSI_EMA('BANDUSDT','15m', 200)
# bot13 = Bot_Stoch_RSI_EMA('BATUSDT','15m', 200)
# bot14 = Bot_Stoch_RSI_EMA('BCHUSDT','15m', 200)
# bot15 = Bot_Stoch_RSI_EMA('BELUSDT','15m', 200)
# bot16 = Bot_Stoch_RSI_EMA('BLZUSDT','15m', 200)
# bot17 = Bot_Stoch_RSI_EMA('BNBUSDT','15m', 200)
# bot18 = Bot_Stoch_RSI_EMA('C98USDT','15m', 200)
# bot19 = Bot_Stoch_RSI_EMA('CELOUSDT','15m', 200)
# bot20 = Bot_Stoch_RSI_EMA('CELRUSDT','15m', 200)
# bot21 = Bot_Stoch_RSI_EMA('CHRUSDT','15m', 200)
bot22 = Bot_Stoch_RSI_EMA('CHZUSDT','15m', 200)
# bot23 = Bot_Stoch_RSI_EMA('COMPUSDT','15m', 200)
# bot24 = Bot_Stoch_RSI_EMA('COTIUSDT','15m', 200)
# bot25 = Bot_Stoch_RSI_EMA('CRVUSDT','15m', 200)
# bot26 = Bot_Stoch_RSI_EMA('CTKUSDT','15m', 200)
# bot27 = Bot_Stoch_RSI_EMA('CVCUSDT','15m', 200)
# bot28 = Bot_Stoch_RSI_EMA('DASHUSDT','15m', 200)
# bot29 = Bot_Stoch_RSI_EMA('DENTUSDT','15m', 200)
# bot30 = Bot_Stoch_RSI_EMA('DGBUSDT','15m', 200)
bot31 = Bot_Stoch_RSI_EMA('DOGEUSDT','15m', 200)
# bot32 = Bot_Stoch_RSI_EMA('DOTUSDT','15m', 200)
# bot33 = Bot_Stoch_RSI_EMA('DYDXUSDT','15m', 200)
# bot34 = Bot_Stoch_RSI_EMA('EGLDUSDT','15m', 200)
# bot35 = Bot_Stoch_RSI_EMA('ENJUSDT','15m', 200)
# bot36 = Bot_Stoch_RSI_EMA('EOSUSDT','15m', 200)
# bot37 = Bot_Stoch_RSI_EMA('ETCUSDT','15m', 200)
# bot38 = Bot_Stoch_RSI_EMA('FILUSDT','15m', 200)
# bot39 = Bot_Stoch_RSI_EMA('FLMUSDT','15m', 200)
# bot40 = Bot_Stoch_RSI_EMA('FTMUSDT','15m', 200)
# bot41 = Bot_Stoch_RSI_EMA('GALAUSDT','15m', 200)
# bot42 = Bot_Stoch_RSI_EMA('GRTUSDT','15m', 200)
# bot43 = Bot_Stoch_RSI_EMA('GTCUSDT','15m', 200)
# bot44 = Bot_Stoch_RSI_EMA('HBARUSDT','15m', 200)
# bot45 = Bot_Stoch_RSI_EMA('ICXUSDT','15m', 200)
# bot46 = Bot_Stoch_RSI_EMA('IOSTUSDT','15m', 200)
# bot47 = Bot_Stoch_RSI_EMA('IOTAUSDT','15m', 200)
# bot48 = Bot_Stoch_RSI_EMA('IOTXUSDT','15m', 200)
# bot49 = Bot_Stoch_RSI_EMA('KAVAUSDT','15m', 200)
# bot50 = Bot_Stoch_RSI_EMA('KLAYUSDT','15m', 200)
# bot51 = Bot_Stoch_RSI_EMA('KSMUSDT','15m', 200)
# bot52 = Bot_Stoch_RSI_EMA('LINAUSDT','15m', 200)
bot53 = Bot_Stoch_RSI_EMA('LINKUSDT','15m', 200)
# bot54 = Bot_Stoch_RSI_EMA('LITUSDT','15m', 200)
# bot55 = Bot_Stoch_RSI_EMA('LRCUSDT','15m', 200)
# bot56 = Bot_Stoch_RSI_EMA('LTCUSDT','15m', 200)
# bot57 = Bot_Stoch_RSI_EMA('MANAUSDT','15m', 200)
bot58 = Bot_Stoch_RSI_EMA('MASKUSDT','15m', 200)
bot59 = Bot_Stoch_RSI_EMA('MATICUSDT','15m', 200)
# bot60 = Bot_Stoch_RSI_EMA('MKRUSDT','15m', 200)
# bot61 = Bot_Stoch_RSI_EMA('MTLUSDT','15m', 200)
# bot62 = Bot_Stoch_RSI_EMA('NEARUSDT','15m', 200)
# bot63 = Bot_Stoch_RSI_EMA('NEOUSDT','15m', 200)
# bot64 = Bot_Stoch_RSI_EMA('NKNUSDT','15m', 200)
# bot65 = Bot_Stoch_RSI_EMA('OCEANUSDT','15m', 200)
# bot66 = Bot_Stoch_RSI_EMA('ONEUSDT','15m', 200)
# bot67 = Bot_Stoch_RSI_EMA('ONTUSDT','15m', 200)
# bot68 = Bot_Stoch_RSI_EMA('QTUMUSDT','15m', 200)
# bot69 = Bot_Stoch_RSI_EMA('RAYUSDT','15m', 200)
# bot70 = Bot_Stoch_RSI_EMA('REEFUSDT','15m', 200)
# bot71 = Bot_Stoch_RSI_EMA('RENUSDT','15m', 200)
# bot72 = Bot_Stoch_RSI_EMA('RLCUSDT','15m', 200)
# bot73 = Bot_Stoch_RSI_EMA('RSRUSDT','15m', 200)
# bot74 = Bot_Stoch_RSI_EMA('RUNEUSDT','15m', 200)
# bot75 = Bot_Stoch_RSI_EMA('RVNUSDT','15m', 200)
# bot76 = Bot_Stoch_RSI_EMA('SFPUSDT','15m', 200)
# bot77 = Bot_Stoch_RSI_EMA('SKLUSDT','15m', 200)
# bot78 = Bot_Stoch_RSI_EMA('SNXUSDT','15m', 200)
# bot79 = Bot_Stoch_RSI_EMA('SOLUSDT','15m', 200)
# bot80 = Bot_Stoch_RSI_EMA('SRMUSDT','15m', 200)
# bot81 = Bot_Stoch_RSI_EMA('STMXUSDT','15m', 200)
# bot82 = Bot_Stoch_RSI_EMA('SUSHIUSDT','15m', 200)
# bot83 = Bot_Stoch_RSI_EMA('SXPUSDT','15m', 200)
# bot84 = Bot_Stoch_RSI_EMA('THETAUSDT','15m', 200)
# bot85 = Bot_Stoch_RSI_EMA('TOMOUSDT','15m', 200)
# bot86 = Bot_Stoch_RSI_EMA('TRBUSDT','15m', 200)
# bot87 = Bot_Stoch_RSI_EMA('TRXUSDT','15m', 200)
# bot88 = Bot_Stoch_RSI_EMA('UNIUSDT','15m', 200)
# bot89 = Bot_Stoch_RSI_EMA('WAVESUSDT','15m', 200)
# bot90 = Bot_Stoch_RSI_EMA('XEMUSDT','15m', 200)
# bot91 = Bot_Stoch_RSI_EMA('XLMUSDT','15m', 200)
# bot92 = Bot_Stoch_RSI_EMA('XMRUSDT','15m', 200)
bot93 = Bot_Stoch_RSI_EMA('XRPUSDT','15m', 200)
# bot94 = Bot_Stoch_RSI_EMA('XTZUSDT','15m', 200)
# bot95 = Bot_Stoch_RSI_EMA('ZILUSDT','15m', 200)
# bot96 = Bot_Stoch_RSI_EMA('ZRXUSDT','15m', 200)

timing = 0.01


# UNCOMMENT TO TRADE

while True:
    bot1.dfall('ADAUSDT', '15m', 200)
    time.sleep(timing)
    # bot2.dfall('ALGOUSDT', '15m', 200)
    # time.sleep(timing)
    # bot3.dfall('ANKRUSDT', '15m', 200)
    # time.sleep(timing)
    # bot4.dfall('APTUSDT', '15m', 200)
    # time.sleep(timing)
    # bot5.dfall('ARUSDT', '15m', 200)
    # time.sleep(timing)
    # bot6.dfall('ATAUSDT', '15m', 200)
    # time.sleep(timing)
    # bot7.dfall('ATOMUSDT', '15m', 200)
    # time.sleep(timing)
    # bot8.dfall('AUDIOUSDT', '15m', 200)
    # time.sleep(timing)
    bot9.dfall('AVAXUSDT', '15m', 200)
    time.sleep(timing)
    # bot10.dfall('AXSUSDT', '15m', 200)
    # time.sleep(timing)
    # bot11.dfall('BAKEUSDT', '15m', 200)
    # time.sleep(timing)
    # bot12.dfall('BANDUSDT', '15m', 200)
    # time.sleep(timing)
    # bot13.dfall('BATUSDT', '15m', 200)
    # time.sleep(timing)
    # bot14.dfall('BCHUSDT', '15m', 200)
    # time.sleep(timing)
    # bot15.dfall('BELUSDT', '15m', 200)
    # time.sleep(timing)
    # bot16.dfall('BLZUSDT', '15m', 200)
    # time.sleep(timing)
    # bot17.dfall('BNBUSDT', '15m', 200)
    # time.sleep(timing)
    # bot18.dfall('C98USDT', '15m', 200)
    # time.sleep(timing)
    # bot19.dfall('CELOUSDT', '15m', 200)
    # time.sleep(timing)
    # bot20.dfall('CELRUSDT', '15m', 200)
    # time.sleep(timing)
    # bot21.dfall('CHRUSDT', '15m', 200)
    # time.sleep(timing)
    bot22.dfall('CHZUSDT', '15m', 200)
    time.sleep(timing)
    # bot23.dfall('COMPUSDT', '15m', 200)
    # time.sleep(timing)
    # bot24.dfall('COTIUSDT', '15m', 200)
    # time.sleep(timing)
    # bot25.dfall('CRVUSDT', '15m', 200)
    # time.sleep(timing)
    # bot26.dfall('CTKUSDT', '15m', 200)
    # time.sleep(timing)
    # bot27.dfall('CVCUSDT', '15m', 200)
    # time.sleep(timing)
    # bot28.dfall('DASHUSDT', '15m', 200)
    # time.sleep(timing)
    # bot29.dfall('DENTUSDT', '15m', 200)
    # time.sleep(timing)
    # bot30.dfall('DGBUSDT', '15m', 200)
    # time.sleep(timing)
    bot31.dfall('DOGEUSDT', '15m', 200)
    time.sleep(timing)
    # bot32.dfall('DOTUSDT', '15m', 200)
    # time.sleep(timing)
    # bot33.dfall('DYDXUSDT', '15m', 200)
    # time.sleep(timing)
    # bot34.dfall('EGLDUSDT', '15m', 200)
    # time.sleep(timing)
    # bot35.dfall('ENJUSDT', '15m', 200)
    # time.sleep(timing)
    # bot36.dfall('EOSUSDT', '15m', 200)
    # time.sleep(timing)
    # bot37.dfall('ETCUSDT', '15m', 200)
    # time.sleep(timing)
    # bot38.dfall('FILUSDT', '15m', 200)
    # time.sleep(timing)
    # bot39.dfall('FLMUSDT', '15m', 200)
    # time.sleep(timing)
    # bot40.dfall('FTMUSDT', '15m', 200)
    # time.sleep(timing)
    # bot41.dfall('GALAUSDT', '15m', 200)
    # time.sleep(timing)
    # bot42.dfall('GRTUSDT', '15m', 200)
    # time.sleep(timing)
    # bot43.dfall('GTCUSDT', '15m', 200)
    # time.sleep(timing)
    # bot44.dfall('HBARUSDT', '15m', 200)
    # time.sleep(timing)
    # bot45.dfall('ICXUSDT', '15m', 200)
    # time.sleep(timing)
    # bot46.dfall('IOSTUSDT', '15m', 200)
    # time.sleep(timing)
    # bot47.dfall('IOTAUSDT', '15m', 200)
    # time.sleep(timing)
    # bot48.dfall('IOTXUSDT', '15m', 200)
    # time.sleep(timing)
    # bot49.dfall('KAVAUSDT', '15m', 200)
    # time.sleep(timing)
    # bot50.dfall('KLAYUSDT', '15m', 200)
    # time.sleep(timing)
    # bot51.dfall('KSMUSDT', '15m', 200)
    # time.sleep(timing)
    # bot52.dfall('LINAUSDT', '15m', 200)
    # time.sleep(timing)
    bot53.dfall('LINKUSDT', '15m', 200)
    time.sleep(timing)
    # bot54.dfall('LITUSDT', '15m', 200)
    # time.sleep(timing)
    # bot55.dfall('LRCUSDT', '15m', 200)
    # time.sleep(timing)
    # bot56.dfall('LTCUSDT', '15m', 200)
    # time.sleep(timing)
    # bot57.dfall('MANAUSDT', '15m', 200)
    # time.sleep(timing)
    bot58.dfall('MASKUSDT', '15m', 200)
    time.sleep(timing)
    bot59.dfall('MATICUSDT', '15m', 200)
    time.sleep(timing)
    # bot60.dfall('MKRUSDT', '15m', 200)
    # time.sleep(timing)
    # bot61.dfall('MTLUSDT', '15m', 200)
    # time.sleep(timing)
    # bot62.dfall('NEARUSDT', '15m', 200)
    # time.sleep(timing)
    # bot63.dfall('NEOUSDT', '15m', 200)
    # time.sleep(timing)
    # bot64.dfall('NKNUSDT', '15m', 200)
    # time.sleep(timing)
    # bot65.dfall('OCEANUSDT', '15m', 200)
    # time.sleep(timing)
    # bot66.dfall('ONEUSDT', '15m', 200)
    # time.sleep(timing)
    # bot67.dfall('ONTUSDT', '15m', 200)
    # time.sleep(timing)
    # bot68.dfall('QTUMUSDT', '15m', 200)
    # time.sleep(timing)
    # bot69.dfall('RAYUSDT', '15m', 200)
    # time.sleep(timing)
    # bot70.dfall('REEFUSDT', '15m', 200)
    # time.sleep(timing)
    # bot71.dfall('RENUSDT', '15m', 200)
    # time.sleep(timing)
    # bot72.dfall('RLCUSDT', '15m', 200)
    # time.sleep(timing)
    # bot73.dfall('RSRUSDT', '15m', 200)
    # time.sleep(timing)
    # bot74.dfall('RUNEUSDT', '15m', 200)
    # time.sleep(timing)
    # bot75.dfall('RVNUSDT', '15m', 200)
    # time.sleep(timing)
    # bot76.dfall('SFPUSDT', '15m', 200)
    # time.sleep(timing)
    # bot77.dfall('SKLUSDT', '15m', 200)
    # time.sleep(timing)
    # bot78.dfall('SNXUSDT', '15m', 200)
    # time.sleep(timing)
    # bot79.dfall('SOLUSDT', '15m', 200)
    # time.sleep(timing)
    # bot80.dfall('SRMUSDT', '15m', 200)
    # time.sleep(timing)
    # bot81.dfall('STMXUSDT', '15m', 200)
    # time.sleep(timing)
    # bot82.dfall('SUSHIUSDT', '15m', 200)
    # time.sleep(timing)
    # bot83.dfall('SXPUSDT', '15m', 200)
    # time.sleep(timing)
    # bot84.dfall('THETAUSDT', '15m', 200)
    # time.sleep(timing)
    # bot85.dfall('TOMOUSDT', '15m', 200)
    # time.sleep(timing)
    # bot86.dfall('TRBUSDT', '15m', 200)
    # time.sleep(timing)
    # bot87.dfall('TRXUSDT', '15m', 200)
    # time.sleep(timing)
    # bot88.dfall('UNIUSDT', '15m', 200)
    # time.sleep(timing)
    # bot89.dfall('WAVESUSDT', '15m', 200)
    # time.sleep(timing)
    # bot90.dfall('XEMUSDT', '15m', 200)
    # time.sleep(timing)
    # bot91.dfall('XLMUSDT', '15m', 200)
    # time.sleep(timing)
    # bot92.dfall('XMRUSDT', '15m', 200)
    # time.sleep(timing)
    bot93.dfall('XRPUSDT', '15m', 200)
    time.sleep(timing)
    # bot94.dfall('XTZUSDT', '15m', 200)
    # time.sleep(timing)
    # bot95.dfall('ZILUSDT', '15m', 200)
    # time.sleep(timing)
    # bot96.dfall('ZRXUSDT', '15m', 200)
    # time.sleep(timing)
