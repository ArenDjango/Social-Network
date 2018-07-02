from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .views import *

app_name = 'chat'

urlpatterns = [
	path('', chated, name='chat')
]