
from django.urls import path

from . import views

from django.conf.urls.static import static
from django.conf import settings

app_main = 'main'
urlpatterns = [
    path('', views.intro, name='intro'),
    # path('tutorial/<int:game_id>', views.game_tutorial, name='gametutorial'),
    path('block/add', views.add_block, name='addblock'),
    path('block/get', views.get_block, name='getblock'),
    path('block/delete', views.del_block, name='delblock'),
    path('usercomment/add', views.add_usercomment, name='addusercomment'),
    path('usercomment/get', views.get_usercomment, name='getusercomment'),
    path('user/join', views.join_user, name='joinuser'),
    path('login', views.login, name='login'),
    path('nickname/change', views.set_nickname, name='setnickname'),
    path('test', views.test, name='test'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)