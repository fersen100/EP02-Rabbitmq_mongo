import pika
import json
import time
import uuid
import requests
from pymongo import MongoClient

cliente = MongoClient('mongodb://localhost:27017/')
banco = cliente['mydb']
db_evento = banco['eventos']

cred = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(
    host='127.0.0.1',
    port=5672,
    virtual_host='/',
    credentials=cred
)
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='eventos')

# CODIGO MONGO VAI AQUI
def callback(ch, method, properties, body):
    bdy = body.decode()
    bdy = bdy.strip('[]"')
    print(" [x] Recebido :%r" % bdy)
    evento = bdy.split('||')[0]
    mensagem = bdy.split('||')[1]

    temp = db_evento.find().sort([("_id", -1)]).limit(1)

    if temp.count() == 0:
        db_evento.insert({'_id': 1,'evento': evento,'mensagem':mensagem})
    else:
        for doc in temp:
            admin_id = int(doc['_id']) + 1
            db_evento.insert({'_id': admin_id,'evento': evento,'mensagem':mensagem})

# CODIGO MONGO TERMINA AQUI 

channel.basic_consume(
    queue='eventos', on_message_callback=callback, auto_ack=True)

print(' [*] Esperando por mensagens. Para sair pressione CTRL+C')
channel.start_consuming()