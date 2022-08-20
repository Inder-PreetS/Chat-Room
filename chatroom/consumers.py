from email import message
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):

    messages = []
    room = {}  

    def join_chat(self,username):
        key = self.room_name
        value = []
        if key in self.room.keys():
            self.room[key].append(username)
            re = self.room
        else:
            value.append(username)
            self.room[key]=value
            re = self.room
        return re


    
    def leave_chat(self, username):
        key = self.room_name
        print(key)
        
        self.room[key].remove(username)
        re = self.room
        return re


    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "_%s" % self.room_name
        f = self.scope['user']
 
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.messages.append({"msg": f"{ f } Join Group", "id": f.id, "username": f.username})


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msgtype = text_data_json.get('type')
        username = text_data_json.get("username")

        if msgtype == "user_joined":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    'type': 'chat_message',
                    'message': 'Join Group',
                    'total_users':self.join_chat(username),
                    'sender': username
                }
            )
            return
        message = text_data_json['message']

        self.messages.append({"msg": message, "username": self.scope['user'].username})
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'total_users':self.room,
                'sender': username 
            }
        )


    def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        total_users = event['total_users']

        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'total_users':total_users
        }))
