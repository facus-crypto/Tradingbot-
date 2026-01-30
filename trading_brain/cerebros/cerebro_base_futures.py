import pandas as pd
import numpy as np
from typing import Dict, Optional
import logging
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CerebroFuturesBase:
    """Clase base para todos los cerebros de trading CON DATOS REALES."""
    
    def __init__(self, symbol: str, binance_manager=None, telegram_bot=None):
        self.symbol = symbol
        self.binance_manager = binance_manager
        self.telegram_bot = telegram_bot
        self.nombre_estrategia = "base"
        self.timeframe = "1h"
        logger.info(f"🧠 Cerebro {symbol} inicializado")
    
    def obtener_datos(self, timeframe: str, limite: int = 100) -> pd.DataFrame:
        """Obtiene datos históricos REALES de Binance."""
        try:
            # Si no hay binance_manager, usar datos simulados (para pruebas)
            if not self.binance_manager:
                logger.warning(f"{self.symbol}: Usando datos simulados (sin Binance Manager)")
                return self._datos_simulados(timeframe, limite)
            
            # Mapear timeframe a formato Binance
            tf_map = {
                "1m": "1m", "3m": "3m", "5m": "5m", "15m": "15m",
                "30m": "30m", "1h": "1h", "2h": "2h", "4h": "4h",
                "6h": "6h", "8h": "8h", "12h": "12h", "1d": "1d"
            }
            
            binance_tf = tf_map.get(timeframe, "1h")
            
            # Obtener datos de Binance
            endpoint = "/fapi/v1/klines"
            params = f"symbol={self.symbol}&interval={binance_tf}&limit={limite}"
            
            response = self.binance_manager._hacer_solicitud(endpoint, params)
            
            if not isinstance(response, list):
                logger.error(f"{self.symbol}: Respuesta inválida de Binance")
                return self._datos_simulados(timeframe, limite)
            
            # Convertir a DataFrame
            datos = []
            for vela in response:
                datos.append({
                    'timestamp': datetime.fromtimestamp(vela[0] / 1000),
                    'open': float(vela[1]),
                    'high': float(vela[2]),
                    'low': float(vela[3]),
                    'close': float(vela[4]),
                    'volume': float(vela[5])
                })
            
            df = pd.DataFrame(datos)
            df.set_index('timestamp', inplace=True)
            
            logger.info(f"{self.symbol}: {len(df)} velas reales obtenidas ({timeframe})")
            return df
            
        except Exception as e:
            logger.error(f"{self.symbol}: Error obteniendo datos: {e}")
            return self._datos_simulados(timeframe, limite)
    
    def _datos_simulados(self, timeframe: str, limite: int) -> pd.DataFrame:
        """Datos simulados como fallback."""
        # Crear fechas
        if 'm' in timeframe:
            freq = f"{timeframe.replace('m', '')}min"
        elif 'h' in timeframe:
            freq = f"{timeframe.replace('h', '')}H"
        else:
            freq = "1H"
        
        dates = pd.date_range(end=pd.Timestamp.now(), periods=limite, freq=freq)
        
        # Precios simulados (random walk)
        np.random.seed(hash(self.symbol) % 10000)
        returns = np.random.normal(0.0001, 0.02, limite)
        prices = 100 * (1 + returns).cumprod()
        
        df = pd.DataFrame({
            'open': prices * 0.995,
            'high': prices * 1.01,
            'low': prices * 0.99,
            'close': prices,
            'volume': np.random.uniform(1000, 5000, limite)
        }, index=dates)
        
        return df
    
    def analizar(self) -> Optional[Dict]:
        """Método base - debe ser sobrescrito por cada cerebro."""
        return {
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'par': self.symbol,
            'direccion': 'NEUTRAL',
            'confianza': 0.0,
            'precio_actual': 0.0,
            'indicadores': {},
            'niveles': {}
        }
    
    def enviar_senal_telegram(self, senal: Dict):
        """Envía señal a Telegram si hay bot configurado."""
        if self.telegram_bot:
            mensaje = f"🔔 {self.symbol}\nDirección: {senal['direccion']}\nConfianza: {senal['confianza']}"
            self.telegram_bot.enviar_mensaje(mensaje)
            return True
        return False
