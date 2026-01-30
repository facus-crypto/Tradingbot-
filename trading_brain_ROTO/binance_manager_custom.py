
"""
Binance Manager personalizado que usa requests+hmac (como tu script funciona)
"""
import requests
import time
import hashlib
import hmac
import json
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class BinanceFuturesManagerCustom:
    """Gestor personalizado de Binance Futures usando requests+hmac"""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        # Configurar endpoints según testnet o real
        if testnet:
            self.base_url = "https://testnet.binancefuture.com"
            logger.warning("⚠️  Usando TESTNET (fondos virtuales)")
        else:
            self.base_url = "https://fapi.binance.com"
            logger.warning("⚠️  Usando BINANCE REAL (dinero real)")
        
        logger.info(f"✅ Binance Manager Custom inicializado")
        logger.info(f"   • Base URL: {self.base_url}")
        logger.info(f"   • API Key: {self.api_key[:15]}...")
    
    def _crear_firma(self, params: str = "") -> str:
        """Crear firma HMAC SHA256 (igual que tu script)"""
        timestamp = int(time.time() * 1000)
        query = f"{params}&timestamp={timestamp}" if params else f"timestamp={timestamp}"
        signature = hmac.new(
            self.api_secret.encode(),
            query.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"{query}&signature={signature}"
    
    def _hacer_solicitud(self, endpoint: str, params: str = "", method: str = "GET") -> Dict:
        """Hacer solicitud HTTP firmada"""
        query_firmada = self._crear_firma(params)
        url = f"{self.base_url}{endpoint}?{query_firmada}"
        headers = {"X-MBX-APIKEY": self.api_key}
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=headers, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                raise ValueError(f"Método no soportado: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error en solicitud: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"   Respuesta: {e.response.text}")
            raise
    
    async def get_balance(self) -> float:
        """Obtener balance de USDT"""
        try:
            data = self._hacer_solicitud("/fapi/v2/account")
            
            # Buscar balance USDT
            assets = data.get('assets', [])
            usdt_balance = next(
                (a for a in assets if a['asset'] == 'USDT'),
                {'walletBalance': '0'}
            )
            
            balance = float(usdt_balance.get('walletBalance', 0))
            logger.info(f"💰 Balance: {balance:.2f} USDT")
            return balance
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo balance: {e}")
            return 0.0
    
    def get_symbol_price(self, symbol: str) -> float:
        """Obtener precio actual de un símbolo"""
        try:
            # Usar endpoint público para precio
            if self.testnet:
                url = f"https://testnet.binancefuture.com/fapi/v1/ticker/price?symbol={symbol}"
            else:
                url = f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            price = float(data.get('price', 0))
            logger.debug(f"📈 {symbol}: {price:.2f}")
            return price
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo precio de {symbol}: {e}")
            return 0.0
    
    async def get_positions(self) -> List[Dict]:
        """Obtener posiciones activas"""
        try:
            data = self._hacer_solicitud("/fapi/v2/account")
            positions = data.get('positions', [])
            
            # Filtrar solo posiciones con cantidad != 0
            active_positions = [
                p for p in positions 
                if float(p.get('positionAmt', 0)) != 0
            ]
            
            logger.info(f"📊 Posiciones activas: {len(active_positions)}")
            return active_positions
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo posiciones: {e}")
            return []
    
    async def set_leverage(self, leverage: int):
        """Configurar leverage (simulado por ahora)"""
        logger.info(f"⚙️  Leverage configurado a {leverage}X (simulado)")
        # Implementación real requeriría endpoint específico
    
    async def set_margin_type(self, margin_type: str):
        """Configurar tipo de margen (simulado por ahora)"""
        logger.info(f"⚙️  Margen configurado a {margin_type} (simulado)")

# Instancia global para usar en el sistema
binance_manager_instance = None

def get_binance_manager(api_key: str, api_secret: str, testnet: bool = False):
    """Obtener instancia del gestor Binance"""
    global binance_manager_instance
    if binance_manager_instance is None:
        binance_manager_instance = BinanceFuturesManagerCustom(api_key, api_secret, testnet)
    return binance_manager_instance
