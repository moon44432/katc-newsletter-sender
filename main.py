from datetime import datetime
from sender import send, _send
from crawler import *
from get_price import *
import pyupbit
import time

access = "g5X0EuacugSKsD90jxbryNpYpGdny9RnW4ksZEfs"
secret = "Ee95di0rNoh84ulXGGQKwGl4j1mIPjPxxBJo04aM"
upbit = pyupbit.Upbit(access, secret)


def send_news():
    soup = get(BASE_ADDRESS + 'main/home.nhn')
    sections = soup.find_all('div', {'class': 'main_component droppable'})

    overview = []
    for section in sections:
        overview.append(get_overview(section))

    overview_output = '\n'.join(overview)

    headline_section = sections[0]
    headlines_details_output = get_details(headline_section)

    now = '{:%Y-%m-%d_%H}H'.format(datetime.now())
    send(f'[NEWS] NEWS OVERVIEW ({now})', overview_output)
    send(f'[NEWS] ARTICLE SNIPPETS ({now})', headlines_details_output)

    print(overview_output)
    print(headlines_details_output)


def send_crypto_info():
    crypt = []

    crypt.append(get_data('upbit', 'KRW-BTC'))
    crypt.append(get_data('upbit', 'KRW-ETH'))
    crypt.append(get_data('upbit', 'KRW-ETC'))
    crypt.append(get_data('upbit', 'KRW-XRP'))
    crypt.append(get_data('upbit', 'KRW-DOGE'))
    crypt.append(get_data('coinone', 'klay'))
    crypt.append(get_data('coinone', 'ksp'))

    output = ""

    now = '{:%Y-%m-%d %H:%M}'.format(datetime.now())
    output += ('<p>' + now + " 기준</p>")
    output += (f'<p>{"종목명":>8} | {"시초가":>8} | {"고가":>9} | {"저가":>9} | {"현재가":>8} | {"전일대비":>3}</p>')

    for curr in crypt:
        output += (f'<p>{curr[0]:>10} | {curr[1]:>10} | {curr[2]:>10} | {curr[3]:>10} | {curr[4]:>10} | {(curr[5] * 100):.2}%</p>')

    krw = upbit.get_balance("KRW")
    eth = upbit.get_balance("KRW-ETH")
    output += ('KRW:' + str(krw) + ', ETH: ' + str(eth) + '\n')
    output += (' Total(KRW): ' + str(krw + eth * pyupbit.get_current_price('KRW-ETH')) + '\n')

    send(f'CRYPTO OVERVIEW ({now})', output)

    print(output)


if __name__ == '__main__':
    sent = False
    while True:
        try:
            now = datetime.now()
            if now.hour == 8 and now.minute == 59:
                if not sent:
                    send_news()
                    send_crypto_info()
                    sent = True
            else:
                sent = False
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)
