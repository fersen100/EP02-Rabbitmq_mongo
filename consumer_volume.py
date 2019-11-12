import pika
import json
import time
import uuid
import requests
from pymongo import MongoClient

cliente = MongoClient('mongodb://localhost:27017/')
banco = cliente['mydb']
db_usu = banco['usuarios']
db_volume = banco['volume']

cred = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(
    host='127.0.0.1',
    port=5672,
    virtual_host='/',
    credentials=cred
)
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='volume')

# CODIGO MONGO VAI AQUI
def callback(ch, method, properties, body):
    temp = db_usu.find().sort([("_id", -1)]).limit(1)
    print(" Volume: " + str(temp.count()))
    db_volume.update({'_id': 1},{'volume': temp.count()},upsert=True)

# CODIGO MONGO TERMINA AQUI 

channel.basic_consume(
    queue='volume', on_message_callback=callback, auto_ack=True)

print(' [*] Esperando por mensagens. Para sair pressione CTRL+C')
channel.start_consuming()