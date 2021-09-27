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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)