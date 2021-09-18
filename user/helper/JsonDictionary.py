def LoginToDictionary(id, access):
    output = {
        'id': id,
        'access': access
    }
    return output

def JoinToDictionary(access, message):
    output = {
        'access': access,
        'message': message,
    }
    return output

def BoolToDictionary(act):
    output = {
        'act': act
    }
    return output

def UsersToDictionary(users):
    output = {
        'meta': {
            'count': len(users)
        },
        'user': []
    }
    for user in users:
        output['user'].append({
            'id': user.id,
            'nickname': user.nickname,
            'profile': user.image,
        })

    return output

def CommentToDictionary(comments, writers):
    print(len(comments))
    output = {
        'meta':{
            'count': len(comments)
        },
        'average': sum([comment.score for comment in comments]) / len(comments) if comments else 0,
        'comment': []
    }
    for comment, writer in zip(comments, writers):
        output['comment'].append({
            'id': comment.id,
            'score': comment.score,
            'content': comment.comment,
            'writer':{
                'id': writer.id,
                'nickname': writer.nickname,
                'profile': writer.image,
            },
        })

    return output

def ProfileToDictionary(user, score):
    output = {
        'id': user.id,
        'nickname': user.nickname,
        'profile': user.image,
        'score': score,
        'message_token': user.message_token,
    }
    return output

def ProfileImageToDictionary(boolean, user):
    output = {
        'act': boolean,
        'id': user.id,
        'image': user.image,
    }
    return output

def ChatprofileToDictionary(user):
    output = {
        'id': user.id,
        'nickname': user.nickname,
        'image': user.image,
    }
    return output