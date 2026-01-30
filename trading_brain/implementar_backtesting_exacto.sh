#!/bin/bash
echo "🔧 IMPLEMENTANDO BACKTESTING SEGÚN EL LINK"
echo "=========================================="

# 1. Arreglar error en cerebro_base_futures.py
echo "1. Arreglando error en cerebro_base_futures.py..."
sed -i '158s/^/    /' cerebros/cerebro_base_futures.py
sed -i '159s/^/    /' cerebros/cerebro_base_futures.py

# 2. Probar que se arregló
if python3 -m py_compile cerebros/cerebro_base_futures.py; then
    echo "   ✅ Error arreglado"
else
    echo "   ❌ Error persistente"
    exit 1
fi

# 3. Añadir importación del backtester
echo "2. Añadiendo importación del backtester..."
sed -i '15a\from backtester import backtestear_señal_rapido' sistema_10_pares.py

# 4. Encontrar y reemplazar el bloque de señales
echo "3. Integrando backtesting en flujo de señales..."
# Buscar línea donde está el bloque
LINEA=$(grep -n "if señal\['direccion'\] != \"NEUTRAL\":" sistema_10_pares.py | head -1 | cut -d: -f1)

if [ -n "$LINEA" ]; then
    echo "   📍 Bloque encontrado en línea: $LINEA"
    
    # Crear archivo temporal con el código nuevo (EXACTO del link)
    cat > /tmp/backtesting_code.py << 'BACKEOF'
    print(f"   ✅ SEÑAL: {señal['direccion']} (conf: {señal['confianza']:.2f})")

    # ===== BACKTESTING EN TIEMPO REAL =====
    print(f"   🔬 Ejecutando backtesting (30 días)...")
    try:
        resultado_backtest = backtestear_señal_rapido(señal, par, bm)

        if resultado_backtest.get('backtest_completado') and resultado_backtest.get('valido'):
            print(f"   📊 Backtesting: Win Rate {resultado_backtest['win_rate']}% | PF: {resultado_backtest['profit_factor']}")

            # Solo enviar si pasa backtesting
            if resultado_backtest['win_rate'] >= 55 and resultado_backtest['profit_factor'] >= 1.2:
                print(f"   ✅ Backtesting APROBADO")

                # Validar con histórico (sistema actual)
                validacion = cerebro.validar_senal_con_historico(señal)

                if validacion['valida']:
                    # Añadir info backtesting a señal
                    if 'comentario' not in señal:
                        señal['comentario'] = ""
                    señal['comentario'] += f" | 📈 Backtest: WR {resultado_backtest['win_rate']}%, PF: {resultado_backtest['profit_factor']:.1f}"

                    # Continuar con envío normal...
            else:
                print(f"   ⏹️  Rechazada por backtesting")
                continue  # Saltar al siguiente par
        else:
            print(f"   ⚠️  Backtesting no válido, continuando sin filtro...")

    except Exception as e:
        print(f"   ❌ Error backtesting: {str(e)[:40]}, continuando sin filtro...")

    # ===== FIN BACKTESTING =====

    # Validación normal (sistema actual) - SOLO si backtesting no aplicó 'continue'
    validacion = cerebro.validar_senal_con_historico(señal)
BACKEOF

    # Reemplazar desde LINEA hasta donde termina el bloque original
    # Buscar siguiente línea con "validacion = cerebro.validar_senal_con_historico"
    END_LINE=$(awk -v start="$LINEA" 'NR > start && /validacion = cerebro\.validar_senal_con_historico/ {print NR; exit}' sistema_10_pares.py)
    
    if [ -n "$END_LINE" ]; then
        # Crear nuevo archivo
        head -n $((LINEA-1)) sistema_10_pares.py > /tmp/new_file.py
        cat /tmp/backtesting_code.py >> /tmp/new_file.py
        tail -n +$((END_LINE+1)) sistema_10_pares.py >> /tmp/new_file.py
        
        mv /tmp/new_file.py sistema_10_pares.py
        echo "   ✅ Backtesting integrado"
    else
        echo "   ❌ No se encontró el final del bloque"
        exit 1
    fi
else
    echo "   ❌ No se encontró el bloque de señales"
    exit 1
fi

# 5. Verificar sintaxis completa
echo "4. Verificando sintaxis completa..."
if python3 -m py_compile sistema_10_pares.py; then
    echo "🎉 ¡BACKTESTING IMPLEMENTADO EXITOSAMENTE!"
    echo "=========================================="
    echo "Reinicia el bot con: pm2 start sistema_10_pares.py --name trading_bot"
else
    echo "❌ Error de sintaxis al integrar backtesting"
    exit 1
fi
