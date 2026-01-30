"""
INTERFAZ TELEGRAM SIMPLIFICADA - Para conectar cerebros con Telegram
"""
import logging
from datetime import datetime
from typing import Dict
import asyncio

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class InterfazTelegramSimple:
    """Versión simple de interfaz Telegram para pruebas"""
    
    def __init__(self, modo_prueba=True):
        self.modo_prueba = modo_prueba
        self.senales_pendientes = {}
        logging.info("📱 Interfaz Telegram Simple creada (modo prueba)")
    
    async def enviar_senal(self, senal_dict: Dict) -> bool:
        """Simula envío de señal a Telegram"""
        try:
            simbolo = senal_dict.get("simbolo", "DESCONOCIDO")
            
            print("\n" + "="*60)
            print("📱 TELEGRAM - SEÑAL DETECTADA")
            print("="*60)
            
            print(f"\n🔔 NUEVA SEÑAL DE TRADING")
            print(f"   Símbolo: {simbolo}")
            print(f"   Dirección: {senal_dict.get('direccion', 'N/A')}")
            print(f"   Fuerza: {senal_dict.get('fuerza', 0)}/10")
            print(f"   Precio: ${senal_dict.get('precio_entrada', 0):.2f}")
            
            if senal_dict.get('razones'):
                print(f"   Razones principales:")
                for i, razon in enumerate(senal_dict['razones'][:3], 1):
                    print(f"     {i}. {razon}")
            
            # Simular cálculo de riesgo básico
            precio = senal_dict.get('precio_entrada', 1)
            cantidad = 0.1 if "BTC" in simbolo else 1.0
            
            print(f"\n   📊 POSICIÓN CALCULADA (SIMULADA):")
            print(f"     • Cantidad: {cantidad}")
            print(f"     • Valor: ${cantidad * precio:.2f}")
            print(f"     • Stop Loss: ${precio * 0.98:.2f}")
            print(f"     • Take Profit: ${precio * 1.03:.2f}")
            
            print(f"\n   ⏰ En producción real:")
            print(f"     → Se enviaría mensaje a Telegram con botones")
            print(f"     → Botones: [✅ CONFIRMAR] [❌ CANCELAR]")
            print(f"     → Esperaría tu confirmación manual")
            
            # Guardar señal
            self.senales_pendientes[simbolo] = senal_dict
            logging.info(f"✅ Señal {simbolo} preparada para Telegram")
            
            return True
            
        except Exception as e:
            logging.error(f"Error enviando señal: {e}")
            return False
    
    def get_estado(self) -> Dict:
        """Devuelve estado de la interfaz"""
        return {
            "senales_pendientes": len(self.senales_pendientes),
            "modo_prueba": self.modo_prueba,
            "funcionando": True
        }

# Función principal para probar
async def prueba_interfaz():
    """Prueba la interfaz Telegram"""
    print("\n🧪 PRUEBA INTERFAZ TELEGRAM")
    print("=" * 50)
    
    # Crear interfaz
    interfaz = InterfazTelegramSimple(modo_prueba=True)
    
    # Crear señal de prueba (como la generaría un cerebro)
    señal_prueba = {
        "simbolo": "BTCUSDT",
        "direccion": "LONG",
        "fuerza": 8,
        "razones": [
            "EMA Ribbon alineado alcista",
            "Divergencia RSI alcista semanal",
            "Volumen 2.5x promedio",
            "Precio en soporte EMA 21"
        ],
        "precio_entrada": 52000.50,
        "timestamp": datetime.now()
    }
    
    # Enviar señal
    print("\n1. Simulando detección de señal por cerebro BTC...")
    exito = await interfaz.enviar_senal(señal_prueba)
    
    if exito:
        print("\n2. Estado de la interfaz:")
        estado = interfaz.get_estado()
        for key, value in estado.items():
            print(f"   • {key}: {value}")
        
        print("\n3. En modo PRODUCCIÓN real:")
        print("   • El mensaje llegaría a tu Telegram")
        print("   • Tendrías 5 minutos para confirmar")
        print("   • Al confirmar, se ejecutaría en Binance")
        print("\n✅ Prueba completada exitosamente")
    else:
        print("❌ Error en la prueba")

# Ejecutar prueba si se llama directamente
if __name__ == "__main__":
    asyncio.run(prueba_interfaz())
