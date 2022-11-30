from django.urls import path
from .views import *

urlpatterns = [
    path('home/signup/', signup, name='signup'),
    path('home/login/', login, name='login'),
    path('home/logout/', logout, name='logout'),
    path('home/', home, name='home'),
    #path('home/signup/', id_check, name='id_check'),
    path('home/save_json/', save_json, name='save_json')


]