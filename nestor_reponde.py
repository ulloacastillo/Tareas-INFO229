import json
import requests
from slack import WebClient
import slack
import os


TOKEN = os.environ.get("SLACK_TOKEN")

#OBTENER DEL NAVEGADOR:
#                       IR A ESPACIO DE TRABAJO Y SELECCIONAR CANAL
#                       EL CHANNEL ID SERA LA ULTIMA SERIE DE DIGITOS-LETRAS ESE LINK
#                       https://app.slack.com/client/XXXXXXXXXXX/C01CB597ZA6

channelId = "C01CB597ZA6"

client = WebClient(token=TOKEN)
#client.chat_postMessage(channel="#general", text="Holaaaa")


slack_url = "https://slack.com/api/conversations.history?token=" + TOKEN + "&channel=" + channelId

messages = requests.get(slack_url).json()


mensajes = messages['messages']

'''
print(mensajes)
print(len(mensajes))

for i in mensajes:
   print(i.keys(), end=" ")
   print(i['text'])
'''

ultimo = mensajes[0]['text']

#print(ultimo)
ID_ultimo = ultimo.split(" ")[-1]
ID_ultimo = ultimo.split(" ")[-1]


bot_id = 'U01CQ5HBWFM'


#CONSULTA QUE RETORNA EL ULTIMO MENSAJE POR CIERTO USUARIO, SE NECESITA OBTENER EL ID DEL USUARIO
if ultimo.rstrip(ID_ultimo).lower() == 'ok nestor ultimo mensaje ':
    for i in mensajes[1:]:
        if i['user'] == ID_ultimo:
            msj = i['text']
            break
     text = "Hola, el ultimo mensaje enviado por @" + ID_ultimo + " es "  + msj
    
     client.chat_postMessage(channel='#general', text=text)

#RETORNA LA CANTIDAD DE MENSAJES 
elif ultimo.rstrip ID_ultimo).lower() == 'ok nestor cuantos mensajes ':
     c = 0
     for i in mensajes[1:]:
         if i['user'] == ID_ultimo:
             c += 1
     text = "Hola, el usuarui " + ID_ultimo + " ha enviado "  + str(c) + " mensajes"

     client.chat_postMessage(channel='#general', text=text)
