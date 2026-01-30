with open('sistema_10_pares.py', 'r') as f:
    lineas = f.readlines()

inicio = 111  # Línea 112

fin = None
for i in range(inicio, len(lineas)):
    if 'validacion = cerebro.validar_senal_con_historico' in lineas[i]:
        fin = i
        break

if fin is not None:
    nuevo_codigo = '''                if señal['direccion'] != "NEUTRAL":
                    print(f"   ✅ SEÑAL: {señal['direccion']} (conf: {señal['confianza']:.2f})")

                    # ===== BACKTESTING EN TIEMPO REAL =====
                    print(f"   🔬 Ejecutando backtesting (30 días)...")
                    try:
                        resultado_backtest = backtestear_señal_rapido(señal, par, bm)

                        if resultado_backtest.get('backtest_completado') and resultado_backtest.get('valido'):
                            print(f"   📊 Backtesting: Win Rate {resultado_backtest['win_rate']}% | PF: {resultado_backtest['profit_factor']}")

                            if resultado_backtest['win_rate'] >= 55 and resultado_backtest['profit_factor'] >= 1.2:
                                print(f"   ✅ Backtesting APROBADO")

                                validacion = cerebro.validar_senal_con_historico(señal)

                                if validacion['valida']:
                                    if 'comentario' not in señal:
                                        señal['comentario'] = ""
                                    señal['comentario'] += f" | 📈 Backtest: WR {resultado_backtest['win_rate']}%, PF: {resultado_backtest['profit_factor']:.1f}"
                            else:
                                print(f"   ⏹️  Rechazada por backtesting")
                                continue
                        else:
                            print(f"   ⚠️  Backtesting no válido, continuando sin filtro...")

                    except Exception as e:
                        print(f"   ❌ Error backtesting: {str(e)[:40]}, continuando sin filtro...")

                    # ===== FIN BACKTESTING =====

                    validacion = cerebro.validar_senal_con_historico(señal)
'''
    
    nuevas_lineas = lineas[:inicio] + [nuevo_codigo] + lineas[fin+1:]
    
    with open('sistema_10_pares.py', 'w') as f:
        f.writelines(nuevas_lineas)
    
    print(f"✅ Backtesting integrado")
else:
    print("❌ Error: No se encontró validacion")
