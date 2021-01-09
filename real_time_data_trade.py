import websocket, json, time, requests
import hashlib, jwt, uuid
import math
from urllib.parse import urlencode
import os

try:
    import thread
except ImportError:
    import _thread as thread


access_key = ''
secret_key = ''

price = 0
sell_price = 0
buy_price = 0

sell_cnt = 0
buy_cnt = 0
fuck_cnt = 0

def on_message(ws, message):
    json_data = json.loads(message)
    global price, sell_price, buy_price, sell_cnt, buy_cnt, fuck_cnt
    if price == 0:
        price = json_data['trade_price']
        print(price, ' [코인의 가격 설정]')
    else:
        percent = (price - json_data['trade_price']) / json_data['trade_price'] * 100
        # print('------------------------')
        # print(price)
        # print('시작 가격보다 ', percent, '변화')
        if percent < -0.3:
            if buy_price == 0:
                price = json_data['trade_price']
                print(math.trunc(price), ' [기준가 재설정]', percent, ' 퍼센트')
            else:# 매도 해야함 - 손절
                print('■□손절□■■□손절□■■□손절□■■□손절□■■□손절□■■□손절□■■□손절□■■□손절□■■□손절□■■□손절□■')
                fuck_cnt = fuck_cnt + 1
                print(math.trunc(price), ' [손절가] : ', fuck_cnt, percent, '%')
                sell_price = json_data['trade_price'] # 판매가격
                price = sell_price
                buy_price = 0
                query = {
                    'market': 'KRW-BTC',
                    'side': 'ask',
                    'volume': '0.00013',
                    # 'price': math.trunc(json_data['trade_price']),
                    # 'ord_type': 'limit',
                    'ord_type': 'market',
                }
                query_string = urlencode(query).encode()

                m = hashlib.sha512()
                m.update(query_string)
                query_hash = m.hexdigest()

                payload = {
                    'access_key': access_key,
                    'nonce': str(uuid.uuid4()),
                    'query_hash': query_hash,
                    'query_hash_alg': 'SHA512',
                }

                jwt_token = jwt.encode(payload, secret_key).decode('utf-8')
                authorize_token = 'Bearer {}'.format(jwt_token)
                headers = {"Authorization": authorize_token}

                res = requests.post('https://api.upbit.com/v1/orders', params=query, headers=headers)
                # print(res.json())
        if percent > 0.1:
            if buy_price != 0:# 익절
                if percent > 0.3:
                    print('■□익절□■■□익절□■■□익절□■■□익절□■■□익절□■■□익절□■■□익절□■■□익절□■■□익절□■■□익절□■')
                    sell_cnt = sell_cnt + 1
                    print(math.trunc(price), ' [익절가] : ', sell_cnt, percent, '%')
                    sell_price = json_data['trade_price'] # 판매가격
                    price = sell_price
                    buy_price = 0
                    query = {
                        'market': 'KRW-BTC',
                        'side': 'ask',
                        'volume': '0.00013',
                        # 'price': math.trunc(json_data['trade_price']),
                        # 'ord_type': 'limit',
                        'ord_type': 'market',
                    }
                    query_string = urlencode(query).encode()

                    m = hashlib.sha512()
                    m.update(query_string)
                    query_hash = m.hexdigest()

                    payload = {
                        'access_key': access_key,
                        'nonce': str(uuid.uuid4()),
                        'query_hash': query_hash,
                        'query_hash_alg': 'SHA512',
                    }

                    jwt_token = jwt.encode(payload, secret_key).decode('utf-8')
                    authorize_token = 'Bearer {}'.format(jwt_token)
                    headers = {"Authorization": authorize_token}

                    res = requests.post('https://api.upbit.com/v1/orders', params=query, headers=headers)
                    # print(res.json())
            else: # 매수
                print('■□매수□■■□매수□■■□매수□■■□매수□■■□매수□■■□매수□■■□매수□■■□매수□■■□매수□■■□매수□■')
                buy_cnt = buy_cnt + 1
                print(math.trunc(price), ' [매수가] : ', buy_cnt)
                buy_price = json_data['trade_price']
                price = json_data['trade_price']
                query = {
                    'market': 'KRW-BTC',
                    'side': 'bid',
                    'volume': '0.00013',
                    'price': math.trunc(json_data['trade_price']) + 50000,
                    # 'ord_type': 'price',
                    'ord_type': 'limit',
                }
                query_string = urlencode(query).encode()

                m = hashlib.sha512()
                m.update(query_string)
                query_hash = m.hexdigest()

                payload = {
                    'access_key': access_key,
                    'nonce': str(uuid.uuid4()),
                    'query_hash': query_hash,
                    'query_hash_alg': 'SHA512',
                }

                jwt_token = jwt.encode(payload, secret_key).decode('utf-8')
                authorize_token = 'Bearer {}'.format(jwt_token)
                headers = {"Authorization": authorize_token}

                res = requests.post('https://api.upbit.com/v1/orders', params=query, headers=headers)
                # print(res.json())


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        ws.send(json.dumps(
            [{"ticket": "test"}, {"type": "ticker", "codes": ["KRW-BTC"]}]))
    thread.start_new_thread(run, ())


websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://api.upbit.com/websocket/v1",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.on_open = on_open
print(ws.on_open)
ws.run_forever()