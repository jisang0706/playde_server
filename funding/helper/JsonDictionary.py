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
            'nickname': user.nickname if user != 0 else 'unknown',
        })
    return output