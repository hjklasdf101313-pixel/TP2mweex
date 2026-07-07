import ccxt
import os
import time

# Ambil API Key dari Github Secrets
apiKey = os.getenv('WEEX_API_KEY')
secret = os.getenv('WEEX_SECRET_KEY')
password = os.getenv('WEEX_PASSPHRASE')

# Konek ke WEEX
exchange = ccxt.weex({
    'apiKey': apiKey,
    'secret': secret,
    'password': password,
    'enableRateLimit': True,
})

symbol = 'BTC/USDT:USDT'  # pair yg mau di trade
amount = 0.001  # lot nya

def check_balance():
    try:
        balance = exchange.fetch_balance()
        print("Balance USDT:", balance['USDT']['free'])
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    print("Bot WEEX Jalan...")
    check_balance()
