import json
import urllib.request


def get_data(market, ticker):
    tk = [ticker]
    if market == 'coinone':
        return tk + get_from_coinone(ticker)
    if market == 'upbit':
        return tk + get_from_upbit(ticker)


def get_from_coinone(ticker):
    urlTicker = urllib.request.urlopen('https://api.coinone.co.kr/ticker/?currency='+ticker)
    readTicker = urlTicker.read()
    jsonTicker = json.loads(readTicker)

    data = []

    l = float(jsonTicker['last'])
    yc = float(jsonTicker['yesterday_last'])
    data.append(float(jsonTicker['first']))
    data.append(float(jsonTicker['high']))
    data.append(float(jsonTicker['low']))
    data.append(l)
    data.append(float((l - yc) / yc))

    return data


def get_from_upbit(ticker):
    urlTicker = urllib.request.urlopen('https://api.upbit.com/v1/ticker?markets='+ticker)
    readTicker = urlTicker.read()
    jsonTicker = json.loads(readTicker)

    data = []

    data.append(float(jsonTicker[0]['opening_price']))
    data.append(float(jsonTicker[0]['high_price']))
    data.append(float(jsonTicker[0]['low_price']))
    data.append(float(jsonTicker[0]['trade_price']))
    data.append(float(jsonTicker[0]['signed_change_rate']))

    return data

