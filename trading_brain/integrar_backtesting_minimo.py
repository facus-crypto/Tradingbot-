with open('sistema_10_pares.py', 'r') as f:
    lineas = f.readlines()

# Encontrar donde añadir la importación
for i, linea in enumerate(lineas):
    if 'from binance_manager_custom import' in linea:
        lineas.insert(i+1, 'from backtester import backtestear_señal_rapido\n')
        break

# Buscar el bloque if señal['direccion'] != "NEUTRAL":
for i, linea in enumerate(lineas):
    if 'if señal[\'direccion\'] != "NEUTRAL":' in linea:
        # Insertar backtesting después del print
        j = i + 2  # Saltar línea del if y del print
        codigo_backtesting = '''    # ===== BACKTESTING EN TIEMPO REAL =====
    try:
        from backtester import backtestear_señal_rapido
        print(f"   🔬 Ejecutando backtesting (30 días)...")
        resultado = backtestear_señal_rapido(señal, par, bm)
        
        if resultado.get("backtest_completado") and resultado.get("valido"):
            print(f"   📊 Backtesting: Win Rate {resultado['win_rate']}% | PF: {resultado['profit_factor']}")
            
            if resultado["win_rate"] >= 55 and resultado["profit_factor"] >= 1.2:
                print(f"   ✅ Backtesting APROBADO")
            else:
                print(f"   ⏹️  Rechazada por backtesting")
                continue
        else:
            print(f"   ⚠️  Backtesting no válido, continuando...")
    except ImportError:
        print(f"   ⚠️  Módulo backtester no disponible")
    except Exception as e:
        print(f"   ❌ Error backtesting: {str(e)[:50]}")
    # ===== FIN BACKTESTING =====
'''
        lineas.insert(j, codigo_backtesting)
        break

with open('sistema_10_pares.py', 'w') as f:
    f.writelines(lineas)

print("✅ Backtesting integrado mínimamente")
