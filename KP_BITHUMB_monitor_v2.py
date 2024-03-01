import requests

symbols = ['BTC']
usdkrw = 1330 #manual

while True:
    for symbol in symbols:
        # Define the symbols for Binance and Upbit
        binance_symbol =    f'{symbol}USDT'
        upbit_symbol =      f'KRW-{symbol}'
        bithumb_symbol =    f'{symbol}_KRW'

        # Get data from Binance API
        binance_endpoint =  f"https://fapi.binance.com/fapi/v1/trades?symbol={binance_symbol}&limit=1"
        binance_response =  requests.get(binance_endpoint).json()
        bin_trade_price =   float(binance_response[0]['price'])
        bin_trade_qty =     float(binance_response[0]['qty'])

        # Get data from Upbit API
        upbit_endpoint =    f"https://api.upbit.com/v1/ticker?markets={upbit_symbol}"
        upbit_response =    requests.get(upbit_endpoint, headers={"accept": "application/json"}).json()
        upbit_trade_price = upbit_response[0]['trade_price']
        upbit_trade_qty =   round(upbit_response[0]['trade_volume'] , 3)

        # Get data from Bithumb API
        bithumb_endpoint =  f"https://api.bithumb.com/public/transaction_history/{bithumb_symbol}"
        bithumb_response =  requests.get(bithumb_endpoint, headers={"accept": "application/json"}).json()
        bithumb_trade_price = float(bithumb_response['data'][-1]['price'])
        bithumb_trade_qty =   round(float(bithumb_response['data'][-1]['units_traded']) , 3)

        # # UPBIT KP
        kimchi_p =          round(( upbit_trade_price / (bin_trade_price * usdkrw) - 1 ) * 100 , 4)

        # BITHUMB KP
        # kimchi_p =          round(( bithumb_trade_price / (bin_trade_price * usdkrw) - 1 ) * 100 , 4)

    

        print(f'{symbol}\'s KP: {kimchi_p}% , BITHUMB: {bithumb_trade_price} ({bithumb_trade_qty}) , BINANCE: {bin_trade_price} ({bin_trade_qty})')
