from django.shortcuts import render
from django.http import HttpResponse
from main.models import User, UserComment, UserBlock, UserWishlist, Boss, Cafe, CafeWorktime, CafeGame, UserCafe,\
    CafeBook, CafeBookWantGame, CafeSales, Game, Genre, GameGenre, PlaySystem, GamePlaySystem, GameImage, GameComment,\
    Funding, FundingSchedule, UserFriend, UserRecent, UserPlayde, Community, CommunityLike, Comment, CommentReply
from django.db.models import Q
# Create your views here.

def upload_community(request):
    data = request.GET
    user_id = int(data['user_id'])
    content = data['content']

    Community.objects.create(user_id=user_id, content=content)
    return HttpResponse('SUCCESS')

def get_community(request):
    data = request.GET
    user_id = int(data['user_id'])
    range = [int(rng) for rng in data['range'].split(',')]
    try:
        top_id = int(data['top_id'])
        communitys = Community.objects.filter(id__lte=top_id).order_by('-created_at')[range[0]:range[1]]
    except:
        communitys = Community.objects.all().order_by('-created_at')[range[0]:range[1]]


    users = [User.objects.get(id=community.user_id) for community in communitys]
    comments = [len(Comment.objects.filter(board_id=community.id)) for community in communitys]
    likes = [len(CommunityLike.objects.filter(board_id=community.id)) for community in communitys]
    my_likes = [1 if len(CommunityLike.objects.filter(board_id=community.id, user_id=user_id)) else 0 for community in communitys]

    return render(request, 'community/community.html', {'datas':list(zip(communitys, users, likes, my_likes, comments))})

def del_community(request):
    data = request.GET
    community_id = int(data['board_id'])
    user_id = int(data['user_id'])
    try:
        obj = Community.objects.get(id=community_id)
        if obj.user_id != user_id:
            return HttpResponse('FAIL')
        Comment.objects.filter(board_id=obj.id).delete()
        CommunityLike.objects.filter(board_id=obj.id).delete()
        obj.delete()
    finally:
        return HttpResponse('SUCCESS')

def like_community(request):
    data = request.GET
    user_id = int(data['user_id'])
    board_id = int(data['board_id'])

    obj, create = CommunityLike.objects.get_or_create(user_id=user_id, board_id=board_id)
    if create:
        return HttpResponse('LIKE')
    obj.delete()
    return HttpResponse('UNLIKE')

def upload_comment(request):
    data = request.GET
    user_id = int(data['user_id'])
    board_id = int(data['board_id'])
    content = data['content']

    Comment.objects.create(user_id=user_id, board_id=board_id, content=content)
    return HttpResponse('SUCCESS')

def del_comment(request):
    data = request.GET
    user_id = int(data['user_id'])
    comment_id = int(data['comment_id'])
    rt = 'SUCCESS'

    try:
        obj = Comment.objects.get(id=comment_id)
        if obj.user_id != user_id:
            rt = 'FAIL'
        else:
            obj.delete()
    finally:
        return HttpResponse(rt)

def upload_reply(request):
    data = request.GET
    user_id = int(data['user_id'])
    comment_id = int(data['comment_id'])
    content = data['content']

    CommentReply.objects.create(user_id=user_id, comment_id=comment_id, content=content)
    return HttpResponse('SUCCESS')

def delete_reply(request):
    data = request.GET
    user_id = int(data['user_id'])
    reply_id = int(data['reply_id'])
    rt = 'SUCCESS'

    try:
        obj = CommentReply.objects.get(id=reply_id)
        if obj.user_id != user_id:
            rt = 'FAIL'
        else:
            obj.delete()
    finally:
        return HttpResponse(rt)

def view_board(request, board_id):
    data = request.GET
    user_id = int(data['user_id'])

    board = Community.objects.get(id=board_id)
    writer = User.objects.get(id=board.user_id)
    comments = Comment.objects.filter(board_id=board_id).order_by('-created_at')
    comments_writer = [User.objects.filter(id=comment.user_id)[0] for comment in comments]
    like = len(CommunityLike.objects.filter(board_id=board_id))
    comment_cnt = len(Comment.objects.filter(board_id=board.id))
    try:
        CommunityLike.objects.get(board_id=board_id, user_id=user_id)
        my_like = 1
    except:
        my_like = 0
    replyss = [CommentReply.objects.filter(comment_id=comment.id).order_by('-created_at') for comment in comments]
    replyss_writer = [[User.objects.filter(id=reply.user_id)[0] for reply in replys] for replys in replyss]
    replyss_and_writerss = list()
    for replys, replys_writer in zip(replyss, replyss_writer):
        temp = [[reply, reply_writer] for reply, reply_writer in zip(replys, replys_writer)]
        replyss_and_writerss.append(temp)

    print(len(replyss[0]))
    context = {
        'board':board,
        'writer':writer,
        'like':like,
        'my_like':my_like,
        'comment_cnt':comment_cnt,
        'comments':list(zip(comments, comments_writer, replyss_and_writerss)),
    }

    return render(request, 'community/board.html', context)