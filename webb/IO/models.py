from django.contrib.auth.models import User
from django.db import models
from .utils import *

# Create your models here.
class Board(models.Model):
    id = models.AutoField(primary_key=True,blank=True,null=False,unique=True)
    patient_id = models.CharField(max_length=20,null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    imgfile = models.ImageField(upload_to=image_upload_path,blank=True,null=True)
    imgfile2 = models.ImageField(upload_to = image_upload_path2, blank=True, null=True)
                        
    def __str__(self):
        return self.patient_id