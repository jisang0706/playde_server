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
            'profile': 'media' + str(user.small_image) if user.small_image else '',
        })

    return output

def CommentToDictionary(comments, writters):
    print(len(comments))
    output = {
        'meta':{
            'count': len(comments)
        },
        'average': sum([comment.score for comment in comments]) / len(comments) if comments else 0,
        'comment': []
    }
    for comment, writter in zip(comments, writters):
        output['comment'].append({
            'id': comment.id,
            'score': comment.score,
            'content': comment.comment,
            'writter':{
                'id': writter.id,
                'nickname': writter.nickname,
                'profile': '/media/' + writter.small_image if writter.small_image else '',
            },
        })

    return output