from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from main.models import Cafe, CafeWorktime, UserCafe, CafeImage
import my_settings
from django.db.models import Q
from cafe.helper import JsonDictionary
import datetime
# Create your views here.

def intro(request):
    url = my_settings.now_url
    return render(request, 'cafe/cafe_intro.html', {'url' : url})

def cafe_list(request):
    data = request.GET
    coords = data['coords'].split(',')
    srt = int(data['sort'])
    latitude = float(coords[0])
    longitude = float(coords[1])
    cafe_range = [int(rng)-1 for rng in data['range'].split(',')]
    cafes = Cafe.objects.filter(latitude__range=(latitude - 0.019, latitude + 0.019),
                                longitude__range=(longitude - 0.022, longitude + 0.022))
    for cafe in cafes:
        cafe.like = len(UserCafe.objects.filter(cafe_id=cafe.id))

    if srt == 0:
        cafes = sorted(cafes, key=lambda cafe: cafe.like)[cafe_range[0]:cafe_range[1]]
    elif srt == 1:
        cafes = sorted(cafes, key=lambda cafe: abs(cafe.latitude - latitude) + abs(cafe.longitude - longitude))[cafe_range[0]:cafe_range[1]]
    else:
        cafes = sorted(cafes, key=lambda cafe: cafe.book_price)[cafe_range[0]:cafe_range[1]]

    worktimes = [CafeWorktime.objects.get(cafe_id=cafe.id, weekday=datetime.datetime.today().weekday()) for cafe in cafes]
    cafes = JsonDictionary.CafesToDictionary(cafes, worktimes, cafe_range)
    return JsonResponse(cafes, json_dumps_params={'ensure_ascii': False},
                            content_type=u"application/json; charset=utf-8", status=200)

def cafe_get(request, cafe_id):
    cafe = Cafe.objects.get(id=cafe_id)
    cafe_images = CafeImage.objects.filter(cafe_id=cafe.id).order_by('order')
    worktime = CafeWorktime.objects.get(cafe_id=cafe.id, weekday=datetime.datetime.today().weekday())
    like = len(UserCafe.objects.filter(cafe_id=cafe_id))
    cafe = JsonDictionary.CafeToDirectory(cafe, cafe_images, worktime, like)
    return JsonResponse(cafe, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def get_fav_cafe(request):
    data = request.GET
    user_id = int(data['user_id'])

    usercafes = UserCafe.objects.filter(user_id=user_id).order_by('-created')
    cafes = [Cafe.objects.get(id=usercafe.cafe_id) for usercafe in usercafes]

    cafes = JsonDictionary.FavCafesToDictionary(cafes)
    return JsonResponse(cafes, json_dumps_params={'ensure_ascii': False},
                            content_type=u"application/json; charset=utf-8", status=200)

def add_fav_cafe(request):
    data = request.GET
    user_id = int(data['user_id'])
    cafe_id = int(data['cafe_id'])

    obj, created = UserCafe.objects.get_or_create(user_id=user_id, cafe_id=cafe_id)
    boolean = JsonDictionary.BoolToDictionary(created)
    return JsonResponse(boolean, json_dumps_params={'ensure_ascii': False},
                            content_type=u"application/json; charset=utf-8", status=200)

def del_fav_cafe(request):
    data = request.GET
    user_id = int(data['user_id'])
    cafe_id = int(data['cafe_id'])

    UserCafe.objects.get_or_create(user_id=user_id, cafe_id=cafe_id)[0].delete()
    boolean = JsonDictionary.BoolToDictionary(True)
    return JsonResponse(boolean, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)