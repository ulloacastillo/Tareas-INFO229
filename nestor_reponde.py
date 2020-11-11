import json
import requests
from flask import Flask
import slack
import os
from slackeventsapi import SlackEventAdapter

#VERSION WINDOWS
from pathlib import Path
from dotenv import load_dotenv
path = Path('.') / '.env'
load_dotenv(dotenv_path=path)
TOKEN = os.environ["SLACK_TOKEN"]
SIGNING_SECRET = os.environ["SIGNING_SECRET"]

'''
#VERSION UNIX
TOKEN = os.environ.get("SLACK_TOKEN")
SIGNING_SECRET = os.environ.get("SIGNING_SECRET")
'''
#OBTENER DEL NAVEGADOR:
#                       IR A ESPACIO DE TRABAJO Y SELECCIONAR CANAL
#                       EL CHANNEL ID SERA LA ULTIMA SERIE DE DIGITOS-LETRAS ESE LINK
#                       https://app.slack.com/client/XXXXXXXXXXX/C01CB597ZA6

client = slack.WebClient(token=TOKEN)
app = Flask(__name__)
slack_event = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)

BOT_ID = client.api_call('auth.test')['user_id']

@slack_event.on('message')
def message(payload):
    print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    if user_id != BOT_ID:
        client.chat_postMessage(channel=channel_id, text=text)


if __name__ == '__main__':
    app.run(debug=True, port=80)










'''
channelId = "C01CB597ZA6"


#client.chat_postMessage(channel="#general", text="Holaaaa")


slack_url = "https://slack.com/api/conversations.history?token=" + TOKEN + "&channel=" + channelId

messages = requests.get(slack_url).json()


mensajes = messages['messages']


print(mensajes)
print(len(mensajes))

for i in mensajes:
   print(i.keys(), end=" ")
   print(i['text'])


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
'''
