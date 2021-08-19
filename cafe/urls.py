
from django.urls import path

from . import views

from django.conf.urls.static import static
from django.conf import settings

app_main = 'cafe'
urlpatterns = [
    path('', views.intro, name='cafeintro'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)