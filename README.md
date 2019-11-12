# EP02-Rabbitmq_mongo
Pré requisitos:                                                                                         

1- necessario ter o docker instalado                                                                                
2- necessário ter o docker compose instalado                                                                         
                                                                                                     

 Executar                                                                                             

logar no docker
comando: docker login

                                                                                        
 subir o docker-compose                                                                    
 docker-compose up --build                                                                       

                                                                                                     
executar em diferentes consoles                                                              
executar o comando: python3 consumer_event.py                                                    

                                                                                                     
executar o comando: python3 consumer_user.py                                                    

                                                                                                     
executar o comando: python3 consumer_volume.py                                                  

                                                                                                 
executar o comando: python3 producer.py                                                        
selecionar a opção que deseja realizar (1=insert,2=delete,3=update)                              
passar as informações solicitadas


## Consultar Informações
Foram criadas 3 collections no mongo para esse EP.

Eventos:
contem informações do eventos ocorridos

Usuarios
guarda todos os usuarios.

Volume
Contem o contador dos usuarios criados
