from django.urls import path

from . import views

from django.conf.urls.static import static
from django.conf import settings

app_main = 'user'
urlpatterns = [
    path('', views.intro, name='userintro'),
    path('login', views.login, name='login'),
    path('join', views.join, name='join'),
    path('block', views.get_block, name='block'),
    path('block/add', views.add_block, name='blockadd'),
    path('block/delete', views.del_block, name='blockdelete'),
    path('comment', views.comment, name='usercomment'),
    path('comment/add', views.add_comment, name='useraddcomment'),
    path('nickname/set', views.set_nickname, name='nicknameset'),
    path('profile', views.profile, name='profile'),
    path('profile/image/set', views.set_profile_image, name='profile'),
    path('posible_nickname', views.posible_nickname, name='posiblenickname'),
    path('push_token/set', views.set_push_token, name='setpushtoken'),
    path('profile/chat', views.get_profile_chat, name='getprofilechat'),
    path('friend', views.get_friends, name='getfriends'),
    path('friend/add', views.add_friends, name='addfriend'),
    path('friend/delete', views.del_friends, name='delfriend'),
    path('friend/<kind>', views.get_friends_request, name='getfriendrequest'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)