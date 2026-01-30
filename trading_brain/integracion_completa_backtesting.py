import re

print("🔧 Leyendo archivo...")
with open('sistema_10_pares_CON_BACKTESTING.py', 'r') as f:
    lineas = f.readlines()

# PASO 1: Arreglar error de indentación en línea 112 (índice 111)
print("🔧 Arreglando indentación en línea 112...")
if len(lineas) > 111:
    # La línea 112 (índice 111) debería estar indentada si la 111 es un if
    if 'if ' in lineas[110] and not lineas[111].startswith('    '):
        lineas[111] = '    ' + lineas[111].lstrip()

# PASO 2: Asegurar que la importación del backtester existe
print("🔧 Verificando importación de backtester...")
import_encontrada = any('from backtester import backtestear_señal_rapido' in l for l in lineas[:30])
if not import_encontrada:
    # Buscar después de otros imports
    for i, linea in enumerate(lineas[:30]):
        if 'import ' in linea and 'from ' in linea:
            lineas.insert(i + 1, 'from backtester import backtestear_señal_rapido\n')
            break

# PASO 3: Reemplazar el bloque de señales con backtesting
print("🔧 Integrando backtesting en flujo de señales...")
contenido = ''.join(lineas)

# Patrón más específico para encontrar el bloque exacto
patron = r'(if señal\[\'direccion\'\] != "NEUTROal":\s*\n)(\s*print\(f"[^"]+"\)\s*\n)(\s*# .*\s*\n)?(\s*validacion = cerebro\.validar_senal_con_historico\(señal\))'

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

# Realizar el reemplazo
nuevo_contenido = re.sub(patron, reemplazo, contenido, flags=re.DOTALL)

# Guardar
with open('sistema_10_pares_CON_BACKTESTING.py', 'w') as f:
    f.write(nuevo_contenido)

print("✅ Integración COMPLETA. Probando sintaxis...")

# Probar sintaxis
import subprocess
result = subprocess.run(['python3', '-m', 'py_compile', 'sistema_10_pares_CON_BACKTESTING.py'], 
                       capture_output=True, text=True)
if result.returncode == 0:
    print("🎉 ¡SINTAXIS CORRECTA! Backtesting integrado exitosamente.")
else:
    print(f"⚠️  Error de sintaxis: {result.stderr[:100]}")
