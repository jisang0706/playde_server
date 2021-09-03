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
            'profile_img': game.image,
            'level': game.level,
            'interest': game.interest,
        })

    return output

def GameinfoToDictionary(game, game_imgs):
    output = {
        'id': game.id,
        'min_age': game.age,
        'kor_name': game.kor_name,
        'min_user': game.min_user,
        'max_user': game.max_user,
        'content': game.content,
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