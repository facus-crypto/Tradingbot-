"""
Configuración real para Telegram Bot
"""
TELEGRAM_CONFIG = {
    # Token de tu bot
    "bot_token": "8336783544:AAFsyl628ALE9RKTInE60HnOjLHMe6mlbtw",
    
    # Tu Chat ID
    "chat_id": "213736357",
    
    # Configuración de botones
    "buttons": {
        "confirm_long": "✅ Entrar LONG",
        "confirm_short": "📉 Entrar SHORT", 
        "cancel": "❌ Cancelar",
        "close_position": "🔴 Cerrar Posición",
        "update_status": "📊 Actualizar Status"
    },
    
    # Configuración de mensajes
    "messages": {
        "signal_title": "🔔 SEÑAL DETECTADA",
        "position_open": "✅ POSICIÓN ABIERTA",
        "position_closed": "🔴 POSICIÓN CERRADA",
        "status_title": "📊 ESTADO DEL SISTEMA"
    }
}

# Comandos disponibles
TELEGRAM_COMMANDS = {
    "/start": "Iniciar bot",
    "/status": "Ver estado completo del sistema",
    "/posiciones": "Ver posiciones activas",
    "/rendimiento": "Ver P&L del día",
    "/cerrar": "Cerrar posición [símbolo]"
}

# Para importación fácil
def get_bot_token():
    return TELEGRAM_CONFIG["bot_token"]

def get_chat_id():
    return TELEGRAM_CONFIG["chat_id"]

if __name__ == "__main__":
    print("✅ Configuración Telegram cargada")
    print(f"   Bot Token: {'*' * 20}{TELEGRAM_CONFIG['bot_token'][-4:]}")
    print(f"   Chat ID: {TELEGRAM_CONFIG['chat_id']}")
