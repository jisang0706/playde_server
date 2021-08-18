from django.urls import path

from . import views

from django.conf.urls.static import static
from django.conf import settings

app_main = 'game'
urlpatterns = [
    path('', views.intro, name='gameintro'),
    path('list', views.game_list, name='gamelist'),
    path('<int:game_id>', views.game_info, name='gameinfo'),
    path('search', views.game_search, name='gamesearch'),
    path('wish/add', views.game_wish_add, name='gamewishadd'),
    path('wish/delete', views.game_wish_del, name='gamewishdel'),
    path('wish', views.game_wish_get, name='gamewish'),
    path('playde', views.game_playde, name='gameplayde'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)