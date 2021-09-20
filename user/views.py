from io import BytesIO
from urllib.parse import urlparse

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render
from main.models import User, UserComment, UserBlock, UserWishlist, Boss, Cafe, CafeGame, UserCafe,\
    CafeBook, CafeBookWantGame, CafeSales, Game, Genre, GameGenre, PlaySystem, GamePlaySystem, GameImage, GameComment,\
    Funding, FundingSchedule, UserFriend, UserRecent, UserPlayde, Community, CommunityLike, Comment, CommentReply
import my_settings
import bcrypt
from django.db.models import Q
from main.helper.JsonDictionary import returnjson
from user.helper import JsonDictionary, LoginHelper, ImageHelper
# Create your views here.

def intro(request):
    url = my_settings.now_url
    return render(request, 'user/user_intro.html', {'url' : url})

def login(request):
    data = request.POST
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

    return returnjson(account)

def join(request):
    data = request.POST
    platform = int(data['platform'])

    if platform == 0:
        email = data['email']
        obj, create = User.objects.get_or_create(platform=platform, email=email)
    else:
        token = data['token']
        obj, create = User.objects.get_or_create(platform=platform, token=token)

    if not create:
        access = JsonDictionary.JoinToDictionary(False, 'ALREADY USER')
        return returnjson(access)

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
            return returnjson(access)
    if 'email' in keys and platform != 0:   obj.email = data['email']
    if 'phone' in keys:                     obj.phone = data['phone']
    if 'age' in keys:                       obj.age = int(data['age'])
    obj.save()

    access = JsonDictionary.JoinToDictionary(True, obj.id)
    return returnjson(access)

def get_block(request):
    data = request.POST
    user_id = int(data['user_id'])

    blocklist = UserBlock.objects.filter(user_id=user_id)

    users = [User.objects.get(id=block[1].user_id_blocked) for block in enumerate(blocklist)]
    users = JsonDictionary.UsersToDictionary(users)
    return returnjson(users)

def add_block(request):
    data = request.POST
    user_id = int(data['user_id'])
    his_id = int(data['his_id'])

    obj, created = UserBlock.objects.get_or_create(user_id=user_id, user_id_blocked=his_id)
    boolean = JsonDictionary.BoolToDictionary(created)
    return returnjson(boolean)

def del_block(request):
    data = request.POST
    user_id = int(data['user_id'])
    his_id = int(data['his_id'])

    try:
        UserBlock.objects.get(user_id=user_id, user_id_blocked=his_id).delete()
        boolean = True
    except:
        boolean = False

    boolean = JsonDictionary.BoolToDictionary(boolean)
    return returnjson(boolean)

def comment(request):
    data = request.POST
    user_id = int(data['user_id'])

    comments = UserComment.objects.filter(his_id=user_id).order_by('-written_date')
    writers = [User.objects.get(id=comment.my_id) for comment in comments]
    comments = JsonDictionary.CommentToDictionary(comments, writers)
    return returnjson(comments)


def add_comment(request):
    data = request.POST
    user_id = int(data['user_id'])
    his_id = int(data['his_id'])
    score = int(data['score'])
    content = data['content']

    obj, created = UserComment.objects.get_or_create(my_id=user_id, his_id=his_id)
    obj.score = score
    obj.comment = content
    obj.save()
    boolean = JsonDictionary.BoolToDictionary(True)
    return returnjson(boolean)

def set_nickname(request):
    data = request.POST
    user_id = int(data['user_id'])
    nickname = data['nickname']
    obj = User.objects.get(id=user_id)
    if obj.nickname != nickname:
        if not LoginHelper.exist_nickname(nickname):
            obj.nickname = nickname
        else:
            access = JsonDictionary.JoinToDictionary(False, 'ALREADY NICKNAME')
            return returnjson(access)
        obj.save()
    access = JsonDictionary.JoinToDictionary(True, 'SUCCESS')
    return returnjson(access)

def profile(request):
    data = request.POST
    user_id = int(data['user_id'])

    user = User.objects.get(id=user_id)
    comments = UserComment.objects.filter(his_id=user_id)
    score = sum([comment.score for comment in comments]) / len(comments) if comments else 0
    user = JsonDictionary.ProfileToDictionary(user, score)
    return returnjson(user)

def set_profile_image(request):
    data = request.POST
    user_id = int(data['user_id'])
    image_url = data['image_url']
    user = User.objects.get(id=user_id)
    user.image = image_url
    user.save()
    user = JsonDictionary.ProfileImageToDictionary(True, User.objects.get(id=user_id))
    return returnjson(user)

def posible_nickname(request):
    data = request.POST
    nickname = data['nickname']
    try:
        User.objects.get(nickname=nickname)
        boolean = False
    except:
        boolean = True
    boolean = JsonDictionary.BoolToDictionary(boolean)
    return returnjson(boolean)


def set_push_token(request):
    data = request.POST
    user_id = int(data['user_id'])
    push_token = data['token']
    user = User.objects.get(id=user_id)
    user.push_token = push_token
    boolean = JsonDictionary.BoolToDictionary(True)
    return returnjson(boolean)

def get_profile_chat(request):
    data = request.POST
    user_id = int(data['user_id'])
    user = User.objects.get(id=user_id)
    user = JsonDictionary.ChatprofileToDictionary(user)
    return returnjson(user)