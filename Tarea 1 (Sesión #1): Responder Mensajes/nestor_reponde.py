import json
import requests
from flask import Flask, request
import slack
import os
from slackeventsapi import SlackEventAdapter
import pymongo

#VERSION WINDOWS

'''from pathlib import Path
from dotenv import load_dotenv
path = Path('.') / '.env'
load_dotenv(dotenv_path=path)
TOKEN = os.environ["SLACK_TOKEN"]
SIGNING_SECRET = os.environ["SIGNING_SECRET"]
'''

#VERSION UNIX
TOKEN = os.environ.get("SLACK_TOKEN")
print(TOKEN)
SIGNING_SECRET = os.environ.get("SIGNING_SECRET")

#OBTENER DEL NAVEGADOR:
#                       IR A ESPACIO DE TRABAJO Y SELECCIONAR CANAL
#                       EL CHANNEL ID SERA LA ULTIMA SERIE DE DIGITOS-LETRAS ESE LINK
#                       https://app.slack.com/client/XXXXXXXXXXX/C01CB597ZA6

client = slack.WebClient(token=TOKEN)
mongo_client = pymongo.MongoClient('localhost', 27017)

db = mongo_client['bot']
collection = db['mensajes']


app = Flask(__name__)

slack_event = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)

BOT_ID = client.api_call('auth.test')['user_id']


#Obtener ID's y nombre de usuarios
result = client.users_list()['members']
users = {}

for user in result:
    users[user['id']] = user['name']


@slack_event.on('message')
def message(payload):
    #print(payload)
    #response = client.users_list()
    #print(response)

    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    # 1) “OK Néstor, cuál es el último mensaje enviado por [“nombre de usuario del canal”]
    # 2) “OK Néstor, cuántos mensajes han sidos enviados por [“nombre de usuario del canal”]

    if user_id != BOT_ID:

        user_name = text.split(' ')[-1]

        if text.rstrip(user_name).lower() == 'ok nestor, cual es el ultimo mensaje enviado por ':
            
            query = collection.find({"user": user_name}).sort("_id", pymongo.DESCENDING).limit(1)

            for q in query:
                client.chat_postMessage(channel=channel_id, 
                                        text='El ultimo mensaje enviado por @' + user_name + 'es: ' +
                                              q['text'])

        elif text.rstrip(user_name).lower() == 'ok nestor, cuantos mensajes han sidos enviados por ':
            query = collection.find({"user": user_name}).count()
            client.chat_postMessage(channel=channel_id, 
                                    text='El usuario @' + user_name + 'ha enviado' + str(query) + 
                                         ' mesajes')

        else:
            collection.insert_one(
                {'user': users[user_id], 
                "text": text}
            )
            #client.chat_postMessage(channel=channel_id, text=text)


if __name__ == '__main__':
    app.run(debug=True, port=4000)







# Segunda Opción


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
