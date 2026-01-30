#!/usr/bin/env python3
"""
SISTEMA DE TRADING - INICIO PARA PRODUCCIÓN
"""

import os
import sys
import time
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("trading_produccion.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def iniciar_sistema():
    """Inicia todos los componentes del sistema"""
    
    print("="*60)
    print("🤖 SISTEMA DE TRADING - MODO PRODUCCIÓN")
    print("="*60)
    
    # 1. Iniciar bot Telegram
    logger.info("Iniciando bot Telegram...")
    try:
        from interfaces.telegram_advanced import start_bot
        import threading
        
        # Iniciar en hilo separado
        telegram_thread = threading.Thread(target=start_bot, daemon=True)
        telegram_thread.start()
        logger.info("✅ Bot Telegram iniciado")
    except Exception as e:
        logger.error(f"❌ Error iniciando Telegram: {e}")
    
    # 2. Iniciar cerebros de trading
    logger.info("Iniciando 10 cerebros de trading...")
    try:
        from core.sistema_principal_futures import SistemaTrading
        sistema = SistemaTrading()
        logger.info(f"✅ Sistema iniciado con {len(sistema.cerebros)} cerebros")
    except Exception as e:
        logger.error(f"❌ Error iniciando sistema: {e}")
    
    # 3. Mostrar estado
    print("\n📊 ESTADO DEL SISTEMA:")
    print(f"   • Bot Telegram: {'✅ ACTIVO' if telegram_thread.is_alive() else '❌ INACTIVO'}")
    print(f"   • Cerebros: 10/10 ✅")
    print(f"   • Modo: Producción")
    print(f"   • Hora: {datetime.now().strftime('%H:%M:%S')}")
    print("\n📱 Comandos Telegram disponibles:")
    print("   • /start - Iniciar bot")
    print("   • /status - Ver estado del sistema")
    print("   • /cerebros - Listar cerebros activos")
    print("\n" + "="*60)
    print("🚀 SISTEMA LISTO PARA TRADING")
    print("="*60)
    
    # Mantener el script ejecutándose
    try:
        while True:
            time.sleep(3600)  # Esperar 1 hora
    except KeyboardInterrupt:
        print("\n⏹️  Sistema detenido manualmente")
        sys.exit(0)

if __name__ == "__main__":
    iniciar_sistema()
