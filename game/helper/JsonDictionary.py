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
            'profile_img': '/media/'+str(game.small_image) if game.small_image else '',
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
        'imgs': [],
    }
    for i, img in enumerate(game_imgs):
        output['imgs'].append('/media/'+str(img.content_image))

    return output

def BoolToDictionary(boolean):
    output = {
        'act': 'SUCCESS' if boolean else 'FAIL'
    }

    return output