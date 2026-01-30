#!/usr/bin/env python3
"""
SISTEMA DE TRADING - VERSIÓN CORREGIDA SIN ERROR DE EVENT LOOP
"""

import os
import sys
import time
import logging
import subprocess
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("trading_corregido.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def iniciar_telegram():
    """Inicia el bot de Telegram en un proceso separado"""
    print("🤖 Iniciando bot Telegram...")
    try:
        # Iniciar Telegram como proceso independiente
        telegram_proc = subprocess.Popen(
            ["python3", "interfaces/telegram_advanced.py"],
            stdout=open('telegram_out.log', 'w'),
            stderr=open('telegram_err.log', 'w')
        )
        time.sleep(5)  # Esperar que inicie
        
        # Verificar si está ejecutándose
        check = subprocess.run(
            "ps aux | grep -E 'python.*telegram_advanced' | grep -v grep",
            shell=True, capture_output=True, text=True
        )
        
        if check.stdout:
            print("✅ Bot Telegram iniciado correctamente")
            return True
        else:
            print("❌ Bot Telegram no se pudo iniciar")
            return False
            
    except Exception as e:
        print(f"❌ Error iniciando Telegram: {e}")
        return False

def iniciar_cerebros():
    """Inicia los cerebros de trading"""
    print("🧠 Iniciando 10 cerebros de trading...")
    try:
        from core.sistema_principal_futures import SistemaTrading
        sistema = SistemaTrading()
        print(f"✅ Sistema iniciado con {len(sistema.cerebros)} cerebros")
        return True
    except Exception as e:
        print(f"❌ Error iniciando cerebros: {e}")
        return False

def main():
    print("="*60)
    print("🚀 SISTEMA DE TRADING - VERSIÓN CORREGIDA")
    print("="*60)
    
    # Iniciar componentes
    telegram_ok = iniciar_telegram()
    cerebros_ok = iniciar_cerebros()
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE INICIO")
    print("="*60)
    print(f"• Telegram: {'✅ ACTIVO' if telegram_ok else '❌ INACTIVO'}")
    print(f"• Cerebros: {'✅ ACTIVOS' if cerebros_ok else '❌ INACTIVOS'}")
    print(f"• Hora: {datetime.now().strftime('%H:%M:%S')}")
    print("\n📱 Comandos Telegram:")
    print("   /start - Iniciar bot")
    print("   /status - Ver estado")
    print("   /cerebros - Listar cerebros")
    print("\n📊 Para monitorear:")
    print("   tail -f trading_corregido.log")
    print("\n⏹️  Para detener: Presiona Ctrl+C en esta terminal")
    print("="*60)
    
    # Mantener script activo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Sistema detenido")
        sys.exit(0)

if __name__ == "__main__":
    main()
