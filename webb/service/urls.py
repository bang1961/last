from django.urls import path
from .views import *

app_name = 'ServiceConfig' 
urlpatterns = [
    path(r'','service.urls'),
]