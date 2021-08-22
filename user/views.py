from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from main.models import User, UserComment, UserBlock, UserWishlist, Boss, Cafe, CafeGame, UserCafe,\
    CafeBook, CafeBookWantGame, CafeSales, Game, Genre, GameGenre, PlaySystem, GamePlaySystem, GameImage, GameComment,\
    Funding, FundingSchedule, UserFriend, UserRecent, UserPlayde, Community, CommunityLike, Comment, CommentReply
import my_settings
import bcrypt
from django.db.models import Q
from user.helper import JsonDictionary, LoginHelper
# Create your views here.

def intro(request):
    url = my_settings.now_url
    return render(request, 'user/user_intro.html', {'url' : url})

def login(request):
    data = request.GET
    platform = int(data['platform'])

    if not platform:
        email = data['email']
        password = data['password']
        try:
            obj = User.objects.get(platform=0, email=email)
            if bcrypt.checkpw(password.encode('utf-8'), obj.password.encode('utf-8')):
                account = JsonDictionary.LoginToDictionary(obj.id, True)
            else:
                account = JsonDictionary.LoginToDictionary(True, False)
        except:
            account = JsonDictionary.LoginToDictionary(False, False)
    else:
        try:
            token = data['token']
            obj = User.objects.get(platform=platform, token=token)
            account = JsonDictionary.LoginToDictionary(obj.id, True)
        except:
            account = JsonDictionary.LoginToDictionary(False, False)

    return JsonResponse(account, json_dumps_params={'ensure_ascii': False},
                            content_type=u"application/json; charset=utf-8", status=200)

def join(request):
    data = request.GET
    platform = int(data['platform'])

    if platform == 0:
        email = data['email']
        obj, create = User.objects.get_or_create(platform=platform, email=email)
    else:
        token = data['token']
        obj, create = User.objects.get_or_create(platform=platform, token=token)

    if not create:
        access = JsonDictionary.JoinToDictionary(False, 'ALREADY USER')
        return JsonResponse(access, json_dumps_params={'ensure_ascii': False},
                            content_type=u"application/json; charset=utf-8", status=200)

    if platform == 0:
        password = data['password']
        obj.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    keys = data.keys()
    if 'name' in keys:                      obj.name = data['name']
    if 'nickname' in keys:
        if not LoginHelper.exist_nickname(data['nickname']):
            obj.nickname = data['nickname']
        else:
            obj.delete()
            access = JsonDictionary.JoinToDictionary(False, 'ALREADY NICKNAME')
            return JsonResponse(access, json_dumps_params={'ensure_ascii': False},
                                content_type=u"application/json; charset=utf-8", status=200)
    if 'email' in keys and platform != 0:   obj.email = data['email']
    if 'phone' in keys:                     obj.phone = data['phone']
    if 'age' in keys:                       obj.age = int(data['age'])
    obj.save()

    access = JsonDictionary.JoinToDictionary(obj.id, 'SUCCESS')
    return JsonResponse(access, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def get_block(request):
    data = request.GET
    user_id = int(data['user_id'])

    blocklist = UserBlock.objects.filter(user_id=user_id)

    users = [User.objects.get(id=block[1].user_id_blocked) for block in enumerate(blocklist)]
    users = JsonDictionary.UsersToDictionary(users)
    return JsonResponse(users, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def add_block(request):
    data = request.GET
    user_id = int(data['user_id'])
    his_id = int(data['his_id'])

    obj, created = UserBlock.objects.get_or_create(user_id=user_id, user_id_blocked=his_id)
    boolean = JsonDictionary.BoolToDictionary(created)
    return JsonResponse(boolean, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def del_block(request):
    data = request.GET
    user_id = int(data['user_id'])
    his_id = int(data['his_id'])

    try:
        UserBlock.objects.get(user_id=user_id, user_id_blocked=his_id).delete()
        boolean = True
    except:
        boolean = False

    boolean = JsonDictionary.BoolToDictionary(boolean)
    return JsonResponse(boolean, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def comment(request):
    data = request.GET
    user_id = int(data['user_id'])

    comments = UserComment.objects.filter(his_id=user_id).order_by('-written_date')
    writters = [User.objects.get(id=comment.my_id) for comment in comments]
    comments = JsonDictionary.CommentToDictionary(comments, writters)
    return JsonResponse(comments, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)


def add_comment(request):
    data = request.GET
    user_id = int(data['user_id'])
    his_id = int(data['his_id'])
    score = int(data['score'])
    content = data['content']

    obj, created = UserComment.objects.get_or_create(my_id=user_id, his_id=his_id)
    obj.score = score
    obj.comment = content
    obj.save()
    boolean = JsonDictionary.BoolToDictionary(True)
    return JsonResponse(boolean, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def set_nickname(request):
    data = request.GET
    id = int(data['user_id'])
    nickname = data['nickname']
    obj = User.objects.get(id=id)
    if obj.nickname != nickname:
        if not LoginHelper.exist_nickname(nickname):
            obj.nickname = nickname
        else:
            access = JsonDictionary.JoinToDictionary(False, 'ALREADY NICKNAME')
            return JsonResponse(access, json_dumps_params={'ensure_ascii': False},
                                content_type=u"application/json; charset=utf-8", status=200)
        obj.save()
    access = JsonDictionary.JoinToDictionary(True, 'SUCCESS')
    return JsonResponse(access, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)