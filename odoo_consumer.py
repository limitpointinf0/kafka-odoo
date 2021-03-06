from kafka import KafkaConsumer
from google.cloud import bigquery
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
table_name = 'pos_order_line'
topic_name = 'odoo.public.' + table_name
consumer = KafkaConsumer (
    topic_name, 
    auto_offset_reset='earliest',
    enable_auto_commit=True, 
    group_id=table_name, 
    bootstrap_servers = ['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
client = bigquery.Client.from_service_account_json('./organic-service-304712-fc78a943d386.json')
dataset_ref = client.dataset('odoo')
table_ref = dataset_ref.table('pos_order_line')
table = client.get_table(table_ref) 

# Read data from kafka
for message in consumer:
    print('Message Offset:', message.offset)
    try:
        after = message[6]['payload']['after']
        print([after])
        errors = client.insert_rows_json(table, [after])
        if errors == []:
            print("New rows have been added.")
        else:
            print("Encountered errors while inserting rows: {}".format(errors))
        # dt = datetime.datetime.now().strftime("%d_%m_%Y__%H_%M_%S")
        # filename = f'data/{table_name}_{dt}.json'
        # with open(filename, 'w') as f:
        #     json.dump(after, f, ensure_ascii=False, indent=4)
        lineNotify(json.dumps(after), 'yhe4T1V2DzScwaDHN3KBAkTCgR5r6PdFtddkoeOk9fQ')
    except Exception as e:
        print(e)
        sys.exit()
# Terminate the script
sys.exit()