def BoolToDictionary(boolean):
    output = {
        'act': boolean
    }

    return output

def CafesToDictionary(cafes, worktimes, rng):
    output = {
        'meta': {
            'count': len(cafes),
            'start': rng[0]+1,
            'end': rng[0]+1+len(cafes),
        },
        'cafe': [],
    }

    for cafe, worktime in zip(cafes, worktimes):
        output['cafe'].append({
            'id': cafe.id,
            'name': cafe.name,
            'profile': cafe.image if type(cafe.image) != int else '0',
            'address': cafe.address,
            'coords': f'{cafe.latitude},{cafe.longitude}',
            'table_cnt': cafe.table_cnt,
            'open': worktime.open if type(worktime) != int else 0,
            'close': worktime.close if type(worktime) != int else 0,
            'like': cafe.like,
            'my_like': cafe.my_like,
        })

    return output

def CafeToDirectory(cafe, cafe_images, worktime, like, my_like):
    output = {
        'id': cafe.id,
        'name': cafe.name,
        'address': cafe.address,
        'coords': f'{cafe.latitude},{cafe.longitude}',
        'table_cnt': cafe.table_cnt,
        'open': worktime.open if type(worktime) != int else 0,
        'close': worktime.close if type(worktime) != int else 0,
        'like': like,
        'my_like': my_like,
        'image': [],
    }
    for image in cafe_images:
        output['image'].append(image)

    return output

def FavCafesToDictionary(cafes):
    output = {
        'meta': {
            'count': len(cafes),
        },
        'cafe': [],
    }

    for cafe in cafes:
        output['cafe'].append({
            'id': cafe.id,
            'name': cafe.name,
            'profile': cafe.image,
        })

    return output

def WorktimeToDictionary(worktimes):
    output = {
        'act': True,
        'worktimes': [],
    }

    for worktime in worktimes:
        output['worktimes'].append({
            'weekday': worktime.weekday,
            'open': worktime.open.strftime("%H:%M"),
            'close': worktime.close.strftime("%H:%M"),
        })
    return output