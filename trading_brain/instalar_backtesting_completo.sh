#!/bin/bash
echo "🔧 INSTALACIÓN COMPLETA DE BACKTESTING 🔧"
echo "=========================================="

# 1. Hacer backup del archivo original
echo "1. Creando backup..."
cp sistema_10_pares.py sistema_10_pares_BACKUP_$(date +%Y%m%d_%H%M%S).py

# 2. Crear archivo temporal con el backtesting integrado
echo "2. Integrando backtesting..."

# Leer el archivo original línea por línea y crear nuevo archivo
awk '
BEGIN { in_signal_block = 0; block_replaced = 0 }
{
    # Añadir importación después de otros imports (alrededor línea 15)
    if (NR == 16 && !/from backtester import/) {
        print "from backtester import backtestear_señal_rapido"
    }

    # Detectar inicio del bloque de señales
    if (/if señal\[.direccion.\] != "NEUTRAL":/ && !block_replaced) {
        print $0
        print ""
        print "    # ===== BACKTESTING EN TIEMPO REAL ====="
        print "    try:"
        print "        print(f\"   🔬 Ejecutando backtesting (30 días)...\")"
        print "        resultado_backtest = backtestear_señal_rapido(señal, par, bm)"
        print ""
        print "        if resultado_backtest.get(\"backtest_completado\") and resultado_backtest.get(\"valido\"):"
        print "            print(f\"   📊 Backtesting: Win Rate {resultado_backtest[\"win_rate\"]}% | PF: {resultado_backtest[\"profit_factor\"]}\")"
        print ""
        print "            # Solo enviar si pasa backtesting"
        print "            if resultado_backtest[\"win_rate\"] >= 55 and resultado_backtest[\"profit_factor\"] >= 1.2:"
        print "                print(f\"   ✅ Backtesting APROBADO\")"
        print ""
        print "                # Validar con histórico (sistema actual)"
        print "                validacion = cerebro.validar_senal_con_historico(señal)"
        print ""
        print "                if validacion[\"valida\"]:"
        print "                    # Añadir info backtesting a señal"
        print "                    if \"comentario\" not in señal:"
        print "                        señal[\"comentario\"] = \"\""
        print "                    señal[\"comentario\"] += f\" | 📈 Backtest: WR {resultado_backtest[\"win_rate\"]}%, PF: {resultado_backtest[\"profit_factor\"]:.1f}\""
        print ""
        print "                    # Continuar con envío normal..."
        print "            else:"
        print "                print(f\"   ⏹️  Rechazada por backtesting\")"
        print "                continue  # Saltar al siguiente par"
        print "        else:"
        print "            print(f\"   ⚠️  Backtesting no válido, continuando sin filtro...\")"
        print ""
        print "    except Exception as e:"
        print "        print(f\"   ❌ Error backtesting: {str(e)[:40]}, continuando sin filtro...\")"
        print ""
        print "    # ===== FIN BACKTESTING ====="
        print ""
        print "    # Validación normal (sistema actual)"
        print "    validacion = cerebro.validar_senal_con_historico(señal)"
        
        in_signal_block = 1
        block_replaced = 1
        next
    }
    
    # Saltar las líneas del bloque original que estamos reemplazando
    if (in_signal_block && /validacion = cerebro.validar_senal_con_historico/) {
        in_signal_block = 0
        next
    }
    
    if (in_signal_block) {
        next
    }
    
    # Imprimir todas las otras líneas
    print $0
}' sistema_10_pares.py > sistema_10_pares_CON_BACKTESTING_FINAL.py

# 3. Verificar sintaxis
echo "3. Verificando sintaxis..."
if python3 -m py_compile sistema_10_pares_CON_BACKTESTING_FINAL.py; then
    echo "✅ Sintaxis CORRECTA"
    
    # 4. Reemplazar archivo original
    echo "4. Reemplazando archivo principal..."
    cp sistema_10_pares_CON_BACKTESTING_FINAL.py sistema_10_pares.py
    
    # 5. Reiniciar el bot
    echo "5. Reiniciando bot de trading..."
    pm2 restart trading_bot
    
    echo ""
    echo "🎉 ¡BACKTESTING INTEGRADO EXITOSAMENTE! 🎉"
    echo "=========================================="
    echo "El bot ahora filtrará señales con:"
    echo "• Win Rate mínimo: 55%"
    echo "• Profit Factor mínimo: 1.2"
    echo "• Historial: 30 días"
    echo ""
    echo "Para verificar: pm2 logs trading_bot --lines 20"
else
    echo "❌ Error de sintaxis. Revertiendo cambios..."
    # No reemplazar el archivo original si hay error
    echo "El archivo original NO fue modificado."
    echo "Archivo con errores guardado como: sistema_10_pares_CON_BACKTESTING_FINAL.py"
fi
