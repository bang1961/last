from django.urls import path
from .views import *

app_name = 'chart' 
urlpatterns = [
    path('', chart_page, name='chart_page'),
]