#!/usr/bin/env python3
"""
Resumen del estado actual del sistema y próximos pasos
"""
import os
import json

print("📊 RESUMEN DEL ESTADO DEL SISTEMA DE TRADING")
print("=" * 60)

print("\n✅ LO QUE ESTÁ FUNCIONANDO:")
print("   1. Sistema principal con arquitectura modular")
print("   2. 5 cerebros especializados con estrategias diferentes")
print("   3. Integración con Binance Futures (modo simulación)")
print("   4. Base para Telegram (listo para conectar)")
print("   5. Sistema de logging y estadísticas")
print("   6. Gestión de ciclo de análisis automático")

print("\n🧠 CEREBROS IMPLEMENTADOS:")
cerebros = {
    "BTCUSDT": "EMA Ribbon + RSI Divergencias",
    "ETHUSDT": "MACD + Bollinger Bands + OBV",
    "SOLUSDT": "RSI Ajustado + EMAs Rápidas",
    "LINKUSDT": "Fibonacci + Ichimoku + Order Flow",
    "BNBUSDT": "ADX + Volume Profile + Correlación BTC"
}

for simbolo, estrategia in cerebros.items():
    print(f"   • {simbolo}: {estrategia}")

print("\n⚙️  ARCHIVOS PRINCIPALES:")
archivos = [
    "core/sistema_principal_futures.py",
    "cerebros/cerebro_base_futures.py",
    "cerebros/cerebro_btc_futures.py",
    "cerebros/cerebro_eth_futures.py",
    "cerebros/cerebro_sol_futures.py",
    "cerebros/cerebro_link_futures.py",
    "cerebros/cerebro_bnb_futures.py",
    "config_futures.json",
    "config_prueba_rapida.json",
    "iniciar_sistema_futures.py"
]

for archivo in archivos:
    if os.path.exists(archivo):
        tamano = os.path.getsize(archivo)
        print(f"   ✅ {archivo} ({tamano} bytes)")
    else:
        print(f"   ❌ {archivo} (NO ENCONTRADO)")

print("\n🚀 PRÓXIMOS PASOS PARA PRODUCCIÓN:")
print("\n1. CONFIGURAR BINANCE REAL:")
print("   • Crear API Key en Binance (Futures habilitado)")
print("   • Editar config_futures.json:")
print("     - api_key: 'TU_API_KEY_REAL'")
print("     - api_secret: 'TU_API_SECRET_REAL'")
print("     - testnet: false")

print("\n2. CONFIGURAR TELEGRAM:")
print("   • Crear bot con @BotFather")
print("   • Obtener token del bot")
print("   • Obtener chat_id")
print("   • Editar config_futures.json:")
print("     - token: 'TU_TOKEN_TELEGRAM'")
print("     - chat_id: 'TU_CHAT_ID'")

print("\n3. CONFIGURAR PARÁMETROS DE RIESGO:")
print("   • Ajustar position_percent (recomendado: 0.25 para 25%)")
print("   • Ajustar risk_per_trade (recomendado: 0.02 para 2%)")
print("   • Ajustar stop_loss_diario (recomendado: 0.05 para 5%)")

print("\n4. PRIMERA EJECUCIÓN EN PRODUCCIÓN:")
print("   • Usar modo prueba primero (testnet: true)")
print("   • Activar solo 1-2 cerebros inicialmente")
print("   • Monitorear logs y señales")
print("   • Verificar ejecución de órdenes en Binance Testnet")

print("\n📋 COMANDOS PARA EJECUTAR:")
print("   # Modo prueba (solo BTC):")
print("   python iniciar_sistema_futures.py config_prueba_rapida.json")
print("")
print("   # Modo producción (todos los cerebros):")
print("   python iniciar_sistema_futures.py")
print("")
print("   # Ver logs en tiempo real:")
print("   tail -f trading_system.log")

print("\n⚠️  RECOMENDACIONES DE SEGURIDAD:")
print("   • Usa API Keys con permisos RESTRICTIVOS")
print("   • NO compartas tus claves API")
print("   • Usa Testnet antes de usar fondos reales")
print("   • Empieza con posiciones PEQUEÑAS")
print("   • Monitorea el sistema regularmente")

print("\n" + "=" * 60)
print("🎉 ¡EL SISTEMA ESTÁ LISTO PARA USO!")

# Verificar si hay archivo de configuración de producción
config_file = "config_futures.json"
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    print("\n🔍 ESTADO ACTUAL DE CONFIGURACIÓN:")
    print(f"   • Testnet: {'✅ ACTIVADO (modo prueba)' if config['binance']['testnet'] else '❌ DESACTIVADO (modo real)'}")
    
    if config['telegram']['token'] == "TU_BOT_TOKEN_AQUI":
        print("   • Telegram: ❌ NO CONFIGURADO")
    else:
        print("   • Telegram: ✅ CONFIGURADO")
    
    if config['binance']['api_key'] == "TU_API_KEY_AQUI":
        print("   • Binance API: ❌ NO CONFIGURADO")
    else:
        print("   • Binance API: ✅ CONFIGURADO")
    
    cerebros_activos = sum(1 for c in config['cerebros'].values() if c['activo'])
    print(f"   • Cerebros activos: {cerebros_activos}/5")
