def BoolToDictionary(boolean):
    output = {
        'act': boolean
    }
    return output

def CommunityToDirectory(community, users, likes, my_likes, comments, rng):
    output = {}
    output['meta'] = {
        'count': len(community),
        'start': rng[0]+1,
        'end': rng[0] + 1 + len(community),
    }
    output['community'] = []
    for board, user, like, my_like, comment in zip(community, users, likes, my_likes, comments):
        output['community'].append({
            'board':{
                'id': board.id,
                'content': board.content,
                'like': like,
                'my_like': bool(my_like),
                'created_at': board.created_at,
                'comment_cnt': comment,
                'tag': board.tag,
            },
            'writer':{
                'id': user.id,
                'nickname': user.nickname,
                'profile': '/media/' + str(user.small_image) if user.small_image else '',
            }
        })
    return output

def BoardToDirectory(board, writer, like, my_like, comment_cnt, comments, comments_writer, replyss, replyss_writer):
    output = {}
    output['board'] = {
        'id': board.id,
        'content': board.content,
        'like': like,
        'my_like': bool(my_like),
        'created_at': board.created_at,
        'comment_cnt': comment_cnt,
        'visit': board.visit,
        'tag': board.tag,
    }
    output['writer'] = {
        'id': writer.id,
        'nickname': writer.nickname,
        'profile': '/media/' + str(writer.small_image) if writer.small_image else '',
    }
    output['comment'] = []
    for comment, comment_writer, replys, replys_writer in zip(comments, comments_writer, replyss, replyss_writer):
        temp = {
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at,
            'writer': {
                'id': comment_writer.id,
                'nickname': comment_writer.nickname,
                'profile': '/media/' + str(comment_writer.small_image) if comment_writer.small_image else '',
            },
            'reply': False,
        }
        output['comment'].append(temp)
        for reply, reply_writer in zip(replys, replys_writer):
            temp = {
                'id': reply.id,
                'content': reply.content,
                'created_at': reply.created_at,
                'writer': {
                    'id': reply_writer.id,
                    'nickname': reply_writer.nickname,
                    'profile': '/media/' + str(reply_writer.small_image) if reply_writer.small_image else '',
                },
                'reply': True,
            }
            output['comment'].append(temp)
    return output