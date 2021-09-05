from django.shortcuts import render
from main.models import UserWishlist, Game, GameImage, UserPlayde
import my_settings
from django.db.models import Q, Min
from main.helper.JsonDictionary import returnjson
from game.helper import JsonDictionary
# Create your views here.

def intro(request):
    url = my_settings.now_url
    return render(request, 'game/game_intro.html', {'url' : url})

def game_list(request):
    data = request.GET
    user_id = int(data['user_id'])
    game_range = [int(num)-1 for num in data['range'].split(',')]
    games = Game.objects.order_by('-interest')[game_range[0]:game_range[1]]
    images = [GameImage.objects.filter(game_id=game.id).order_by('order')[0]
              if GameImage.objects.filter(game_id=game.id).order_by('order') else 0 for game in games]
    for i, image in enumerate(images):
        games[i].image = image
    my_likes = [True if UserWishlist.objects.filter(game_id=game.id, user_id=user_id) else False for game in games]
    for i, my_like in enumerate(my_likes):
        games[i].my_like = my_like
    games = JsonDictionary.GamesToDictionary(games, game_range)

    return returnjson(games)

def game_info(request, game_id):
    data = request.GET
    user_id = data['user_id']
    game = Game.objects.get(id=game_id)
    game.interest += 1
    game.save()
    game_images = GameImage.objects.filter(game_id=game_id).order_by('order')
    my_like = True if UserWishlist.objects.filter(game_id=game.id, user_id=user_id) else False
    game = JsonDictionary.GameinfoToDictionary(game, my_like, game_images)


    return returnjson(game)

def game_search(request):
    data = request.GET
    user_id = int(data['user_id'])
    game_name = data['game_name']
    game_range = [int(num) - 1 for num in data['range'].split(',')]
    games = Game.objects.filter(Q(kor_name__icontains=game_name)|Q(eng_name__icontains=game_name)).order_by('-interest')[game_range[0]:game_range[1]]
    images = [GameImage.objects.filter(game_id=game.id).order_by('order')[0]
              if GameImage.objects.filter(game_id=game.id).order_by('order') else 0 for game in games]
    for i, image in enumerate(images):
        games[i].image = image
    my_likes = [True if UserWishlist.objects.filter(game_id=game.id, user_id=user_id) else False for game in games]
    for i, my_like in enumerate(my_likes):
        games[i].my_like = my_like
    games = JsonDictionary.GamesToDictionary(games, game_range)

    return returnjson(games)

def game_wish_add(request):
    data = request.GET
    user_id = int(data['user_id'])
    game_id = int(data['game_id'])
    UserWishlist.objects.get_or_create(user_id=user_id, game_id=game_id)
    boolean = JsonDictionary.BoolToDictionary(True)
    return returnjson(boolean)

def game_wish_get(request):
    data = request.GET
    user_id = int(data['user_id'])
    wishlist = UserWishlist.objects.filter(user_id=user_id)
    games = [Game.objects.get(id=wish[1].game_id) for wish in enumerate(wishlist)]
    games = JsonDictionary.GamesToDictionary(games, [0,len(games)])
    print(games)
    return returnjson(games)

def game_wish_del(request):
    data = request.GET
    user_id = int(data['user_id'])
    game_id = int(data['game_id'])
    UserWishlist.objects.get_or_create(user_id=user_id, game_id=game_id).delete()
    boolean = JsonDictionary.BoolToDictionary(True)
    return returnjson(boolean)

def game_playde(request):
    data = request.GET
    user_id = int(data['user_id'])
    game_ids = [int(game_id) for game_id in data['game_ids'].split(',')]
    for game_id in game_ids:
        UserPlayde.objects.get_or_create(user_id=user_id, game_id=game_id)
    boolean = JsonDictionary.BoolToDictionary(True)
    return returnjson(boolean)
