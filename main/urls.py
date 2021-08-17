
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
    path('wishlist/add', views.add_wishlist, name='addwishlist'),
    path('wishlist/get', views.get_wishlist, name='getwishlist'),
    path('wishlist/delete', views.del_wishlist, name='popwishlist'),
    path('block/add', views.add_block, name='addblock'),
    path('block/get', views.get_block, name='getblock'),
    path('block/delete', views.del_block, name='delblock'),
    path('fav_cafe/add', views.add_fav_cafe, name='addfavcafe'),
    path('fav_cafe/get', views.get_fav_cafe, name='getfavcafe'),
    path('fav_cafe/delete', views.del_fav_cafe, name='delfavcafe'),
    path('usercomment/add', views.add_usercomment, name='addusercomment'),
    path('usercomment/get', views.get_usercomment, name='getusercomment'),
    path('user/join', views.join_user, name='joinuser'),
    path('login', views.login, name='login'),
    path('nickname/change', views.set_nickname, name='setnickname'),
    # path('add_meet', views.add_meet, name='addmeet'),
    # path('del_meet', views.del_meet, name='delmeet'),
    # path('get_meet', views.get_meet, name='getmeet'),
    path('playde_game', views.playde_game, name='playdegame'),
    path('game/search', views.search_game, name='searchgame'),
    path('test', views.test, name='test'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)