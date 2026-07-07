from flask import Flask, request
import ccxt
import os

app = Flask(__name__)

exchange = ccxt.weex({
    'apiKey': os.environ.get('WEEX_API_KEY'),
    'secret': os.environ.get('WEEX_API_SECRET'),
    'enableRateLimit': True,
    'options': {'defaultType': 'swap'}
})

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    
    if data.get('action') == 'entry':
        symbol_tv = data.get('symbol')
        symbol = symbol_tv.replace("USD", "/USDT")
        
        try:
            # 1. SET LEVERAGE 400x
            exchange.set_leverage(400, symbol)
            
            # 2. HITUNG 0.1% DARI BALANCE
            balance = exchange.fetch_balance()
            usdt_balance = balance['USDT']['free']
            amount_usdt = usdt_balance * 0.01
            
            # 3. DAPATIN HARGA & HITUNG QTY
            ticker = exchange.fetch_ticker(symbol)
            price = ticker['last']
            qty = amount_usdt / price
            qty = exchange.amount_to_precision(symbol, qty)
            
            # 4. BUKA POSISI SHORT
            order = exchange.create_market_sell_order(symbol, qty)
            
            # 5. SET TP 400% 
            entry_price = order['average']
            tp_price = entry_price * 0.99
            tp_price = exchange.price_to_precision(symbol, tp_price)
            
            exchange.create_limit_sell_order(symbol, qty, tp_price)
            
            print(f"SUKSES: SHORT {symbol} Qty:{qty} Leverage:400x TP:{tp_price}")
            return "Order executed", 200
            
        except Exception as e:
            print("ERROR:", e)
            return str(e), 400
        
    return "ok", 200

@app.route("/")
def home():
    return "Bot WEEX Jalan", 200
