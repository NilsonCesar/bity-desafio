import requests, copy, time

saldo_original = {"BRL": 10 ** 5, "BTC": 3, "USDT": 10 ** 5, "ETH": 10}
saldo_atual = copy.deepcopy(saldo_original)

def checa_arbitragem(preco_compra, preco_venda, quantidade, moeda):
    if preco_compra < preco_venda:
            saldo_atual["BRL"] -= preco_compra
            saldo_atual[moeda] += quantidade
            print("Saldo original:", saldo_original[moeda])
            print("Saldo atual:", saldo_atual[moeda])


while True:
    bit = {
        "ETH": requests.get("https://api.bitpreco.com/eth-brl/orderbook").json(),
        "BTC": requests.get("https://api.bitpreco.com/btc-brl/orderbook").json(),
        "USDT": requests.get("https://api.bitpreco.com/usdt-brl/orderbook").json()
    }
    
    bin = {
        "ETH": requests.get("https://api.binance.com/api/v3/depth?symbol=ETHBRL").json(),
        "BTC": requests.get("https://api.binance.com/api/v3/depth?symbol=BTCBRL").json(),
        "USDT": requests.get("https://api.binance.com/api/v3/depth?symbol=USDTBRL").json()
    }

    for moeda in bit.keys():
        print(float(bin[moeda]["asks"][0][0]), bit[moeda]["bids"][0]["price"])
        preco_compra_bin = float(bin[moeda]["bids"][0][0])
        preco_venda_bit = bit[moeda]["asks"][0]["price"]
        quantidade_bit =  bit[moeda]["asks"][0]["amount"]

        checa_arbitragem(preco_compra_bin, preco_venda_bit, quantidade_bit, moeda)

        preco_compra_bit = bit[moeda]["bids"][0]["price"] 
        preco_venda_bin = float(bin[moeda]["asks"][0][0])
        quantidade_bin = float(bin[moeda]["asks"][0][1])

        checa_arbitragem(preco_compra_bit, preco_venda_bin, quantidade_bin, moeda)

    time.sleep(3)