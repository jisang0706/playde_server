from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from main.models import User, UserComment, UserBlock, UserWishlist, Boss, Cafe, CafeWorktime, CafeGame, UserCafe,\
    CafeBook, CafeBookWantGame, CafeSales, Game, Genre, GameGenre, PlaySystem, GamePlaySystem, GameImage, GameComment,\
    Funding, FundingSchedule, UserFriend, UserRecent, UserPlayde, Community, CommunityLike, Comment, CommentReply
import my_settings
from django.db.models import Q
from game.helper import JsonDictionary
# Create your views here.

def intro(request):
    url = my_settings.now_url
    return render(request, 'game/intro.html', {'url' : url})

def game_list(request):
    data = request.GET
    game_range = [int(num) for num in data['range'].split(',')]
    games = Game.objects.order_by('-interest')[game_range[0]:game_range[1]]
    games = JsonDictionary.GamesToDictionary(games, game_range)

    return JsonResponse(games, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def game_info(request, game_id):
    game = Game.objects.get(id=game_id)
    game.interest += 1
    game.save()
    game_images = GameImage.objects.filter(game_id=game_id).order_by('order')
    game = JsonDictionary.GameinfoToDictionary(game, game_images)

    return JsonResponse(game, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def game_search(request):
    data = request.GET
    game_name = data['game_name']
    game_range = [int(rng) for rng in data['range'].split(',')]
    games = Game.objects.filter(Q(kor_name__icontains=game_name)|Q(eng_name__icontains=game_name)).order_by('-interest')[game_range[0]:game_range[1]]
    games = JsonDictionary.GamesToDictionary(games, game_range)

    return JsonResponse(games, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def game_wish_add(request):
    data = request.GET
    user_id = int(data['user_id'])
    game_id = int(data['game_id'])
    UserWishlist.objects.get_or_create(user_id=user_id, game_id=game_id)
    boolean = JsonDictionary.BoolToDictionary(True)
    return JsonResponse(boolean, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def game_wish_get(request):
    data = request.GET
    user_id = int(data['user_id'])
    wishlist = UserWishlist.objects.filter(user_id=user_id)
    games = [Game.objects.get(id=wish[1].game_id) for wish in enumerate(wishlist)]
    games = JsonDictionary.GamesToDictionary(games, [0,len(games)])
    print(games)
    return JsonResponse(games, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def game_wish_del(request):
    data = request.GET
    user_id = int(data['user_id'])
    game_id = int(data['game_id'])
    UserWishlist.objects.get_or_create(user_id=user_id, game_id=game_id).delete()
    boolean = JsonDictionary.BoolToDictionary(True)
    return JsonResponse(boolean, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def game_playde(request):
    data = request.GET
    user_id = int(data['user_id'])
    game_ids = [int(game_id) for game_id in data['game_ids'].split(',')]
    for game_id in game_ids:
        UserPlayde.objects.get_or_create(user_id=user_id, game_id=game_id)
    boolean = JsonDictionary.BoolToDictionary(True)
    return JsonResponse(boolean, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)
