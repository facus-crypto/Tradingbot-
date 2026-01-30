#!/usr/bin/env python3
"""
SISTEMA 10 PARES OPERATIVOS - CON BACKTESTING LIMPIO
"""
import sys
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("="*70)
print("🤖 SISTEMA COMPLETO - 10/10 PARES CON BACKTESTING")
print("="*70)
from backtester import backtestear_señal_rapido
print(f"Inicio: {datetime.now().strftime('%H:%M:%S')}")

# Cargar configuración
with open('config_futures.json', 'r') as f:
    config = json.load(f)

# Inicializar
from binance_manager_custom import BinanceFuturesManagerCustom
from interfaces.telegram_advanced import TelegramAdvancedBot

bm = BinanceFuturesManagerCustom(
    config['binance']['api_key'],
    config['binance']['api_secret'],
    config['binance'].get('testnet', False)
)

telegram_bot = TelegramAdvancedBot(
    config['telegram']['token'],
    config['telegram']['chat_id']
)

# Enviar estado inicial
print("\n📡 Enviando estado del sistema a Telegram...")
telegram_bot.send_status(cerebros_activos=10, modo="Señales con Backtesting")

# TODOS los 10 cerebros
cerebros_completos = [
    ("BTC", "cerebro_btc_futures", "CerebroBTCFutures"),
    ("ETH", "cerebro_eth_futures", "CerebroETHFutures"),
    ("SOL", "cerebro_sol_futures", "CerebroSOLFutures"),
    ("LINK", "cerebro_link_futures", "CerebroLINKFutures"),
    ("BNB", "cerebro_bnb_futures", "CerebroBNBFutures"),
    ("ADA", "cerebro_ada_futures", "CerebroADAFutures"),
    ("AVAX", "cerebro_avax_futures", "CerebroAVAXFutures"),
    ("XRP", "cerebro_xrp_futures", "CerebroXRPFutures"),
    ("DOT", "cerebro_dot_futures", "CerebroDOTFutures"),
    ("ATOM", "cerebro_atom_futures", "CerebroATOMFutures")
]

# ===== FUNCIÓN PARA ACTUALIZAR ESTADÍSTICAS =====
def actualizar_estadisticas(señales_enviadas=0):
    try:
        # Cargar estadísticas existentes
        try:
            with open('stats.json', 'r') as f:
                stats = json.load(f)
        except:
            stats = {
                "inicio_sistema": datetime.now().isoformat(),
                "señales_enviadas": 0,
                "ciclos_completados": 0,
                "operaciones_activas": 0,
                "ultimo_ciclo": datetime.now().isoformat()
            }
        
        # Actualizar
        stats["ciclos_completados"] += 1
        stats["señales_enviadas"] += señales_enviadas
        stats["ultimo_ciclo"] = datetime.now().isoformat()
        
        # Guardar
        with open('stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
            
        print(f"📊 Estadísticas actualizadas: {stats['ciclos_completados']} ciclos, {stats['señales_enviadas']} señales")
        
    except Exception as e:
        print(f"⚠️ Error actualizando stats: {e}")

import time

while True:
    print("\n" + "="*70)
    print(f"🔄 CICLO DE ANÁLISIS INICIADO: {datetime.now().strftime('%H:%M:%S')}")
    print("="*70)
    
    señales_encontradas = 0
    
    for nombre, modulo, clase in cerebros_completos:
        par = f"{nombre}USDT"
        print(f"\n[{nombre}] Analizando...")
        
        try:
            # Importar
            module_path = f"cerebros.{modulo}"
            cerebro_module = __import__(module_path, fromlist=[clase])
            cerebro_class = getattr(cerebro_module, clase)

            # Crear cerebro
            cerebro = cerebro_class(bm, telegram_bot)

            # Analizar
            señal = cerebro.analizar()

            if señal:
                if señal['direccion'] != "NEUTRAL":

    # ===== BACKTESTING EN TIEMPO REAL =====
    try:
        print(f"   🔬 Ejecutando backtesting (30 días)...")
        resultado_backtest = backtestear_señal_rapido(señal, par, bm)

        if resultado_backtest.get("backtest_completado") and resultado_backtest.get("valido"):
            print(f"   📊 Backtesting: Win Rate {resultado_backtest["win_rate"]}% | PF: {resultado_backtest["profit_factor"]}")

            # Solo enviar si pasa backtesting
            if resultado_backtest["win_rate"] >= 55 and resultado_backtest["profit_factor"] >= 1.2:
                print(f"   ✅ Backtesting APROBADO")

                # Validar con histórico (sistema actual)
                validacion = cerebro.validar_senal_con_historico(señal)

                if validacion["valida"]:
                    # Añadir info backtesting a señal
                    if "comentario" not in señal:
                        señal["comentario"] = ""
                    señal["comentario"] += f" | 📈 Backtest: WR {resultado_backtest["win_rate"]}%, PF: {resultado_backtest["profit_factor"]:.1f}"

                    # Continuar con envío normal...
            else:
                print(f"   ⏹️  Rechazada por backtesting")
                continue  # Saltar al siguiente par
        else:
            print(f"   ⚠️  Backtesting no válido, continuando sin filtro...")

    except Exception as e:
        print(f"   ❌ Error backtesting: {str(e)[:40]}, continuando sin filtro...")

    # ===== FIN BACKTESTING =====

    # Validación normal (sistema actual)
    validacion = cerebro.validar_senal_con_historico(señal)
                    
                    if validacion['valida']:
                        print(f"   📊 Validada: conf {validacion['confianza_combinada']:.2f}")
                        
                        # Enviar a Telegram
                        enviado = cerebro.enviar_senal_con_validacion(señal, validacion)
                        if enviado:
                            print(f"   📤 Enviada a Telegram")
                            señales_encontradas += 1
                        else:
                            print(f"   ❌ Error enviando")
                    else:
                        print(f"   ⏹️  Rechazada por validador")
                else:
                    print(f"   ⚪ Neutral (conf: {señal['confianza']:.2f})")
            else:
                print(f"   ❌ Error en análisis")

        except Exception as e:
            print(f"   ❌ Error: {str(e)[:40]}")

    print("\n" + "="*70)
    print("✅ MONITOREO COMPLETADO")
    print("="*70)
    print(f"📊 Resultados:")
    print(f"• Pares analizados: 10/10")
    print(f"• Señales encontradas: {señales_encontradas}")
    print(f"• Señales enviadas a Telegram: {señales_encontradas}")
    print(f"• Sistema: 100% OPERATIVO")
    print(f"\n🎯 Revisa Telegram: @facusssss_bot")
    print("="*70)
    
    # ===== ACTUALIZAR ESTADÍSTICAS =====
    actualizar_estadisticas(señales_encontradas)
    
    print("\n" + "="*70)
    print("⏳ Esperando 4 minutos para próximo análisis...")
    print("="*70)
    time.sleep(240)  # 240 segundos = 4 minutos
