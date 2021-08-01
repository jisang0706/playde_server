
from django.urls import path

from . import views

from django.conf.urls.static import static
from django.conf import settings

app_main = 'main'
urlpatterns = [
    path('', views.intro, name='intro'),
    path('game_list', views.GameList.as_view(), name='gamelistinfo'),
    path('game/<int:pk>', views.GameInfo.as_view(), name='gmaeinfo'),
    # path('tutorial/<int:game_id>', views.game_tutorial, name='gametutorial'),
    path('cafelatlng/<user_lat>/<user_lng>', views.cafe_latlng, name='cafelatlng'),
    path('add_wishlist/<user_token>/<int:game_id>', views.add_wishlist, name='addwishlist'),
    path('get_wishlist/<user_token>', views.get_wishlist, name='getwishlist'),
    path('del_wishlist/<user_token>/<int:game_id>', views.del_wishlist, name='popwishlist'),
    path('add_block/<user_token>/<int:other_user_id>', views.add_block, name='addblock'),
    path('get_block/<user_token>', views.get_block, name='getblock'),
    path('del_block/<user_token>/<int:other_user_id>', views.del_block, name='delblock'),
    path('add_fav_cafe/<user_token>/<int:cafe_id>', views.add_fav_cafe, name='addfavcafe'),
    path('get_fav_cafe/<user_token>', views.get_fav_cafe, name='getfavcafe'),
    path('del_fav_cafe/<user_token>/<int:cafe_id>', views.del_fav_cafe, name='delfavcafe'),
    path('add_usercomment/<my_token>/<int:his_id>/<int:score>/<comment>', views.add_usercomment, name='addusercomment'),
    path('get_usercomment/<user_id>/<int:is_me>', views.get_usercomment, name='getusercomment'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)