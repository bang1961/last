from django.urls import path
from .views import *

app_name = 'history' 
urlpatterns = [
    path('', tagging_history_total_list, name='tagging_patient_total_history'),
    path('tagging_history', tagging_history_partial_list, name='tagging_history'),
    path('pretagging',tagging_tables_pre_tagging, name = 'tagging_tables_pre_tagging'),
    path('preinterpretation', tagging_tables_pre_interpretion, name = 'tagging_tables_pre_interpretion'),

    path('<int:id>', tagging_history_detail, name='detail'),

    path('remove/<int:pk>', HDDelete, name='remove'),
    path('<int:id>/ments', tagging_history_detail, name='detail2'),
    path('<int:id>/ments/<int:comment_id>', ment_delete, name='ment_delete'),




    path('like', like ,name='like'), path('like_ready', like_ready,name='like_ready'),
    path('dislike', dislike ,name='dislike'), path('dislike_ready', dislike_ready,name='dislike_ready'),
    path('tagging_reset_like', tagging_reset_like ,name='tagging_reset_like'), path('tagging_reset_dislike', tagging_reset_dislike ,name='tagging_reset_dislike'),
    
    path('like1', like1 ,name='like1'), path('like_ready1', like_ready1,name='like_ready1'),
    path('dislike1', dislike1 ,name='dislike1'), path('dislike_ready1', dislike_ready1,name='dislike_ready1'),
    path('tagging_reset_like1', tagging_reset_like1 ,name='tagging_reset_like1'), path('tagging_reset_dislike1', tagging_reset_dislike1 ,name='tagging_reset_dislike1'),

    path('like2', like2 ,name='like2'), path('like_ready2', like_ready2,name='like_ready2'),
    path('dislike2', dislike2 ,name='dislike2'), path('dislike_ready2', dislike_ready2,name='dislike_ready2'),
    path('tagging_reset_like2', tagging_reset_like2 ,name='tagging_reset_like2'), path('tagging_reset_dislike2', tagging_reset_dislike2 ,name='tagging_reset_dislike2'),

    path('like3', like3 ,name='like3'), path('like_ready3', like_ready3,name='like_ready3'),
    path('dislike3', dislike3 ,name='dislike3'), path('dislike_ready3', dislike_ready3,name='dislike_ready3'),
    path('tagging_reset_like3', tagging_reset_like3 ,name='tagging_reset_like3'), path('tagging_reset_dislike3', tagging_reset_dislike3 ,name='tagging_reset_dislike3'),
]