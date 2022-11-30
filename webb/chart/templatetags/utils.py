from UTIL import config
import traceback
import json

## 현재 로그인 되어 있는 사용자 용
def partial_chart_data(chart_dict, user_name, json_path):
    try:
        ## DB에 저장되어 있는 json 경로의 json 파일을 불러오는 부분 ##
        json_data = json.loads(open(json_path, 'rb').read())
        n_count = json_data['result']['ncount'] 

        if n_count != 0:
            for key, value in json_data['result'].items():
                
                ## key 값이 ncount인 부분은 넘기고 결절 (nodule1, nodule2, ..., nodule n)에 있는 부분 중 분류 모델 결과가 저장된 텍스트 파일 경로를 가지고 옴.##
                if 'ncount' in key.lower(): continue
                else:
                    text_path = value['classi_text_path']
                    ## 텍스트 파일에 저장되어 있는 K-TIRADS 정보를 기반으로 K-TIRADS, Benign/Malignant, Positive/Negative 카운트 올림 ##
                    grade = text_mining(text_path)
                    malignant = 'Malignant' if grade in set(['C4', 'C5']) else 'Benign'
                    positive = 'Positive' if grade in set(['C4', 'C5']) else 'Negative'

                    chart_dict[user_name]['K-TIRADS'][grade] += 1
                    chart_dict[user_name]['Malignant'][malignant] += 1
                    chart_dict[user_name]['Positive'][positive] += 1

            ## 따로 차트 표시용 json 파일을 만들려고 했으나 고쳐야 할 부분이 너무 많아서 잠정 보류 ##
            # json.dump(chart_dict, open(f'media/chart.json', 'w'), ensure_ascii=False, indent = 4)

            #! json file 예시 !#
            #         {
            #     "patient id": "test003",    => 환자 id
            #     "visit date": "2022/01/11",   => 방문 날짜
            #     "original image path": "/home/super/바탕화면/share/lt4/media/2022/01/11/test003/test003.jpg",  => 원본 입력 이미지 경로
            #     "inspection image path": "/home/super/바탕화면/share/lt4/media/2022/01/11/test003/detected/test003_detected.jpg", => 결절 검출 검사된 이미지 경로 
            #     "result": {
            #         "ncount": 1, => 결절 갯수
            #         "nodule1": {
            #             "nodule image path": "/home/super/바탕화면/share/lt4/media/2022/01/11/test003/nodule/test003_nodule_0.jpg", => 결절만 잘려진 이미지
            #             "classi_text_path": "/home/super/바탕화면/share/lt4/media/2022/01/11/test003/nodule/nodule_0.txt", => 분류모델 결과가 저장된 텍스트 파일 경로
            #             ## 결절 특성들 ##
            #             "Shape": null, 
            #             "Margin": null,
            #             "Calcification": null,
            #             "Spongiform": null,
            #             "Internal content": null,
            #             "Echogenicity": null,
            #             "Orientation": null,
            #             "comet tail": null
            #         }
            #     }
            # }

        else:
            ## 이미지에서 결절을 찾지 못한 경우에 데이터 처리 ##
            chart_dict[user_name]['K-TIRADS']['C1'] += 1
            chart_dict[user_name]['Malignant']['Absent'] += 1
            chart_dict[user_name]['Positive']['Absent'] += 1
            
    ## json 파일이 없는 경우에 입력으로 받았던 딕셔너리를 반환 ##
    except Exception as e:
        ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조

        config.log_writer(f'{user_name}님의 검진 json 파일이 존재하지 않습니다.', level='warn')
    return chart_dict

## 전체 사용자 용
def total_chart_data(chart_dict, json_path):
    try:
        ## DB에 저장되어 있는 json 경로의 json 파일을 불러오는 부분 ##
        json_data = json.loads(open(json_path, 'rb').read())
        n_count = json_data['result']['ncount'] 

        if n_count != 0:
            for key, value in json_data['result'].items():
                
                ## key 값이 ncount인 부분은 넘기고 결절 (nodule1, nodule2, ..., nodule n)에 있는 부분 중 분류 모델 결과가 저장된 텍스트 파일 경로를 가지고 옴.##
                if 'ncount' in key.lower(): continue
                else:
                    text_path = value['classi_text_path']
                    ## 텍스트 파일에 저장되어 있는 K-TIRADS 정보를 기반으로 K-TIRADS, Benign/Malignant, Positive/Negative 카운트 올림 ##
                    grade = text_mining(text_path)
                    malignant = 'Malignant' if grade in set(['C4', 'C5']) else 'Benign'
                    positive = 'Positive' if grade in set(['C4', 'C5']) else 'Negative'

                    chart_dict['K-TIRADS'][grade] += 1
                    chart_dict['Malignant'][malignant] += 1
                    chart_dict['Positive'][positive] += 1

            ## 따로 차트 표시용 json 파일을 만들려고 했으나 고쳐야 할 부분이 너무 많아서 잠정 보류 ##
            # json.dump(chart_dict, open(f'media/chart.json', 'w'), ensure_ascii=False, indent = 4)

                #! json file 예시 !#
                #         {
                #     "patient id": "test003",    => 환자 id
                #     "visit date": "2022/01/11",   => 방문 날짜
                #     "original image path": "/home/super/바탕화면/share/lt4/media/2022/01/11/test003/test003.jpg",  => 원본 입력 이미지 경로
                #     "inspection image path": "/home/super/바탕화면/share/lt4/media/2022/01/11/test003/detected/test003_detected.jpg", => 결절 검출 검사된 이미지 경로 
                #     "result": {
                #         "ncount": 1, => 결절 갯수
                #         "nodule1": {
                #             "nodule image path": "/home/super/바탕화면/share/lt4/media/2022/01/11/test003/nodule/test003_nodule_0.jpg", => 결절만 잘려진 이미지
                #             "classi_text_path": "/home/super/바탕화면/share/lt4/media/2022/01/11/test003/nodule/nodule_0.txt", => 분류모델 결과가 저장된 텍스트 파일 경로
                #             ## 결절 특성들 ##
                #             "Shape": null, 
                #             "Margin": null,
                #             "Calcification": null,
                #             "Spongiform": null,
                #             "Internal content": null,
                #             "Echogenicity": null,
                #             "Orientation": null,
                #             "comet tail": null
                #         }
                #     }
                # }

            else:
                ## 이미지에서 결절을 찾지 못한 경우에 데이터 처리 ##
                chart_dict['K-TIRADS']['C1'] += 1
                chart_dict['Malignant']['Absent'] += 1
                chart_dict['Positive']['Absent'] += 1
            
    ## json 파일이 없는 경우에 입력으로 받았던 딕셔너리를 반환 ##
    except Exception as e:
        ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
        ERR = f'[ERR] 전체 검진 json 파일이 존재하지 않습니다. - {e} \n상세 : {traceback.format_exc()}'
        config.log_writer(ERR, level='warn')

    return chart_dict

## 텍스트 파일을 불러와서 K-TIRADS를 뽑아주는 함수 ##
def text_mining(text_path):

    ## 텍스트 파일을 불러 올 경우에 아래와 같이 저장되어 쉼표로 나눈 것을 기준으로 마지막 텍스트에서 다시 한 번 콜론으로 나눈것의 마지막 값을 가져옴. ##
    ## (e. g.) ##
    ## text = 'nodule name : 0, percent : [0.014 0.000 0.001 0.985], label_name : C5' ## 
    ## text.split(',')[-1] => label_name : C5, text.split(',')[-1] .split(':')[-1] => C5 ##

    text = open(text_path, 'r').readline()
    grade =  text.split(',')[-1].split(' : ')[-1].replace('\n', '')

    return grade.replace(' ', '')

if __name__ == '__main__':
    partial_chart_data('/home/super/바탕화면/share/lt4/media/2022/01/06/test020/nodule/nodule.json')