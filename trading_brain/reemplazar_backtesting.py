import re

# Leer el archivo
with open('sistema_10_pares_CON_BACKTESTING.py', 'r') as f:
    lineas = f.readlines()

# Encontrar el inicio del bloque a modificar
inicio_bloque = None
for i, linea in enumerate(lineas):
    if "if señal['direccion'] != \"NEUTRAL\":" in linea:
        inicio_bloque = i
        break

if inicio_bloque is None:
    print("❌ No se encontró el bloque a modificar")
    exit(1)

# Buscar la línea de validación histórica (donde termina el bloque a reemplazar)
fin_bloque = None
for i in range(inicio_bloque, len(lineas)):
    if "validacion = cerebro.validar_senal_con_historico(señal)" in lineas[i] and i > inicio_bloque:
        # Asegurarnos que es la primera validación después del inicio
        fin_bloque = i
        break

if fin_bloque is None:
    print("❌ No se encontró el final del bloque")
    exit(1)

# El nuevo bloque con backtesting
nuevo_bloque = '''    print(f"   ✅ SEÑAL: {señal['direccion']} (conf: {señal['confianza']:.2f})")

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
    validacion = cerebro.validar_senal_con_historico(señal)
'''

# Reemplazar las líneas del bloque antiguo con el nuevo bloque
lineas_modificadas = lineas[:inicio_bloque] + [nuevo_bloque] + lineas[fin_bloque+1:]

# Escribir el archivo modificado
with open('sistema_10_pares_CON_BACKTESTING.py', 'w') as f:
    f.writelines(lineas_modificadas)

print(f"✅ Bloque reemplazado exitosamente (líneas {inicio_bloque+1} a {fin_bloque+1})")
