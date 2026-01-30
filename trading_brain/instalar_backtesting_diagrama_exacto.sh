#!/bin/bash
echo "🔧 INSTALANDO BACKTESTING CON FLUJO EXACTO DEL DIAGRAMA"
echo "========================================================"

# 1. Backup
cp sistema_10_pares.py sistema_10_pares_BACKUP_DIAGRAMA.py
echo "✅ Backup creado"

# 2. Añadir importación si no existe
if ! grep -q "from backtester import backtestear_señal_rapido" sistema_10_pares.py; then
    sed -i '15a\from backtester import backtestear_señal_rapido' sistema_10_pares.py
    echo "✅ Importación añadida"
fi

# 3. Leer archivo completo
mapfile -t lineas < sistema_10_pares.py

# 4. Encontrar inicio del bloque
inicio=-1
for i in "${!lineas[@]}"; do
    if [[ "${lineas[i]}" == *"if señal['direccion'] != \"NEUTRAL\":"* ]]; then
        inicio=$i
        break
    fi
done

if [ $inicio -eq -1 ]; then
    echo "❌ No se encontró el bloque de señales"
    exit 1
fi

echo "📍 Bloque encontrado en línea: $((inicio+1))"

# 5. Encontrar fin del bloque (validacion = cerebro.validar_senal_con_historico)
fin=-1
for ((i=inicio; i<${#lineas[@]}; i++)); do
    if [[ "${lineas[i]}" == *"validacion = cerebro.validar_senal_con_historico(señal)"* ]]; then
        fin=$i
        break
    fi
done

if [ $fin -eq -1 ]; then
    echo "❌ No se encontró el final del bloque"
    exit 1
fi

echo "📍 Fin del bloque en línea: $((fin+1))"

# 6. Crear nuevo archivo
{
    # Primeras líneas (hasta inicio)
    for ((i=0; i<inicio; i++)); do
        echo "${lineas[i]}"
    done
    
    # NUEVO BLOQUE CON DIAGRAMA EXACTO
    echo "                if señal['direccion'] != \"NEUTRAL\":"
    echo "                    print(f\"   ✅ SEÑAL: {señal['direccion']} (conf: {señal['confianza']:.2f})\")"
    echo "                    "
    echo "                    # ===== FLUJO SEGÚN DIAGRAMA DEL LINK ====="
    echo "                    # PASO 1: Confianza > 0.70"
    echo "                    if señal['confianza'] > 0.70:"
    echo "                        "
    echo "                        # PASO 2: BACKTESTING (30 días)"
    echo "                        print(f\"   🔬 Ejecutando backtesting (30 días)...\")"
    echo "                        try:"
    echo "                            resultado_backtest = backtestear_señal_rapido(señal, par, bm)"
    echo ""
    echo "                            if resultado_backtest.get('backtest_completado') and resultado_backtest.get('valido'):"
    echo "                                print(f\"   📊 Backtesting: Win Rate {resultado_backtest['win_rate']}% | PF: {resultado_backtest['profit_factor']}\")"
    echo ""
    echo "                                # PASO 3: FILTRO (Win Rate ≥55%, Profit Factor ≥1.2)"
    echo "                                if resultado_backtest['win_rate'] >= 55 and resultado_backtest['profit_factor'] >= 1.2:"
    echo "                                    print(f\"   ✅ Backtesting APROBADO\")"
    echo ""
    echo "                                    # PASO 4: VALIDACIÓN (sistema actual)"
    echo "                                    validacion = cerebro.validar_senal_con_historico(señal)"
    echo ""
    echo "                                    if validacion['valida']:"
    echo "                                        # PASO 5: TELEGRAM (preparar envío)"
    echo "                                        if 'comentario' not in señal:"
    echo "                                            señal['comentario'] = \"\""
    echo "                                        señal['comentario'] += f\" | 📈 Backtest: WR {resultado_backtest['win_rate']}%, PF: {resultado_backtest['profit_factor']:.1f}\""
    echo "                                        "
    echo "                                        # Continuar con envío normal..."
    echo "                                else:"
    echo "                                    print(f\"   ⏹️  Rechazada por backtesting\")"
    echo "                                    continue  # Saltar al siguiente par"
    echo "                            else:"
    echo "                                print(f\"   ⚠️  Backtesting no válido, continuando sin filtro...\")"
    echo ""
    echo "                        except Exception as e:"
    echo "                            print(f\"   ❌ Error backtesting: {str(e)[:40]}, continuando sin filtro...\")"
    echo "                    else:"
    echo "                        print(f\"   ⏹️  Confianza ≤ 0.70, saltando backtesting\")"
    echo "                        continue"
    echo ""
    echo "                    # ===== FIN FLUJO DIAGRAMA ====="
    echo ""
    echo "                    # Validación normal (sistema actual)"
    echo "                    validacion = cerebro.validar_senal_con_historico(señal)"
    
    # Resto del archivo (después de fin)
    for ((i=fin+1; i<${#lineas[@]}; i++)); do
        echo "${lineas[i]}"
    done
} > sistema_10_pares_NUEVO.py

# 7. Reemplazar archivo
mv sistema_10_pares_NUEVO.py sistema_10_pares.py

echo "✅ Backtesting con flujo EXACTO instalado"

# 8. Verificar sintaxis
echo "🔍 Verificando sintaxis..."
if python3 -m py_compile sistema_10_pares.py; then
    echo "🎉 ¡SINTÁXIS CORRECTA! Backtesting instalado."
    echo ""
    echo "📊 FLUJO IMPLEMENTADO:"
    echo "1. Confianza > 0.70 → 2. Backtesting 30 días → 3. Win Rate ≥55% y PF ≥1.2"
    echo "4. Validación → 5. Telegram"
    echo ""
    echo "🔄 Reinicia el bot:"
    echo "pm2 restart trading_bot"
else
    echo "❌ Error de sintaxis. Se restauró backup."
    cp sistema_10_pares_BACKUP_DIAGRAMA.py sistema_10_pares.py
fi
