def BoolToDictionary(boolean):
    output = {
        'act': boolean,
    }
    return output

def FundingsToDictionary(fundings, tags, rng):
    output = {
        'meta':{
            'count': len(fundings),
            'start': rng[0]+1,
            'end': rng[0]+1 + len(fundings),
        },
        'fundings': [],
    }

    for funding, tag in zip(fundings, tags):
        output['fundings'].append({
            'id': funding.id,
            'name': funding.name,
            'image': funding.image,
            'tags': {
                'count': len(tag),
                'objects': [tg.tag for tg in tag]
            }
        })

    return output

def FundingToDictionary(funding, tag, funding_fav):
    output = {
        'id': funding.id,
        'name': funding.name,
        'image': funding.image,
        'content': funding.content,
        'like': funding_fav,
        'goal': funding.goal,
        'finish_date': funding.goal_date,
        'link': funding.link,
        'tags': {
            'count': len(tag),
            'objects': [tg.tag for tg in tag],
        }
    }
    return output

def FundingBoardNewsToDictionary(news, users, rng):
    output = {
        'meta': {
            'count': len(news),
            'start': rng[0]+1,
            'end': len(news) + rng[0]+1,
        },
        'news': [],
    }

    for new, user in zip(news, users):
        output['news'].append({
            'id': new.id,
            'title': new.title,
            'created_at': new.written_date.strftime("%Y.%m.%d %H:%M"),
            'nickname': user.nickname if user != 0 else '',
        })
    return output

def FundingNewsToDictionary(news, writer):
    output = {
        'id': news.id,
        'title': news.title,
        'content': news.content,
        'image': news.image,
        'created_at': news.created_at.strftime("%Y.%m.%d %H:%M"),
        'writer': {
            'id': writer.id,
            'nickname': writer.nickname,
            'image': writer.image,
        }
    }
    return output

def FundingNewslistToDictionary(news, rng):
    output = {
        'meta': {
            'count': len(news),
            'start': rng[0]+1,
            'end': rng[0]+1 + len(news),
        },
        'news': [],
    }
    for new in news:
        output['news'].append({
            'id': new.id,
            'title': new.title,
            'funding_name': new.funding_name,
        })
    return output

def FundingCommunityToDictionary(community, user_id, funding_user_id, rng):
    output = {
        'meta': {
            'count': len(community),
            'start': rng[0]+1,
            'end': rng[0] + len(community)+1,
        },
        'community': [],
    }
    for board in community:
        output['community'].append({
            'kind': 'board',
            'id': board.id,
            'content': board.content if (not board.secret) or board.user.id == user_id or funding_user_id == user_id else '비밀글입니다',
            'created_at': board.written_date.strftime("%Y.%m.%d %H:%M"),
            'user': {
                'id': board.user.id if (not board.secret) or board.user.id == user_id or funding_user_id == user_id else 0,
                'nickname': board.user.nickname if (not board.secret) or board.user.id == user_id or funding_user_id == user_id else '',
                'image': board.user.image if (not board.secret) or board.user.id == user_id or funding_user_id == user_id else '',
            },
        })
        for reply in board.replys:
            output['community'].append({
                'kind': 'reply',
                'id': reply.id,
                'content': reply.content if (not board.secret) or board.user.id == user_id or funding_user_id == user_id else '비밀글입니다',
                'created_at': reply.written_date.strftime("%Y.%m.%d %H:%M"),
                'parent_id': reply.parent_id,
                'user': {
                    'id': reply.user.id if (not board.secret) or board.user.id == user_id or funding_user_id == user_id else 0,
                    'nickname': reply.user.nickname if (not board.secret) or board.user.id == user_id or funding_user_id == user_id else '',
                    'image': reply.user.image if (not board.secret) or board.user.id == user_id or funding_user_id == user_id else '',
                },
            })

    output['meta']['count'] = len(output['community'])
    return output