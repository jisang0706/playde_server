from django.shortcuts import render
from main.models import User
import my_settings
from django.db.models import Q, Min
from main.helper import push_fcm_notification
from main.helper.JsonDictionary import returnjson
from message.helper import JsonDictionary
# Create your views here.

def intro(request):
    url = my_settings.now_url
    return render(request, 'message/message_intro.html', {'url' : url})

def send(request):
    data = request.GET
    writer_id = data['writer_id']
    target_id = data['target_id']
    content = data['content']

    writer = User.objects.get(id=writer_id)
    target = User.objects.get(id=target_id)

    content = JsonDictionary.SendToDictionaty(
        push_fcm_notification.send_to_firebase_cloud_messaging(
            target.push_token, 'PlayDe', f'{writer.nickname} - {content}'))
    return returnjson(content)