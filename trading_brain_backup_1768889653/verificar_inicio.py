#!/usr/bin/env python3
"""
Verificar archivo de inicio del sistema
"""
import os

print("🔍 VERIFICANDO ARCHIVO DE INICIO")
print("=" * 50)

archivo_inicio = "iniciar_sistema_futures.py"

# Verificar si existe
if not os.path.exists(archivo_inicio):
    print(f"❌ {archivo_inicio} no existe")
    print("📝 Creando archivo de inicio correcto...")
    
    contenido = '''#!/usr/bin/env python3
"""
Script simplificado para iniciar el Sistema Principal Futures
"""
import asyncio
import sys
import os

# Añadir directorio actual al path
sys.path.append('.')

async def main():
    print("🚀 Iniciando Sistema de Trading Futures...")
    print("📁 Directorio:", os.getcwd())
    
    try:
        # Importar e instanciar sistema
        from core.sistema_principal_futures import SistemaPrincipalFutures
        
        sistema = SistemaPrincipalFutures(config_path="config_futures.json")
        
        # Iniciar sistema
        print("⏳ Inicializando componentes...")
        exito = await sistema.iniciar()
        
        if exito:
            print("✅ Sistema iniciado correctamente")
            print("🔄 Ciclo de análisis en ejecución")
            print("🛑 Presiona Ctrl+C para detener")
            
            # Mantener el programa ejecutándose
            try:
                while sistema.estado == "EJECUTANDO":
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Detención solicitada por usuario")
                await sistema.detener()
        else:
            print("❌ Error al iniciar el sistema")
            
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Asegúrate de tener todos los módulos instalados")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Ejecutar el sistema
    asyncio.run(main())
'''
    
    with open(archivo_inicio, 'w') as f:
        f.write(contenido)
    
    print(f"✅ {archivo_inicio} creado")
    os.chmod(archivo_inicio, 0o755)  # Hacerlo ejecutable
    print(f"✅ Permisos de ejecución otorgados")
else:
    print(f"✅ {archivo_inicio} existe")
    
    # Verificar sintaxis
    try:
        with open(archivo_inicio, 'r') as f:
            codigo = f.read()
        compile(codigo, archivo_inicio, 'exec')
        print("✅ Sintaxis correcta")
    except SyntaxError as e:
        print(f"❌ Error de sintaxis: {e}")
        print(f"   Línea {e.lineno}: {e.text}")

# Verificar archivo de configuración
print(f"\n🔍 VERIFICANDO ARCHIVO DE CONFIGURACIÓN")
archivo_config = "config_futures.json"

if not os.path.exists(archivo_config):
    print(f"❌ {archivo_config} no existe")
    print("📝 Creando archivo de configuración básico...")
    
    config_basica = '''{
    "binance": {
        "api_key": "TU_API_KEY_AQUI",
        "api_secret": "TU_API_SECRET_AQUI",
        "testnet": true,
        "leverage": 2,
        "margin_type": "ISOLATED",
        "position_percent": 0.25,
        "risk_per_trade": 0.02
    },
    "telegram": {
        "token": "TU_BOT_TOKEN_AQUI",
        "chat_id": "TU_CHAT_ID_AQUI",
        "notificar_señales": true,
        "notificar_errores": true,
        "notificar_cierre": true
    },
    "cerebros": {
        "BTCUSDT": {
            "activo": true,
            "estrategia": "ema_ribbon_rsi"
        },
        "ETHUSDT": {
            "activo": true,
            "estrategia": "macd_bollinger"
        },
        "SOLUSDT": {
            "activo": true,
            "estrategia": "rsi_ajustado"
        },
        "LINKUSDT": {
            "activo": true,
            "estrategia": "fibonacci_ichimoku"
        },
        "BNBUSDT": {
            "activo": true,
            "estrategia": "adx_volume_profile"
        }
    },
    "sistema": {
        "intervalo_analisis": 60,
        "max_posiciones_simultaneas": 3,
        "stop_loss_diario": 0.05,
        "modo_prueba": true,
        "log_level": "INFO"
    }
}
'''
    
    with open(archivo_config, 'w') as f:
        f.write(config_basica)
    
    print(f"✅ {archivo_config} creado")
    print("⚠️  RECUERDA: Debes editar este archivo y añadir tus credenciales reales")
else:
    print(f"✅ {archivo_config} existe")
    # Verificar que sea JSON válido
    try:
        import json
        with open(archivo_config, 'r') as f:
            config = json.load(f)
        print("✅ JSON válido")
    except json.JSONDecodeError as e:
        print(f"❌ Error en JSON: {e}")

print("\n" + "=" * 50)
print("📋 PARA EJECUTAR EL SISTEMA:")
print(f"   python {archivo_inicio}")
print("\n⚠️  RECOMENDACIÓN: Ejecuta primero en modo prueba (testnet: true)")
print("   y con un intervalo de análisis mayor para pruebas")
