#!/usr/bin/env python3
"""
Monitor mejorado - Verifica estado PM2 Y actividad real
"""
import json
import requests
import subprocess
import time
from datetime import datetime

# Cargar configuración
with open('config_futures.json', 'r') as f:
    config = json.load(f)

TOKEN = config['telegram']['token']
CHAT_ID = config['telegram']['chat_id']

# Estados
ESTADO_ANTERIOR = "desconocido"
ULTIMA_ALERTA = None
ULTIMA_ACTIVIDAD = None

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
        # pm2 show es más específico
        cmd = ['pm2', 'show', 'trading_bot']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Buscar la línea con "status"
        for linea in result.stdout.split('\n'):
            linea = linea.strip().lower()
            if 'status' in linea and '│' in linea:
                if 'online' in linea:
                    return "online"
                elif 'stopped' in linea:
                    return "stopped"
                elif 'errored' in linea:
                    return "errored"
        
        return "desconocido"
            
    except Exception as e:
        print(f"Error: {e}")
        return "error"

def verificar_actividad():
    """Verifica actividad real (último ciclo)"""
    try:
        with open('stats.json', 'r') as f:
            stats = json.load(f)
        
        ultimo_ciclo_str = stats.get('ultimo_ciclo', '')
        if not ultimo_ciclo_str:
            return None, "no_hay_datos"
        
        ultimo_ciclo = datetime.fromisoformat(ultimo_ciclo_str)
        ahora = datetime.now()
        diferencia_segundos = (ahora - ultimo_ciclo).total_seconds()
        diferencia_minutos = diferencia_segundos / 60
        
        return ultimo_ciclo, diferencia_minutos
        
    except Exception as e:
        print(f"Error verificando actividad: {e}")
        return None, "error"

def main():
    global ESTADO_ANTERIOR, ULTIMA_ALERTA, ULTIMA_ACTIVIDAD
    
    print("🔍 Monitor mejorado iniciado")
    print("Chat:", CHAT_ID)
    print("Verificando estado PM2 Y actividad cada 30s")
    print("="*50)
    
    while True:
        try:
            estado = verificar_estado()
            hora = datetime.now().strftime("%H:%M:%S")
            
            # Verificar actividad real
            ultimo_ciclo, dif_minutos = verificar_actividad()
            
            if ultimo_ciclo:
                print(f"[{hora}] Estado: {estado} | Últ.actividad: {dif_minutos:.1f} min")
            else:
                print(f"[{hora}] Estado: {estado} | Actividad: {dif_minutos}")
            
            # ========== DETECCIÓN DE CAÍDA (PM2) ==========
            if estado != "online" and ESTADO_ANTERIOR == "online":
                print(f"⚠️  CAÍDA DETECTADA: {estado}")
                
                mensaje = f"""🚨 <b>BOT DE TRADING DETENIDO</b>

El sistema sufrió una caída y está actualmente inactivo.

• Hora: {hora}
• Estado: {estado}

Se reanudará automáticamente en breve."""
                
                if enviar_telegram(mensaje):
                    print("✅ Alerta de caída enviada")
                    ULTIMA_ALERTA = datetime.now()
            
            # ========== DETECCIÓN DE INACTIVIDAD (aunque PM2 diga online) ==========
            elif estado == "online" and dif_minutos != "error" and dif_minutos != "no_hay_datos":
                if dif_minutos > 15:  # Más de 15 minutos sin actividad
                    print(f"⚠️  INACTIVIDAD DETECTADA: {dif_minutos:.1f} min sin ciclo")
                    
                    # Solo alertar si no alertamos hace más de 30 minutos
                    if not ULTIMA_ACTIVIDAD or (datetime.now() - ULTIMA_ACTIVIDAD).total_seconds() > 1800:
                        mensaje = f"""⚠️ <b>BOT INACTIVO</b>

El bot aparece como "online" pero no ha analizado en {dif_minutos:.0f} minutos.

• Hora: {hora}
• Último ciclo: {ultimo_ciclo.strftime('%H:%M:%S')}
• Minutos sin actividad: {dif_minutos:.0f}

Posible congelamiento del sistema."""
                        
                        if enviar_telegram(mensaje):
                            print("✅ Alerta de inactividad enviada")
                            ULTIMA_ACTIVIDAD = datetime.now()
            
            # ========== DETECCIÓN DE RECUPERACIÓN ==========
            elif estado == "online" and ESTADO_ANTERIOR != "online":
                print("✅ RECUPERACIÓN DETECTADA")
                
                tiempo = ""
                if ULTIMA_ALERTA:
                    seg = int((datetime.now() - ULTIMA_ALERTA).total_seconds())
                    min = seg // 60
                    segs = seg % 60
                    tiempo = f"{min} min {segs} seg"
                
                mensaje = f"""✅ <b>SISTEMA RESTAURADO</b>

El bot de trading ha sido reanudado exitosamente.

• Hora: {hora}
• Inactivo: {tiempo if tiempo else 'desconocido'}
• Estado: OPERATIVO

Reanudando análisis."""
                
                if enviar_telegram(mensaje):
                    print("✅ Alerta recuperación enviada")
            
            ESTADO_ANTERIOR = estado
            time.sleep(30)
            
        except KeyboardInterrupt:
            print("\n⏹️  Monitor detenido manualmente")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
