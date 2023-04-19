import json

with open('topics.txt') as file:
    topics = file.read().split('\n')

with open('topics.json', 'w') as file:
    json.dump(topics, file, ensure_ascii=False)