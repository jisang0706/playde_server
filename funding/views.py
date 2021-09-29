from django.shortcuts import render
from main.models import User, Funding, FundingTag, FundingFav, FundingNews, FundingCommunity
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

def get_funding_news_board(request, news_id):
    news = FundingNews.obejcts.get(id=news_id)
    writer = User.objects.get(id=news.writer_id)
    news = JsonDictionary.FundingNewsToDictionary(news, writer)
    return returnjson(news)

def get_funding_news(request):
    data = request.POST
    rng = [int(rng)-1 for rng in data['range'].split(',')]
    if 'top_id' in data.keys():
        top_id = int(data['top_id'])
        top_id = Q(id__lte=top_id)
    else:
        top_id = Q(id__gte=0)
    news = FundingNews.objects.filter(top_id).order_by('-written_date')[rng[0]:rng[1]]
    for i in range(len(news)):
        news[i].funding_name = Funding.objects.get(id=news[i].funding_id).name
    news = JsonDictionary.FundingNewslistToDictionary(news, rng)
    return returnjson(news)

def get_funding_community(request, funding_id):
    data = request.POST
    user_id = int(data['user_id'])
    tag = data['tag']
    if 'top_id' in data.keys():
        top_id = int(data['top_id'])
        top_id = Q(id__lte=top_id)
    else:
        top_id = Q(id__gte=0)
    rng = [int(rng)-1 for rng in data['range'].split(',')]
    funding_user_id = Funding.objects.get(id=funding_id)
    community = FundingCommunity.objects.filter(Q(funding_id=funding_id), top_id, Q(tag=tag), Q(parent_id=0)).order_by('-written_date')[rng[0]:rng[1]]
    for i in range(len(community)):
        try:
            community[i].user = User.objects.get(id=community[i].writer_id)
        except:
            community[i].user = 0

    for i in range(len(community)):
        community[i].replys = FundingCommunity.objects.filter(parent_id=community[i].id).order_by('written_date')
        for j in range(len(community[i].replys)):
            try:
                community[i].replys[j].user = User.objects.get(id=community[i].replys[j].writer_id)
            except:
                community[i].replys[j].user = 0
    community = JsonDictionary.FundingCommunityToDictionary(community, user_id, funding_user_id, rng)
    return returnjson(community)

def upload_funding_community(request, funding_id):
    data = request.POST
    user_id = int(data['user_id'])
    tag = data['tag']
    content = data['content']
    try:
        board_id = int(data['board_id'])
        board = FundingCommunity.objects.get(id=board_id)
        funding = Funding.objects.get(id=funding_id)
        if board.secret and user_id != board.writer_id and user_id != funding.user_id:
            return returnjson(JsonDictionary.BoolToDictionary(False))
    except:
        board_id = 0
        board = 0
    try:
        secret = bool(data['secret'])
    except:
        secret = False if board != 0 and not board.secret else True

    FundingCommunity.objects.create(funding_id=funding_id, content=content, writer_id=user_id, tag=tag, parent_id=board_id, secret=secret)
    return returnjson(JsonDictionary.BoolToDictionary(True))

def delete_funding_community(request, funding_id):
    data = request.POST
    user_id = int(data['user_id'])
    board_id = int(data['board_id'])
    if user_id == Funding.objects.get(id=funding_id).user_id or user_id == FundingCommunity.objects.get(id=board_id).writer_id:
        FundingCommunity.objects.get(id=board_id).delete()
        return returnjson(JsonDictionary.BoolToDictionary(True))
    return returnjson(JsonDictionary.BoolToDictionary(False))