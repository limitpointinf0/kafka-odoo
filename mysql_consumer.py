from kafka import KafkaConsumer
import sys
import json
import datetime
import os
import requests
from time import sleep


def lineNotify(message, token):
    payload = {'message':message}
    return _lineNotify(payload, token)

def _lineNotify(payload, token, file=None):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization':'Bearer ' + token}
    return requests.post(url, headers=headers , data=payload, files=file)

# Initialize consumer variable and set property for JSON decode
table_name = 'customers'
topic_name = 'dbserver1.inventory.' + table_name
consumer = KafkaConsumer (
    topic_name, 
    auto_offset_reset='earliest',
    enable_auto_commit=True, 
    group_id=table_name, 
    bootstrap_servers = ['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Read data from kafka
for message in consumer:
    print('Message Offset:', message.offset)
    try:
        before = message[6]['payload']['before']
        after = message[6]['payload']['after']
        if not before and after:
            print('CREATE')
            lineNotify('CREATE -> ' + json.dumps(after), 'yhe4T1V2DzScwaDHN3KBAkTCgR5r6PdFtddkoeOk9fQ')
        if before and after:
            print('UPDATE')
            lineNotify('UPDATE -> ' + json.dumps(after), 'yhe4T1V2DzScwaDHN3KBAkTCgR5r6PdFtddkoeOk9fQ')
        if before and not after:
            print('DELETE')
            lineNotify('DELETE -> ' + json.dumps(before), 'yhe4T1V2DzScwaDHN3KBAkTCgR5r6PdFtddkoeOk9fQ')
    except Exception as e:
        print(e)
        sys.exit()
# Terminate the script
sys.exit()