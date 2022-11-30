# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from history.models import PatientDB
# from pyfcm import FCMNotification
# from UTIL import config
# import json, os

# ROOT_PATH = '/home/lt4/lt4/' if config.SNUBH else '/home/super/바탕화면/share/lt4/'
# json_path = f'{ROOT_PATH}media/tokens'

# original_token_path = f'{json_path}/tokens.json'
# backup_token_path = f'{json_path}/tokens_backup.json'

# config = json.loads(open(f'{json_path}/config.json', 'r').read())
# push_service = FCMNotification(config['api-key'])

# @receiver(post_save, sender = PatientDB)
# def patient_post_save(sender, **kwargs):

#     ## @receiver에 인자값으로 들어간 sender의  ##
#     db_data = kwargs['instance']

#     try:
#         tokens = json.loads(open(original_token_path, 'r').read()) if os.path.isfile(original_token_path) \
#                         else json.loads(open(backup_token_path, 'r').read())

#     except Exception as e:
#         ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
#         config.log_writer('토큰이 저장되어 있는 json 파일이 존재하지 않습니다.', level = 'err')
#         print(f'토큰이 저장되어 있는 json 파일이 존재하지 않습니다. \n{e}')
#         tokens = {}

#     primary_key = db_data.pk
#     user = db_data.user
#     patient_id = db_data.patient_id

    
#     data_messages = {
#         'title' : '태깅 알림',
#         'body' : f'{user}님, {patient_id} 환자분의 \n새로운 태깅 데이터가 도착하였습니다.',
#         'url'  : f'https://ltlux.duckdns.org:8000/history/{primary_key}',
#     }

#     tokens = [token for token in tokens.values()]
#     result = push_service.multiple_devices_data_message(registration_ids = tokens, data_message = data_messages)
#     print(result, '\n', data_messages['url'])