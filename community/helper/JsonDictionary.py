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
                'visit': board.visit,
                'tag': board.tag,
            },
            'writer':{
                'id': user.id,
                'nickname': user.nickname,
                'profile': user.image,
            }
        })
    return output

def BoardToDirectory(board, board_images, writer, like, my_like, comment_cnt, comments, comments_writer, replyss, replyss_writer, user_block):
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
        'images': list(),
    }
    for board_image in board_images:
        output['board']['images'].append({
            'id': board_image.id,
            'order': board_image.order,
            'image': board_image.image,
        })
    output['writer'] = {
        'id': writer.id,
        'nickname': writer.nickname,
        'profile': writer.image,
    }
    output['comment'] = []
    for comment, comment_writer, replys, replys_writer in zip(comments, comments_writer, replyss, replyss_writer):
        temp = {
            'id': comment.id,
            'content': comment.content if comment_writer not in user_block else '차단한 사용자의 댓글입니다.',
            'created_at': comment.created_at,
            'writer': {
                'id': comment_writer.id if comment_writer not in user_block else 0,
                'nickname': comment_writer.nickname if comment_writer not in user_block else '',
                'profile': comment_writer.image,
            },
            'reply': False,
        }
        output['comment'].append(temp)
        for reply, reply_writer in zip(replys, replys_writer):
            temp = {
                'id': reply.id,
                'content': reply.content if reply_writer not in user_block else '차단한 사용자의 답글입니다.',
                'created_at': reply.created_at,
                'writer': {
                    'id': reply_writer.id if reply_writer not in user_block else 0,
                    'nickname': reply_writer.nickname if reply_writer not in user_block else '',
                    'profile': reply_writer.image,
                },
                'reply': True,
            }
            output['comment'].append(temp)
    return output

def TempCommunityToDirectory(community, rng):
    output = {}
    output['meta'] = {
        'count': len(community),
        'start': rng[0]+1,
        'end': rng[0] + 1 + len(community),
    }
    output['community'] = []
    for board in community:
        output['community'].append({
            'id': board.id,
            'content': board.content,
            'tag': board.tag,
        })
    return output