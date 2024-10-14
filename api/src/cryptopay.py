from config import http

class Crypto:

    def __init__(self, token, testnet = False):
        self.token = str(token)
        if testnet:
            self.url = 'https://testnet-pay.crypt.bot/api'
            
        else:
            self.url = 'https://pay.crypt.bot/api'   
        self.headers = {'Content-Type': 'application/json', 'Crypto-Pay-API-Token': self.token}  
        
    async def getMe(self) -> dict:
        r = await http(f'{self.url}/getMe', headers=self.headers)
        return r
    
    async def createInvoice(self, asset: str, amount: str, params= {}) -> dict:
        params = {
            'asset': asset,
            'amount': amount,
            **params
        }
        r = await http(method="POST", url=f'{self.url}/createInvoice', params = params, headers = self.headers)
        return r.json()

    async def getInvoices(self, invoice_id) -> dict:
        params = {
            "invoice_ids" : invoice_id
        }
        r = await http(url = f'{self.url}/getInvoices', headers=self.headers, params=params)
        print(r)
        return r.json()

    async def getCurrencies(self) -> dict:
        r = await http(f'{self.url}/getCurrencies', headers=self.headers)
        return r.json()
    
    