from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from history.models import PatientDB
from chart.templatetags import utils
from UTIL import config

@csrf_exempt
def chart_page(request):
    ## PatientDB에서 현재 로그인 되어 있는 id로 게시된 게시물 목록을 가져옴. ##
    ## user_id : 현재 로그인 되어 있는 id 정보 ##
    ## partial_db: 현재 로그인 되어 있는 id로  등록 되어있는 레코드 목록 ##

    ## 로그인 되어있으면 history 페이지로 이동 ##
    if request.user.is_authenticated:
        user_id = request.user
        partial_db = PatientDB.objects.filter(user_id = user_id)
        total_db = PatientDB.objects.order_by('-visit_date')

        ## user_idx : 게시글 목록에서 첫 번째 게시글의 User id 인덱스 값을 가지고 옴. ##
        ## user_name : 가입된 계정들 DB에서의 user_idx값을 조회하여 user_name을 가지고 옴. ##
        try:
            user_idx = partial_db[0].user_id
            user_name = User.objects.filter(id = user_idx)
            user_name = user_name[0].username

        except:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'DB에서 사용자 id를 가져올 수 없어 현재 로그인 되어있는 id를 사용합니다.', level='warn')
            user_name = user_id

        ## total_chart_dict : 전체 계정의 환자 통계 자료를 저장시켜주는 변수 ##
        total_chart_dict =  {
            'K-TIRADS' : {k : 0 for  k in ['C1', 'C2', 'C3', 'C4', 'C5']},
            'Malignant' : {m : 0 for m in ['Absent', 'Benign', 'Malignant']},
            'Positive' : {p :0 for p in ['Absent', 'Negative', 'Positive']}
        }


        ## partial_chart_dict : 로그인 되어 있는 계정의 환자 통계 자료를 저장시켜주는 변수 ##
        partial_chart_dict =  {
            user_name : {
            'K-TIRADS' : {k : 0 for  k in ['C1', 'C2', 'C3', 'C4', 'C5']},
            'Malignant' : {m : 0 for m in ['Absent', 'Benign', 'Malignant']},
            'Positive' : {p :0 for p in ['Absent', 'Negative', 'Positive']}
            }
        }

        ##  DB에 있는 json 경로들을 이용해 K-TIRADS, Malignant/Benign .... 등 수치를 가져오도록 함. ##
        ##  수치를 가져오는 자세한 코드는 /home/super/바탕화면/share/lt4/chart/templatetags/utils.py 참조 ##
        for data in total_db: total_chart_data = utils.total_chart_data(total_chart_dict, data.json_path)
        for data in partial_db: partial_chart_data = utils.partial_chart_data(partial_chart_dict, user_name, data.json_path)[user_name]

        ## 파이차트에 적어줄 범례(legend)들 ##
        k_labels, m_labels, p_labels = [f'C{idx}' for idx in range(1, 6)], [ 'Absent', 'Benign', 'Malignant'], [ 'Absent', 'Negative', 'Positive']
        
        
        ## 환자 이력 DB에 데이터가 있을 경우에 k_datas, m_datas, p_datas를 가져옴. ##
        ## tk_datas (total k-tirads datas) : 전체 사용자의 k-tirads 데이터만 담겨져 있는 데이터
        ## tm_datas (total malignant datas) : 전체 사용자의 malignant 데이터만 담겨져 있는 데이터
        ## tp_datas (total positive datas) : 전체 사용자의 positive 데이터만 담겨져 있는 데이터
        try:
            tk_datas = [tkv for tkv in total_chart_data['K-TIRADS'].values()]
            tm_datas = [tmv for tmv in total_chart_data['Malignant'].values()]
            tp_datas = [tpv for tpv in total_chart_data['Positive'].values()]
            
        except Exception as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer('전체 검진 데이터가 존재하지 않습니다. - {e}', level='err')
            print('[ERROR] 전체 데이터가 존재하질 않습니다.')
            tk_datas, tm_datas, tp_datas = [0, 0, 0, 0], [0, 0], [0, 0]

        ## 환자 이력 DB에 데이터가 있을 경우에 k_datas, m_datas, p_datas를 가져옴. ##
        ## pk_datas (partial k-tirads datas) : 현재 로그인 되어있는 사용자의 k-tirads 데이터만 담겨져 있는 데이터
        ## pm_datas (partial malignant datas) : 현재 로그인 되어있는 사용자의 malignant 데이터만 담겨져 있는 데이터
        ## pp_datas (partial positive datas) : 현재 로그인 되어있는 사용자의 positive 데이터만 담겨져 있는 데이터
        try:
            pk_datas = [pkv for pkv in partial_chart_data['K-TIRADS'].values()]
            pm_datas = [pmv for pmv in partial_chart_data['Malignant'].values()]
            pp_datas = [ppv for ppv in partial_chart_data['Positive'].values()]

        except Exception as e:
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer(f'{user_name}님의 검진 데이터가 존재하지 않습니다. - {e}', level='err')
            print(f'[ERROR] {user_name}님의 데이터가 존재하질 않습니다.')
            pk_datas, pm_datas, pp_datas = [0, 0, 0, 0], [0, 0], [0, 0]

        context = {'user_name' : user_name, 'total_db' : total_db, 'partial_db' : partial_db, 
                        'tk_datas' : tk_datas, 'pk_datas' : pk_datas, 'k_labels' : k_labels,
                        'tm_datas' : tm_datas, 'pm_datas' : pm_datas, 'm_labels' : m_labels , 
                        'tp_datas' : tp_datas, 'pp_datas' : pp_datas, 'p_labels' : p_labels}

        return render(request, 'charts.html', context)

        ## 로그인 되어 있지 않으면 로그인 페이지로 이동 후 검사 페이지로 이동 ##
    else:
        return redirect('login')

