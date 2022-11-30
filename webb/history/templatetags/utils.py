from imutils.paths import list_files
from UTIL import config
import numpy as np
import traceback
import json, os
from pathlib import Path
ROOT_PATH = config.ROOT_PATH

####################### 유틸리티 함수 #################################

## JSON 파일 경로를 입력하면 데이터를 불러오는 함수
def get_patient_info(json_path):
    #
    json_data = json.loads(open(json_path, 'rb').read())

    ## 웹 페이지에 표시해줄 데이터를 담는 리스트
    data_list = []

    ## 환자 id, 환자 방문 날짜 
    patient_id, visit_date = json_data['patient id'], json_data['visit date']

    ## 원본 이미지, 검사 이미지 경로
    original_image_path = json_data['original image path']
    inspection_image_path = json_data['inspection image path']

    ## 환자 검사 이력 중 결절의 갯수
    
    num_nodules = json_data['result']['ncount']
    
    append = data_list.append

    ##  딕셔너리 형인 Json 데이터 중 결과 데이터를 key, value 값으로 가져오는 부분
    for (key, value) in json_data['result'].items():
        
        ## key 값이 ncount인 경우 그냥 넘김
        if 'ncount' in key.lower(): continue
        else:

            ##  nodule_image_path | 검출된 결절 박스의 좌표를 기준으로 잘린 이미지 경로
            ##       classi_text_path | K-TIRADS 분류 결과가 담긴 텍스트가 저장된 경로
            nodule_image_path = value['nodule image path']
            
            try:
                ## classi_text_path | 검사 결과가 저장되어 있는 텍스트 파일의 경로
                classi_text_path = value['classi_text_path']

            ## 횡단면 이미지에서 검출된 결절의 수가 종단면에서 검출한 결절의 수보다 많을 경우를 대비한 예외처리
            except Exception as e:
                WARN = f'[WARN] 횡단면 이미지에서 종단면 보다 많은 결절이 검출되어 Axial 텍스트 파일을 이용합니다.. {e} \n상세 : {traceback.format_exc()}'
                config.log_writer(WARN, level = 'warn')

                ## Sagittal 이미지가 Axial 이미지보다 더 많이 검출하였을 때 Axial 텍스트 파일을 Sagittal 텍스트 파일로 이용
                ## json_path_exception | 입력받은 json 파일 경로에서 sagittal을 axial로 변경한 경로
                ## e.g.) media/2022/05/23/예외처리 테스트/jsons/예외처리_테스트_sagittal_nodule.json → media/2022/05/23/예외처리 테스트/jsons/예외처리_테스트_axial_nodule.json

                ## json_data_exception | axial json 데이터를 불러온 내용
                json_path_exception = json_path.replace('sagittal', 'axial')
                json_data_exception = json.loads(open(json_path_exception, 'rb').read())

                ## nodule_keys | axial json 데이터의 result 키 값 중에 nodule이 들어가는 키값 중에서 첫번째 값
                nodule_keys = [key for key in json_data_exception['result'].keys() if 'nodule' in key][0]
                classi_text_path = json_data_exception['result'][nodule_keys]['classi_text_path']

            ## score |  텍스트 파일 경로를 입력받아 각 특성별 점수를 뽑아낸 변수
            scores = text_mining(classi_text_path)
            
            ## 검사 결과 텍스트에 K-TIRADS를 포함한 결절별 특성이 모두 있는 경우
            if scores == None:
                print("NO Detect",data_list)
                
                return num_nodules, (patient_id, visit_date, classi_text_path), (original_image_path, inspection_image_path), data_list
            elif len(scores) == 9:
                grade_score, echogenicity, margin, spongiform, orientation, calcification, shape, internal, internal2  = scores
                grade_score = list(map(float, grade_score))
                echogenicity = list(map(float, echogenicity))
                margin = list(map(float, margin))
                calcification = list(map(float, calcification))
                orientation = list(map(float, orientation))
                shape = list(map(float, shape))

                try:
                    ## grade_score에서 점수가 가장 높게 나온 index 값을 가져와서 K-Tirads 추출
                    labels = ['C2', 'C3', 'C4', 'C5']
                    score_idx = np.argmax(grade_score)
                    grade = labels[score_idx]

                    ## e.g.)
                    ## grade | C2 (index :  0) => K-TIRADS
                    ## scores | [0.999, 0.0, 0.001, 0.0] => K-TIRADS 라벨별 점수

                    ## grade가 'C2'인 경우에는 'Benign', 'Colloid', 'Spongiform'의 점수 로 반환
                    ## grade가 'C2'가 아닌 경우에는 'predominantly solid', 'solid'의 점수로 반환
                    ## internal content : [0.0, 1.0, 0.0] => C2일 경우에 internal content 라벨별 점수
                    
                    max_i,min_i = sorted(internal, reverse = True)
                    print('internal:',internal)
                    internal         = [max_i, min_i]
                    
                    internal_content = list(map(float, internal)) if 'C2' not in grade else list(map(float, internal2))
                    
                    ## grade가 'C2'인 경우에는 internal content  점수로 반환
                    ## grade가 'C2'가 아닌 경우에는 Spongiform 점수로 반환
                    spongiform = list(map(float, spongiform)) if 'C2' not in grade else list(map(float, internal2))

                    ## K-TIRADS가 C2, C3인지 아닌지 판단하기 위해 만든 변수
                    condition           = grade not in ['C2', 'C3']

                    ## 원래 판독결과를 내림차순으로 정렬하여 변수에 할당
                    max_m, mid_m, min_m = sorted(margin, reverse = True)
                    max_c, mid_c, min_c = sorted(calcification, reverse = True)

                    ## C2, C3인 경우에 인공지능 판독 결과 위치 바꿔주는 부분
                    
                    ## C2, C3인 경우에 margin에서는 smooth가 가장 높게, spiculated가 가장 낮은 점수를 갖게 설정
                    ## margin의 경우에는 [smooth, spiculated, ill-defined] 순으로 반환해야 함.
                    margin         = margin if condition else [max_m, min_m, mid_m]

                    
                    ## C2, C3인 경우에 calcification에서는 absent가 가장 높게, micro calcification이 가장 낮은 점수를 갖게 설정
                    ## calcification의 경우에는 [absent, microcalcification, macrocalcification] 순으로 반환해야 함.
                    calcification  = calcification if condition else [max_c, min_c, mid_c]
                    xcondition = grade not in ['C2','C3','C4']

                    max_o,min_o = sorted(orientation, reverse = True)
                    orientation = orientation if xcondition else [max_o,min_o]
                except Exception as e:
                    print(e)

            ## 검사 결과 텍스트에 C2용 internal content가 없는 경우
            elif len(scores) == 8:
                grade_score, echogenicity, margin, spongiform, orientation, calcification, shape, internal  = scores
                grade_score = list(map(float, grade_score))
                echogenicity = list(map(float, echogenicity))
                margin = list(map(float, margin))
                spongiform = list(map(float, spongiform))
                calcification = list(map(float, calcification))
                orientation = list(map(float, orientation))
                shape = list(map(float, shape))
                internal_content = list(map(float, internal))

            ## 검사 결과 텍스트에 internal content가 없는 경우
            elif len(scores) == 7:
                grade_score, echogenicity, margin, spongiform, orientation, calcification, shape  = scores
                grade_score = list(map(float, grade_score))
                echogenicity = list(map(float, echogenicity))
                margin = list(map(float, margin))
                spongiform = list(map(float, spongiform))
                calcification = list(map(float, calcification))
                orientation = list(map(float, orientation))
                shape = list(map(float, shape))
                internal_content = value['Internal content']

            ## 검사 결과 텍스트에 internal content, shape가 없는 경우
            elif len(scores) == 6:
                grade_score, echogenicity, margin, spongiform, orientation, calcification  = scores
                grade_score = list(map(float, grade_score))
                echogenicity = list(map(float, echogenicity))
                margin = list(map(float, margin))
                spongiform = list(map(float, spongiform))
                calcification = list(map(float, calcification))
                orientation = list(map(float, orientation))

                shape = value['Shape']
                orientation = value['Orientation']
                calcification = value['Calcification']
                internal_content = value['Internal content']

            ## 검사 결과 텍스트에 internal content, shape, orientation이 없는 경우
            elif len(scores) == 5:
                grade_score, echogenicity, margin, spongiform, calcification = scores
                grade_score = list(map(float, grade_score))
                echogenicity = list(map(float, echogenicity))
                margin = list(map(float, margin))
                spongiform = list(map(float, spongiform))
                calcification = list(map(float, calcification))

                shape = value['Shape']
                orientation = value['Orientation']
                calcification = value['Calcification']
                internal_content = value['Internal content']

            ## 검사 결과 텍스트에 internal content, shape, orientation, calcification이 없는 경우
            elif len(scores) == 4:
                grade_score, echogenicity, margin, spongiform = scores
                grade_score = list(map(float, grade_score))
                echogenicity = list(map(float, echogenicity))
                margin = list(map(float, margin))
                spongiform = list(map(float, spongiform))

                shape = value['Shape']
                orientation = value['Orientation']
                calcification = value['Calcification']
                internal_content = value['Internal content']

            ## 검사 결과 텍스트에 internal content, shape, orientation, calcification, spongiform이 없는 경우
            elif len(scores) == 3:
                grade_score, echogenicity, margin = scores
                grade_score = list(map(float, grade_score))
                echogenicity = list(map(float, echogenicity))
                margin = list(map(float, margin))

                shape = value['Shape']
                orientation = value['Orientation']
                spongiform = value['Spongiform']
                calcification = value['Calcification']
                internal_content = value['Internal content']

            ## 검사 결과 텍스트에 K-TIRADS  결과만 저장되어 있는 경우 ##
            elif len(scores) == 1:
                grade_score = list(map(float, scores[0]))

                margin = value['Margin']
                echogenicity = value['Echogenicity']
                spongiform = value['Spongiform']
                calcification = value['Calcification']
                internal_content = value['Internal content']

        if scores != None:
            ##    grade_score | K-TIRADS 분류 결과가 담긴 텍스트에서 점수만 뽑아서 실수형으로 담긴 리스트
            ## C2, C3, C4, C5 | 각 K-TIRADS 별 분류 검증 스코어
            C2, C3, C4, C5 = grade_score

            ## Malignant 확률값은 C4 +C5, Benign 확률 값은 C2+C3로 계산 ##
            ## Malignant/Benign과 Positive/Negative는 같은 값을 공유##
            malignant_score = [C2 + C3, C4 + C5]

            ##  data_names  | 화면에 표시해 줄때 데이터들의 이름을 저장하는 리스트 
            ## patient_data  | 결절 정보 데이터를 저장하는 리스트
            data_names = ['#th nodule', 'nodule image path', 'malignant', 'echogenicity', 'margin', 'calcification', 
                                'orientation','shape', 'internal', 'spongiform', 'grade']
    
            patient_data = [key, nodule_image_path,  malignant_score, echogenicity, 
                             margin, calcification, orientation, shape, internal_content, spongiform, grade_score]

            ## data_names와 patient_data를 1 : 1 매칭하여 검사 결과 표시할 때 사용됨.
            data = zip(data_names, patient_data)
            append(data)
        print('godsu',classi_text_path)
    ## num_nodules가 0이면 존재하지 않음(absent), 아니면 존재(present)로 표시 
    return num_nodules, (patient_id, visit_date, classi_text_path), (original_image_path, inspection_image_path), data_list
    

## 텍스트 파일을 불러와서 각 특성별 판독 결과를 뽑아주는 함수
def text_mining(text_path):
    if text_path == None:
        scores = None
    else:
        try: texts = open(text_path, 'r').readlines()
        except TypeError as e:
            print(f"ERROR--{e}")    
        except: texts = open(text_path, 'r', encoding='utf-8').readlines()
        scores = []
        
        ## 텍스트 파일을 한 줄씩 불러와 필요한 정보만 추출
        for text in texts:
            print("ASD")
            score = text.split(',')[1].split(' : ')[-1]
            score = score.replace('[', '').replace(']', '').split(' ')
            scores.append(score)
    
    return scores

