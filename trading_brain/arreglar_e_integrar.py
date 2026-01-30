print("🔧 ARREGLANDO ERROR ORIGINAL E INTEGRANDO BACKTESTING")

# 1. Leer el archivo original
with open("sistema_10_pares.py", "r") as f:
    lineas = f.readlines()

# 2. Arreglar el error en línea 112
print("1. Arreglando error en línea 112...")
for i in range(len(lineas)):
    if i == 111:  # Línea 112 (índice 111)
        if "if " in lineas[i] and not lineas[i].startswith("    "):
            lineas[i] = "    " + lineas[i].lstrip()
        # Asegurar que la siguiente línea esté indentada
        if i+1 < len(lineas) and not lineas[i+1].startswith("        "):
            lineas[i+1] = "        " + lineas[i+1].lstrip()

# 3. Añadir importación del backtester
print("2. Añadiendo importación de backtester...")
for i in range(min(20, len(lineas))):
    if "import " in lineas[i] and "from " in lineas[i]:
        lineas.insert(i + 1, "from backtester import backtestear_señal_rapido\n")
        break

# 4. Buscar y reemplazar el bloque de señales
print("3. Integrando backtesting en flujo de señales...")
contenido = "".join(lineas)

# Encontrar posición exacta del bloque
import re
patron = r'if señal\[\"direccion\"\] != "NEUTRAL":\s*\n\s*print\(f"[^"]+"\)\s*\n\s*# .*\s*\n\s*validacion = cerebro\.validar_senal_con_historico\(señal\)'

if re.search(patron, contenido):
    # Código nuevo CON backtesting
    nuevo_codigo = '''if señal["direccion"] != "NEUTRAL":
    print(f"   ✅ SEÑAL: {señal['direccion']} (conf: {señal['confianza']:.2f})")

    # ===== BACKTESTING EN TIEMPO REAL =====
    print(f"   🔬 Ejecutando backtesting (30 días)...")
    
    try:
        resultado_backtest = backtestear_señal_rapido(señal, par, bm)

        if resultado_backtest.get("backtest_completado") and resultado_backtest.get("valido"):
            print(f"   📊 Backtesting: Win Rate {resultado_backtest['win_rate']}% | PF: {resultado_backtest['profit_factor']}")

            # Solo enviar si pasa backtesting
            if resultado_backtest["win_rate"] >= 55 and resultado_backtest["profit_factor"] >= 1.2:
                print(f"   ✅ Backtesting APROBADO")

                # Validar con histórico (sistema actual)
                validacion = cerebro.validar_senal_con_historico(señal)

                if validacion["valida"]:
                    # Añadir info backtesting a señal
                    if "comentario" not in señal:
                        señal["comentario"] = ""
                    señal["comentario"] += f" | 📈 Backtest: WR {resultado_backtest['win_rate']}%, PF: {resultado_backtest['profit_factor']:.1f}"

                    # Continuar con envío normal...
            else:
                print(f"   ⏹️  Rechazada por backtesting")
                continue  # Saltar al siguiente par
        else:
            print(f"   ⚠️  Backtesting no válido, continuando sin filtro...")
            
    except Exception as e:
        print(f"   ❌ Error backtesting: {str(e)[:50]}, continuando sin filtro...")

    # ===== FIN BACKTESTING =====

    # Validación normal (sistema actual)
    validacion = cerebro.validar_senal_con_historico(señal)'''
    
    contenido = re.sub(patron, nuevo_codigo, contenido, flags=re.DOTALL)
    print("✅ Backtesting integrado")
else:
    print("⚠️  No se encontró el patrón del bloque de señales")

# 5. Guardar archivo corregido
with open("sistema_10_pares_ARREGLADO.py", "w") as f:
    f.write(contenido)

print("4. Verificando sintaxis...")
import subprocess
result = subprocess.run(["python3", "-m", "py_compile", "sistema_10_pares_ARREGLADO.py"], 
                       capture_output=True, text=True)

if result.returncode == 0:
    print("🎉 ¡ARCHIVO CORREGIDO Y BACKTESTING INTEGRADO!")
    print("Ejecuta estos comandos para desplegar:")
    print("1. cp sistema_10_pares_ARREGLADO.py sistema_10_pares.py")
    print("2. pm2 restart trading_bot")
    print("3. pm2 logs trading_bot --lines 20")
else:
    print(f"❌ Error: {result.stderr[:100]}")
