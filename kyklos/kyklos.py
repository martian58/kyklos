from binance import Client

class Kyklos:

    def __init__(self,
                  api_key: str,
                  secret_key: str,
                  ) -> None:
        
        self.api_key = api_key
        self.secret_key = secret_key
        self.client = Client(self.api_key,self.secret_key)


        