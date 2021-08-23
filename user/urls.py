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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)