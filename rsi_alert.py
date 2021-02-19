#!/usr/bin/env python

import argparse
import logging
import os
import platform
from ta.momentum import rsi
import time

import yfinance as yf

BEEP_DURATION = 0.5  # Seconds
BEEP_FREQ = 880  # Hz


def alert():
    sys = platform.system()
    if sys == "Linux":
        os.system(f"play -nq -t alsa synth {BEEP_DURATION} sine {BEEP_FREQ}")
    elif sys == "Windows":
        import winsound

        winsound.Beep(BEEP_FREQ, BEEP_DURATION)


def main():
    parser = argparse.ArgumentParser("RSI Alert")
    parser.add_argument("coins", type=str, nargs="+")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    args = parser.parse_args()

    log_level = (3 - min(args.verbose, 2)) * 10
    logging.basicConfig(level=log_level)
    logging.debug(f"{args=}")

    iteration = 0

    while True:

        iteration += 1
        print(f"\n-- Iteration {iteration} --\n")

        for coin in args.coins:
            updating_message = f"Updating {coin}"
            logging.info(updating_message)
            print(updating_message)

            series = yf.download(
                tickers=f"{coin.upper()}-USD", period="22h", interval="1m"
            )
            logging.debug(f"{series=}")

            closes = series["Close"]
            closes = closes.loc[closes != 0]
            logging.info(f"Series fetched for {coin=}")
            logging.debug(f"{closes=}")

            rsi_series = rsi(closes)
            logging.info(f"Calculated rsi for {coin=}")
            rsi_series = rsi_series.dropna()
            logging.debug(f"{rsi_series=}")
            last_rsi_val = int(rsi_series.iloc[-1])
            logging.info(f"{last_rsi_val=}")

            if last_rsi_val < 30 or last_rsi_val > 70:
                print(f"-- RSI ALERT for {coin}: {last_rsi_val} --\n")
                logging.info(f"RSI value alert for {coin}: {last_rsi_val}")
                alert()

        time.sleep(60)


if __name__ == "__main__":
    main()
