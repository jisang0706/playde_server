
from django.urls import path

from . import views

from django.conf.urls.static import static
from django.conf import settings

app_main = 'main'
urlpatterns = [
    path('', views.intro, name='intro'),
    path('game_list', views.GameList, name='gamelist'),
    path('game/<int:game_id>', views.GameInfo, name='gameinfo'),
    # path('tutorial/<int:game_id>', views.game_tutorial, name='gametutorial'),
    path('vicinity_cafe', views.vicinity_cafe, name='cafelatlng'),
    path('add_wishlist', views.add_wishlist, name='addwishlist'),
    path('get_wishlist', views.get_wishlist, name='getwishlist'),
    path('del_wishlist', views.del_wishlist, name='popwishlist'),
    path('add_block', views.add_block, name='addblock'),
    path('get_block', views.get_block, name='getblock'),
    path('del_block', views.del_block, name='delblock'),
    path('add_fav_cafe', views.add_fav_cafe, name='addfavcafe'),
    path('get_fav_cafe', views.get_fav_cafe, name='getfavcafe'),
    path('del_fav_cafe', views.del_fav_cafe, name='delfavcafe'),
    path('add_usercomment', views.add_usercomment, name='addusercomment'),
    path('get_usercomment', views.get_usercomment, name='getusercomment'),
    path('join_user', views.join_user, name='joinuser'),
    path('login', views.login, name='login'),
    path('set_nickname', views.set_nickname, name='setnickname'),
    path('add_meet', views.add_meet, name='addmeet'),
    path('del_meet', views.del_meet, name='delmeet'),
    path('get_meet', views.get_meet, name='getmeet'),
    path('test', views.test, name='test')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)