from django.forms import ModelForm
from .models import *

class MentForm(ModelForm):
    class Meta:
        model = Ment
        fields = ('body',)

class InterpretationForm(ModelForm):
    class Meta:
        model = Ment
        fields = ('interpretation',)


class TaggingForm(ModelForm):
    class Meta:
        model = Nodule
        fields = ('id','user','Vote',)
