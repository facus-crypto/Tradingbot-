#!/usr/bin/env python3
"""
SISTEMA 10 PARES OPERATIVOS - Con alertas de reinicio
"""
import sys
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("="*70)
print("🤖 SISTEMA COMPLETO - 10/10 PARES OPERATIVOS")
print("="*70)
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

# ===== ALERTA DE REINICIO/MANTENIMIENTO =====
def enviar_alerta_reinicio(tipo="reinicio"):
    """Envía alerta a Telegram sobre estado del sistema"""
    try:
        if tipo == "reinicio":
            mensaje = (
                "🔄 *REINICIO DEL SISTEMA DETECTADO*\n\n"
                "⚠️ El bot de trading se está reiniciando\n"
                "📋 **Motivo:** Mantenimiento automático\n"
                "🕐 Hora: {}\n\n"
                "🔧 **Estado:** Sistema en mantenimiento\n"
                "⏳ **Estimado:** Volverá operativo en 1-2 minutos\n\n"
                "📊 Se reanudará el análisis automáticamente\n"
                "#reinicio #mantenimiento #bot"
            ).format(datetime.now().strftime('%H:%M:%S'))
        
        elif tipo == "operativo":
            mensaje = (
                "✅ *SISTEMA OPERATIVO NUEVAMENTE*\n\n"
                "🎯 Bot de trading completamente restaurado\n"
                "🕐 Hora: {}\n"
                "📊 Estado: 100% OPERATIVO\n\n"
                "🔧 **Funcionalidades activas:**\n"
                "• Monitoreo de 10 pares\n"
                "• Análisis técnico avanzado\n"
                "• Señales automáticas\n"
                "• Validación histórica\n\n"
                "📈 Mercados monitoreados:\n"
                "BTC, ETH, SOL, LINK, BNB, ADA, AVAX, XRP, DOT, ATOM\n\n"
                "#operativo #trading #bot"
            ).format(datetime.now().strftime('%H:%M:%S'))
        
        elif tipo == "error":
            mensaje = (
                "🚨 *ERROR EN EL SISTEMA*\n\n"
                "❌ Se detectó un problema en el bot\n"
                "🕐 Hora: {}\n"
                "📋 **Acción requerida:**\n"
                "1. Revisar Termux\n"
                "2. Verificar logs\n"
                "3. Reiniciar si es necesario\n\n"
                "🔧 Sistema: @facusssss_bot\n"
                "#error #alerta #bot"
            ).format(datetime.now().strftime('%H:%M:%S'))
        
        # Enviar mensaje
        telegram_bot.enviar_mensaje(mensaje)
        print(f"📤 Alerta {tipo} enviada a Telegram")
        
    except Exception as e:
        print(f"⚠️ Error enviando alerta: {e}")

# ===== ENVIAR ALERTA DE REINICIO =====
print("\n📡 Enviando alerta de reinicio a Telegram...")
try:
    enviar_alerta_reinicio("reinicio")
    print("✅ Alerta de reinicio enviada")
except Exception as e:
    print(f"❌ Error: {e}")

# Enviar estado inicial normal
print("\n📡 Enviando estado del sistema a Telegram...")
telegram_bot.send_status(cerebros_activos=10, modo="Señales manuales")

# ===== ENVIAR ALERTA DE SISTEMA OPERATIVO =====
print("\n📡 Enviando alerta de sistema operativo...")
try:
    # Esperar 5 segundos para que todo esté listo
    import time
    time.sleep(5)
    
    enviar_alerta_reinicio("operativo")
    print("✅ Alerta de sistema operativo enviada")
except Exception as e:
    print(f"❌ Error: {e}")

# TODOS los 10 cerebros (resto del código sigue igual...)
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
                    print(f"   ✅ SEÑAL: {señal['direccion']} (conf: {señal['confianza']:.2f})")
                    
                    # Validar
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
            
            # Enviar alerta si hay error grave
            if "KeyboardInterrupt" not in str(e) and "timeout" not in str(e).lower():
                try:
                    enviar_alerta_reinicio("error")
                except:
                    pass

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
    
    # ===== ACTUALIZAR ESTADÍSTICAS DESPUÉS DE CADA CICLO =====
    actualizar_estadisticas(señales_encontradas)
    
    print("\n" + "="*70)
    print("⏳ Esperando 4 minutos para próximo análisis...")
    print("="*70)
    time.sleep(240)  # 240 segundos = 4 minutos
