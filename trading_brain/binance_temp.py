    def ejecutar_orden(self, symbol: str, side: str, quantity: float, 
                      price: float = None, order_type: str = "MARKET"):
        """Ejecuta orden en Binance Futures."""
        try:
            endpoint = "/fapi/v1/order"
            
            # Parámetros base
            params = f"symbol={symbol}&side={side}&type={order_type}&quantity={quantity}"
            
            # Si es LIMIT, agregar precio
            if order_type == "LIMIT" and price:
                params += f"&price={price}&timeInForce=GTC"
            
            response = self._hacer_solicitud(endpoint, params, method="POST")
            
            if isinstance(response, dict) and response.get('status') in ['NEW', 'FILLED']:
                logger.info(f"✅ Orden ejecutada: {symbol} {side} {quantity}")
                return response
            else:
                logger.error(f"❌ Error ejecutando orden: {response}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error ejecutando orden {symbol}: {e}")
            return None
    
    def obtener_balance_disponible(self):
        """Obtiene balance disponible en USDT."""
        try:
            endpoint = "/fapi/v2/balance"
            response = self._hacer_solicitud(endpoint, "")
            
            if isinstance(response, list):
                for asset in response:
                    if asset['asset'] == 'USDT':
                        return float(asset['availableBalance'])
            return 0.0
        except Exception as e:
            logger.error(f"❌ Error obteniendo balance: {e}")
            return 0.0
    
    def calcular_tamanio_posicion(self, symbol: str, porcentaje_capital: float = 0.25, 
                                  apalancamiento: int = 2):
        """Calcula tamaño de posición para % de capital con apalancamiento."""
        try:
            # Obtener balance
            balance = self.obtener_balance_disponible()
            if balance <= 0:
                logger.error("❌ Balance insuficiente")
                return 0.0
            
            # Capital a arriesgar
            capital_riesgo = balance * porcentaje_capital
            
            # Obtener precio actual
            endpoint_price = "/fapi/v1/ticker/price"
            params_price = f"symbol={symbol}"
            response_price = self._hacer_solicitud(endpoint_price, params_price)
            
            if not isinstance(response_price, dict) or 'price' not in response_price:
                return 0.0
            
            precio = float(response_price['price'])
            
            # Calcular cantidad (con apalancamiento)
            valor_posicion = capital_riesgo * apalancamiento
            cantidad = valor_posicion / precio
            
            logger.info(f"💰 Calculado: Balance ${balance:.2f}, {porcentaje_capital*100}% = ${capital_riesgo:.2f}, {apalancamiento}x = ${valor_posicion:.2f}, {cantidad:.6f} {symbol}")
            return cantidad
            
        except Exception as e:
            logger.error(f"❌ Error calculando tamaño: {e}")
            return 0.0
