#!/bin/bash
# Script para detener sistema de trading

echo "🛑 DETENIENDO SISTEMA DE TRADING"

if [ -f "trading.pid" ]; then
    PID=$(cat trading.pid)
    echo "   PID encontrado: $PID"
    
    # Verificar si el proceso existe
    if ps -p $PID > /dev/null; then
        echo "   Enviando señal de terminación..."
        kill $PID
        sleep 2
        
        # Verificar si se detuvo
        if ps -p $PID > /dev/null; then
            echo "   Forzando terminación..."
            kill -9 $PID
        fi
        
        echo "✅ Sistema detenido"
    else
        echo "⚠️  Proceso no encontrado"
    fi
    
    # Eliminar archivo PID
    rm trading.pid
else
    echo "❌ Archivo trading.pid no encontrado"
    echo "   Deteniendo manualmente procesos Python..."
    pkill -f cerebro_principal_con_telegram
fi

echo ""
echo "📊 RESUMEN DE EJECUCIÓN:"
echo "   • Logs disponibles en: logs/"
echo "   • Último log: ls -la logs/ | tail -5"
echo "   • Para reiniciar: ./iniciar_produccion.sh"
