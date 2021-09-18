def SendToDictionaty(response):
    output = {
        'response': response
    }
    return output

def RoomsToDictionary(rooms):
    output = {
        'count': len(rooms),
        'rooms': [],
    }

    for room in rooms:
        output['rooms'].append({
            'id': room.id,
            'token': room.room_token,
            'user_count': len(room.users),
            'users': [{
                'id': user.id,
                'nickname': user.nickname,
                'image': user.image,
            } for user in room.users]
        })
    return output

def RoomToDictionary(room):
    output = {
        'id': room.id,
        'token': room.room_token,
        'user_count': len(room.users),
        'users': [{
            'id': user.id,
            'nickname': user.nickname,
            'image': user.image,
        } for user in room.users]
    }
    return output