from django.shortcuts import render, get_object_or_404 , redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from history.templatetags import utils
from history.models import PatientDB
import django, os

def tagging(request):
    if request.user.is_authenticated:
        user_id = request.user
        patient_list = PatientDB.objects.filter(user_id=user_id)
        try:
            user_idx = patient_list[0].user_id
            user_name = User.objects.filter(id=user_idx)
            user_name = user_name[0].username
        
        except:
            user_name = user_id
        