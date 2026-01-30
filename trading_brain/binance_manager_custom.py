"""Binance Manager personalizado que usa requests+hmac (como tu script funciona)"""
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
            if method == "POST":
                response = requests.post(url, headers=headers)
            else:
                response = requests.get(url, headers=headers)
            
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"❌ Error en solicitud: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"   Respuesta: {e.response.text}")
            return {"error": str(e)}
