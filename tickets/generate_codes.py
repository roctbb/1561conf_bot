import json

import qrcode
import uuid

def get_code():
    return str(uuid.uuid4()).split('-')[0]


codes = set()

while len(codes) < 100:
    codes.add(get_code())

with open('codes.json', 'w') as code_storage:
    json.dump(list(codes), code_storage)

for i, code in enumerate(codes):
    img = qrcode.make(code, box_size=10)
    img.save(f"codes/{i}.png")

