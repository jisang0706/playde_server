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

class test(CreateAPIView):
    serializer_class = imageSerializer
    queryset = User.objects.all()

def rescale(image):
    img = Image.open(image)
    width, height = img.size
    mn = min(width, height)
    area = ((width - mn) / 2, (height - mn) / 2, (width + mn) / 2, (height + mn) / 2)
    img = img.crop(area)
    img.save(image.name, 'PNG')
    image.file = img

    image.file.name = image.name
    return image

def test(request):
    data = request.POST
    user_id = data.get('user_id')
    obj = User.objects.get(id=user_id)
    image = request.FILES['image']

    image1 = Image.open(image)
    width, height = image1.size
    mn = min(width, height)
    area = ((width - mn) / 2, (height - mn) / 2, (width + mn) / 2, (height + mn) / 2)
    image1 = image1.crop(area)
    buffer1 = BytesIO()
    image1.save(buffer1, format='png')
    file1 = InMemoryUploadedFile(
        buffer1,
        '{}'.format(obj.big_image),
        '{}'.format(obj.big_image),
        'image/png',
        buffer1.tell(),
        None,
    )
    obj.big_image = file1

    image2 = image1.resize((100, 100))
    buffer2 = BytesIO()
    image2.save(buffer2, format='png')
    file2 = InMemoryUploadedFile(
        buffer2,
        '{}'.format(obj.small_image),
        '{}'.format(obj.small_image),
        'image/png',
        buffer2.tell(),
        None,
    )
    obj.small_image = file2
    obj.save()

    return HttpResponse('SUCCESS')