from django.urls import path
from .views import *
from history.views import *
from UTIL.config import AGREE

## UTIL/config.py 파일의 AGREE 변수에 맞춰 표시되는 페이지 수정  ##
BOARD = 'board/' if AGREE else ''
AGREE_PAGE = '' if AGREE  else 'agree/'

urlpatterns = [
    path(BOARD, board, name='board'),
    path(AGREE_PAGE, agree, name='agree'),
    path('agreeimgsave/', agreeimgsave, name='agreeimgsave'),
    path('edit/<int:pk>', boardEdit, name='edit'),
    path('delete/<int:pk>', boardDelete, name='delete'),
    path('<int:id>', tagging_history_detail, name='detail'),
]