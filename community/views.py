from PIL import Image
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render
from main.models import User, Community, CommunityLike, Comment, CommentReply, UserBlock, CommunityImage, CommunityReport
import my_settings
from django.db.models import Q
from main.helper.JsonDictionary import returnjson
from community.helper import JsonDictionary, ImageHelper
# Create your views here.

def intro(request):
    url = my_settings.now_url
    return render(request, 'community/community_intro.html', {'url' : url})

def upload_community(request):
    data = request.POST
    user_id = int(data['user_id'])
    content = data['content']
    temporary = bool(data['temp'])

    obj = Community.objects.create(user_id=user_id, content=content, temp=temporary)
    if 'tag' in data.keys():
        obj.tag = data['tag']

    if 'images' in data.keys():
        urls = data['images'].split(',')
        for i, url in enumerate(urls):
            CommunityImage.objects.create(board_id=obj.id, order=i, image=url)

    obj.save()

    boolean = JsonDictionary.BoolToDictionary(True)
    return returnjson(boolean)

def get_community(request):
    data = request.POST
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
    temporary = Q(temp=False)

    block = Q(user_id__in=[block.user_id_blocked for block in UserBlock.objects.filter(user_id=user_id)])
    blocked = Q(user_id__in=[block.user_id for block in UserBlock.objects.filter(user_id_blocked=user_id)])

    community = Community.objects.filter(temporary, tag, top_id, content).exclude(block | blocked).order_by('-created_at')[board_range[0]:board_range[1]]
    users = [User.objects.get(id=board.user_id) for board in community]
    comments = [len(Comment.objects.filter(board_id=board.id)) + len(CommentReply.objects.filter(board_id=board.id)) for board in community]
    likes = [len(CommunityLike.objects.filter(board_id=board.id)) for board in community]
    my_likes = [1 if len(CommunityLike.objects.filter(board_id=board.id, user_id=user_id)) else 0 for board in community]
    community = JsonDictionary.CommunityToDirectory(community, users, likes, my_likes, comments, board_range)

    return returnjson(community)

def del_community(request):
    data = request.POST
    community_id = int(data['board_id'])
    user_id = int(data['user_id'])
    try:
        obj = Community.objects.get(id=community_id)
        if obj.user_id != user_id:
            boolean = False
        else:
            Comment.objects.filter(board_id=obj.id).delete()
            CommentReply.objects.filter(board_id=obj.id).delete()
            CommunityLike.objects.filter(board_id=obj.id).delete()
            CommunityImage.objects.filter(board_id=obj.id).delete()
            CommunityReport.objects.filter(board_id=obj.id).delete()
            obj.delete()
            boolean = True
    finally:
        boolean = JsonDictionary.BoolToDictionary(boolean)
        return returnjson(boolean)

def like_community(request):
    data = request.POST
    user_id = int(data['user_id'])
    board_id = int(data['board_id'])

    obj, create = CommunityLike.objects.get_or_create(user_id=user_id, board_id=board_id)
    boolean = JsonDictionary.BoolToDictionary(create)
    if not create:
        obj.delete()
    return returnjson(boolean)

def upload_comment(request):
    data = request.POST
    user_id = int(data['user_id'])
    board_id = int(data['board_id'])
    content = data['content']

    Comment.objects.create(user_id=user_id, board_id=board_id, content=content)
    boolean = JsonDictionary.BoolToDictionary(True)
    return returnjson(boolean)

def del_comment(request):
    data = request.POST
    user_id = int(data['user_id'])
    comment_id = int(data['comment_id'])
    boolean = True

    try:
        obj = Comment.objects.get(id=comment_id)
        if obj.user_id != user_id:
            boolean = False
        else:
            CommentReply.objects.filter(comment_id=obj.id).delete()
            obj.delete()
    finally:
        boolean = JsonDictionary.BoolToDictionary(boolean)
        return returnjson(boolean)

def upload_reply(request):
    data = request.POST
    user_id = int(data['user_id'])
    comment_id = int(data['comment_id'])
    content = data['content']

    CommentReply.objects.create(user_id=user_id, comment_id=comment_id, board_id=Comment.objects.get(id=comment_id).board_id, content=content)

    boolean = JsonDictionary.BoolToDictionary(True)
    return returnjson(boolean)

def delete_reply(request):
    data = request.POST
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
        return returnjson(boolean)

def view_board(request, board_id):
    data = request.POST
    user_id = int(data['user_id'])

    board = Community.objects.get(id=board_id)
    board.visit += 1
    board.save()
    writer = User.objects.get(id=board.user_id)
    comments = Comment.objects.filter(board_id=board_id).order_by('-created_at')
    comments_writer = []
    for comment in comments:
        try:
            comments_writer.append(User.objects.get(id=comment.user_id))
        except:
            comments_writer.append(0)
    like = len(CommunityLike.objects.filter(board_id=board_id))
    comment_cnt = len(Comment.objects.filter(board_id=board.id)) + len(CommentReply.objects.filter(board_id=board.id))
    try:
        CommunityLike.objects.get(board_id=board_id, user_id=user_id)
        my_like = 1
    except:
        my_like = 0
    replyss = [CommentReply.objects.filter(comment_id=comment.id).order_by('-created_at') for comment in comments]
    replyss_writer = []
    for replys in replyss:
        temp = []
        for reply in replys:
            try:
                temp.append(User.objects.get(id=reply.user_id))
            except:
                temp.append(0)
        replyss_writer.append(temp)
    user_block = [block.user_id_blocked for block in UserBlock.objects.filter(user_id=user_id)]
    board_images = CommunityImage.objects.filter(board_id=board_id).order_by('order')

    board = JsonDictionary.BoardToDirectory(board, board_images, writer, like, my_like, comment_cnt, comments, comments_writer, replyss, replyss_writer, user_block)

    return returnjson(board)

def del_board_image(request):
    data = request.POST
    user_id = int(data['user_id'])
    board_id = int(data['board_id'])
    image_id = int(data['image_id'])

    obj = Community.objects.get(id=board_id)
    if obj.user_id == user_id:
        CommunityImage.objects.get(id=image_id).delete()
        boolean = True
    else:
        boolean = False
    boolean = JsonDictionary.BoolToDictionary(boolean)
    return returnjson(boolean)

def get_temp_community(request):
    data = request.POST
    user_id = int(data['user_id'])
    board_range = [int(rng)-1 for rng in data['range'].split(',')]

    community = Community.objects.filter(user_id=user_id, temp=True).order_by('-created_at')[board_range[0]:board_range[1]]
    community = JsonDictionary.TempCommunityToDirectory(community, board_range)
    return returnjson(community)

def board_report(request, kind):
    data = request.POST
    kind = 0 if kind == 'board' else 1 if kind == 'comment' else 2
    user_id = int(data['user_id'])
    board_id = int(data['content_id'])
    content = data['content']

    obj, create = CommunityReport.objects.get_or_create(user_id=user_id, board_id=board_id, kind=kind)
    obj.content = content
    obj.save()

    boolean = False
    if len(CommunityReport.objects.filter(board_id=board_id, kind=kind)) >= 10:
        if kind == 0 and len(CommunityReport.objects.filter(board_id=board_id, kind=kind)) > len(CommunityLike.objects.filter(board_id=board_id)):
            Comment.objects.filter(board_id=board_id).delete()
            CommentReply.objects.filter(board_id=board_id).delete()
            CommunityLike.objects.filter(board_id=board_id).delete()
            CommunityImage.objects.filter(board_id=board_id).delete()
            CommunityReport.objects.filter(board_id=board_id, kind=kind).delete()
            boolean = True
        elif kind == 1:
            if len(CommentReply.objects.filter(comment_id=board_id)):
                obj = Comment.objects.get(id=board_id)
                obj.content = "삭제된 댓글입니다."
                obj.save()
            else:
                Comment.objects.get(id=board_id).delete()
            CommunityReport.objects.filter(board_id=board_id, kind=kind).delete()
            boolean = True
        elif kind == 2:
            CommentReply.objects.get(id=board_id).delete()
            CommunityReport.objects.filter(board_id=board_id, kind=kind).delete()
            boolean = True

    boolean = JsonDictionary.BoolToDictionary(boolean)
    return returnjson(boolean)