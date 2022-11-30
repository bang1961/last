from django.contrib import admin
from history.models import *




class PatientDBAdmin(admin.ModelAdmin):
    list_display = ['patient_id','visit_date','user','json_path']
    list_filter =  ['patient_id','visit_date','user','json_path']
    list_display_links = ['json_path']
    search_fields = ['patient_id','visit_date','user','json_path']
admin.site.register(PatientDB,PatientDBAdmin)

class MentAdmin(admin.ModelAdmin):
    list_display = ['id','post','body','date','user','interpretation']
admin.site.register(Ment,MentAdmin)

class NoduleAdmin(admin.ModelAdmin):
    list_display = ['id','user','Vote']

admin.site.register(Nodule,NoduleAdmin)

class Nodule1Admin(admin.ModelAdmin):
    list_display = ['id','user','Vote']

admin.site.register(Nodule1,NoduleAdmin)

class Nodule2Admin(admin.ModelAdmin):
    list_display = ['id','user','Vote']

admin.site.register(Nodule2,Nodule2Admin)

class Nodule3Admin(admin.ModelAdmin):
    list_display = ['id','user','Vote']

admin.site.register(Nodule3,Nodule3Admin)