import re
from datetime import datetime
from pybithumb import Bithumb
import ccxt


Bithumb_KEY =       ''
Bithumb_SECRET =    ''
bithumb =            Bithumb(Bithumb_KEY, Bithumb_SECRET)

Binance_KEY =       ''
Binance_SECRET =    ''
binance =            ccxt.binance({'enableRateLimit': True,
                                 'apiKey': Binance_KEY,
                                 'secret': Binance_SECRET,
                                 'options': {'defaultType':'future'}
                                 })

# symbols = ["SOL"]

def extract_price(exchange, input_string):

    pattern = r'\d+\.\d+'
    matches = re.findall(pattern, input_string)
    KR_price = float(matches[1])
    INT_price = float(matches[3])

    if exchange == 'KR_exchange':
        return KR_price
    elif exchange == 'INT_exchange':
        return INT_price

def extract_symbol(input_string):
    symbol_match = re.search(r'([A-Za-z0-9]+)\'s KP', input_string).group(1)
    return symbol_match

# Prompt the user for buy or sell
action = input("BUY / SELL (b/s): ")

# Validate the action
while action.lower() not in ["b", "s"]:
    print("Invalid input. Please type 'b' or 's'.")
    action = input("BUY / SELL (b/s): ")

# Prompt the user to paste their input
input_amt = float(input("AMT: "))
input_string = input("INPUT: ")

# Extract the price from both KRW/INT exchanges
bithumb_price = extract_price('KR_exchange', input_string)
binance_price = extract_price('INT_exchange', input_string)
symbol = extract_symbol(input_string)

# Order Submission
if action.lower() == "b":
    bithumb.buy_limit_order(symbol, bithumb_price, input_amt)
    binance.create_limit_sell_order(f'{symbol}/USDT', input_amt, binance_price)
    bithumb.buy_market_order('BTC', 0.01 )

elif action.lower() == "s":
    bithumb.sell_limit_order(symbol, bithumb_price, input_amt)
    binance.create_limit_buy_order(f'{symbol}/USDT', input_amt, binance_price)

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print('--------------------  O R D E R   S U B M I T T E D  --------------------')
print(f'-------------------------  {current_time}  -------------------------')
