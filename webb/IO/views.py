from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import *
from .models import *
from .models import Board
from django.utils import timezone
from .forms import BoardForm
from .utils import *
from django.contrib import messages
from history.models import PatientDB
from history.views import *
from UTIL import config
import datetime
import base64
from django.views.decorators.csrf import csrf_exempt
import time


today = datetime.date.today()
month= str(today.month).zfill(2)
day= str(today.day).zfill(2)
visit_date =f'{today.year}/{month}/{day}'


ROOT_PATH = config.ROOT_PATH

def board(request):
    
    if request.user.is_authenticated:
        user_id = request.user
        patient_list = Board.objects.filter(user_id=user_id)
        try:
            user_idx = patient_list[0].user_id
            user_name = User.objects.filter(id=user_idx)
            user_name = user_name[0].username
        except:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'DB에서 사용자 id를 가져올 수 없어 현재 로그인 되어있는 id를 사용합니다.', level='warn')
            user_name = user_id
        if request.method == 'POST':
            patient_id = request.POST['patient_id']
            #comment = request.POST['comment']
            user = request.user
            
            try:
                img = request.FILES["imgfile"]
            except:
                img = "none"

            try:
                img2 = request.FILES["imgfile2"]
            except:
                img2 = "none"

            board = Board(
                #comment=comment,
                patient_id=patient_id,
                user=user,
                imgfile=img,
                imgfile2 = img2
            )
            board.save()
            time.sleep(2)

            return redirect('board')

        else:
            boardForm = BoardForm
            board = Board.objects.all()
            date = f"media/{timezone.localtime().now().strftime('%Y/%m/%d')}"
            json_path = PatientDB.json_path
            history = PatientDB.objects.all()

            context = {
                'user_id' : user_name,
                'history' : history, 
                'json' : json_path,
                'boardForm': boardForm,
                'board': board,
                'imgfile' : date,
            }
            ##########detect.py

            return render(request,'blank.html', context)
    else:
        return redirect('login')

def boardEdit(request, pk):
    #board = Board.objects.get(id=pk)

    try :
        board = Board.objects.get(id=pk)
        Test = f'{board.imgfile}'
        Test = Test.split(os.path.sep)[-2]
        print("====adadad===",Test)
        history = PatientDB(
            patient_id = board.patient_id,
            visit_date = visit_date,
            user = board.user,
            #comment = board.comment,
            json_path = f'media/{visit_date}/{Test}/jsons/{board.patient_id}_axial_nodule.json',
            json_path_sagittal = f'media/{visit_date}/{Test}/jsons/{board.patient_id}_sagittal_nodule.json',
            pk =pk
        )
        ############## IMGFIELD 에있는 _SECOND 가져와서 JSON_PATH에 적용 
        ##  Django의 post_save 함수를 사용하여 PatientDB에 데이터가 저장되면 알림이 가도록 구현함. ##
        #!   post_save 함수는 IO/signal.py에서 사용되었습니다.   !#
        history.save()
        board.delete()
        
        ## history_blank 페이지에서 Json 데이터가 표시되도록 rendering ##
        return redirect(' src:detail', pk)

    except Board.DoesNotExist :
        return redirect('board')

def boardDelete(request, pk):
    try : 
        board = Board.objects.get(id=pk)
        Test = f'{board.imgfile}'
        Test = Test.split(os.path.sep)[-2]
        TODAY = datetime.date.today()
        YEAR = TODAY.year
        MONTH= str(TODAY.month).zfill(2)
        DAY= str(TODAY.day).zfill(2)
        print('TTTT\n\n\n\n'f'{ROOT_PATH}media/{YEAR}/{MONTH}/{DAY}/{Test}')
        file_path = f'{ROOT_PATH}media/{YEAR}/{MONTH}/{DAY}/{Test}'
        if os.path.exists(file_path):
            shutil.rmtree(file_path)
            board.delete()
        return redirect('board')
    except :
        return redirect('board')

# home
def agree(request):
    if request.user.is_authenticated:
        user_id = request.user

        context = {'user_id' : user_id, 'year' : today.year, 'month' : month, 'day' : day}
        if request.method == 'POST':

            user_name = request.POST.get('username') != ''
            user_name2 = request.POST.get('username2') != ''
            agree_condition1 = request.POST.get('agree1') != None
            agree_condition2 = request.POST.get('agree2') != None

            condition = [user_name, agree_condition1, agree_condition2] if user_name else [user_name2, agree_condition1, agree_condition2]
            print("ADS")
            if all(condition):    
                agree1 = request.POST.get('agree1')
                agree2 = request.POST.get('agree2')


                agree_condition = [agree1 == '1', agree2 == '1']

                if all(agree_condition): return redirect('board')
                else: return render(request, 'agree.html', context)

            else:
                messages.warning(request, '필요한 정보를 모두 입력해주세요.')
                return render(request, 'agree.html', context)

        else:
            return render(request, 'agree.html', context)
    else:
        return redirect('login')

@csrf_exempt
def agreeimgsave(request):

        data = request.POST.__getitem__('imagedata')
        data = data[22:]
        
        path = str(f'{ROOT_PATH}media/agreetext/')
        filename = 'image.png'

        image = open(path+filename,"wb")
        image.write(base64.b64decode(data))
        image.close()
