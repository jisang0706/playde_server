from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import User, UserComment, UserBlock, UserWishlist, Boss, Cafe, CafeGame, UserCafe,\
    CafeBook, CafeBookWantGame, CafeSales, Game, Genre, GameGenre, PlaySystem, GamePlaySystem, GameImage, GameComment,\
    Funding, FundingSchedule, UserFriend, UserRecent, UserPlayde, Community, CommunityLike, Comment, CommentReply
from django.views import generic
import bcrypt
from django.db.models import Q
from main.helper import ConvertLocation
import my_settings

# Create your views here.
def intro(request):
    url = my_settings.now_url
    return render(request, 'main/main_intro.html', {'url' : url})

def set_nickname(request):
    data = request.GET
    id = int(data['user_id'])
    nickname = data['nickname']
    obj = User.objects.get(id=id)
    if obj.nickname == nickname:    return HttpResponse('SUCCESS')

    if not exist_nickname:
        obj.nickname = nickname
    else:
        return HttpResponse('ALREADY NICKNAME')

    obj.save()
    return HttpResponse('SUCCESS')

def test(request):
    data= request.GET
    try:
        coords = data['coords'].split(',')
        latitude = float(coords[0])
        longitude = float(coords[1])
    except:
        return HttpResponse("COORDS EXCEPT")

    return HttpResponse(f'{ConvertLocation.latlng_to_address([latitude, longitude])}')
