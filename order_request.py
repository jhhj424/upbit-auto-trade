import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

access_key = ''
secret_key = ''

# 시장가 매수
# query = {
#     'market': 'KRW-ETH',
#     'side': 'bid',
#     'volume': '0.005',
#     'price': '100.0',
#     'ord_type': 'price',
# }
# 시장가 매도
# query = {
#     'market': 'KRW-ETH',
#     'side': 'ask',
#     'volume': '0.0015',
#     'price': '100.0',
#     'ord_type': 'market',
# }
query = {
    'market': 'KRW-BTC',
    'side': 'ask',
    'volume': '0.00015',
    'price': '100.0',
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