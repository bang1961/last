from django.forms import ModelForm
from .models import *

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['patient_id','id']
        #fields = ['patient_id','id','imgfile','imgfile2']