from django import template
from UTIL import config
import os, time

ROOT_PATH = config.ROOT_PATH
register = template.Library()

#! 이전 커스텀 태그 인자 여러개 적용 참조용 !#
# @register.filter
# def sub(value, arg):
#     return value - arg

## 페이지 별로 테이블에 인덱스 값을 넣기 위한 함수 ##
@register.filter
def calculate_index(page):
    return 20*(page-1)

## 인공지능 판독결과  페이지에 K-TIRADS 및 결절 특성별 판단 확률을 기입해주기 위한 함수
## 기존에는 특성별 결과를 표시하는 함수를 따로 만들었던 것을 한 개의 함수로 통합함.
@register.filter
def search(value, content):
    ## templates/tagging_history_blank.html에서 사용

    ## K-TIRADS, Benign/Malignant, Positive/Negative 판독 결과
    if 'grade' in content.lower(): zips = zip(['C2', 'C3', 'C4', 'C5'], value)
    elif 'bm' in content.lower(): zips = zip(['B', 'M'], value)
    elif 'pn' in content.lower(): zips = zip(['N', 'P'], value)

    ## echogenicity 판독 결과
    elif 'echo' in content.lower(): zips = zip(['Hyper~', 'Hypo~', 'Iso~'], value)

    ## margin 판독 결과
    elif 'margin' in content.lower(): zips = zip(['Smooth', 'Spiculated', 'Ill-defined'], value)

    ## calcification 판독 결과
    elif 'calcification' in content.lower(): zips = zip(['Absent', 'Micro~','Macro~'], value)

    ## spongiform 판독 결과
    elif 'spongiform' in content.lower(): zips = zip(['absent', 'present'], value)

    ## internal content  판독 결과
    ## internal2 는 internal content가 C2인 경우에 적용됨.
    elif content.lower() == 'internal': zips = zip(['Solid', 'Predominantly Solid'], value)
    elif content.lower() == 'internal2': zips = zip(['Benign','Colloid','Spongiform'], value)

    ## shape 판독 결과
    elif 'shape' in content.lower(): zips = zip(['Irregular ', 'Round_to_oval '], value)

    ## orientation 판독 결과
    elif 'orientation' in content.lower(): zips = zip(['Parallel ', 'Nonparallel '], value)

    value = {grade : f'{score*100:.2f}%' for grade, score in zips}

    return value.items()


@register.filter
def sub_index(value):
    return value - 1


## json 파일에 적혀있는 경로대로 이미지를 불러올 경우에 에러가 발생하여 폴더 이름을 media 부터 시작하도록 하고, 앞에 /을 붙임.##
## e.g. "/home/super/바탕화면/share/lt4/media/2022/01/11/test003/test003.jpg => /media/2022/01/11/test003/test003.jpg ##
@register.filter
def add_dir(path, image_type='crop'):
    ## lt4 서버와 super, 사내 3번째 서버에서 lt4/media 폴더에 접근하는 길이가 달라 수정
    path = path.split(os.path.sep)[4:] if config.SNUBH else (path.split(os.path.sep)[7:] 
                                        if config.MK3 else path.split(os.path.sep)[6:])

    ## 검출된 이미지와 크롭된 이미지의 접근 경로가 달라 수정
    #! 하나로 통일할 경우에 아래와 같이 지정되어 수정함.
    ## 검출된 이미지 경로 | //media/2022/01/11/test003/detected/test_axial_detected.jpg
    ## 크롭된 이미지 경로 | /media/2022/01/11/test003/nodule/dove_axial/dove_axial_nodule_1.jpg 
                    
    return "/".join(path) if 'detection' in image_type else f'/{"/".join(path)}'

## json 파일에서 특성별 판독결과가 None인 경우에 결과 표시안하고 그냥 넘어감.
@register.filter
def is_None(value):
    return value == None


#colloid시 comettail 값 동일한 결과 출력을 위함
@register.filter
def back(value):
    value = value.replace('%', '')
    value = float(100.00-float(value))
    return value


## 100 - value 값 반환 commet tail , spongiform C2일때 사용
@register.filter
def split(value):
    value = (value)/2
    return int(value)


## 결과가 저장되어 있는 텍스트 파일 불러와 표시
@register.filter
def history_view(text_path, sleep_seconds=4):
    
    try:
        text = open(text_path, 'r').readlines()[0]
        score = text.split(',')
        score = score[-1].split(':')[-1]
        score = score.replace(' ', '')

    ## 첫 검사시 텍스트 파일 못찾을 때
    except:
        time.sleep(sleep_seconds)
        
        ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
        config.log_writer(f'첫 검사 텍스트 파일을 찾지 못하였습니다.', level='warn')

        text = open(text_path, 'r').readlines()[0]
        score = text.split(',')
        score = score[-1].split(':')[-1]
        score = score.replace(' ', '')

    return score


## 입력받은 K-TIRADS 값이 C2, C3면 True, C4, C5면 False를 반환해주는 함수
@register.filter
def is_positive(grade):
    
    ## 입력받는 grade값에 \n이 포함되어 있어 \n을 제거하고 C2, C3인지 판단
    result = grade.replace('\n', '') in ["C2", "C3"]
    return result

## K-TIRADS가 C2, C3인 경우에 
## calcification -> micro calcification,
## margin        -> spiculated,
## orientation   -> nonparallel 인지 아닌지 판단해주는 함수
@register.filter
def NA_contents(content, feature):
  
  ## feature가 calcification인 경우 content에 micro가 포함되어 있으면 True, 아니면 False 반환
  if 'calci' in feature: result = 'micro' in content.lower()
  
  ## feature가 margin인 경우 content에 spiculated가 포함되어 있으면 True, 아니면 False 반환
  elif 'margin' in feature: result = 'spiculated' in content.lower()
  
  ## feature가 orientation인 경우 content에 nonparallel이 포함되어 있으면 True, 아니면 False 반환
  elif 'ori' in feature: result = 'nonparallel' in content.lower()
  return result
