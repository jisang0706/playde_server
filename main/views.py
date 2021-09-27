import sys

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from PIL import Image
from io import BytesIO

from .models import User, UserComment, UserBlock, UserWishlist, Boss, Cafe, CafeGame, UserCafe,\
    CafeBook, CafeBookWantGame, CafeSales, Game, Genre, GameGenre, PlaySystem, GamePlaySystem, GameImage, GameComment,\
    Funding, FundingSchedule, UserFriend, UserRecent, UserPlayde, Community, CommunityLike, Comment, CommentReply
from django.views import generic
import bcrypt
from django.db.models import Q, ImageField
from main.helper import ConvertLocation
import my_settings

# Create your views here.
def intro(request):
    url = my_settings.now_url
    return render(request, 'main/main_intro.html', {'url' : url})