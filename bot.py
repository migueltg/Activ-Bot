import subprocess
import time
from subprocess import DEVNULL, STDOUT

import pandas as pd
import ta
from binance import Client
from termcolor import colored

# Path to your config
config_live_path = "configs/live/test/live_config.json"

# Wallet Exposure Long | Short
we_long = "1"
we_short = "1"

# Interval to Trade Whatever
interval = "1m"

# EMA
emafast = 50
emamiddle = 100
emaslow = 200

# Limit for EMA 200
limit = 200

timing = 0.01


class Bot_Stoch_RSI_EMA:
    def __init__(self, binance_client, symbol, interval, limit):
        self.binance_client = binance_client
        self.symbol = symbol
        self.interval = interval
        self.limit = limit

    def dfall(self):

        bars = binance_client.get_historical_klines(
            self.symbol, interval=self.interval, limit=self.limit
        )

        df = pd.DataFrame(bars)
        df = df.iloc[:, 0:5]
        df.columns = ["Time", "Open", "High", "Low", "Close"]
        df.set_index("Time", inplace=True)
        df.index = pd.to_datetime(df.index, unit="ms")
        df = df.astype(float)

        df[f"EMA_" + str(emafast)] = ta.trend.ema_indicator(df.Close, window=emafast)
        df[f"EMA_" + str(emamiddle)] = ta.trend.ema_indicator(
            df.Close, window=emamiddle
        )
        df[f"EMA_" + str(emaslow)] = ta.trend.ema_indicator(df.Close, window=emaslow)
        df["stochrsi_k"] = ta.momentum.stochrsi_k(
            df.Close, window=10, smooth1=5, smooth2=5
        )
        df["stochrsi_d"] = ta.momentum.stochrsi_d(
            df.Close, window=10, smooth1=5, smooth2=5
        )
        df.dropna(inplace=True)

        # Long Signal
        df["Buy"] = (
            (df.stochrsi_k <= 0.15)
            & (df.stochrsi_d <= 0.15)
            & (df.stochrsi_k > df.stochrsi_d)
            & (
                # df.Close > df[f'EMA_'+str(emafast)]) #& (
                # df.Close > df[f'EMA_'+str(emamiddle)]) & (
                df.Close
                > df[f"EMA_" + str(emaslow)]
            )
        )  # & (
        # df[f'EMA_'+str(emafast)] > df[f'EMA_'+str(emamiddle)]) & (
        # df[f'EMA_'+str(emafast)] > df[f'EMA_'+str(emaslow)]) & (
        # df[f'EMA_'+str(emamiddle)] > df[f'EMA_'+str(emaslow)]
        # )

        # #Sell Signal
        df["Sell"] = (
            (df.stochrsi_k >= 0.85)
            & (df.stochrsi_d >= 0.85)
            & (df.stochrsi_k < df.stochrsi_d)
            & (
                # df.Close < df[f'EMA_'+str(emafast)]) #& (
                # df.Close < df[f'EMA_'+str(emamiddle)]) & (
                df.Close
                < df[f"EMA_" + str(emaslow)]
            )
        )  # & (
        # df[f'EMA_'+str(emafast)] < df[f'EMA_'+str(emamiddle)]) & (
        # df[f'EMA_'+str(emafast)] < df[f'EMA_'+str(emaslow)]) & (
        # df[f'EMA_'+str(emamiddle)] < df[f'EMA_'+str(emaslow)]
        # )
        pos_dict = {"in_position": False}

        # Start Passivbot
        if df.Buy.values:
            print(colored(f"Started Long on {self.symbol}...", "blue"))
            startlong = subprocess.Popen(
                [
                    "python3",
                    "passivbot.py",
                    "bybit_01",
                    self.symbol,
                    config_live_path,
                    "-lm",
                    "n",
                    "-sm",
                    "gs",
                    "-lw",
                    we_long,
                    "-sw",
                    we_short,
                ],
                stdout=DEVNULL,
                stderr=STDOUT,
            )
            time.sleep(45)
            startlong.kill()
            pos_dict["in_position"] = True

        elif df.Sell.values:
            print(colored(f"Start Short on {self.symbol}...", "red"))
            startshort = subprocess.Popen(
                [
                    "python3",
                    "passivbot.py",
                    "bybit_01",
                    self.symbol,
                    config_live_path,
                    "-lm",
                    "gs",
                    "-sm",
                    "n",
                    "-lw",
                    we_long,
                    "-sw",
                    we_short,
                ],
                stdout=DEVNULL,
                stderr=STDOUT,
            )
            time.sleep(45)
            startshort.kill()
            pos_dict["in_position"] = True

        else:
            print(colored(f"Waiting for entry on {self.symbol}...", "yellow"))
            stopbot = subprocess.Popen(
                [
                    "python3",
                    "passivbot.py",
                    "bybit_01",
                    self.symbol,
                    config_live_path,
                    "-lm",
                    "gs",
                    "-sm",
                    "gs",
                    "-lw",
                    we_long,
                    "-sw",
                    we_short,
                ],
                stdout=DEVNULL,
                stderr=STDOUT,
            )
            time.sleep(45)
            stopbot.kill()
            pos_dict["in_position"] = False

        return df


def read_config():
    import json

    file_api_key = open("api-key.json")
    api_key_config = json.load(file_api_key)
    file_api_key.close()
    file_config = open("config.json")
    symbols_config = json.load(file_config)
    file_config.close()
    return api_key_config, symbols_config


api_key_config, symbols_config = read_config()
binance_client = Client(
    api_key=api_key_config["binance_api_key"],
    api_secret=api_key_config["binance_api_secret"],
)

while True:
    for symbol in symbols_config["symbols"]:
        bot = Bot_Stoch_RSI_EMA(
            binance_client, symbol["symbol"], symbol["interval"], symbol["limit"]
        )
        bot.dfall()
        time.sleep(timing)
