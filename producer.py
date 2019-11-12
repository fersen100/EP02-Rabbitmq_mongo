import json
import pika
import sys
import os

operacao = [1,2,3]
in_operacao = 0
while in_operacao not in operacao:
    try:
        in_operacao = int(input("Operacoes Validas:\n1=Insert\n2=Delete\n3=Update\nDigite uma Operacao:"))
    except ValueError as error:
        print('Por favor, entre com uma operacao valida')


if in_operacao == 1:
    evento='insert'
    Mensagem = input("Nome de Usuario:")
elif in_operacao == 2:
    evento='delete'
    Mensagem = input("Id do usuario:")
elif in_operacao == 3:
    evento='update'
    in_id_usuario = input("ID do usuario antigo:")
    in_nm_usuario = input("Nome de Usuario novo:")
    Mensagem = in_id_usuario + "|" + in_nm_usuario
else:
    evento='invalida'



cred = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(
    host='127.0.0.1',
    port=5672,
    virtual_host='/',
    credentials=cred
)
connection = pika.BlockingConnection(params)
channel = connection.channel()

#Fila de usuarios
channel.queue_declare(queue='usuarios')

channel.basic_publish(exchange='',
                      routing_key='usuarios',
                      body=evento+"||"+Mensagem)

#Fila de Eventos
channel.queue_declare(queue='eventos')

channel.basic_publish(exchange='',
                      routing_key='eventos',
                      body=evento+"||"+Mensagem)

channel.queue_declare(queue='volume')

#Fila de volume
channel.basic_publish(exchange='',
                      routing_key='volume',
                      body='')

print(" [x] Mensagem enviada: '" + Mensagem + "'")

connection.close()