from django.shortcuts import render
from main.models import Cafe, CafeWorktime, UserCafe, CafeImage
import my_settings
from django.db.models import Q, Min
from main.helper.JsonDictionary import returnjson
from cafe.helper import JsonDictionary
import datetime
# Create your views here.

def intro(request):
    url = my_settings.now_url
    return render(request, 'cafe/cafe_intro.html', {'url' : url})

def cafe_list(request):
    data = request.GET
    user_id = data['user_id']
    if 'coords' in data.keys():
        coords = data['coords'].split(',')
        latitude = float(coords[0])
        latitudeQ = Q(latitude__range=(latitude - 0.19, latitude + 0.19))
        longitude = float(coords[1])
        longitudeQ = Q(longitude__range=(longitude - 0.22, longitude + 0.22))
    else:
        latitudeQ = Q(latitude__range=(-181, 181))
        longitudeQ = Q(longitude__range=(-91, 91))

    if 'cafe_name' in data.keys():
        cafe_name = data['cafe_name']
        cafe_name = Q(name__icontains=cafe_name)
    else:
        cafe_name = Q(name__icontains='')

    srt = int(data['sort'])

    cafe_range = [int(rng)-1 for rng in data['range'].split(',')]
    cafes = Cafe.objects.filter(latitudeQ, longitudeQ, cafe_name)
    for cafe in cafes:
        cafe.like = len(UserCafe.objects.filter(cafe_id=cafe.id))
        cafe.my_like = True if len(UserCafe.objects.filter(cafe_id=cafe.id, user_id=user_id)) else False

    if srt == 0:
        cafes = sorted(cafes, key=lambda cafe: -cafe.id)[cafe_range[0]:cafe_range[1]]
    elif srt == 1:
        cafes = sorted(cafes, key=lambda cafe: abs(cafe.latitude - latitude) + abs(cafe.longitude - longitude))[cafe_range[0]:cafe_range[1]]
    elif srt == 2:
        cafes = sorted(cafes, key=lambda cafe: -cafe.like)[cafe_range[0]:cafe_range[1]]
    else:
        cafes = sorted(cafes, key=lambda cafe: cafe.book_price)[cafe_range[0]:cafe_range[1]]

    images = [CafeImage.objects.filter(cafe_id=cafe.id).order_by('order')[0].content_image
              if CafeImage.objects.filter(cafe_id=cafe.id).order_by('order') else 0 for cafe in cafes]
    for i, image in enumerate(images):
        cafes[i].image = image
    worktimes = [CafeWorktime.objects.filter(cafe_id=cafe.id, weekday=datetime.datetime.today().weekday())[0]
                 if CafeWorktime.objects.filter(cafe_id=cafe.id, weekday=datetime.datetime.today().weekday()) else 0 for cafe in cafes]
    cafes = JsonDictionary.CafesToDictionary(cafes, worktimes, cafe_range)
    return returnjson(cafes)

def cafe_get(request, cafe_id):
    data = request.GET
    user_id = data['user_id']
    cafe = Cafe.objects.get(id=cafe_id)
    cafe_images = CafeImage.objects.filter(cafe_id=cafe.id).order_by('order')
    try:
        worktime = CafeWorktime.objects.get(cafe_id=cafe.id, weekday=datetime.datetime.today().weekday())
    except:
        worktime = 0
    like = len(UserCafe.objects.filter(cafe_id=cafe_id))
    my_like = True if len(UserCafe.objects.filter(cafe_id=cafe_id, user_id=user_id)) else False
    cafe = JsonDictionary.CafeToDirectory(cafe, cafe_images, worktime, like, my_like)
    return returnjson(cafe)

def get_fav_cafe(request):
    data = request.GET
    user_id = int(data['user_id'])

    usercafes = UserCafe.objects.filter(user_id=user_id).order_by('-id')
    cafes = [Cafe.objects.get(id=usercafe.cafe_id) for usercafe in usercafes]
    images = [CafeImage.objects.filter(cafe_id=cafe.id).aggregate(order=Min('order')) for cafe in cafes]
    for i, image in enumerate(images):
        cafes[i].image = image

    cafes = JsonDictionary.FavCafesToDictionary(cafes)
    return returnjson(cafes)

def add_fav_cafe(request):
    data = request.GET
    user_id = int(data['user_id'])
    cafe_id = int(data['cafe_id'])

    obj, created = UserCafe.objects.get_or_create(user_id=user_id, cafe_id=cafe_id)
    boolean = JsonDictionary.BoolToDictionary(created)
    return returnjson(boolean)

def del_fav_cafe(request):
    data = request.GET
    user_id = int(data['user_id'])
    cafe_id = int(data['cafe_id'])

    UserCafe.objects.get_or_create(user_id=user_id, cafe_id=cafe_id)[0].delete()
    boolean = JsonDictionary.BoolToDictionary(True)
    return returnjson(boolean)
