from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from UTIL import config
from django.contrib import messages
import shutil, json, os


ROOT_PATH = config.ROOT_PATH

# Create your views here.
def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                                            username=request.POST['username'],
                                            password=request.POST['password1'],
                                            email=request.POST['email'],)
            messages.info(request, " 회원가입이 완료되었습니다!")
            auth.login(request, user)
            return redirect('../login')
        return render(request, 'signup.html')
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)

            ## 분당 서울대 병원 실증테스트 용 ##
            if config.AGREE: return redirect('agree')
            else: return redirect('board')
        else:
            messages.warning(request, '* 아이디와 비밀번호를 확인해주세요.') 
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')
    
def home(request):
    return render(request, 'home.html')

@csrf_exempt
def save_json(request):
    ## javascript에서 ajax로 데이터를 받아오는 부분 ##
    if request.method == 'POST':

        ## POST 형식으로 들어온 데이터 중에서 body에 해당하는 부분이 각 브라우저에서의 토큰 값임. ##
        recv_data = json.loads(request.body)

        ## token 값 들을 저장하고 있는 json 파일경로 ##
        json_path = f'{ROOT_PATH}media/tokens'
        original_token_path = f'{json_path}/tokens.json'
        backup_token_path = f'{json_path}/tokens_backup.json'
        
        os.makedirs(json_path, exist_ok = True)
        ## json 파일이 깨져있는 경우에 빈 딕셔너리 사용  ##
        #!  except 부분에 프린트를 찍어주면 어떤 부분에서 에러가 났는지 파악하기 쉽습미다.  !#
        #!  덤으로 어떤 에러 내용이었는지 Exception을 e로 지정하여 프린트하면 어떤 에러인지 알 수 있습니다. !#
        try:

            ## /home/super/바탕화면/share/lt4/media/tokens 폴더에 ##
            ## tokens.json, tokens_backup.json 파일이 없을 경우에 빈 딕셔너리 사용 ##
            try:
                json_data = json.loads(open(original_token_path, 'r').read()) if os.path.isfile(original_token_path) \
                                else json.loads(open(backup_token_path, 'r').read())

            except Exception as e:
                ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
                config.log_writer(f'토큰이 저장되어 있는 json 파일이 존재하지 않습니다. - {e}', level='err')
                print(f'토큰이 저장되어 있는 json 파일이 존재하지 않습니다. \n{e}')
                json_data = {}
        except Exception as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'토큰이 저장되어 있는 json 파일이 손상 되었습니다. - {e}', level='err')
            print(f'토큰이 저장되어 있는 json 파일이 손상 되었습니다. \n{e}')
            json_data = {}

        ## json 파일에 토큰 값 추가해주는 부분 (key : user0, user1, ..., value : 로그인 할 때 받은 고유의 token 값 ) ##
        #! 이후 user0, user1, ... 이 아닌 각자의 id로 key를 대체할 예정입니다.                          !#
        #! 각자 id로 token 값을 저장할 경우 유저가 한 id로 여러 pc에 로그인 할 경우 모든 pc에 !#
        #! 알림이 가지 않아 토큰이 중복 저장 되지 않도록 저장하도록 수정 하였습니다.            !#

        ## token.json 파일에 api로 부터 전달 받은 토큰 값이 없는 경우에만 json 파일에 token 저장 ##
        #! 중복된 token 값이 저장되게 되면 알림이 여러번 가는 문제가 발생하여 수정하였습니다.    !#
        if recv_data['token'] not in set(json_data.values()):
            json_data[f'user{len(json_data)}'] = recv_data['token']

            ## json 파일을 저장 시켜주는 부분  ##
            json.dump(json_data, open(original_token_path, 'w'), indent = 2)
            ## 백업용 json 파일을 생성을 위해 원본 json 파일을 복사해주는 부분 ##
            shutil.copy(original_token_path, backup_token_path)

    return JsonResponse({'result' : 'result result'})