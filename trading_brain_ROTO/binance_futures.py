"""
Módulo para operaciones con Binance Futures
Modo: ISOLATED (Aislado)
Leverage: 2X
Posición: 25% del capital por trade
"""

import hmac
import hashlib
import time
import requests
import json
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class BinanceFuturesManager:
    """Gestor de operaciones en Binance Futures"""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        """
        Inicializa el cliente de Binance Futures
        
        Args:
            api_key: API Key de Binance
            api_secret: API Secret de Binance
            testnet: True para usar testnet (recomendado para pruebas)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        
        # Configurar base URL según testnet o producción
        if testnet:
            self.base_url = "https://testnet.binancefuture.com"
            logger.info("✅ Conectado a Binance Futures TESTNET")
        else:
            self.base_url = "https://fapi.binance.com"
            logger.info("✅ Conectado a Binance Futures PRODUCCIÓN")
            
        self.recv_window = 5000
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/json'
        })
        
        # Configuración por defecto para nuestro sistema
        self.leverage = 2  # 2X leverage
        self.position_percent = 0.25  # 25% del capital por posición
        self.margin_type = "ISOLATED"  # Margen aislado
        
    def _generate_signature(self, params: Dict) -> str:
        """Genera firma HMAC SHA256 para autenticación"""
        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _signed_request(self, method: str, endpoint: str, params: Dict = None) -> Dict:
        """Realiza una petición firmada a la API"""
        if params is None:
            params = {}
            
        # Añadir timestamp y recvWindow
        params['timestamp'] = int(time.time() * 1000)
        params['recvWindow'] = self.recv_window
        
        # Generar firma
        signature = self._generate_signature(params)
        params['signature'] = signature
        
        url = f"{self.base_url}{endpoint}"
        
        if method == "GET":
            response = self.session.get(url, params=params)
        elif method == "POST":
            response = self.session.post(url, params=params)
        elif method == "DELETE":
            response = self.session.delete(url, params=params)
        else:
            raise ValueError(f"Método no soportado: {method}")
            
        response.raise_for_status()
        return response.json()
    
    def get_account_balance(self) -> Dict:
        """Obtiene el balance de la cuenta de futures"""
        endpoint = "/fapi/v2/balance"
        return self._signed_request("GET", endpoint)
    
    def get_usdt_balance(self) -> float:
        """Obtiene el balance disponible en USDT"""
        try:
            balances = self.get_account_balance()
            for balance in balances:
                if balance['asset'] == 'USDT':
                    return float(balance['availableBalance'])
            return 0.0
        except Exception as e:
            logger.error(f"Error obteniendo balance USDT: {e}")
            return 0.0
    
    def set_leverage(self, symbol: str, leverage: int = 2) -> Dict:
        """
        Configura el leverage para un símbolo
        
        Args:
            symbol: Símbolo de trading (ej: BTCUSDT)
            leverage: Leverage deseado (default: 2)
        """
        endpoint = "/fapi/v1/leverage"
        params = {
            'symbol': symbol,
            'leverage': leverage
        }
        return self._signed_request("POST", endpoint, params)
    
    def set_margin_type(self, symbol: str, margin_type: str = "ISOLATED") -> Dict:
        """
        Configura el tipo de margen para un símbolo
        
        Args:
            symbol: Símbolo de trading
            margin_type: "ISOLATED" o "CROSSED"
        """
        endpoint = "/fapi/v1/marginType"
        params = {
            'symbol': symbol,
            'marginType': margin_type
        }
        return self._signed_request("POST", endpoint, params)
    
    def get_symbol_price(self, symbol: str) -> float:
        """Obtiene el precio actual de un símbolo"""
        endpoint = "/fapi/v1/ticker/price"
        params = {'symbol': symbol}
        
        try:
            response = self.session.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()
            return float(data['price'])
        except Exception as e:
            logger.error(f"Error obteniendo precio de {symbol}: {e}")
            return 0.0
    
    def calculate_position_size(self, symbol: str, entry_price: float, stop_loss: float) -> Dict:
        """
        Calcula el tamaño de posición según el 25% del capital
        
        Args:
            symbol: Símbolo de trading
            entry_price: Precio de entrada
            stop_loss: Precio de stop loss
            
        Returns:
            Dict con cantidad, valor en USDT y riesgo
        """
        try:
            # Obtener balance disponible
            usdt_balance = self.get_usdt_balance()
            
            # Calcular 25% del capital
            capital_allocated = usdt_balance * self.position_percent
            
            # Calcular cantidad basada en entry_price
            quantity = capital_allocated / entry_price
            
            # Ajustar a los lotes permitidos por Binance
            # Primero obtener info del símbolo
            endpoint = "/fapi/v1/exchangeInfo"
            response = self.session.get(f"{self.base_url}{endpoint}")
            data = response.json()
            
            symbol_info = None
            for s in data['symbols']:
                if s['symbol'] == symbol:
                    symbol_info = s
                    break
            
            if symbol_info:
                # Ajustar cantidad al stepSize
                lot_size_filter = next(
                    (f for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE'),
                    None
                )
                
                if lot_size_filter:
                    step_size = float(lot_size_filter['stepSize'])
                    quantity = round(quantity / step_size) * step_size
            
            # Calcular riesgo
            risk_per_coin = abs(entry_price - stop_loss)
            risk_total = risk_per_coin * quantity
            
            return {
                'symbol': symbol,
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'capital_allocated': capital_allocated,
                'quantity': quantity,
                'risk_per_trade': risk_total,
                'risk_percent': (risk_total / usdt_balance) * 100 if usdt_balance > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error calculando tamaño de posición: {e}")
            return {}
    
    def place_order(self, symbol: str, side: str, quantity: float, 
                   order_type: str = "MARKET", price: float = None,
                   stop_price: float = None, sl_price: float = None,
                   tp_price: float = None) -> Dict:
        """
        Coloca una orden en Binance Futures
        
        Args:
            symbol: Símbolo de trading
            side: "BUY" o "SELL"
            quantity: Cantidad a operar
            order_type: Tipo de orden (MARKET, LIMIT, etc.)
            price: Precio para órdenes LIMIT
            stop_price: Precio de activación para STOP_MARKET
            sl_price: Precio de stop loss
            tp_price: Precio de take profit
            
        Returns:
            Dict con respuesta de la orden
        """
        endpoint = "/fapi/v1/order"
        
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
            'timeInForce': 'GTC' if order_type == 'LIMIT' else None
        }
        
        # Añadir precio si es orden LIMIT
        if order_type == "LIMIT" and price:
            params['price'] = price
            
        # Añadir stopPrice si es orden STOP
        if stop_price:
            params['stopPrice'] = stop_price
            
        logger.info(f"📊 Colocando orden: {symbol} {side} {quantity} {order_type}")
        
        try:
            # Primero configurar leverage y margen
            self.set_leverage(symbol, self.leverage)
            self.set_margin_type(symbol, self.margin_type)
            
            # Colocar orden principal
            order_result = self._signed_request("POST", endpoint, params)
            
            # Si se especificó SL o TP, colocar órdenes OCO
            if sl_price or tp_price:
                self.place_oco_order(
                    symbol=symbol,
                    side="SELL" if side == "BUY" else "BUY",  # Opuesta a la posición
                    quantity=quantity,
                    stop_price=sl_price,
                    limit_price=tp_price
                )
            
            return order_result
            
        except Exception as e:
            logger.error(f"Error colocando orden: {e}")
            return {'error': str(e)}
    
    def place_oco_order(self, symbol: str, side: str, quantity: float,
                       stop_price: float, limit_price: float) -> Dict:
        """
        Coloca una orden OCO (One-Cancels-Other) para SL y TP
        
        Args:
            symbol: Símbolo de trading
            side: "BUY" o "SELL"
            quantity: Cantidad
            stop_price: Precio de stop loss
            limit_price: Precio de take profit
        """
        endpoint = "/fapi/v1/order/oco"
        
        params = {
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'price': limit_price,
            'stopPrice': stop_price,
            'stopLimitPrice': stop_price,
            'stopLimitTimeInForce': 'GTC'
        }
        
        try:
            return self._signed_request("POST", endpoint, params)
        except Exception as e:
            logger.error(f"Error colocando orden OCO: {e}")
            return {'error': str(e)}
    
    def get_open_positions(self) -> List[Dict]:
        """Obtiene las posiciones abiertas"""
        endpoint = "/fapi/v2/positionRisk"
        return self._signed_request("GET", endpoint)
    
    def get_position(self, symbol: str) -> Optional[Dict]:
        """Obtiene información de una posición específica"""
        positions = self.get_open_positions()
        for position in positions:
            if position['symbol'] == symbol and float(position['positionAmt']) != 0:
                return position
        return None
    
    def close_position(self, symbol: str, quantity: float = None) -> Dict:
        """
        Cierra una posición abierta
        
        Args:
            symbol: Símbolo de trading
            quantity: Cantidad a cerrar (None para cerrar toda)
        """
        position = self.get_position(symbol)
        if not position:
            return {'error': 'No hay posición abierta'}
        
        position_amount = float(position['positionAmt'])
        
        # Si no se especifica cantidad, cerrar toda la posición
        if quantity is None:
            quantity = abs(position_amount)
        
        # Determinar lado opuesto
        if position_amount > 0:  # Long position
            side = "SELL"
        else:  # Short position
            side = "BUY"
            quantity = abs(quantity)
        
        return self.place_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            order_type="MARKET"
        )
    
    def cancel_all_orders(self, symbol: str) -> Dict:
        """Cancela todas las órdenes abiertas de un símbolo"""
        endpoint = "/fapi/v1/allOpenOrders"
        params = {'symbol': symbol}
        return self._signed_request("DELETE", endpoint, params)

# Singleton para acceso global
_futures_manager = None

def get_futures_manager() -> BinanceFuturesManager:
    """Obtiene la instancia global del gestor de futures"""
    global _futures_manager
    return _futures_manager

def initialize_futures_manager(config: Dict) -> BinanceFuturesManager:
    """Inicializa el gestor de futures con la configuración"""
    global _futures_manager
    
    if _futures_manager is None:
        _futures_manager = BinanceFuturesManager(
            api_key=config.get('api_key', ''),
            api_secret=config.get('api_secret', ''),
            testnet=config.get('testnet', False)
        )
        logger.info("✅ Binance Futures Manager inicializado")
    
    return _futures_manager

if __name__ == "__main__":
    # Ejemplo de uso
    import config
    manager = initialize_futures_manager(config.BINANCE_CONFIG)
    
    # Obtener balance
    balance = manager.get_usdt_balance()
    print(f"💰 Balance USDT: {balance}")
    
    # Obtener precio de BTC
    price = manager.get_symbol_price("BTCUSDT")
    print(f"📈 Precio BTCUSDT: {price}")
