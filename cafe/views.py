from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from main.models import User, UserComment, UserBlock, UserWishlist, Boss, Cafe, CafeWorktime, CafeGame, UserCafe,\
    CafeBook, CafeBookWantGame, CafeSales, Game, Genre, GameGenre, PlaySystem, GamePlaySystem, GameImage, GameComment,\
    Funding, FundingSchedule, UserFriend, UserRecent, UserPlayde, Community, CommunityLike, Comment, CommentReply
import my_settings
from django.db.models import Q
from cafe.helper import JsonDictionary
# Create your views here.

def intro(request):
    url = my_settings.now_url
    return render(request, 'cafe/cafe_intro.html', {'url' : url})