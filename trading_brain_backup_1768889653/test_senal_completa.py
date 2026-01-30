import sys
import asyncio
sys.path.insert(0, '/data/data/com.termux/files/home/bot_trading/trading_brain')

# Clase simple para simular trading_executor
class MockTradingExecutor:
    async def process_signal(self, symbol, action, price, stop_loss, take_profit):
        print(f"📊 [MOCK] Procesando señal:")
        print(f"   • Símbolo: {symbol}")
        print(f"   • Acción: {action}")
        print(f"   • Precio: {price}")
        print(f"   • Stop Loss: {stop_loss}")
        print(f"   • Take Profit: {take_profit}")
        return {"success": True, "order_id": "MOCK123"}

async def enviar_senal_completa():
    try:
        from interfaces.telegram_advanced import TelegramAdvancedBot
        
        print("🤖 Creando bot de Telegram con botones...")
        
        # Crea instancia con mock executor
        bot = TelegramAdvancedBot(
            bot_token='8336783544:AAFsyl628ALE9RKTInE60HnOjLHMe6mlbtw',
            chat_id='213736357',
            trading_executor=MockTradingExecutor()
        )
        
        print("✅ Bot creado")
        
        # Inicia el bot (necesario para recibir callbacks)
        await bot.start()
        print("✅ Bot iniciado y escuchando")
        
        # Espera 2 segundos para que se inicialice
        await asyncio.sleep(2)
        
        # Datos de señal realista
        signal_data = {
            'symbol': 'BTCUSDT',
            'action': 'LONG',
            'price': 45234.56,
            'stop_loss': 44500.00,
            'take_profit': 46500.00,
            'reason': '🔔 EMA Ribbon alineación alcista + RSI oversold\n📊 Volumen acumulativo positivo\n⚡ Momentum alcista confirmado',
            'timestamp': '2024-01-15 19:15:00',
            'indicators': {
                'rsi': 32.4,
                'macd': 'Bullish crossover',
                'ema_ribbon': 'Alineado alcista',
                'volume': 'Alto acumulativo'
            }
        }
        
        print("📡 Enviando señal con botones a Telegram...")
        
        # Envía la señal
        message_id = await bot.send_signal(signal_data)
        
        if message_id:
            print(f"🎉 ✅ Señal enviada exitosamente!")
            print(f"   • Message ID: {message_id}")
            print(f"   • Revisa tu Telegram para ver los botones")
            print(f"   • Botones esperados: ✅ CONFIRMAR | ❌ CANCELAR")
        else:
            print("❌ Error enviando señal")
            
        # Mantén el bot corriendo por 30 segundos para que puedas interactuar
        print("\n⏰ Bot activo por 30 segundos...")
        print("   • Ve a Telegram y prueba los botones")
        print("   • Luego vuelve aquí y presiona Ctrl+C")
        
        await asyncio.sleep(30)
        
        await bot.stop()
        print("✅ Bot detenido")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

# Ejecutar
if __name__ == "__main__":
    print("="*60)
    print("🚀 PRUEBA DE SEÑAL COMPLETA CON BOTONES")
    print("="*60)
    asyncio.run(enviar_senal_completa())
