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
            'address': cafe.address,
            'coords': f'{cafe.latitude},{cafe.longitude}',
            'profile': '/media/' + str(cafe.small_image) if cafe.small_image else '',
            'table_cnt': cafe.table_cnt,
            'open': worktime.open,
            'close': worktime.close,
            'like': cafe.like,
        })

    return output

def CafeToDirectory(cafe, cafe_images, worktime, like):
    output = {
        'id': cafe.id,
        'name': cafe.name,
        'address': cafe.address,
        'coords': f'{cafe.latitude},{cafe.longitude}',
        'profile': '/media/' + str(cafe.small_image) if cafe.small_image else '',
        'table_cnt': cafe.table_cnt,
        'open': worktime.open,
        'close': worktime.close,
        'like': like,
        'image': [],
    }
    for image in cafe_images:
        output['image'].append('/media/' + str(image))

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
            'profile': '/media/' + str(cafe.small_image) if cafe.small_image else '',
        })

    return output