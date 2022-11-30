from imutils.paths import list_images, list_files
from django import template
from UTIL import config
import json, os, time

register = template.Library()
ROOT_PATH = config.ROOT_PATH


@register.filter
def substring(value):
    return value.split(os.path.sep)[-1]

# @register.filter
# def add_string(date, patient):
#     print("a", str(date) + str(f'/{patient}'))
#     return str(date) + str(f'/{patient}')

@register.filter
def add_string(date, imgfile):
    before = '/'.join(str(imgfile).split(os.path.sep)[:-1])
    after = f'media/{before}'

    return str(after)

@register.filter
def nodule_idx(nodule_image_path):
    image_paths = sorted(list_images(f'{ROOT_PATH}{nodule_image_path}'))
    #nodule_image_path.split(os.path.sep)[-1]
    #print("확인2",[image_path for image_path in image_paths if 'axial_nodule_' in image_path.lower()])
    image_paths = [image_path for image_path in image_paths if 'axial_nodule_' in image_path.lower()]
    image_path=[]
    image_path.append(str(ROOT_PATH)+str(nodule_image_path)+'/'+str(nodule_image_path.split(os.path.sep)[-1])+'_axial/'+ str(nodule_image_path.split(os.path.sep)[-1])+ '_axial_nodule_0.jpg')
    print("확인1",image_paths)
    return image_paths
 
@register.filter
def nodule_idx2(nodule_image_path):
    
    # image_paths = sorted(list_images(f'{ROOT_PATH}{nodule_image_path}'))
    # #nodule_image_path.split(os.path.sep)[-1]
    # image_paths = [image_path for image_path in image_paths if 'hst' in image_path.lower()]

    image_paths=(str(ROOT_PATH)+str(nodule_image_path)+'/'+str(nodule_image_path.split(os.path.sep)[-1])+'_axial/'+ str(nodule_image_path.split(os.path.sep)[-1])+ '_axial_nodule_0.jpg')
    
    print("nodule_image_path2:",image_paths)
    return image_paths
    
def nodule_sagittal(nodule_image_path,patient):
    
    image_paths = sorted(list_images(f'{ROOT_PATH}{nodule_image_path}/{patient}_sagittal.jpg'))
    return image_paths

## media/date/patient_id
@register.filter
def result(date,patient):
    patient_path = ROOT_PATH+ str(date) + str(f'/{patient}')
    file_path = os.listdir(f"{file_path}/nodule")
    file_path = [file_path for file_path in file_path if 'txt' in file_path.lower()]
    line = []
    for idx, _ in enumerate(file_path):
        with open(f"{patient_path}/nodule/nodule_{idx}.txt") as f:
            idx = f.readlines()           
            line.append(idx)

    return line

@register.filter
def nodule_images_number(nodule_image_path):
    #
    image_paths = sorted(list_images(nodule_image_path))

    image_paths = [image_path for image_path in image_paths if 'hst' in image_path.lower()]

    return len(image_paths)

@register.filter
def detectfile(nodule_image_path):
    #
    Detect_paths = sorted(list_images(f'{ROOT_PATH}{nodule_image_path}'))
    Detect_paths = [image_path for image_path in Detect_paths if 'detected' in image_path.lower()]

    return Detect_paths

@register.filter
def isfile(date, patient):
    return os.path.exists(ROOT_PATH + str(date) + str(f'/{patient}') + str(f'/nodule/{patient}_axial/'))
    #return os.path.isfile(ROOT_PATH+str(date) + str(f'/{patient}') + str(f'/nodule/{patient}_axial/{patient}_axial_nodule_0.txt'))

#json 파일 발견함수
@register.filter
def isjson(date, patient):
    return os.path.isfile(ROOT_PATH+str(date) + str(f'/{patient}') + str(f'/jsons/{patient}_axial_nodule.json'))

#nodule.json 에서 model complete의 value return
@register.filter
def isimg(date, patient):
    with open(ROOT_PATH+str(date) + str(f'/{patient}') +str(f'/jsons/{patient}_axial_nodule.json'), 'r') as f:
        json_data = json.load(f)

        return int(json_data['model complete'])

@register.filter
def view(date, patient, sleep_seconds=3):

    ## 결절을 여러개 검출한 경우 탭에서 선택하여 텍스트 파일을 불러오는 인덱스 지정 
    ## 입력값은 환자id/1, 환자id/2 처럼 들어옴.
    num = patient.split('/')[-1]
    patient = patient.split('/')[:-1]
    patient = ('/').join(patient)
    
    #after = patient.split('_')[0]
    after = patient.split('_')[:-1]
    after = after[0]

    try:
        ## 이미지에서 결절과 협부, 경동맥도 검출하는 경우에 이미지랑 텍스트의 인덱스가 2로 붙어서 
        ## 텍스트 파일을 불러오는 방법을 변경

        file_path = f'{ROOT_PATH}{str(date)}/{patient}/nodule/{after}_axial'
        file_paths = sorted(list_files(file_path))
        confirm = os.listdir(file_path)
        print(f'\n\n확인 : {confirm} \n\n')
        
        ## 결절만 크롭된 이미지와 텍스트 파일이 저장되있는 경로에서 텍스트 파일만 가져오는 부분 
        file_paths = [file_path.split(os.path.sep)[-1] for file_path in file_paths if file_path.split('.')[1] in 'txt']
        file_paths = [f'{ROOT_PATH}{str(date)}/{patient}/nodule/{after}_axial/{file_path}' for file_path in file_paths]

        print(f'\n\n file_paths : {file_paths} \n\n')
        text = open(file_paths[int(num) - 1],'r').readlines()[0]
        score = text.split(',')
        score = score[-1].split(':')[-1]
        score = score.replace(' ', '')

    ## 첫 검사시 텍스트 파일 못찾을 때
    except:
        time.sleep(sleep_seconds)
        ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
        config.log_writer(f'첫 검사 텍스트 파일을 찾지 못하였습니다.', level='warn')
        file_paths = '/'.join([file_path,f'{after}_axial_nodule_0.txt'])
        file_paths = [file_paths]
        print(f'\n\n file_paths : {file_paths} \n\n')
        text = open(file_paths[int(num) - 1],'r').readlines()[0]
        score = text.split(',')
        score = score[-1].split(':')[-1]
        score = score.replace(' ', '')




    return score

@register.filter
def view_score(date,patient):
    
    ## 103, 104번째 라인 주석(view 함수 첫 번째 주석) 참조
    num = patient.split('/')[-1]
    patient = patient.split('/')[:-1]
    patient = ('/').join(patient)

    #after = patient.split('_')[0]
    after = patient.split('_')[:-1]
    after = after[0]
    ## 110, 111번째 라인 주석(view 함수에서 try 바로 아래 주석) 참조
    file_path = f'{ROOT_PATH}{str(date)}/{patient}/nodule/{after}_axial'
    
    file_paths = sorted(list_files(file_path))

    file_paths = [file_path.split(os.path.sep)[-1] for file_path in file_paths if file_path.split('.')[1] in 'txt']
    file_paths = [f'{ROOT_PATH}{str(date)}/{patient}/nodule/{after}_axial/{file_path}' for file_path in file_paths]

    text = open(file_paths[int(num) - 1],'r').readlines()[0]
    scores = text.split(',')
    scores = scores[1].split(':')[-1]
    scores = scores.replace('[', '').replace(']', '').split(' ')
    scores = scores[1:]

    return {f'C{idx}' :f'{float(score)*100:.2f}%' for idx, score in enumerate(scores, 2)}.items()

@register.filter
def view_score_bm(date,patient):

    ## 103, 104번째 라인 주석(view 함수 첫 번째 주석) 참조
    num = patient.split('/')[-1]
    patient = patient.split('/')[:-1]
    patient = ('/').join(patient)
    after = patient.split('_')[:-1]
    after = after[0]
    #after = patient.split('_')[0]
    ## 110, 111번째 라인 주석(view 함수에서 try 바로 아래 주석) 참조
    file_path = f'{ROOT_PATH}{str(date)}/{patient}/nodule/{after}_axial'
    file_paths = sorted(list_files(file_path))
    file_paths = [file_path.split(os.path.sep)[-1] for file_path in file_paths if file_path.split('.')[1] in 'txt']
    file_paths = [f'{ROOT_PATH}{str(date)}/{patient}/nodule/{after}_axial/{file_path}' for file_path in file_paths]

    text = open(file_paths[int(num) - 1],'r').readlines()[0]
    scores = text.split(',')
    scores = scores[1].split(':')[-1]
    scores = scores.replace('[', '').replace(']', '').split(' ')
    scores = scores[1:]
    
    GRADE = [float(score) for score in scores]
    return {bm : f'{float(score)*100:.2f}%' for bm, score in zip(['B', 'M'], [GRADE[0] + GRADE[1], GRADE[2] + GRADE[3]])}.items()

@register.filter
def view_score_pn(date,patient):

    ## 103, 104번째 라인 주석(view 함수 첫 번째 주석) 참조
    num = patient.split('/')[-1]
    patient = patient.split('/')[:-1]
    patient = ('/').join(patient)

    #after = patient.split('_')[0]
    after = patient.split('_')[:-1]
    after = after[0]
    ## 110, 111번째 라인 주석(view 함수에서 try 바로 아래 주석) 참조
    file_path = f'{ROOT_PATH}{str(date)}/{patient}/nodule/{after}_axial'
    file_paths = sorted(list_files(file_path))
    file_paths = [file_path.split(os.path.sep)[-1] for file_path in file_paths if file_path.split('.')[1] in 'txt']
    file_paths = [f'{ROOT_PATH}{str(date)}/{patient}/nodule/{after}_axial/{file_path}' for file_path in file_paths]

    text = open(file_paths[int(num) - 1],'r').readlines()[0]
    scores = text.split(',')
    scores = scores[1].split(':')[-1]
    scores = scores.replace('[', '').replace(']', '').split(' ')
    scores = scores[1:]
    
    GRADE = [float(score) for score in scores]
    return {pn : f'{float(score)*100:.2f}%' for pn, score in zip(['P', 'N'], [GRADE[2] + GRADE[3], GRADE[0] + GRADE[1]])}.items()


@register.filter
def BM(grade):
    return 'B' if grade in ('C2', 'C3') else 'M'

@register.filter
def PN(grade):
    return 'N' if grade in ('C2', 'C3') else 'P'


@register.filter
def add_slash(path):
    return f'/{path}'

@register.filter
def add_slash_extension(string1, string2):
    print('add_slash_extension',string1)
    string1 = str(string1).split(os.path.sep)[-2]
    string = f'{string1}/{string2}'

    
    return string



@register.filter
def patient_id_time_slash_extension(string1, string2):
    #print('patient_id_time_slash_extension', str(string1).split('_'), end="\n\n\n" )
    
    if len(str(string1).split('_')[:-1]) >= 2 :
        string1 = '_'.join(str(string1).split('_')[:-1])
    else :
        string1 = str(string1).split('_')[:-1]
    
    string = f'{string1}/{string2}'
    
    return string