import re

with open('sistema_10_pares_CON_BACKTESTING.py', 'r') as f:
    contenido = f.read()

# Patrón para encontrar el bloque a modificar
patron = r'(if señal\[\'direccion\'\] != "NEUTRAL":\s*\n\s*print\(f"[^"]+"\)\s*\n\s*# .*\s*\n\s*validacion = cerebro\.validar_senal_con_historico\(señal\))'

# Reemplazo con backtesting
reemplazo = '''if señal['direccion'] != "NEUTRAL":
    print(f"   ✅ SEÑAL: {señal['direccion']} (conf: {señal['confianza']:.2f})")

    # ===== BACKTESTING EN TIEMPO REAL =====
    print(f"   🔬 Ejecutando backtesting (30 días)...")
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

    # ===== FIN BACKTESTING =====

    # Validación normal (sistema actual) - SOLO si backtesting no aplicó 'continue'
    validacion = cerebro.validar_senal_con_historico(señal)'''

nuevo_contenido = re.sub(patron, reemplazo, contenido, flags=re.DOTALL)

with open('sistema_10_pares_CON_BACKTESTING.py', 'w') as f:
    f.write(nuevo_contenido)

print("✅ Backtesting integrado. Verificando sintaxis...")
