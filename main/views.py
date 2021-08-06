from django.shortcuts import render
from django.http import HttpResponse
from .models import User, UserComment, UserBlock, Meet, UserWishlist, Boss, Cafe, CafeWorktime, CafeGame, UserCafe, CafeBook, CafeBookWantGame, CafeSales, Game, Genre, GameGenre, PlaySystem, GamePlaySystem, GameImage, GameComment, Funding, FundingSchedule
from django.views import generic
import bcrypt
from main.helper import ConvertLocation
import my_settings

# Create your views here.
def intro(request):
    url = my_settings.now_url
    return render(request, 'main/intro.html', {'url' : url})

class GameList(generic.ListView):
    template_name = 'main/gamelist.html'

    def get_queryset(self):
        return Game.objects.order_by('-interest')[:100]


class GameInfo(generic.DetailView):
    model = Game
    template_name = 'main/game.html'


# def game_tutorial(request, game_id):
#     try:
#         tutorial_data = Tutorial.objects.get(game_id = game_id)
#         tutorial_timelines = TutorialTimeLine.objects.filter(tutorial_id = tutorial_data.id).order_by('number')

#         return render(request, 'main/tutorial_link.html', {'tutorial_data' : tutorial_data, 'timelines' : tutorial_timelines})
#     except:
#         return HttpResponse("NULL")

def vicinity_cafe(request):
    data = request.GET
    coords = data['coords'].split(',')
    try:
        user_lat = float(coords[0])
        user_lng = float(coords[1])
    except:
        return HttpResponse("NULL")

    cafes = Cafe.objects.filter(latitude__range=(user_lat - 0.019, user_lat + 0.019),
                                      longitude__range=(user_lng - 0.022, user_lng + 0.022))
    cafes = sorted(cafes, key=lambda cafe: abs(cafe.latitude - user_lat) + abs(cafe.longitude - user_lng))[:5]

    return render(request, 'main/vicinity_cafe.html', {'cafes': cafes}) if cafes else HttpResponse(
        "NULL")


def add_wishlist(request):
    data = request.GET
    user_id = int(data['user_id'])
    game_id = int(data['game_id'])

    obj, created = UserWishlist.objects.get_or_create(user_id=user_id, game_id=game_id)
    return HttpResponse("SUCCESS" if created else "FAIL")


def get_wishlist(request):
    data = request.GET
    user_id = int(data['user_id'])

    wishlist = UserWishlist.objects.filter(user_id=user_id)
    games = [Game.objects.get(id=wish[1].game_id) for wish in enumerate(wishlist)]
    return render(request, 'main/gamelist.html', {'game_list': games})


def del_wishlist(request):
    data = request.GET
    user_id = int(data['user_id'])
    game_id = int(data['game_id'])

    try:
        UserWishlist.objects.get(user_id=user_id, game_id=game_id).delete()
        result = "SUCCESS"
    except:
        result = "FAIL"
    return HttpResponse(result)


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


def add_fav_cafe(request):
    data = request.GET
    user_id = int(data['user_id'])
    cafe_id = int(data['cafe_id'])

    obj, created = UserCafe.objects.get_or_create(user_id=user_id, cafe_id=cafe_id)
    return HttpResponse("SUCCESS" if created else "FAIL")


def get_fav_cafe(request):
    data = request.GET
    user_id = int(data['user_id'])

    cafelist = UserCafe.objects.filter(user_id=user_id)
    cafes = [Cafe.objects.get(id=cafe[1].cafe_id) for cafe in enumerate(cafelist)]
    return render(request, 'main/cafelist.html', {'cafe_list': cafes})


def del_fav_cafe(request):
    data = request.GET
    user_id = int(data['user_id'])
    cafe_id = int(data['cafe_id'])

    try:
        UserCafe.objects.get(user_id=user_id, cafe_id=cafe_id).delete()
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
        return HttpResponse('이미 존재하는 사용자입니다')

    if platform == 0:
        password = data['password']
        obj.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    keys = data.keys()
    if 'name' in keys:                      obj.name = data['name']
    if 'nickname' in keys:                  obj.nickname = data['nickname']
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
        obj = User.objects.get(platform=0, email=email)
        if bcrypt.checkpw(password.encode('utf-8'), obj.password.encode('utf-8')):
            return HttpResponse(f'{obj.id}')
    try:
        token = data['token']
        obj = User.objects.get(platform=platform, token=token)
        return HttpResponse(f'{obj.id}')
    except:
        return HttpResponse('FAIL')

def test(request):
    data = request.GET
    password = data['password']
    print()
    return HttpResponse('SUCCESS')