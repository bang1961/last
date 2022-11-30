from dataclasses import Field
from django.shortcuts import render, get_object_or_404 , redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from history.templatetags import utils
from UTIL import config
import traceback
from imutils.paths import list_files
from .models import *
from .forms import *
import json, os, shutil
from pathlib import Path



ROOT_PATH = config.ROOT_PATH
search_username = lambda user_idx: User.objects.filter(id = user_idx)[0].username

# Pre-Interpretion Page 	- 진료의가 판독문을 작성하기 전인 애들이 모인 곳

############################
# Pre - Tagging Page #
############################

@csrf_exempt
def tagging_tables_pre_tagging(request):
    ## PatientDB에서 현재 로그인 되어 있는 id로 게시된 게시물 목록을 가져옴. ##
    ## user_id : 현재 로그인 되어 있는 id 정보 ##
    ## patient_list : 현재 로그인 되어 있는 id로 작성되어 있는 게시물 목록 ##

    ## 로그인 되어있으면 history 페이지로 이동 ##
    if request.user.is_authenticated:
        user_name = request.user

        order_by = request.POST.get('order_by')
        
        order_by = order_by if order_by != None else 'newrest'

        try:
            keyword = request.POST.get('keyword')
            keyword = keyword if keyword != None else 'patient_id'

            search = request.POST.get('search')
            search = search if search != None else ''
            
            ## select에서 정렬 기준으로 최신 순, 오래된 순 선택했을 때 동작하는 부분
            ## 기존에 동작하던 코드와 거의 비슷한 원리로 동작한다.
            if  'est' in order_by.lower():
                if 'newrest' in order_by.lower():
                    order = '-visit_date' if 'newrest' in order_by.lower() else 'visit_date'
                    
                    ## 기존의 방문일자로 정렬하였으나, 같은 방문환자일 때, 정렬할 수 없어 idx값을 가져옴
                    patient_list = PatientDB.objects.values_list('id').order_by(order)

                    ## user_idx : 게시글 목록에서 첫 번째 게시글의 User id 인덱스 값을 가지고 옴. ##
                    ## user_name : 가입된 계정들 DB에서의 user_idx값을 조회하여 user_name을 가지고 옴. ##
                    user_idxs = [patient.user_id for patient in patient_list]
                    
                    user_names = [User.objects.filter(id=user_idx)[0].username for user_idx in user_idxs]
                elif 'oldest' in order_by.lower():         
                    order = '-visit_date' if 'newrest' in order_by.lower() else 'visit_date'
                    patient_list = PatientDB.objects.order_by(order)
                    
                    ## user_idx : 게시글 목록에서 첫 번째 게시글의 User id 인덱스 값을 가지고 옴. ##
                    ## user_name : 가입된 계정들 DB에서의 user_idx값을 조회하여 user_name을 가지고 옴. ##
                    user_idxs = [patient.user_id for patient in patient_list]
                    user_names = [User.objects.filter(id=user_idx)[0].username for user_idx in user_idxs]
                
            ## select에서 정렬 기준으로 사용자 id 오름차순, 내림차 순 선택했을 때 동작하는 부분
            elif 'ing' in order_by.lower():
                ## 사용자 인덱스 번호로 사용자 아이디 찾는 함수
                ## PatientDB에서 user_id가 문자열이 아닌 숫자로 들어와 제작함

                order = '-user_id' if 'ascending' in order_by.lower() else 'user_id'
                patient_list = PatientDB.objects.order_by(order)
                patient_list = [(search_username(user.user_id), user) for user in patient_list]

                ## 오름차 순을 선택한 경우 문자를 기준으로 내림차순으로 정렬한다.
                ## i.e.) a -> z, A -> Z 순으로 

                ## key = lambda x: x[0] => 정렬할 리스트의 첫 번째 요소를 기준으로 정렬
                ## e.g) patient_list = [(1, 2, 3), (9, 7, 4), (8, 6, 3), (2, 5, 7), (10, 9, 7)]
                ##       patient_list.sort(key = lambda x: x[0])
                ##       →  [(1, 2, 3), (2, 5, 7), (8, 6, 3), (9, 7, 4), (10, 9, 7)]
                if 'ascending' in order_by.lower(): patient_list.sort(key = lambda x: x[0])
                

                ## 내림차순을 선택한 경우 문자를 기준으로 내림차순으로 정렬한다.
                ## i.e.) z → a, Z → A 순으로 

                ## 오름차순과 동작 원리는 동일하지만, 정렬 기준만 역순으로 정렬
                elif 'descending' in order_by.lower(): patient_list.sort(reverse = True, key = lambda x: x[0])
                
                ## user_idx : 게시글 목록에서 첫 번째 게시글의 User id 인덱스 값을 가지고 옴. ##
                ## user_name : 가입된 계정들 DB에서의 user_idx값을 조회하여 user_name을 가지고 옴. ##
                user_names = [user[0] for user in patient_list]
                patient_list = [user[1] for user in patient_list]

            try:
                filtered_data = data_filter(patient_list, keyword, search)
                patient_list = [data[1] for data in filtered_data]
                user_names = [data[0] for data in filtered_data]
                
            except Exception as e:
                ERR = f'[ERR] {e} \n상세 : {traceback.format_exc()}'
                config.log_writer(ERR, level='err')

        ## 정렬 기준의 기본 값으로는 최신 순으로 정렬하게 지정하였다.
        except Exception as e:
            patient_list = PatientDB.objects.order_by('-visit_date')

            ## user_idx : 게시글 목록에서 첫 번째 게시글의 User id 인덱스 값을 가지고 옴. ##
            ## user_name : 가입된 계정들 DB에서의 user_idx값을 조회하여 user_name을 가지고 옴. ##
            user_idxs = [patient.user_id for patient in patient_list]
            
            user_names = [User.objects.filter(id=user_idx)[0].username for user_idx in user_idxs]

        entry = request.POST.get('entry')
        entry = int(entry) if entry != None else 20

        ## 입력 파라미터 조회하는 부분 ##
        page = request.GET.get('page', 1)

        # data_number_per_page = int(data_number_per_page)
        ## 한 페이지 당 20개씩 데이터를 나누어 주는 부분 ##
        paginator = Paginator(patient_list, entry)
        last_page = len(paginator.page_range)
        page_obj = paginator.get_page(page)

        tagging_count = PatientDB.total_likes
        ##  다음 페이지로 넘어갔을때  이전 페이지에 있는 환자 id가 표시되어 수정##
        user_names = user_names[20*(page_obj.number - 1) : 20*page_obj.number]

        context = {'datas' : zip(page_obj, user_names), 'number' : page_obj.number, 'search' : search, 'entry' : str(entry), 
                    'keyword' : keyword, 'order_by' : order_by, 'page_obj' : page_obj, 'last_page' : last_page, 'user_name' : str(user_name),
                    'tagging_count' : tagging_count}

        return render(request, 'tagging_tables_pre_tagging.html', context)


    ## 로그인 되어 있지 않으면 로그인 페이지로 이동 후 검사 페이지로 이동 ##
    else:
        return redirect('login')


############################
# Pre -Interpretation Page #
############################
@csrf_exempt
def tagging_tables_pre_interpretion(request):
    ## PatientDB에서 현재 로그인 되어 있는 id로 게시된 게시물 목록을 가져옴. ##
    ## user_id : 현재 로그인 되어 있는 id 정보 ##
    ## patient_list : 현재 로그인 되어 있는 id로 작성되어 있는 게시물 목록 ##

    ## 로그인 되어있으면 history 페이지로 이동 ##

    if request.user.is_authenticated:
        user_id = request.user
        try:
            user_idx = patient_list[0].user_id
            user_name = search_username(user_idx)
        
        except:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'DB에서 사용자 id를 가져올 수 없어 현재 로그인 되어있는 id를 사용합니다.', level='warn')
            user_name = user_id
        
        ##      ments  : 판독문 작성이 되있는 데이터만 불러오는 변수
        ## patient_list : ments에 담긴 데이터 중에서 현재 로그인 되어있는 id의 PatientDB 데이터를 가져옴.
        ##             i.e) 현재 로그인 되어 있는 계정의 판독문 작성이 되어있는 데이터만 가져옴.
        ments = Ment.objects.filter(interpretation=None,body=None)
        patient_list =  [ment.post.pk for ment in ments if search_username(ment.user.id) == str(user_name)]
        queryset = PatientDB.objects.filter(pk__in = patient_list)

        order_by = request.POST.get('order_by')

        order_by = order_by if order_by != None else 'newrest'
        
        try:
            keyword = request.POST.get('keyword')
            keyword = keyword if keyword != None else 'patient_id'

            search = request.POST.get('search')
            search = search if search != None else ''

            ## select에서 정렬 기준으로 최신 순, 오래된 순 선택했을 때 동작하는 부분
            if  'est' in order_by.lower():
                # queryset = queryset.objects.order_by(order)
                queryset = [(query.id, query) for query in queryset]
                ## 오래된 순을 선택한 경우 날짜를 기준으로 오름차순으로 정렬한다.
                ## i.e.) 01 -> 12, 01 -> 31 순으로 
                if 'oldest' in order_by.lower(): queryset.sort(key = lambda x: x[0])

                ## 최신 순을 선택한 경우 날짜를 기준으로 내림차순으로 정렬한다.
                ## i.e.) 12 - >01, 31 -> 01 순으로 
                elif 'newrest' in order_by.lower(): queryset.sort(reverse = True, key = lambda x: x[0])

            ## select에서 정렬 기준으로 사용자 id 오름차순, 내림차 순 선택했을 때 동작하는 부분
            elif 'ing' in order_by.lower():
                ## 환자 id와 query 데이터를 담고 있는 리스트
                queryset = [(query.patient_id, query) for query in queryset]

                ## 오름차 순을 선택한 경우 문자를 기준으로 내림차순으로 정렬한다.
                ## i.e.) a -> z, A -> Z 순으로 

                ## key = lambda x: x[0] => 정렬할 리스트의 첫 번째 요소를 기준으로 정렬
                ## e.g) queryset = [(1, 2, 3), (9, 7, 4), (8, 6, 3), (2, 5, 7), (10, 9, 7)]
                ##       queryset.sort(key = lambda x: x[0])
                ##       →  [(1, 2, 3), (2, 5, 7), (8, 6, 3), (9, 7, 4), (10, 9, 7)]
                if 'ascending' in order_by.lower(): queryset.sort(key = lambda x: x[0])


                ## 내림차 순을 선택한 경우 문자를 기준으로 내림차순으로 정렬한다.
                ## i.e.) z → a, Z → A 순으로 

                ## 오름차 순과 동작 원리는 동일하지만, 정렬 기준만 역순으로 정렬
                elif 'descending' in order_by.lower(): queryset.sort(reverse = True, key = lambda x: x[0])


            ## 정렬을 마친 데이터는 환자 id를 제외하고 query 데이터만 담고 있는다.
            queryset = [user[1] for user in queryset]

            try:
                ## 검색하고자 하는 데이터를 담는 부분 본 코드의 data_filter 함수 참조
                queryset = data_filter(queryset, keyword, search)
                queryset = [data[1] for data in queryset]
                
            except Exception as e:
                ERR = f'[ERR] {e} \n상세 : {traceback.format_exc()}'
                config.log_writer(ERR, level='err')

        ## 정렬 기준의 기본 값으로는 최신 순으로 정렬하게 지정하였다.
        except Exception as e:
            ERR = f'[ERR] {e} \n상세 : {traceback.format_exc()}'
            config.log_writer(ERR, level='err')

            queryset = (query for query in queryset)

        entry = request.POST.get('entry')
        entry = int(entry) if entry != None else 20

        ## user_idx : 게시글 목록에서 첫 번째 게시글의 User id 인덱스 값을 가지고 옴. ##
        ## user_name : 가입된 계정들 DB에서의 user_idx값을 조회하여 user_name을 가지고 옴. ##8


        ## 입력 파라미터 조회하는 부분 ##
        page = request.GET.get('page', 1)
        
        # data_number_per_page = int(data_number_per_page)
        ## 한 페이지 당 20개씩 데이터를 나누어 주는 부분 ##
        paginator = Paginator(queryset, entry)
        last_page = len(paginator.page_range)
        page_obj = paginator.get_page(page)

        context = {'datas' : page_obj, 'last_page' : last_page, 'user_name' : user_name, 'data' : queryset,
                    'entry' : entry, 'order_by' : order_by, 'keyword' : keyword, 'search' : search}


        return render(request, 'tagging_tables_pre_interpretion.html', context)

    ## 로그인 되어 있지 않으면 로그인 페이지로 이동 후 검사 페이지로 이동 ##
    else:
        return redirect('login')

#########################
# Tagging history Page  #
#########################

@csrf_exempt
def tagging_history_partial_list(request):

    ## PatientDB에서 현재 로그인 되어 있는 id로 게시된 게시물 목록을 가져옴. ##
    ## user_id : 현재 로그인 되어 있는 id 정보 ##
    ## patient_list : 현재 로그인 되어 있는 id로 작성되어 있는 게시물 목록 ##

    ## 로그인 되어있으면 history 페이지로 이동 ##
    if request.user.is_authenticated:
        user_id = request.user
        try:
            user_idx = patient_list[0].user_id
            user_name = search_username(user_idx)
        
        except:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'DB에서 사용자 id를 가져올 수 없어 현재 로그인 되어있는 id를 사용합니다.', level='warn')
            user_name = user_id
        
        ##      ments  : 판독문 작성이 되있는 데이터만 불러오는 변수
        ## patient_list : ments에 담긴 데이터 중에서 현재 로그인 되어있는 id의 PatientDB 데이터를 가져옴.
        ##             i.e) 현재 로그인 되어 있는 계정의 판독문 작성이 되어있는 데이터만 가져옴.
        ments = Ment.objects.filter(interpretation=None)
        patient_list =  [ment.post.pk for ment in ments if search_username(ment.user.id) == str(user_name)]
        queryset = PatientDB.objects.filter(pk__in = patient_list)

        order_by = request.POST.get('order_by')

        order_by = order_by if order_by != None else 'newrest'
        
        try:
            keyword = request.POST.get('keyword')
            keyword = keyword if keyword != None else 'patient_id'

            search = request.POST.get('search')
            search = search if search != None else ''

            ## select에서 정렬 기준으로 최신 순, 오래된 순 선택했을 때 동작하는 부분
            if  'est' in order_by.lower():
                # queryset = queryset.objects.order_by(order)
                queryset = [(query.id, query) for query in queryset]
                ## 오래된 순을 선택한 경우 날짜를 기준으로 오름차순으로 정렬한다.
                ## i.e.) 01 -> 12, 01 -> 31 순으로 
                if 'oldest' in order_by.lower(): queryset.sort(key = lambda x: x[0])

                ## 최신 순을 선택한 경우 날짜를 기준으로 내림차순으로 정렬한다.
                ## i.e.) 12 - >01, 31 -> 01 순으로 
                elif 'newrest' in order_by.lower(): queryset.sort(reverse = True, key = lambda x: x[0])

            ## select에서 정렬 기준으로 사용자 id 오름차순, 내림차 순 선택했을 때 동작하는 부분
            elif 'ing' in order_by.lower():
                ## 환자 id와 query 데이터를 담고 있는 리스트
                queryset = [(query.patient_id, query) for query in queryset]

                ## 오름차 순을 선택한 경우 문자를 기준으로 내림차순으로 정렬한다.
                ## i.e.) a -> z, A -> Z 순으로 

                ## key = lambda x: x[0] => 정렬할 리스트의 첫 번째 요소를 기준으로 정렬
                ## e.g) queryset = [(1, 2, 3), (9, 7, 4), (8, 6, 3), (2, 5, 7), (10, 9, 7)]
                ##       queryset.sort(key = lambda x: x[0])
                ##       →  [(1, 2, 3), (2, 5, 7), (8, 6, 3), (9, 7, 4), (10, 9, 7)]
                if 'ascending' in order_by.lower(): queryset.sort(key = lambda x: x[0])


                ## 내림차 순을 선택한 경우 문자를 기준으로 내림차순으로 정렬한다.
                ## i.e.) z → a, Z → A 순으로 

                ## 오름차 순과 동작 원리는 동일하지만, 정렬 기준만 역순으로 정렬
                elif 'descending' in order_by.lower(): queryset.sort(reverse = True, key = lambda x: x[0])


            ## 정렬을 마친 데이터는 환자 id를 제외하고 query 데이터만 담고 있는다.
            queryset = [user[1] for user in queryset]

            try:
                ## 검색하고자 하는 데이터를 담는 부분 본 코드의 data_filter 함수 참조
                queryset = data_filter(queryset, keyword, search)
                queryset = [data[1] for data in queryset]
                
            except Exception as e:
                ERR = f'[ERR] {e} \n상세 : {traceback.format_exc()}'
                config.log_writer(ERR, level='err')

        ## 정렬 기준의 기본 값으로는 최신 순으로 정렬하게 지정하였다.
        except Exception as e:
            ERR = f'[ERR] {e} \n상세 : {traceback.format_exc()}'
            config.log_writer(ERR, level='err')

            queryset = (query for query in queryset)

        entry = request.POST.get('entry')
        entry = int(entry) if entry != None else 20

        ## user_idx : 게시글 목록에서 첫 번째 게시글의 User id 인덱스 값을 가지고 옴. ##
        ## user_name : 가입된 계정들 DB에서의 user_idx값을 조회하여 user_name을 가지고 옴. ##8


        ## 입력 파라미터 조회하는 부분 ##
        page = request.GET.get('page', 1)
        
        # data_number_per_page = int(data_number_per_page)
        ## 한 페이지 당 20개씩 데이터를 나누어 주는 부분 ##
        paginator = Paginator(queryset, entry)
        last_page = len(paginator.page_range)
        page_obj = paginator.get_page(page)

        context = {'datas' : page_obj, 'last_page' : last_page, 'user_name' : user_name, 'data' : queryset,
                    'entry' : entry, 'order_by' : order_by, 'keyword' : keyword, 'search' : search}

        return render(request, 'tagging_history.html', context)
        # return render(request, 'patient_list.html', context)

    ## 로그인 되어 있지 않으면 로그인 페이지로 이동 후 검사 페이지로 이동 ##
    else:
        return redirect('login')
        
################
# Tagging Page #
################
@csrf_exempt
def tagging_history_total_list(request):
    ## PatientDB에서 현재 로그인 되어 있는 id로 게시된 게시물 목록을 가져옴. ##
    ## user_id : 현재 로그인 되어 있는 id 정보 ##
    ## patient_list : 현재 로그인 되어 있는 id로 작성되어 있는 게시물 목록 ##

    ## 로그인 되어있으면 history 페이지로 이동 ##
    if request.user.is_authenticated:
        user_name = request.user

        order_by = request.POST.get('order_by')
        
        order_by = order_by if order_by != None else 'newrest'
        ments = Ment.objects.filter(body=None)&Ment.objects.filter(interpretation=None)
        patient_list =  [ment.post.pk for ment in ments if search_username(ment.user.id) == str(user_name)]

        try:
            keyword = request.POST.get('keyword')
            keyword = keyword if keyword != None else 'patient_id'

            search = request.POST.get('search')
            search = search if search != None else ''
            print(1)
            ## select에서 정렬 기준으로 최신 순, 오래된 순 선택했을 때 동작하는 부분
            ## 기존에 동작하던 코드와 거의 비슷한 원리로 동작한다.
            if  'est' in order_by.lower():
                if 'newrest' in order_by.lower():
                    order = '-visit_date' if 'newrest' in order_by.lower() else 'visit_date'
                    
                    ## 기존의 방문일자로 정렬하였으나, 같은 방문환자일 때, 정렬할 수 없어 idx값을 가져옴
                    patient_list = PatientDB.objects.filter(pk__in = patient_list).order_by(order)

                    ## user_idx : 게시글 목록에서 첫 번째 게시글의 User id 인덱스 값을 가지고 옴. ##
                    ## user_name : 가입된 계정들 DB에서의 user_idx값을 조회하여 user_name을 가지고 옴. ##
                    user_idxs = [patient.user_id for patient in patient_list]
                    
                    user_names = [User.objects.filter(id=user_idx)[0].username for user_idx in user_idxs]
                    print(2,patient_list)
                elif 'oldest' in order_by.lower():         
                    order = '-visit_date' if 'newrest' in order_by.lower() else 'visit_date'
                    patient_list = PatientDB.objects.filter(pk__in = patient_list).order_by(order)
                    print(3)
                    ## user_idx : 게시글 목록에서 첫 번째 게시글의 User id 인덱스 값을 가지고 옴. ##
                    ## user_name : 가입된 계정들 DB에서의 user_idx값을 조회하여 user_name을 가지고 옴. ##
                    user_idxs = [patient.user_id for patient in patient_list]
                    user_names = [User.objects.filter(id=user_idx)[0].username for user_idx in user_idxs]
                
            ## select에서 정렬 기준으로 사용자 id 오름차순, 내림차 순 선택했을 때 동작하는 부분
            elif 'ing' in order_by.lower():
                ## 사용자 인덱스 번호로 사용자 아이디 찾는 함수
                ## PatientDB에서 user_id가 문자열이 아닌 숫자로 들어와 제작함
                print(4)
                order = '-user_id' if 'ascending' in order_by.lower() else 'user_id'
                patient_list = PatientDB.objects.filter(pk__in = patient_list).order_by(order)
                patient_list = [(search_username(user.user_id), user) for user in patient_list]

                ## 오름차 순을 선택한 경우 문자를 기준으로 내림차순으로 정렬한다.
                ## i.e.) a -> z, A -> Z 순으로 

                ## key = lambda x: x[0] => 정렬할 리스트의 첫 번째 요소를 기준으로 정렬
                ## e.g) patient_list = [(1, 2, 3), (9, 7, 4), (8, 6, 3), (2, 5, 7), (10, 9, 7)]
                ##       patient_list.sort(key = lambda x: x[0])
                ##       →  [(1, 2, 3), (2, 5, 7), (8, 6, 3), (9, 7, 4), (10, 9, 7)]
                if 'ascending' in order_by.lower(): patient_list.sort(key = lambda x: x[0])
                

                ## 내림차순을 선택한 경우 문자를 기준으로 내림차순으로 정렬한다.
                ## i.e.) z → a, Z → A 순으로 

                ## 오름차순과 동작 원리는 동일하지만, 정렬 기준만 역순으로 정렬
                elif 'descending' in order_by.lower(): patient_list.sort(reverse = True, key = lambda x: x[0])
                
                ## user_idx : 게시글 목록에서 첫 번째 게시글의 User id 인덱스 값을 가지고 옴. ##
                ## user_name : 가입된 계정들 DB에서의 user_idx값을 조회하여 user_name을 가지고 옴. ##
                user_names = [user[0] for user in patient_list]
                patient_list = [user[1] for user in patient_list]
                print(5)
            try:
                filtered_data = data_filter(patient_list, keyword, search)
                patient_list = [data[1] for data in filtered_data]
                user_names = [data[0] for data in filtered_data]
                print(6)
            except Exception as e:
                ERR = f'[ERR] {e} \n상세 : {traceback.format_exc()}'
                config.log_writer(ERR, level='err')

        ## 정렬 기준의 기본 값으로는 최신 순으로 정렬하게 지정하였다.
        except Exception as e:
            patient_list = PatientDB.objects.filter(pk__in = patient_list).order_by('-visit_date')

            ## user_idx : 게시글 목록에서 첫 번째 게시글의 User id 인덱스 값을 가지고 옴. ##
            ## user_name : 가입된 계정들 DB에서의 user_idx값을 조회하여 user_name을 가지고 옴. ##
            user_idxs = [patient.user_id for patient in patient_list]
            
            user_names = [User.objects.filter(id=user_idx)[0].username for user_idx in user_idxs]
            print(e)
        entry = request.POST.get('entry')
        entry = int(entry) if entry != None else 20

        ## 입력 파라미터 조회하는 부분 ##
        page = request.GET.get('page', 1)
        print("8",patient_list)
        # data_number_per_page = int(data_number_per_page)
        ## 한 페이지 당 20개씩 데이터를 나누어 주는 부분 ##
        paginator = Paginator(patient_list, entry)
        print(patient_list)
        last_page = len(paginator.page_range)
        page_obj = paginator.get_page(page)

        tagging_count = PatientDB.total_likes
        ##  다음 페이지로 넘어갔을때  이전 페이지에 있는 환자 id가 표시되어 수정##
        user_names = user_names[20*(page_obj.number - 1) : 20*page_obj.number]
        
        context = {'datas' : zip(page_obj, user_names), 'number' : page_obj.number, 'search' : search, 'entry' : str(entry), 
                    'keyword' : keyword, 'order_by' : order_by, 'page_obj' : page_obj, 'last_page' : last_page, 'user_name' : str(user_name),
                    'tagging_count' : tagging_count}
        print("\ntotal_user:",str(entry))
        return render(request, 'tagging_tables_total.html', context)

    ## 로그인 되어 있지 않으면 로그인 페이지로 이동 후 검사 페이지로 이동 ##
    else:
        return redirect('login')


@csrf_exempt
def tagging_history_detail(request, id):

    ## PatientDB에서 id를 primary key로 하여 검색 query에 있으면 표시, 아니면 404표시  ##
    patient = get_object_or_404(PatientDB, pk=id)
    
    join1_json_path = patient.json_path.split(os.path.sep)[:4]
    join2_json_path = patient.json_path.split(os.path.sep)[4:]
    new_json_path = '/'.join([('/'.join(join1_json_path)),('/'.join(join2_json_path))])


    # Axial에 결절이 없지만 Sagittal에 결절이 있을때, Axial의 Json 생성
    image_HMS_path = patient.json_path.split(os.path.sep)[4]
    visit_date = '/'.join(patient.json_path.split(os.path.sep)[1:4])
    image_path = '/'.join([ROOT_PATH,('/'.join(join1_json_path)),image_HMS_path,f'{patient.patient_id}_axial.jpg'])
    detected_image_path = '/'.join([ROOT_PATH,('/'.join(join1_json_path)),image_HMS_path,f'detected/{patient.patient_id}_axial_detected.jpg'])
    print("-----------------------------",image_path)
    ## detail 페이지에서  종단인지 횡단인지 구분하여 검사결과를 보여줌.
    direction = request.POST.get('direction_select')
    direction = direction if direction != None else 'axial'

    json_path = f'{ROOT_PATH}{patient.json_path}' if 'axial' in direction else  f'{ROOT_PATH}{patient.json_path_sagittal}'
    
    user_id = request.user
    ments = patient.ment_set.all()

    ments_form = MentForm(request.POST)
    I_F = InterpretationForm(request.POST)
    
    ##  DB에서 검색된 데이터에서 json 경로를  get_patient_info 함수에 입력 ##
    if os.path.exists(json_path) == False:
        newjson = {"patient id" : patient.patient_id, "visit date" : visit_date,
        "original image path" : f"{image_path}",
        "inspection image path" : f"{image_path}",
        "model complete" : "complete",
        "result" : {}}
        print(image_path)
        newjson['result']['ncount'] = 0
        # 결절이 detect 되지않았을 때 json
        newjson['result'][f'nodule1'] = {
                            "nodule image path" : image_path,
                            "classi_text_path" : None,
                            "Shape" : None,
                            "Margin" : None,
                            "Calcification" : None,
                            "Spongiform" : None,
                            "Internal content" : None,
                            "Echogenicity" : None,
                            "Orientation" : None,
                            "comet tail" : None
                        }
        json.dump(newjson, open(Path(new_json_path),'w'),ensure_ascii=False, indent =4)

    num_nodules, (patient_id, visit_date, classi_text_path), (ori_image_path, ins_image_path), patient_info = utils.get_patient_info(json_path)
    
    ## tagging tagging tagging tagging tagging tagging
    Tags = Nodule.objects.all()
    Tags1 = Nodule1.objects.all()
    Tags2 = Nodule2.objects.all()
    Tags3 = Nodule3.objects.all()

    json_length = '/'.join(json_path.split(os.path.sep)[:-1])
    json_length = sorted(list_files(json_length))

    if request.method == 'POST':
        if request.user.is_authenticated : 
            
            if ments_form.is_valid() and request.POST.get('body') != None:
                ment = ments_form.save(commit=False)
                ment.post = patient
                ment.user = request.user
                ment.save()

            elif I_F.is_valid():
                if Ment.objects.filter(user=patient.user.pk):
                #판독문은 진단한 사람만 할 수 있음 save시 이벤트 추가예정
                    I_Form = I_F.save(commit = False)
                    I_Form.post = patient #ment.post
                    I_Form.user = request.user
                    I_Form.save()

        else:
            return redirect('login')
 
        context = {
        'patient' : patient, 'original_image_path' : ori_image_path, 'json_path ' : json_path ,
        'inspection_image_path' : ins_image_path, 'num_nodules' : num_nodules, 
        'patient_info' : patient_info, 'user_id' : user_id, 'patient_id' : patient_id, 'visit_date' : visit_date,
        'all_member' : User.objects.count()-1, 'players' : Tags, 'players1' :Tags1,'players2' :Tags2,'players3' :Tags3,
        'ments_form': ments_form, 'ments' : ments, 'classi_text_path' : classi_text_path, 'direction' : direction, 
        'IF' : I_F, 'image_length' : len(json_length)}

        ## history_blank 페이지에서 Json 데이터가 표시되도록 rendering ##
        return render(request, 'tagging_history_blank.html', context)
    else:
        # 로그인 하지 않은 상황에서 쓰려하면 로그인페이지로 이동
        ## 딕셔너리 형식으로 데이터들을 history_blank.html에 전달 ##
        context = {
                'patient' : patient, 'original_image_path' : ori_image_path, 'json_path ' : json_path ,
                'inspection_image_path' : ins_image_path, 'num_nodules' : num_nodules,  
                'patient_info' : patient_info, 'user_id' : user_id, 'patient_id' : patient_id, 'visit_date' : visit_date,
                'all_member' : User.objects.count()-1, 'players' : Tags, 'players1' :Tags1,'players2' :Tags2,'players3' :Tags3,
                'ments_form': ments_form, 'ments' : ments, 'classi_text_path' : classi_text_path, 'direction' : direction,
                'IF' : I_F, 'image_length' : len(json_length)}

        ## history_blank 페이지에서 Json 데이터가 표시되도록 rendering ##
        return render(request, 'tagging_history_blank.html', context)


## 데이터 검색 기능을 위한 함수 queryset.objects.filter()로 해도 되었지만, 
## .filter()을 사용하면 kimdove를 검색하면 kimdove001, kimdove002, ... 등 나오지 않아 따로 구현함.
## e.g) 방문 날짜 | 2022/03 데이터 검색 => data_filter(query_set, 'visit', '2022/03')
##       환자 id    | kimdove 데이터 검색 => data_filter(query_set, 'patient', 'kimdove')
def data_filter(query_set, keyword, search):
    filtered_data = []
    data_append = filtered_data.append

    lower = keyword.lower()
    for user in query_set:
        user_name = search_username(user.user_id)
        category = user.patient_id.lower() if 'patient' in lower else (user_name if 'user' in lower else user.visit_date)

        ## DB 데이터만 집어 넣었을때, 환자 id랑 실제 검사한 의사 id랑 매칭되지 않아 의사 id도 같이 집어 넣음.
        if search in category: data_append((search_username(user.user_id), user))

    return tuple(filtered_data)

@csrf_exempt
def HDDelete(request, pk):
    HD = PatientDB.objects.get(id=pk)
    
    if request.user == HD.user :
        field_name = getattr(HD, 'patient_id')
        field_date = getattr(HD, 'visit_date')
        after      = getattr(HD, 'json_path')
        after = str(after).split(os.path.sep)[-3]
        file_path = f'{ROOT_PATH}media/{field_date}/{after}'
        print(file_path)
        if os.path.exists(file_path):
            shutil.rmtree(file_path)
            HD.delete()
        return redirect(' src:tagging_patient_total_history')
    return HttpResponse(status=401)

def ment_delete(request,id,comment_id):
    comment = get_object_or_404(Ment , pk=comment_id)
    pk = id
    if request.user.is_authenticated :         # 로그인 확인 
        if request.user == comment.user:
            comment.delete()
            return redirect(' src:detail2',pk)
    return HttpResponse(status=401)


## --TAG 1 -- ##
def tagging_reset_like(request):
    if request.method == 'POST':
        user = request.user
        name_id = request.POST.get('pk', None)
        
        obj = PatientDB.objects.get(pk=name_id)
        ##pk 값 받아옴
        try:
            if obj.Tags.filter(id=user.id).exists():
                obj.Tags.remove(user)
                
            message = 'Agree '
            #else:
                #message = 'Cancel '
        

        except PatientDB.DoesNotExist:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer('PatientDB에 조회하고자 하시는 쿼리가 없습니다.', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None
        context = {
            'message': message, 'Tag_count' : obj.total_likes
        }
        return HttpResponse(json.dumps(context), content_type='application/json')


## --TAG 1 -- ##
def tagging_reset_dislike(request):
    if request.method == 'POST':
        user = request.user
        name_id = request.POST.get('pk', None)
        obj = PatientDB.objects.get(pk=name_id)

        ##pk 값 받아옴
        try:
            if obj.Tags_default.filter(id=user.id).exists():
                obj.Tags_default.remove(user)
            
            message = 'DisAgree '
            #else:
                #message = 'Cancel '


        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None

    context = {
        'message1': message, 'Tags_default' : obj.total_dislikes
    }
    return HttpResponse(json.dumps(context), content_type='application/json')


## --TAG 1 -- ##
def like(request):
    if request.method == 'POST':

        user = request.user
        name_id = request.POST.get('pk', None)

        obj = PatientDB.objects.get(pk=name_id)
        ##pk 값 받아옴
        try:
            
            if obj.Tags.filter(id=user.id).exists():
                obj.Tags.remove(user)
                message = 'Agree '
            else:
                obj.Tags.add(user)

                message = ' Agree '
            
            
            
        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None
        context = {
            'message': message, 'Tag_count' : obj.total_likes
        }
        
        return HttpResponse(json.dumps(context), content_type='application/json')
        

## --TAG 1 -- ##
def like_ready(request):
    if request.method == 'POST':

        user = request.user
        name_id = request.POST.get('pk', None)
        obj = PatientDB.objects.get(pk=name_id)
        ##pk 값 받아옴
        try:
            

            if obj.Tags.filter(id=user.id).exists():
                message = ' Agree '
                
            else:
                message = 'Agree '
        
            
            
        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None

        context = {
            'message': message, 'Tag_count' : obj.total_likes
        }
        return HttpResponse(json.dumps(context), content_type='application/json')


## --TAG 1 -- ##
def dislike(request):
    if request.method == 'POST':
        user = request.user # Doctor ID
        name_id = request.POST.get('pk', None) # Patient ID
        obj = PatientDB.objects.get(pk=name_id)
        
        ##pk 값 받아옴
        try:
            
            if obj.Tags_default.filter(id=user.id).exists():
                obj.Tags_default.remove(user)
                #message = 'DisAgree '
            else:
                obj.Tags_default.add(user)
                #message = 'Cancel '
            message = 'DisAgree '
            
        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None

    context = {
        'message1': message, 'Tags_default' : obj.total_dislikes
    }
    return HttpResponse(json.dumps(context), content_type='application/json')


## --TAG 1 -- ##
def dislike_ready(request):
    if request.method == 'POST':
        user = request.user
        name_id = request.POST.get('pk', None)
        obj = PatientDB.objects.get(pk=name_id)
        ##pk 값 받아옴
        try:
            message = 'DisAgree '
            if obj.Tags_default.filter(id=user.id).exists():
                message = ' DisAgree '
                
            else:
                message = 'DisAgree '

        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None

        context = {
            'message1': message, 'Tags_default' : obj.total_dislikes

        }
        return HttpResponse(json.dumps(context), content_type='application/json')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#TAG2

def tagging_reset_like1(request):
    if request.method == 'POST':
        user = request.user
        name_id = request.POST.get('pk', None)
        
        obj = PatientDB.objects.get(pk=name_id)
        ##pk 값 받아옴
        try:
            if obj.Tags1.filter(id=user.id).exists():
                obj.Tags1.remove(user)
                
            message = 'Agree '
            #else:
                #message = 'Cancel '
        

        except PatientDB.DoesNotExist:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer('PatientDB에 조회하고자 하시는 쿼리가 없습니다.', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None
        context = {
            'message3': message, 'Tag_count1' : obj.total_likes1
        }
        return HttpResponse(json.dumps(context), content_type='application/json')



def tagging_reset_dislike1(request):
    if request.method == 'POST':
        user = request.user
        name_id = request.POST.get('pk', None)
        obj = PatientDB.objects.get(pk=name_id)

        ##pk 값 받아옴
        try:
            if obj.Tags_default1.filter(id=user.id).exists():
                obj.Tags_default1.remove(user)
            
            message = 'DisAgree '
            #else:
                #message = 'Cancel '


        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None

    context = {
        'message4': message, 'Tags_default1' : obj.total_dislikes1
    }
    return HttpResponse(json.dumps(context), content_type='application/json')



def like1(request):
    if request.method == 'POST':

        user = request.user
        name_id = request.POST.get('pk', None)

        obj = PatientDB.objects.get(pk=name_id)
        ##pk 값 받아옴
        try:
            
            if obj.Tags1.filter(id=user.id).exists():
                obj.Tags1.remove(user)
                message = 'Agree '
            else:
                obj.Tags1.add(user)

                message = ' Agree '

        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None
        context = {
            'message3': message, 'Tag_count1' : obj.total_likes1
        }
        
        return HttpResponse(json.dumps(context), content_type='application/json')
        


def like_ready1(request):
    if request.method == 'POST':

        user = request.user
        name_id = request.POST.get('pk', None)
        obj = PatientDB.objects.get(pk=name_id)
        ##pk 값 받아옴
        try:
           

            if obj.Tags1.filter(id=user.id).exists():
                message = ' Agree '
                
            else:
                message = 'Agree '
            
            
        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None

        context = {
            'message3': message, 'Tag_count1' : obj.total_likes1
        }
        return HttpResponse(json.dumps(context), content_type='application/json')



def dislike1(request):
    if request.method == 'POST':
        user = request.user
        name_id = request.POST.get('pk', None)
        obj = PatientDB.objects.get(pk=name_id)

        ##pk 값 받아옴
        try:
            
            if obj.Tags_default1.filter(id=user.id).exists():
                obj.Tags_default1.remove(user)
                #message = 'DisAgree '
            else:
                obj.Tags_default1.add(user)
                #message = 'Cancel '
            message = 'DisAgree '

        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None

    context = {
        'message4': message, 'Tags_default1' : obj.total_dislikes1
    }
    return HttpResponse(json.dumps(context), content_type='application/json')



def dislike_ready1(request):
    if request.method == 'POST':
        user = request.user
        name_id = request.POST.get('pk', None)
        obj = PatientDB.objects.get(pk=name_id)
        ##pk 값 받아옴
        try:
            #message = 'DisAgree '
            if obj.Tags_default1.filter(id=user.id).exists():
                message = ' DisAgree '
                
            else:
                message = 'DisAgree '

        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None

        context = {
            'message4': message, 'Tags_default1' : obj.total_dislikes1

        }
        return HttpResponse(json.dumps(context), content_type='application/json')





#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#TAG3

def tagging_reset_like2(request):
    if request.method == 'POST':
        user = request.user
        name_id = request.POST.get('pk', None)
        
        obj = PatientDB.objects.get(pk=name_id)
        ##pk 값 받아옴
        try:
            if obj.Tags2.filter(id=user.id).exists():
                obj.Tags2.remove(user)
                
            message = 'Agree '
            #else:
                #message = 'Cancel '
        

        except PatientDB.DoesNotExist:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer('PatientDB에 조회하고자 하시는 쿼리가 없습니다.', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None
        context = {
            'message5': message, 'Tag_count2' : obj.total_likes2
        }
        return HttpResponse(json.dumps(context), content_type='application/json')



def tagging_reset_dislike2(request):
    if request.method == 'POST':
        user = request.user
        name_id = request.POST.get('pk', None)
        obj = PatientDB.objects.get(pk=name_id)

        ##pk 값 받아옴
        try:
            if obj.Tags_default2.filter(id=user.id).exists():
                obj.Tags_default2.remove(user)
            
            message = 'DisAgree '
            #else:
                #message = 'Cancel '


        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None

    context = {
        'message6': message, 'Tags_default2' : obj.total_dislikes2
    }
    return HttpResponse(json.dumps(context), content_type='application/json')



def like2(request):
    if request.method == 'POST':

        user = request.user
        name_id = request.POST.get('pk', None)

        obj = PatientDB.objects.get(pk=name_id)
        ##pk 값 받아옴
        try:
            
            if obj.Tags2.filter(id=user.id).exists():
                obj.Tags2.remove(user)
                message = 'Agree '
            else:
                obj.Tags2.add(user)

                message = ' Agree '

        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None
        context = {
            'message5': message, 'Tag_count2' : obj.total_likes2
        }
        
        return HttpResponse(json.dumps(context), content_type='application/json')
        


def like_ready2(request):
    if request.method == 'POST':

        user = request.user
        name_id = request.POST.get('pk', None)
        obj = PatientDB.objects.get(pk=name_id)
        ##pk 값 받아옴
        try:
           

            if obj.Tags2.filter(id=user.id).exists():
                message = ' Agree '
                
            else:
                message = 'Agree '
            
            
        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None

        context = {
            'message5': message, 'Tag_count2' : obj.total_likes2
        }
        return HttpResponse(json.dumps(context), content_type='application/json')



def dislike2(request):
    if request.method == 'POST':
        user = request.user
        name_id = request.POST.get('pk', None)
        obj = PatientDB.objects.get(pk=name_id)

        ##pk 값 받아옴
        try:
            
            if obj.Tags_default2.filter(id=user.id).exists():
                obj.Tags_default2.remove(user)
                #message = 'DisAgree '
            else:
                obj.Tags_default2.add(user)
                #message = 'Cancel '
            message = 'DisAgree '

        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None

    context = {
        'message6': message, 'Tags_default2' : obj.total_dislikes2
    }
    return HttpResponse(json.dumps(context), content_type='application/json')



def dislike_ready2(request):
    if request.method == 'POST':
        user = request.user
        name_id = request.POST.get('pk', None)
        obj = PatientDB.objects.get(pk=name_id)
        ##pk 값 받아옴
        try:
            #message = 'DisAgree '
            if obj.Tags_default2.filter(id=user.id).exists():
                message = ' DisAgree '
                
            else:
                message = 'DisAgree '

        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None

        context = {
            'message6': message, 'Tags_default2' : obj.total_dislikes2

        }
        return HttpResponse(json.dumps(context), content_type='application/json')



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#TAG4

def tagging_reset_like3(request):
    if request.method == 'POST':
        user = request.user
        name_id = request.POST.get('pk', None)
        
        obj = PatientDB.objects.get(pk=name_id)
        ##pk 값 받아옴
        try:
            if obj.Tags3.filter(id=user.id).exists():
                obj.Tags3.remove(user)
                
            message = 'Agree '
            #else:
                #message = 'Cancel '
        

        except PatientDB.DoesNotExist:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer('PatientDB에 조회하고자 하시는 쿼리가 없습니다.', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None
        context = {
            'message7': message, 'Tag_count3' : obj.total_likes3
        }
        return HttpResponse(json.dumps(context), content_type='application/json')



def tagging_reset_dislike3(request):
    if request.method == 'POST':
        user = request.user
        name_id = request.POST.get('pk', None)
        obj = PatientDB.objects.get(pk=name_id)

        ##pk 값 받아옴
        try:
            if obj.Tags_default3.filter(id=user.id).exists():
                obj.Tags_default3.remove(user)
            
            message = 'DisAgree '
            #else:
                #message = 'Cancel '


        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None

    context = {
        'message8': message, 'Tags_default3' : obj.total_dislikes3
    }
    return HttpResponse(json.dumps(context), content_type='application/json')



def like3(request):
    if request.method == 'POST':

        user = request.user
        name_id = request.POST.get('pk', None)

        obj = PatientDB.objects.get(pk=name_id)
        ##pk 값 받아옴
        try:
            
            if obj.Tags3.filter(id=user.id).exists():
                obj.Tags3.remove(user)
                message = 'Agree '
            else:
                obj.Tags3.add(user)

                message = ' Agree '

        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None
        context = {
            'message7': message, 'Tag_count3' : obj.total_likes3
        }
        
        return HttpResponse(json.dumps(context), content_type='application/json')
        


def like_ready3(request):
    if request.method == 'POST':

        user = request.user
        name_id = request.POST.get('pk', None)
        obj = PatientDB.objects.get(pk=name_id)
        ##pk 값 받아옴
        try:
           

            if obj.Tags3.filter(id=user.id).exists():
                message = ' Agree '
                
            else:
                message = 'Agree '
            
            
        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None

        context = {
            'message7': message, 'Tag_count3' : obj.total_likes3
        }
        return HttpResponse(json.dumps(context), content_type='application/json')



def dislike3(request):
    if request.method == 'POST':
        user = request.user
        name_id = request.POST.get('pk', None)
        obj = PatientDB.objects.get(pk=name_id)

        ##pk 값 받아옴
        try:
            
            if obj.Tags_default3.filter(id=user.id).exists():
                obj.Tags_default3.remove(user)
                #message = 'DisAgree '
            else:
                obj.Tags_default3.add(user)
                #message = 'Cancel '
            message = 'DisAgree '

        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None

    context = {
        'message8': message, 'Tags_default3' : obj.total_dislikes3
    }
    return HttpResponse(json.dumps(context), content_type='application/json')



def dislike_ready3(request):
    if request.method == 'POST':
        user = request.user
        name_id = request.POST.get('pk', None)
        obj = PatientDB.objects.get(pk=name_id)
        ##pk 값 받아옴
        try:
            #message = 'DisAgree '
            if obj.Tags_default3.filter(id=user.id).exists():
                message = ' DisAgree '
                
            else:
                message = 'DisAgree '

        except PatientDB.DoesNotExist as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'PatientDB에 조회하고자 하시는 쿼리가 없습니다. - {e}', level='err')
            obj = PatientDB.objects.get(pk=name_id)
            user_info = None

        context = {
            'message8': message, 'Tags_default3' : obj.total_dislikes3

        }
        return HttpResponse(json.dumps(context), content_type='application/json')

