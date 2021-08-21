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

def exist_nickname(nickname):
    return bool(len(User.objects.filter(nickname=nickname)))

# Create your views here.
def intro(request):
    url = my_settings.now_url
    return render(request, 'main/main_intro.html', {'url' : url})

def add_block(request):
    data = request.GET
    user_id = int(data['user_id'])
    his_id = int(data['his_id'])

    obj, created = UserBlock.objects.get_or_create(user_id=user_id, user_id_blocked=his_id)
    return HttpResponse("SUCCESS" if created else "FALSE")


def get_block(request):
    data = request.GET
    user_id = int(data['user_id'])

    blocklist = UserBlock.objects.filter(user_id=user_id)

    users = [User.objects.get(id=block[1].user_id_blocked) for block in enumerate(blocklist)]
    return render(request, 'main/blocklist.html', {'block_list': users})


def del_block(request):
    data = request.GET
    user_id = int(data['user_id'])
    his_id = int(data['his_id'])

    try:
        UserBlock.objects.get(user_id=user_id, user_id_blocked=his_id).delete()
        result = "SUCCESS"
    except:
        result = "FAIL"
    return HttpResponse(result)

def add_usercomment(request):
    data = request.GET
    user_id = int(data['user_id'])
    his_id = int(data['his_id'])
    score = int(data['score'])
    comment = data['comment']

    obj, created = UserComment.objects.get_or_create(my_id=user_id, his_id=his_id)
    UserComment.objects.filter(my_id=user_id, his_id=his_id).update(score=score, comment=comment)
    return HttpResponse("SUCCESS")


def get_usercomment(request):
    data = request.GET
    user_id = int(data['user_id'])

    comments = UserComment.objects.filter(his_id=user_id).order_by('-written_date')
    if not comments:    return HttpResponse("NULL")
    writters = [User.objects.get(id=comment[1].my_id) for comment in enumerate(comments)]
    return render(request, 'main/usercomment.html', {'comments_and_writters': zip(comments, writters),
                                                     'score_average': sum(
                                                         [comment.score for comment in comments]) / len(comments)})

def join_user(request):
    data = request.GET
    platform = int(data['platform'])

    if platform == 0:
        email = data['email']
        obj, create = User.objects.get_or_create(platform=platform, email=email)
    else:
        token = data['token']
        obj, create = User.objects.get_or_create(platform=platform, token=token)

    if not create:
        return HttpResponse('ALREADY USER')

    if platform == 0:
        password = data['password']
        obj.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    keys = data.keys()
    if 'name' in keys:                      obj.name = data['name']
    if 'nickname' in keys:
        if not exist_nickname(data['nickname']):
            obj.nickname = data['nickname']
        else:
            obj.delete()
            return HttpResponse('ALREADY NICKNAME')
    if 'email' in keys and platform != 0:   obj.email = data['email']
    if 'phone' in keys:                     obj.phone = data['phone']
    if 'age' in keys:                       obj.age = int(data['age'])
    obj.save()

    return HttpResponse("SUCCESS")

def login(request):
    data = request.GET
    platform = int(data['platform'])

    if not platform:
        email = data['email']
        password = data['password']
        try:
            obj = User.objects.get(platform=0, email=email)
        except:
            return HttpResponse('FAIL')

        return HttpResponse(f'{obj.id}') if bcrypt.checkpw(password.encode('utf-8'), obj.password.encode('utf-8')) else HttpResponse('FAIL')

    try:
        token = data['token']
        obj = User.objects.get(platform=platform, token=token)
        return HttpResponse(f'{obj.id}')
    except:
        return HttpResponse('FAIL')

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

"""def add_meet(request):
    data = request.GET
    id = int(data['user_id'])
    try:
        coords = data['coords'].split(',')
        latitude, longitude = float(coords[0]), float(coords[1])
    except:
        return HttpResponse("COORDS EXCEPT")

    if not User.objects.filter(id=id):
        return HttpResponse("UNKNOWN USER")
    obj, create = Meet.objects.get_or_create(user_id=id)
    obj.latitude = latitude
    obj.longitude = longitude
    area1, area2, area3 = ConvertLocation.latlng_to_address([latitude, longitude])
    if area1 != 'ERROR':
        obj.area1 = area1
        obj.area2 = area2
        obj.area3 = area3
    obj.save()

    return HttpResponse('SUCCESS')

def del_meet(request):
    data = request.GET
    id = int(data['user_id'])
    obj, create = Meet.objects.get_or_create(user_id=id)
    obj.delete()

    return HttpResponse('SUCCESS')

def get_meet(request):
    data = request.GET
    id = int(data['user_id'])
    srt = int(data['sort'])
    try:
        coords = data['coords'].split(',')
        latitude, longitude = float(coords[0]), float(coords[1])
    except:
        return HttpResponse("COORDS EXCEPT")

    meets = Meet.objects.filter(latitude__range=(latitude - 0.038, latitude + 0.038),
                                longitude__range=(longitude - 0.044, longitude + 0.044))
    meets = sorted(meets, key=lambda meet: abs(meet.latitude - latitude) + abs(meet.longitude - longitude))[:40]
    users = list()
    for meet in meets:
        obj = User.objects.filter(id=meet.user_id)
        if obj and obj[0].id != id:
            users.append(obj[0])

    usercafes = [UserCafe.objects.filter(user_id=user.id) for user in users]
    usergames = [UserWishlist.objects.filter(user_id=user.id) for user in users]
    values = list()
    for user, usercafe, usergame in zip(users, usercafes, usergames):
        cafe_cnt = len([1 for cafe_id in usercafe if UserCafe.objects.filter(user_id=id, cafe_id=cafe_id.cafe_id)])
        game_cnt = len([1 for game_id in usergame if UserWishlist.objects.filter(user_id=id, game_id=game_id.game_id)])
        values.append([user, cafe_cnt, game_cnt])

    if srt == 0:
        values = values[:20]
    elif srt == 1:
        values = sorted(values, key=lambda value: value[1], reverse=True)[:20]
    else:
        values = sorted(values, key=lambda value: value[2], reverse=True)[:20]

    return render(request, 'main/meet.html', {'values': values})"""

def test(request):
    data= request.GET
    try:
        coords = data['coords'].split(',')
        latitude = float(coords[0])
        longitude = float(coords[1])
    except:
        return HttpResponse("COORDS EXCEPT")

    return HttpResponse(f'{ConvertLocation.latlng_to_address([latitude, longitude])}')
