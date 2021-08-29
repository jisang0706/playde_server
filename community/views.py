from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from main.models import User, Community, CommunityLike, Comment, CommentReply
import my_settings
from django.db.models import Q
from community.helper import JsonDictionary
# Create your views here.

def intro(request):
    url = my_settings.now_url
    return render(request, 'community/community_intro.html', {'url' : url})

def upload_community(request):
    data = request.GET
    user_id = int(data['user_id'])
    content = data['content']

    obj = Community.objects.create(user_id=user_id, content=content)
    try:
        tag = data['tag']
        obj.tag = tag
        obj.save()
    except:
        1

    boolean = JsonDictionary.BoolToDictionary(True)
    return JsonResponse(boolean, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def get_community(request):
    data = request.GET
    user_id = int(data['user_id'])
    board_range = [int(rng)-1 for rng in data['range'].split(',')]

    if 'tag' in data.keys():
        tag = data['tag']
        tag = Q(tag=tag)
    else:
        tag = Q(tag__icontains='')

    if 'top_id' in data.keys():
        top_id = int(data['top_id'])
        top_id = Q(id__lte=top_id)
    else:
        top_id = Q(id__gte=0)

    if 'content' in data.keys():
        content = data['content']
        content = Q(content__icontains=content)
    else:
        content = Q(content__icontains='')

    community = Community.objects.filter(tag, top_id, content).order_by('-created_at')[board_range[0]:board_range[1]]
    users = [User.objects.get(id=board.user_id) for board in community]
    comments = [len(Comment.objects.filter(board_id=board.id)) + len(CommentReply.objects.filter(board_id=board.id)) for board in community]
    likes = [len(CommunityLike.objects.filter(board_id=board.id)) for board in community]
    my_likes = [1 if len(CommunityLike.objects.filter(board_id=board.id, user_id=user_id)) else 0 for board in community]
    community = JsonDictionary.CommunityToDirectory(community, users, likes, my_likes, comments, board_range)

    return JsonResponse(community, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def del_community(request):
    data = request.GET
    community_id = int(data['board_id'])
    user_id = int(data['user_id'])
    try:
        obj = Community.objects.get(id=community_id)
        if obj.user_id != user_id:
            boolean = False
        else:
            Comment.objects.filter(board_id=obj.id).delete()
            CommunityLike.objects.filter(board_id=obj.id).delete()
            obj.delete()
            boolean = True
    finally:
        boolean = JsonDictionary.BoolToDictionary(boolean)
        return JsonResponse(boolean, json_dumps_params={'ensure_ascii': False},
                            content_type=u"application/json; charset=utf-8", status=200)

def like_community(request):
    data = request.GET
    user_id = int(data['user_id'])
    board_id = int(data['board_id'])

    obj, create = CommunityLike.objects.get_or_create(user_id=user_id, board_id=board_id)
    boolean = JsonDictionary.BoolToDictionary(create)
    if not create:
        obj.delete()
    return JsonResponse(boolean, json_dumps_params={'ensure_ascii': False},
                            content_type=u"application/json; charset=utf-8", status=200)

def upload_comment(request):
    data = request.GET
    user_id = int(data['user_id'])
    board_id = int(data['board_id'])
    content = data['content']

    Comment.objects.create(user_id=user_id, board_id=board_id, content=content)
    boolean = JsonDictionary.BoolToDictionary(True)
    return JsonResponse(boolean, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def del_comment(request):
    data = request.GET
    user_id = int(data['user_id'])
    comment_id = int(data['comment_id'])
    boolean = True

    try:
        obj = Comment.objects.get(id=comment_id)
        if obj.user_id != user_id:
            boolean = False
        else:
            obj.delete()
    finally:
        boolean = JsonDictionary.BoolToDictionary(boolean)
        return JsonResponse(boolean, json_dumps_params={'ensure_ascii': False},
                            content_type=u"application/json; charset=utf-8", status=200)

def upload_reply(request):
    data = request.GET
    user_id = int(data['user_id'])
    comment_id = int(data['comment_id'])
    content = data['content']

    CommentReply.objects.create(user_id=user_id, comment_id=comment_id, board_id=Comment.objects.get(id=comment_id).board_id, content=content)

    boolean = JsonDictionary.BoolToDictionary(True)
    return JsonResponse(boolean, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def delete_reply(request):
    data = request.GET
    user_id = int(data['user_id'])
    reply_id = int(data['reply_id'])
    boolean = True

    try:
        obj = CommentReply.objects.get(id=reply_id)
        if obj.user_id != user_id:
            boolean = False
        else:
            obj.delete()
    finally:
        boolean = JsonDictionary.BoolToDictionary(boolean)
        return JsonResponse(boolean, json_dumps_params={'ensure_ascii': False},
                            content_type=u"application/json; charset=utf-8", status=200)

def view_board(request, board_id):
    data = request.GET
    user_id = int(data['user_id'])

    board = Community.objects.get(id=board_id)
    board.visit += 1
    board.save()
    writer = User.objects.get(id=board.user_id)
    comments = Comment.objects.filter(board_id=board_id).order_by('-created_at')
    comments_writer = [User.objects.filter(id=comment.user_id)[0] for comment in comments]
    like = len(CommunityLike.objects.filter(board_id=board_id))
    comment_cnt = len(Comment.objects.filter(board_id=board.id)) + len(CommentReply.objects.filter(board_id=board.id))
    try:
        CommunityLike.objects.get(board_id=board_id, user_id=user_id)
        my_like = 1
    except:
        my_like = 0
    replyss = [CommentReply.objects.filter(comment_id=comment.id).order_by('-created_at') for comment in comments]
    replyss_writer = [[User.objects.filter(id=reply.user_id)[0] for reply in replys] for replys in replyss]

    board = JsonDictionary.BoardToDirectory(board, writer, like, my_like, comment_cnt, comments, comments_writer, replyss, replyss_writer)

    return JsonResponse(board, json_dumps_params={'ensure_ascii': False},
                            content_type=u"application/json; charset=utf-8", status=200)