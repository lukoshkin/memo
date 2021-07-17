# original: https://gist.github.com/karpitsky/29b49c3ae759a606b7db39ad3c3315ca
# This code was taken from karpitsky's gist.

# Modifications:
# --------------
# Takes a collection id obtained from a public collection
# on 'translate.yandex.ru'. Writes the collection to `dict/newdict.txt`
# under the current folder.

import sys
import string
import random
import requests

from pathlib import Path


collection_id = sys.argv[1]
uid = ''.join(random.choices(string.digits, k=18))

cookies = {
    'first_visit_src': 'collection_share_desktop',
    'yandexuid': uid
}

url = f'https://translate.yandex.ru/props/api/collections/{collection_id}?srv=tr-text&uid'
response = requests.get(url, cookies=cookies).json()

Path('dict').mkdir(exist_ok=True)
with open('dict/newdict.txt', 'w') as fp:
    for pair in response['collection']['records']:
        fp.write(f'{pair["text"]} - {pair["translation"]}\n')
