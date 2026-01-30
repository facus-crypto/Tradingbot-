#!/usr/bin/env python3
"""
SCRIPT DE PRUEBA - ENVÍA SEÑAL COMPLETA
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
import json

def enviar_prueba_completa():
    print("🚀 ENVIANDO SEÑAL DE PRUEBA COMPLETA")
    
    try:
        from interfaces.telegram_advanced import send_signal
        
        # Datos de prueba
        signal_id = f"PRUEBA_{int(time.time())}"
        
        trailing_info = {
            'phase': 1,
            'dynamic_sl': 67053.07,
            'dynamic_tp': 70474.15,
            'pnl_percent': 0.0
        }
        
        print(f"📤 Signal ID: {signal_id}")
        print("📊 Enviando señal BTC...")
        
        # Enviar señal
        success = send_signal(
            signal_id=signal_id,
            symbol="BTCUSDT",
            side="LONG",
            entry=68421.50,
            sl=67053.07,
            tp=70474.15,
            comment="🔴 SEÑAL DE PRUEBA - Sistema reparado y funcional",
            trailing_info=trailing_info
        )
        
        if success:
            print("✅ SEÑAL ENVIADA CON ÉXITO")
            print("📱 Verifica Telegram para ver:")
            print("   • Lista VERTICAL de mercados")
            print("   • Botones '✅ EJECUTAR' y '❌ CANCELAR'")
            print("   • Información completa de Trailing Stop")
            return True
        else:
            print("❌ Error al enviar señal")
            return False
            
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    enviar_prueba_completa()
