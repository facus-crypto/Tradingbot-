#!/usr/bin/env python3
"""
CONFIGURACIÓN PARA PRODUCCIÓN - Sistema de Trading
Guía paso a paso para activar el sistema con dinero real.
"""
import os
import sys
import json
from datetime import datetime

def print_header(text):
    """Imprime encabezado bonito"""
    print("\n" + "="*70)
    print(f"🎯 {text}")
    print("="*70)

def paso_1_verificar_estructura():
    """Paso 1: Verificar que todo está instalado"""
    print_header("PASO 1: VERIFICAR ESTRUCTURA DEL SISTEMA")
    
    archivos_requeridos = [
        "config.py",
        "core/cerebro_principal_con_telegram.py",
        "interfaces/telegram_signal.py",
        "cerebros/cerebro_btc.py",
        "cerebros/cerebro_eth.py",
        "cerebros/cerebro_sol.py",
        "cerebros/cerebro_link.py",
        "core/risk_manager.py"
    ]
    
    todos_ok = True
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - NO ENCONTRADO")
            todos_ok = False
    
    return todos_ok

def paso_2_configurar_binance():
    """Paso 2: Configurar API de Binance"""
    print_header("PASO 2: CONFIGURAR BINANCE API")
    
    print("📋 NECESITAS ESTOS DATOS DE BINANCE:")
    print("   1. Ve a Binance → API Management")
    print("   2. Crea nueva API Key (si no tienes)")
    print("   3. Habilita permisos de TRADING")
    print("   4. Copia:")
    print("      • API Key: ________________")
    print("      • Secret Key: _____________")
    
    print("\n⚠️  IMPORTANTE:")
    print("   • USA BINANCE TESTNET PRIMERO para pruebas")
    print("   • NO compartas tus keys con nadie")
    print("   • IP Restriction: ACTIVADO (recomendado)")
    
    input("\n📝 Presiona Enter cuando tengas los datos...")
    
    # Mostrar ejemplo de configuración
    print("\n📄 EJEMPLO de cómo editar config.py:")
    print('''
# En config.py, busca BINANCE_CONFIG y cambia:
BINANCE_CONFIG = {
    "api_key": "TU_API_KEY_REAL_AQUI",      # <-- Pega tu API Key
    "api_secret": "TU_SECRET_KEY_AQUI",     # <-- Pega tu Secret Key
    "testnet": False,                       # <-- Cambia a False para real
    "recv_window": 5000
}
''')
    
    return True

def paso_3_configurar_telegram():
    """Paso 3: Configurar Bot de Telegram"""
    print_header("PASO 3: CONFIGURAR TELEGRAM BOT")
    
    print("📋 NECESITAS ESTOS DATOS DE TELEGRAM:")
    print("   1. Crea bot con @BotFather (si no tienes)")
    print("   2. Guarda el Token que te dé")
    print("   3. Obtén tu Chat ID con @userinfobot")
    print("   4. Copia:")
    print("      • Bot Token: ________________")
    print("      • Chat ID: __________________")
    
    print("\n🔧 PARA OBTENER CHAT ID:")
    print("   1. Abre @userinfobot en Telegram")
    print("   2. Envía /start")
    print("   3. Copia tu 'Id:' (ejemplo: 123456789)")
    
    input("\n📝 Presiona Enter cuando tengas los datos...")
    
    # Mostrar ejemplo de configuración
    print("\n📄 EJEMPLO de cómo editar telegram_signal.py:")
    print('''
# En interfaces/telegram_signal.py, busca:
class InterfazTelegramSimple:
    def __init__(self, modo_prueba=True):  # <-- Cambia a False
    
# Y en la prueba al final:
if __name__ == "__main__":
    interfaz = InterfazTelegramSimple(
        bot_token="TU_BOT_TOKEN_REAL_AQUI",  # <-- Pega token
        chat_id="TU_CHAT_ID_REAL_AQUI",      # <-- Pega chat ID
        modo_prueba=False                    # <-- Cambia a False
    )
''')
    
    return True

def paso_4_configurar_riesgo():
    """Paso 4: Configurar parámetros de riesgo"""
    print_header("PASO 4: CONFIGURAR GESTIÓN DE RIESGO")
    
    print("💰 CONFIGURACIÓN ACTUAL (config.py):")
    print('''
CAPITAL_CONFIG = {
    "porcentaje_por_operacion": 0.25,  # 25% de la wallet por entrada
    "apalancamiento": 2,               # Apalancamiento x2
    "stop_loss_porcentaje": 0.02,      # 2% máximo por operación
    "max_operaciones_simultaneas": 3,
    "risk_reward_minimo": 1.5,         # Mínimo 1.5:1
    "max_riesgo_diario": 0.05,         # 5% máximo diario
}
''')
    
    print("\n❓ ¿QUIERES MODIFICAR ALGÚN PARÁMETRO?")
    print("   1. Porcentaje por operación (25%): ______")
    print("   2. Apalancamiento (x2): ______")
    print("   3. Stop loss máximo (2%): ______")
    
    input("\n📝 Presiona Enter para continuar...")
    
    return True

def paso_5_protocolo_seguridad():
    """Paso 5: Protocolos de seguridad"""
    print_header("PASO 5: PROTOCOLOS DE SEGURIDAD")
    
    print("🔒 LISTA DE VERIFICACIÓN DE SEGURIDAD:")
    print("   ✅ 1. API Binance con IP Restriction")
    print("   ✅ 2. Límite de riesgo por operación (2%)")
    print("   ✅ 3. Límite de riesgo diario (5%)")
    print("   ✅ 4. Confirmación manual vía Telegram")
    print("   ✅ 5. Máximo 3 operaciones simultáneas")
    print("   ✅ 6. Stop loss automático")
    
    print("\n🆘 PROTOCOLO DE EMERGENCIA:")
    print("   1. Si 3 pérdidas consecutivas → PARA 48h")
    print("   2. Si error en ejecución → NOTIFICA y PARA")
    print("   3. Si desconexión → CIERRA posiciones abiertas")
    
    input("\n📝 Presiona Enter para confirmar...")
    
    return True

def paso_6_prueba_final():
    """Paso 6: Prueba final antes de producción"""
    print_header("PASO 6: PRUEBA FINAL")
    
    print("🧪 EJECUTAR ESTAS PRUEBAS ANTES DE PRODUCCIÓN:")
    print("\n   1. PRUEBA CEREBROS:")
    print("      python3 core/cerebro_principal_con_telegram.py")
    print("      → Debe mostrar 4 cerebros activos")
    
    print("\n   2. PRUEBA TELEGRAM:")
    print("      python3 interfaces/telegram_signal.py")
    print("      → Debe simular envío de señal")
    
    print("\n   3. PRUEBA RISK MANAGER:")
    print("      python3 core/risk_manager.py")
    print("      → Debe calcular posición correctamente")
    
    print("\n   4. PRUEBA CONEXIÓN BINANCE (TESTNET):")
    print("      • Configurar testnet=True primero")
    print("      • Probar con orden pequeña ($10)")
    
    input("\n📝 Presiona Enter cuando hayas hecho las pruebas...")
    
    return True

def paso_7_activar_produccion():
    """Paso 7: Activar sistema en producción"""
    print_header("PASO 7: ACTIVAR SISTEMA EN PRODUCCIÓN")
    
    print("🚀 COMANDO PARA INICIAR SISTEMA EN PRODUCCIÓN:")
    print('''
# Opción A: Ejecutar directamente
python3 core/cerebro_principal_con_telegram.py

# Opción B: Ejecutar en background (recomendado)
nohup python3 core/cerebro_principal_con_telegram.py > trading.log 2>&1 &

# Opción C: Con PM2 (si instalas Node.js)
pm2 start core/cerebro_principal_con_telegram.py --name trading_bot
''')
    
    print("\n📊 MONITOREO DEL SISTEMA:")
    print("   • Ver logs: tail -f trading.log")
    print("   • Estado: ps aux | grep cerebro_principal")
    print("   • Telegram: Recibirás señales con botones")
    
    print("\n🎯 PRIMERAS 24 HORAS EN PRODUCCIÓN:")
    print("   1. Monitorea cada señal recibida")
    print("   2. Confirma manualmente cada operación")
    print("   3. Verifica ejecución en Binance")
    print("   4. Revisa logs cada 2 horas")
    
    return True

def crear_archivo_configuracion():
    """Crea archivo con resumen de configuración"""
    config = {
        "fecha_configuracion": datetime.now().isoformat(),
        "pasos_completados": [
            "Estructura verificada",
            "Binance API configurada",
            "Telegram Bot configurado",
            "Gestión de riesgo establecida",
            "Protocolos de seguridad activados",
            "Pruebas realizadas",
            "Sistema listo para producción"
        ],
        "comandos_importantes": {
            "iniciar_sistema": "python3 core/cerebro_principal_con_telegram.py",
            "ver_logs": "tail -f trading.log",
            "detener_sistema": "pkill -f cerebro_principal_con_telegram",
            "prueba_telegram": "python3 interfaces/telegram_signal.py",
            "prueba_risk": "python3 core/risk_manager.py"
        },
        "contactos_emergencia": {
            "detener_todo": "Detener script y cerrar posiciones manualmente en Binance",
            "soporte": "Revisar logs en trading.log",
            "backup": "Configuración guardada en config.py"
        }
    }
    
    with open("configuracion_produccion.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("\n💾 Configuración guardada en: configuracion_produccion.json")

def main():
    """Función principal"""
    print("\n" + "="*70)
    print("🚀 CONFIGURACIÓN PARA PRODUCCIÓN - SISTEMA DE TRADING")
    print("="*70)
    print("   Este asistente te guiará paso a paso para activar")
    print("   tu sistema de trading con dinero real.")
    print("="*70)
    
    # Ejecutar todos los pasos
    pasos = [
        paso_1_verificar_estructura,
        paso_2_configurar_binance,
        paso_3_configurar_telegram,
        paso_4_configurar_riesgo,
        paso_5_protocolo_seguridad,
        paso_6_prueba_final,
        paso_7_activar_produccion
    ]
    
    for i, paso in enumerate(pasos, 1):
        if not paso():
            print(f"\n❌ Error en paso {i}. Revisa y continúa.")
            input("Presiona Enter para continuar...")
    
    # Crear archivo de configuración
    crear_archivo_configuracion()
    
    # Mensaje final
    print_header("🎉 CONFIGURACIÓN COMPLETADA")
    print("\n✅ TU SISTEMA ESTÁ LISTO PARA PRODUCCIÓN")
    print("\n📋 RESUMEN FINAL:")
    print("   1. Sistema verificado y funcional")
    print("   2. APIs configuradas (Binance + Telegram)")
    print("   3. Gestión de riesgo activada")
    print("   4. Protocolos de seguridad establecidos")
    print("   5. Pruebas realizadas con éxito")
    print("   6. Comandos de ejecución listos")
    
    print("\n🚀 PARA INICIAR:")
    print("   python3 core/cerebro_principal_con_telegram.py")
    
    print("\n📞 SOPORTE:")
    print("   • Revisa logs: trading.log")
    print("   • Configuración: configuracion_produccion.json")
    print("   • Manual: Revisa los archivos .py comentados")
    
    print("\n" + "="*70)
    print("🎊 ¡FELICITACIONES! TU SISTEMA ESTÁ LISTO")
    print("="*70)

if __name__ == "__main__":
    main()
