def GamesToDictionary(games, rng):
    output = {}
    output['meta'] = {
        'count': len(games),
        'start': rng[0]+1,
        'end': rng[0] + 1 + len(games),
    }
    output['games'] = []
    for i, game in enumerate(games):
        output['games'].append({
            'id': game.id,
            'kor_name': game.kor_name,
            'my_like': game.my_like,
            'profile': game.image.content_image if type(game.image) != int else '0',
            'level': game.level,
            'interest': game.interest,
        })

    return output

def GameinfoToDictionary(game, my_like, game_imgs):
    output = {
        'id': game.id,
        'min_age': game.age,
        'kor_name': game.kor_name,
        'min_user': game.min_user,
        'max_user': game.max_user,
        'content': game.content,
        'my_like': my_like,
        'images': [],
    }
    for i, img in enumerate(game_imgs):
        output['images'].append(img.content_image)

    return output

def BoolToDictionary(boolean):
    output = {
        'act': boolean
    }

    return output