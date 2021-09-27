from django.shortcuts import render
from main.models import User, Funding, FundingTag, FundingFav, FundingNews
import my_settings
import bcrypt
from django.db.models import Q
from main.helper.JsonDictionary import returnjson
from funding.helper import JsonDictionary
# Create your views here.

def intro(request):
    url = my_settings.now_url
    return render(request, 'funding/funding_intro.html', {'url' : url})

def get_funding_list(request):
    data = request.POST
    if 'top_id' in data.keys():
        top_id = int(data['top_id'])
        top_id = Q(id__lte=top_id)
    else:
        top_id = Q(id__gte=0)
    rng = [int(rng)-1 for rng in data['range'].split(',')]

    fundings = Funding.objects.filter(top_id).order_by('-upload_date')[rng[0]:rng[1]]
    tags = []
    for funding in fundings:
        try:
            tags.append(FundingTag.objects.filter(funding_id=funding.id))
        except:
            tags.append(0)
    fundings = JsonDictionary.FundingsToDictionary(fundings, tags, rng)
    return returnjson(fundings)

def get_funding_board(request, funding_id):
    data = request.POST
    user_id = int(data['user_id'])
    funding = Funding.objects.get(id=funding_id)
    tags = FundingTag.objects.filter(funding_id=funding_id)
    funding_fav = bool(FundingFav.objects.filter(funding_id=funding_id, user_id=user_id))
    funding = JsonDictionary.FundingToDictionary(funding, tags, funding_fav)
    return returnjson(funding)

def get_funding_board_news(request, funding_id):
    data = request.POST
    srt = '-written_date' if int(data['sort']) else 'written_date'
    if 'top_id' in data.keys():
        top_id = int(data['top_id'])
        top_id = Q(id__lte=top_id)
    else:
        top_id = Q(id__gte=0)
    rng = [int(rng)-1 for rng in data['range'].split(',')]
    news = FundingNews.objects.filter(Q(funding_id=funding_id), top_id).order_by(srt)[rng[0]:rng[1]]
    users = []
    for new in news:
        try:
            users.append(User.objects.get(id=new.writer_id))
        except:
            users.append(0)
    news = JsonDictionary.FundingBoardNewsToDictionary(news, users, rng)
    return returnjson(news)