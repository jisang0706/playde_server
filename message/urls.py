from django.urls import path

from . import views

from django.conf.urls.static import static
from django.conf import settings

app_main = 'message'
urlpatterns = [
    path('', views.intro, name='messageintro'),
    path('send', views.send, name='send'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)