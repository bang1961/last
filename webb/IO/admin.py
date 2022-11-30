from django.contrib import admin
from IO.models import Board



class IOAdmin(admin.ModelAdmin):
    list_display = ['patient_id','id']

admin.site.register(Board,IOAdmin)