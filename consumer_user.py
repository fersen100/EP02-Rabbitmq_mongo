import pika
import json
import time
import uuid
import requests
from pymongo import MongoClient

cliente = MongoClient('mongodb://localhost:27017/')
banco = cliente['mydb']
posicoes_collection = banco['usuarios']

cred = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(
    host='127.0.0.1',
    port=5672,
    virtual_host='/',
    credentials=cred
)
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='usuarios')

# CODIGO MONGO VAI AQUI
def callback(ch, method, properties, body):
    bdy = body.decode()
    bdy = bdy.strip('[]"')
    evento = bdy.split('||')[0]
    mensagem = bdy.split('||')[1]
    print(" [x] Solicitacao de: %r" % evento)
    print(" [x] Recebido :%r" % mensagem)

    if evento == 'insert':
        temp = posicoes_collection.find().sort([("_id", -1)]).limit(1)
        if temp.count() == 0:
            posicoes_collection.insert({'_id': 1,'nome': mensagem})
        else:
            for doc in temp:
                admin_id = int(doc['_id']) + 1
                posicoes_collection.insert({'_id': admin_id,'nome': mensagem})
    elif evento == 'update':
        _id = int(mensagem.split('|')[0])
        nome = mensagem.split('|')[1]
        posicoes_collection.update_one({'_id':_id},{'$set':{'nome':nome}})


    elif evento == 'delete':
        posicoes_collection.delete_one({'_id':int(mensagem)})
    else:
        print("Nao foi possivel realizar nenhuma operacao")

# CODIGO MONGO TERMINA AQUI 

channel.basic_consume(
    queue='usuarios', on_message_callback=callback, auto_ack=True)

print(' [*] Esperando por mensagens. Para sair pressione CTRL+C')
channel.start_consuming()