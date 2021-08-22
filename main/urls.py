
from django.urls import path

from . import views

from django.conf.urls.static import static
from django.conf import settings

app_main = 'main'
urlpatterns = [
    path('', views.intro, name='intro'),
    path('test', views.test, name='test'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)