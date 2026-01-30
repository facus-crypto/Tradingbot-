#!/data/data/com.termux/files/usr/bin/bash

cd ~/bot_trading

# Loop infinito - si el bot crashea, se reinicia solo
while true; do
    echo "[$(date)] Iniciando bot..."
    python mi_bot.py
    
    echo "[$(date)] Bot se detuvo. Reiniciando en 10 segundos..."
    sleep 10
done
