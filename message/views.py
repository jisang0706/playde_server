from django.shortcuts import render
from main.models import User, Room, UserRoom
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
    data = request.POST
    writer_id = data['writer_id']
    target_id = data['target_id']
    content = data['content']

    writer = User.objects.get(id=writer_id)
    target = User.objects.get(id=target_id)

    content = JsonDictionary.SendToDictionaty(
        push_fcm_notification.send_to_firebase_cloud_messaging(
            target.push_token, writer.nickname, content))
    return returnjson(content)

def get_rooms(request):
    data = request.POST
    user_id = int(data['user_id'])
    rooms = [Room.objects.filter(id=room.room_id)[0] for room in UserRoom.objects.filter(user_id=user_id) if Room.objects.filter(id=room.room_id)]
    for i, room in enumerate(rooms):
        for userroom in UserRoom.objects.filter(room_id=room.id):
            rooms[i].users = []
            try:
                if userroom.user_id != user_id:
                    rooms[i].users.append(User.objects.get(id=userroom.user_id))
            except:
                pass

    rooms = JsonDictionary.RoomsToDictionary(rooms)
    return returnjson(rooms)

def get_room(request):
    data = request.POST
    user_id = int(data['user_id'])
    his_id = int(data['his_id'])
    my_rooms = [room.room_id for room in UserRoom.objects.filter(user_id=user_id)]
    his_rooms = [room.room_id for room in UserRoom.objects.filter(user_id=his_id)]
    my_rooms = list(set(my_rooms).intersection(his_rooms))
    rt_room = 0
    for room in my_rooms:
        if len(UserRoom.objects.filter(room_id=room)) == 2:
            rt_room = Room.objects.get(id=room)
            break
    if rt_room == 0:
        rt_room = Room.objects.create()
        UserRoom.objects.create(room_id=rt_room.id, user_id=user_id)
        UserRoom.objects.create(room_id=rt_room.id, user_id=his_id)

    rt_room.users = []
    for userroom in UserRoom.objects.filter(room_id=rt_room.id):
        try:
            if userroom.user_id != user_id:
                rt_room.users.append(User.objects.get(id=userroom.user_id))
        except:
            pass

    rt_room = JsonDictionary.RoomToDictionary(rt_room)
    return returnjson(rt_room)