import os
from dotenv import load_dotenv
import requests
import json

class Bot:
    def __init__(self) -> None:
        load_dotenv()
        self.TK = os.environ.get("TK")
        self.URL =  f'http://api.telegram.org/bot{self.TK}/'        
        #temporario
        self.users = []
    
    def Start(self):
        update_id = None
        while 1:
            att = self.getMessage(update_id) 
            posts = att['result']
            if posts:
                for message in posts:
                    update_id = message['update_id']
                    chat_id = message['message']['from']['id']
                    #temporario
                    if chat_id in self.users:
                        print(f'chat_id = {chat_id} message = Usuario ja exite, mensagem ignorada name = {name} text={text}')
                        self.response("Usuario ja exite, mensagem ignorada", chat_id)
                    else:
                        self.users.append(chat_id)
                        name = message['message']['from']['first_name']
                        try:
                            text = message['message']['text']
                            response = self.createResponse()
                            self.response(response, chat_id)
                            print(f'chat_id = {chat_id} message = {response} name = {name} text={text}')
                        except:
                            response = self.createResponse()
                            self.response(response, chat_id)
                            print(f'chat_id = {chat_id} message = {response} name = {name} ')
    
    def getMessage(self,update_id):
        requestsLink = f'{self.URL}getUpdates?timeout=100'
        if update_id:
            requestsLink = f'{requestsLink}&offset={update_id+1}'
        
        result = requests.get(requestsLink)
        return json.loads(result.content)
    
    def createResponse(self):
        return 'Bem vindo ao bot'
    
    def response(self, response, chat_id):
        link = f'{self.URL}sendMessage?chat_id={chat_id}&text={response}'
        requests.get(link)
