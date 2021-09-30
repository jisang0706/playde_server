from django.urls import path

from . import views

from django.conf.urls.static import static
from django.conf import settings

app_main = 'community'
urlpatterns = [
    path('', views.intro, name='communityintro'),
    path('board/upload', views.upload_community, name='uploadcommunity'),
    path('get', views.get_community, name='getcommunity'),
    path('board/delete', views.del_community, name='delcommunity'),
    path('board/like', views.like_community, name='likecommunity'),
    path('comment/upload', views.upload_comment, name='uploadcomment'),
    path('comment/delete', views.del_comment, name='delcomment'),
    path('reply/upload', views.upload_reply, name='uploadreply'),
    path('reply/delete', views.delete_reply, name='deletereply'),
    path('board/<int:board_id>', views.view_board, name='board'),
    path('board/image/delete', views.del_board_image, name='boardimagedelete'),
    path('temp/get', views.get_temp_community, name='tempget'),
    path('<kind>/report', views.board_report, name='boardreport'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)