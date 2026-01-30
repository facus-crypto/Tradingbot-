#!/usr/bin/env python3
"""
Monitor de caídas del bot - Envía alerta a Telegram si el bot se cae
"""
import json
import requests
import subprocess
import time
from datetime import datetime
import os

# Cargar configuración
with open('config_futures.json', 'r') as f:
    config = json.load(f)

TOKEN = config['telegram']['token']
CHAT_ID = config['telegram']['chat_id']

# Estados
ESTADO_ANTERIOR = "desconocido"
ULTIMA_ALERTA = None

def enviar_telegram(mensaje):
    """Envía mensaje a Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": mensaje,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=data, timeout=10)
        return response.status_code == 200
    except:
        return False

def verificar_estado():
    """Verifica si el bot está corriendo"""
    try:
        # Verificar con PM2
        result = subprocess.run(['pm2', 'status', 'trading_bot'], 
                              capture_output=True, text=True)
        
        if 'online' in result.stdout:
            return "online"
        elif 'stopped' in result.stdout or 'errored' in result.stdout:
            return "stopped"
        else:
            return "desconocido"
            
    except:
        return "error"

def obtener_estadisticas():
    """Obtiene estadísticas actuales"""
    try:
        with open('stats.json', 'r') as f:
            stats = json.load(f)
        return stats
    except:
        return None

def main():
    global ESTADO_ANTERIOR, ULTIMA_ALERTA
    
    print("🔍 Iniciando monitor de caídas...")
    print(f"Chat ID: {CHAT_ID}")
    print("Monitoreando cada 30 segundos")
    print("="*50)
    
    while True:
        try:
            estado_actual = verificar_estado()
            ahora = datetime.now()
            hora_str = ahora.strftime("%H:%M:%S")
            
            print(f"[{hora_str}] Estado: {estado_actual} | Anterior: {ESTADO_ANTERIOR}")
            
            # DETECCIÓN DE CAÍDA
            if estado_actual != "online" and ESTADO_ANTERIOR == "online":
                print("⚠️  DETECTADA CAÍDA DEL SISTEMA")
                
                stats = obtener_estadisticas()
                if stats:
                    ultimo_ciclo = stats.get('ultimo_ciclo', 'desconocido')
                    ciclos = stats.get('ciclos_completados', 0)
                    
                    mensaje = f"""🚨 <b>BOT DE TRADING DETENIDO</b>

El sistema sufrió una caída y está actualmente inactivo.

• Hora de la caída: {hora_str}
• Último ciclo: {ultimo_ciclo[11:19] if len(ultimo_ciclo) > 10 else 'desconocido'}
• Ciclos completados: {ciclos}

Se reanudará automáticamente en breve."""
                else:
                    mensaje = f"""🚨 <b>BOT DE TRADING DETENIDO</b>

El sistema sufrió una caída y está actualmente inactivo.

• Hora de la caída: {hora_str}
• Estado: {estado_actual}

Se reanudará automáticamente en breve."""
                
                if enviar_telegram(mensaje):
                    print("✅ Alerta de caída enviada")
                    ULTIMA_ALERTA = ahora
            
            # DETECCIÓN DE RECUPERACIÓN
            elif estado_actual == "online" and ESTADO_ANTERIOR != "online":
                print("✅ SISTEMA RECUPERADO")
                
                tiempo_inactivo = ""
                if ULTIMA_ALERTA:
                    segundos = int((ahora - ULTIMA_ALERTA).total_seconds())
                    minutos = segundos // 60
                    segs = segundos % 60
                    tiempo_inactivo = f"{minutos} min {segs} seg"
                
                mensaje = f"""✅ <b>SISTEMA RESTAURADO</b>

El bot de trading ha sido reanudado exitosamente.

• Hora de reinicio: {hora_str}
• Tiempo inactivo: {tiempo_inactivo if tiempo_inactivo else 'desconocido'}
• Estado: 100% OPERATIVO

Reanudando análisis de los 10 pares."""
                
                if enviar_telegram(mensaje):
                    print("✅ Alerta de recuperación enviada")
            
            # Actualizar estado anterior
            ESTADO_ANTERIOR = estado_actual
            
            # Esperar 30 segundos
            time.sleep(30)
            
        except KeyboardInterrupt:
            print("\n⏹️  Monitor detenido manualmente")
            break
        except Exception as e:
            print(f"❌ Error en monitor: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
