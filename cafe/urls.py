from django.urls import path

from . import views

from django.conf.urls.static import static
from django.conf import settings

app_main = 'cafe'
urlpatterns = [
    path('', views.intro, name='cafeintro'),
    path('list', views.cafe_list, name='cafelist'),
    path('<int:cafe_id>', views.cafe_get, name='get'),
    path('fav', views.get_fav_cafe, name='fav'),
    path('fav/add', views.add_fav_cafe, name='favadd'),
    path('fav/delete', views.del_fav_cafe, name='favdel'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)