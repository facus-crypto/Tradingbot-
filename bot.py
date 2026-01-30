import time
import time

import requests
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator


import os
from binance.client import Client
from dotenv import load_dotenv

# Cargar llaves
load_dotenv()
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_SECRET_KEY')

# Conectar
client = Client(api_key, api_secret)
TOKEN = "8336783544:AAFsyl628ALE9RKTInE60HnOjLHMe6mlbtw"
CHAT_ID = "213736357"

def enviar_alerta(txt):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": txt, "reply_markup": {"inline_keyboard": [[{"text": "✅ EJECUTAR", "callback_data": "exec"}]]}}
    requests.post(url, json=payload)
def analizar(simbolo):
    klines = client.futures_klines(symbol=simbolo, interval='15m', limit=100)
    df = pd.DataFrame(klines, columns=['time','open','high','low','close','vol','ct','qav','nt','tb','tq','i'])
    df['close'] = df['close'].astype(float)
    df['ema9'] = EMAIndicator(df['close'], 9).ema_indicator()
    df['rsi'] = RSIIndicator(df['close'], 14).rsi()
    return df.iloc[-1]
MONEDAS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT', 'LINKUSDT']


try:
    info = client.futures_account_balance()
    print("¡Conexión Exitosa!")
    print("Tu saldo en Futuros es:")
    for asset in info:
        if float(asset['balance']) > 0:
            print(f"{asset['asset']}: {asset['balance']}")
except Exception as e:
    print(f"Error: {e}")

while True:
    for moneda in MONEDAS:
        try:
            dato = analizar(moneda)
            # Condición: Precio > EMA 9 y RSI > 50
            if dato['close'] > dato['ema9'] and dato['rsi'] > 50:
                txt = f"🚀 SEÑAL {moneda}\nPrecio: {dato['close']}\nRSI: {dato['rsi']:.2f}"
                enviar_alerta(txt)
                print(f"Alerta enviada para {moneda}")
        except:
            print(f"Error analizando {moneda}")
    time.sleep(60)


