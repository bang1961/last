from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
##  환자 Json 테이블 -> 환자 id, 방문 낳짜, Json경로 레코드로 구성 
class PatientDB(models.Model):
    patient_id = models.CharField(max_length=50)
    visit_date = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    json_path = models.TextField()
    json_path_sagittal = models.TextField(null=True, default='')
    Tags = models.ManyToManyField(User,blank=True, related_name='Tags')
    Tags_default = models.ManyToManyField(User,blank=True, related_name='Tags_default')
    Tags1 = models.ManyToManyField(User,blank=True, related_name='Tags1')
    Tags_default1 = models.ManyToManyField(User,blank=True, related_name='Tags_default1')
    Tags2 = models.ManyToManyField(User,blank=True, related_name='Tags2')
    Tags_default2 = models.ManyToManyField(User,blank=True, related_name='Tags_default2')
    Tags3 = models.ManyToManyField(User,blank=True, related_name='Tags3')
    Tags_default3 = models.ManyToManyField(User,blank=True, related_name='Tags_default3')
    @property
    def total_likes(self):
        return self.Tags.count()
    @property
    def total_dislikes(self):
        return self.Tags_default.count()
    @property
    def total_likes1(self):
        return self.Tags1.count()
    @property
    def total_dislikes1(self):
        return self.Tags_default1.count()
    @property
    def total_likes2(self):
        return self.Tags2.count()
    @property
    def total_dislikes2(self):
        return self.Tags_default2.count()
    @property
    def total_likes3(self):
        return self.Tags3.count()
    @property
    def total_dislikes3(self):
        return self.Tags_default3.count()

    ##  클래스가 호출될 때 한 개의 레코드씩 반환됨.
    def __str__(self):
        return f'patient id : {str(self.patient_id)} / visit date : {self.visit_date}'

class Ment(models.Model):
    post = models.ForeignKey(PatientDB, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    id = models.AutoField(primary_key=True,blank=True,null=False,unique=True)
    body = models.TextField(max_length=200,blank=True,default=None,null = True)
    date = models.DateTimeField(default=timezone.now)
    interpretation = models.TextField(max_length=200,blank=True,default=None,null = True)

    def getpost(self):
        return self.post.id


class Nodule(models.Model):
    id = models.AutoField(primary_key=True,blank=True,null=False,unique=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    Vote = models.BooleanField(default=False, db_column='결절_1')

class Nodule1(models.Model):
    id = models.AutoField(primary_key=True,blank=True,null=False,unique=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    Vote = models.BooleanField(default=False, db_column='결절_2')

class Nodule2(models.Model):
    id = models.AutoField(primary_key=True,blank=True,null=False,unique=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    Vote = models.BooleanField(default=False, db_column='결절_3')

class Nodule3(models.Model):
    id = models.AutoField(primary_key=True,blank=True,null=False,unique=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    Vote = models.BooleanField(default=False, db_column='결절_4')