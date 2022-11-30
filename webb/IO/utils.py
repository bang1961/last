import os
from django.utils import timezone
from django.conf import settings
import datetime


ymd_path = timezone.now().strftime('%Y/%m/%d')

def image_upload_path(board, filename):
    msm = datetime.datetime.now()
    extension = os.path.splitext(filename)[-1].lower()
    patient_forder = f'{board.patient_id}_{msm.hour}{msm.minute}{msm.second}'
    print(board.patient_id)
    print('=================',patient_forder)
    x =  '/'.join([ymd_path, patient_forder, f'{board.patient_id}_axial' + extension,])
    return x

def image_upload_path2(board, filename):
    msm = datetime.datetime.now()
    extension = os.path.splitext(filename)[-1].lower()
    patient_forder2 = f'{board.patient_id}_{msm.hour}{msm.minute}{msm.second}'
    x =  '/'.join([ymd_path, patient_forder2, f'{board.patient_id}_sagittal'+ extension,])
    return x

    


# classifi_model,classifi_model2 = class_model_load()