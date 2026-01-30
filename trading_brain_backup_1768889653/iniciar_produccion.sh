#!/bin/bash
# Script para iniciar sistema de trading en producción

echo "🚀 INICIANDO SISTEMA DE TRADING INSTITUCIONAL"
echo "=========================================="

# Verificar que estamos en el directorio correcto
if [ ! -f "config.py" ]; then
    echo "❌ Error: No se encuentra config.py"
    echo "   Ejecuta desde: trading_brain/"
    exit 1
fi

# Verificar Python y dependencias
echo "📦 Verificando dependencias..."
python3 -c "import telegram, requests, pandas, numpy, ta" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Algunas dependencias faltan"
    echo "   Ejecuta: pip3 install python-telegram-bot pandas numpy ta requests"
fi

# Crear directorio de logs si no existe
mkdir -p logs

# Fecha y hora de inicio
FECHA=$(date +"%Y-%m-%d_%H-%M-%S")
LOG_FILE="logs/trading_$FECHA.log"

echo "📊 Iniciando sistema..."
echo "   Fecha: $FECHA"
echo "   Log: $LOG_FILE"
echo "   PID: $$"

# Iniciar sistema
echo "🔧 Ejecutando cerebro principal..."
python3 core/cerebro_principal_con_telegram.py > "$LOG_FILE" 2>&1 &

# Guardar PID
PID=$!
echo $PID > trading.pid

echo "✅ Sistema iniciado con PID: $PID"
echo ""
echo "📋 COMANDOS ÚTILES:"
echo "   • Ver logs: tail -f $LOG_FILE"
echo "   • Estado: ps aux | grep $PID"
echo "   • Detener: ./detener_sistema.sh"
echo "   • Logs anteriores: ls -la logs/"
echo ""
echo "🎯 El sistema ahora:"
echo "   1. Analiza 4 monedas (BTC, ETH, SOL, LINK)"
echo "   2. Busca señales institucionales"
echo "   3. Envía señales a Telegram"
echo "   4. Espera tu confirmación manual"
echo "   5. Ejecuta en Binance al confirmar"
echo ""
echo "⚠️  MONITOREA LOS LOGS LAS PRIMERAS HORAS"
