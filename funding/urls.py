from django.urls import path

from . import views

from django.conf.urls.static import static
from django.conf import settings

app_main = 'user'
urlpatterns = [
    path('', views.intro, name='fundingintro'),
    path('list', views.get_funding_list, name='fundinglist'),
    path('<int:funding_id>', views.get_funding_board, name='fundingboard'),
    path('<int:funding_id>/news', views.get_funding_board_news, name='fundingboardnews'),
    path('news/<int:news_id>', views.get_funding_news_board, name='newsdetail'),
    path('news', views.get_funding_news, name='fundingnews'),
    path('<int:funding_id>/community', views.get_funding_community, name='fundingcommunity'),
    path('<int:funding_id>/community/upload', views.upload_funding_community, name='fundingcommunityupload'),
    path('<int:funding_id/community/delete', views.delete_funding_community, name='fundingcommunitydelete'),
    path('<int:funding_id>/calendar/upload', views.upload_funding_calendar, name='fundinguploadcalendar'),
    path('<int:funding_id>/calendar/delete', views.delete_funding_calendar, name='fundingdeleteschedule'),
    path('calendar', views.get_funding_calendar, name='fundinggetcalendar'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)