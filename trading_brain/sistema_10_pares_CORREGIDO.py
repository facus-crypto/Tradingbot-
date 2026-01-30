#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA 10 PARES - ORQUESTADOR PRINCIPAL
"""

import json
import time
import sys
import os
from datetime import datetime

# Agregar el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar configuración
try:
    with open('config_futures.json', 'r') as f:
        config = json.load(f)
    BINANCE_API_KEY = config['BINANCE_API_KEY']
    BINANCE_API_SECRET = config['BINANCE_API_SECRET']
except Exception as e:
    print(f"❌ ERROR cargando config_futures.json: {e}")
    sys.exit(1)

# Importar backtesting
from backtester import backtestear_señal_rapido

# Importar manager Binance
from binance_manager_custom import BinanceFuturesManagerCustom

# Resto del código original (imports de cerebros, etc.)
# ... [Todo el código original] ...

# BUSCAR en el archivo original esta línea:
# "if señal['direccion'] != "NEUTRAL":"
# Y REEMPLAZAR desde ahí hasta "validacion = cerebro.validar_senal_con_historico(señal)"
# CON ESTO:

                if señal['direccion'] != "NEUTRAL":
                    print(f"   ✅ SEÑAL: {señal['direccion']} (conf: {señal['confianza']:.2f})")
                    
                    # ===== FLUJO SEGÚN DIAGRAMA DEL LINK =====
                    # PASO 1: Confianza > 0.70
                    if señal['confianza'] > 0.70:
                        
                        # PASO 2: BACKTESTING (30 días)
                        print(f"   🔬 Ejecutando backtesting (30 días)...")
                        try:
                            resultado_backtest = backtestear_señal_rapido(señal, par, bm)

                            if resultado_backtest.get('backtest_completado') and resultado_backtest.get('valido'):
                                print(f"   📊 Backtesting: Win Rate {resultado_backtest['win_rate']}% | PF: {resultado_backtest['profit_factor']}")

                                # PASO 3: FILTRO (Win Rate ≥55%, Profit Factor ≥1.2)
                                if resultado_backtest['win_rate'] >= 55 and resultado_backtest['profit_factor'] >= 1.2:
                                    print(f"   ✅ Backtesting APROBADO")

                                    # PASO 4: VALIDACIÓN (sistema actual)
                                    validacion = cerebro.validar_senal_con_historico(señal)

                                    if validacion['valida']:
                                        # PASO 5: TELEGRAM (preparar envío)
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
                    else:
                        print(f"   ⏹️  Confianza ≤ 0.70, saltando backtesting")
                        continue

                    # ===== FIN FLUJO DIAGRAMA =====

                    # Validación normal (sistema actual)
                    validacion = cerebro.validar_senal_con_historico(señal)
