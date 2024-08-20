from binance.client import Client

        
class Kyklos:
    def __init__(self, api_key:str ,secret_key: str, client: Client) -> None:

        self.api_key = api_key
        self.secret_key = secret_key
        self.client = client

    def get_historical_data(self, symbol, interval, start_str):
        return self.client.get_historical_klines(symbol, interval, start_str)
    
    def place_order(self, symbol, side, quantity, order_type='MARKET'):
        return self.client.create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity
        )