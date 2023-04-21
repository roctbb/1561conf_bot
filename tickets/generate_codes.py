import json

import qrcode
import uuid

def get_code():
    return str(uuid.uuid4()).split('-')[0]

try:
    with open('codes.json') as code_storage:
        codes = json.load(code_storage)
except:
    codes = []

while len(codes) < 200:
    code = get_code()
    if code not in codes:
        codes.append(code)

with open('codes.json', 'w') as code_storage:
    json.dump(list(codes), code_storage)

for i, code in enumerate(codes):
    img = qrcode.make(code, box_size=10)
    img.save(f"codes/{i}.png")

