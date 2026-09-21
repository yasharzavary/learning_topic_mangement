from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('create/', create_topic, name='create_topic')
]
