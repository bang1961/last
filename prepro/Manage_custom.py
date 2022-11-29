## 첫번째 전처리 코드 파일이름 바꿔줌 *histogram 제외
## 파일이동시 수정사항 : PATH, len(dst), src[:]
## 데이터 개수 전과 후 확인!! 두번 실행시 두번 저장될 수있으므로 백업해야함

from sklearn.model_selection import train_test_split
from collections import Counter
from datetime import datetime
import os, glob,  cv2
from imutils import paths
import pandas as pd
import numpy as np
import shutil
from random import *
YEAR, MONTH, DAY = datetime.today().year, datetime.today().month, datetime.today().day
MODE = 'add_dataset' # MODE 는 900과 add_dataset 둘 중에 하나 골라서 하면 됨.

ROOT_PATH =  '/home/super'
DATASET_PATH = f'{ROOT_PATH}/jong/어치' # 데이터 셋 경로

SAVE_PATH = f'{ROOT_PATH}/jong/어치' # 저장 경로
TEST_SIZE = 0.3 # 학습용 데이터 셋과 검증용 데이터 셋을 나누는 비율

# 대분류되어 저장될 폴더 이름들 #
main_category = ['Internal_content', 'Echogenicity', 'Shape', 'Orientation', 
                'Margin', 'Calcification', 'spongiform']

# 소분류되어 저장될 폴더 이름들 #
subcategory = [
    {1 : 'Solid', 2 : 'Predominantly_solid', 3: 'Predominantly_cystic', 4: 'cystic'},
    {1 : 'Hypoechogenicity', 2 : 'Isoechogenicity', 3 : 'Hyperechogenicity'},
    {1 : 'Round_to_oval', 2 : 'Irregular'}, {1 : 'Parallel', 2 : 'NonParallel'},
    {0 : 'Smooth', 1 : 'Smooth', 2 : 'Spiculated_microlobulated', 3 : 'Ill-defined'},
    {0 : 'absent', 1 : 'Microcalcification', 2 : 'Macrocalcification', 3 : 'Rimcalcification', 4 : '1,2', 5 : '1,3'},
    {0 : 'absent', 1 : 'present'}
]

# 이미지 파일을 엑셀 파일에 맞게 이름 변경해주는 함수
def file_rename(grade = 'C3'):
    file_path = f'{DATASET_PATH}/train/{grade.upper()}'
    print(grade)
    total_str_list = []
    files = glob.glob(file_path + '/*')
    file_names = os.listdir(file_path)    
    excel_file = pd.read_excel(f'{DATASET_PATH}/excels/영상전달Data_{grade.upper()}.xlsx')
    excel_file = pd.DataFrame(excel_file)

    excel_file = excel_file.replace("1,2",4)
    excel_file = excel_file.replace("1,3",5)
    excel_file = excel_file.replace("해당없음. ","")
    excel_file = excel_file.replace("위쪽 결절","")
    excel_file = excel_file.replace("화면잘못표기_RT가 맞음","")
    excel_file = excel_file.replace("제일 오른쪽 cystic 결절","")

    patient_key = list(excel_file.columns)[0]
    label_key = list(excel_file.columns)[1]
    remove_key = list(excel_file.columns)[-2]

    excel_file = excel_file.loc[:, :remove_key]
    patient_data = excel_file.loc[:, patient_key]
    label_data = excel_file.loc[:, label_key:]
    print("patient_data",patient_data)
    label_data = label_data.dropna(axis = 0, how = 'all')
    label_data = label_data.dropna(axis = 1, how = 'all')

    # 900 데이터 셋 용
    if MODE == '900':
        label_data.index = label_data.index if grade == 'C5' else (label_data.index + 520 if grade == 'C3' else label_data.index + 300)

    # 현재 데이터 셋 용
    else:
        patient_data = [patient for patient in patient_data if ((patient - 1) in label_data.index)]
        print("patient_dataset",patient_data)
    for name in file_names:
            src = os.path.join(file_path, name)
            #dst = str(name).replace('batch_', '')
            dst = str(name).replace('batch_', '')
            dst = str(dst[4:])
            dst = os.path.join(file_path, dst)

        # 900 데이터 셋 용
            if MODE == '900':
                new_name = os.path.join(file_path, os.path.basename(dst))
                os.rename(src, new_name)

            # 현재 데이터 셋 용
            else:		
                # len(dst) 는 일의자릿수는 01 -> 두글자 십의자리는 011 새글자로 되어있어 파일이름을 수정함 
                # 경로의전체길이에서 -3 
                if len(dst) == 39: # 전체 경로란 이미지 포함
                    new_name = os.path.join(file_path, '0' + os.path.basename(dst))
                    os.rename(src, new_name)
                else:
                    new_name = os.path.join(file_path, '00' + os.path.basename(dst))
                    os.rename(src, new_name)

    for (patient, labels) in zip(patient_data, label_data.values):

        patient, tail_str = str(patient).zfill(3), ''
        for label in labels: tail_str = tail_str + f'{str(int(label))}_' if pd.notnull(label) else f'{tail_str}_'
        print("total__--==",patient)
        total_str = f'{patient}_{tail_str}.jpg'
        total_str = os.path.join(file_path,total_str)
        total_str_list.append(total_str)

    file_src = os.listdir(file_path)
    src_list = [os.path.join(file_path, src) for src in file_src]
    for idx, src in enumerate(src_list, 1):
            for total in total_str_list:
                    #print(f'src : {src} subsrc : {src[35:38]}\n total : {total} subtotal : {total[35:38]}\n')
                compare_src = os.path.basename(src)
                compare_total = os.path.basename(total)
                
                    #src[전체 경로길이-13:전체 경로길이-10]
                if src[29:32] == total[29:32]:
                    file_name = os.path.splitext(total)[0]
                    print(file_name)

                    file_name = f'{file_name}{YEAR}_{str(MONTH).zfill(2)}_{str(DAY).zfill(2)}_{str(idx).zfill(4)}.jpg'
                    os.rename(src, file_name)
                    
                    print('{} ==> {}'.format(src, file_name))


## 결절의 등급(C3, C4, C5)별로 이미지 목록을 불러 와, 데이터 셋 유형(train, test) 별로 나누어 복사하는 함수
def file_move(grade = 'C3', dataset_type = 'train', percentage = 0.3):
    filepaths = f'{DATASET_PATH}/train/{grade.upper()}'
    filelist = os.listdir(filepaths)

    main_category_bu = main_category if nodule_grade in ['C3', 'C4', 'C5'] else [main_category[0]] + main_category[2:]
    subcategory_bu = subcategory if nodule_grade in ['C3', 'C4', 'C5'] else [subcategory[0]] + subcategory[2:]

    #################################### 대분류와 소분류 매칭 ###############################
    labels = {feat : lb for feat, lb in zip(main_category_bu, subcategory_bu)}
    
    ###################################################### labels 출력결과 ##########################################################
    # {
    # 'Internal_content': {1: 'Solid', 2: 'Predominantly_solid', 3: 'Predominantly_cystic', 4: 'cystic'}, 
    # 'Echogenicity': {1: 'Hypoechogenicity', 2: 'Isoechogenicity', 3: 'Hyperechogenicity'}, 
    # 'Shape': {1: 'Round_to_oval', 2: 'Irregular'}, 'Orientation': {1: 'Parallel', 2: 'NonParallel'}, 
    # 'Margin': {1: 'Smooth', 2: 'Spiculated_microlobulated', 3: 'Ill-defined'}, 
    # 'Calcification': {0: 'absent', 1: 'Microcalcification', 2: 'Macrocalcification', 3: 'Rimcalcification', 4: '1,2', 5: '1,3'}, 
    # 'spongiform': {0: 'absent', 1: 'present'}
    # }

    ########################################################################################

    ####################### train, test 별로 데이터 셋을 나누는 부분 #########################
    train_dataset, test_dataset = train_test_split(filelist, random_state = 999, 
                                                    shuffle = True, test_size = percentage)
    datasets = {'train' : train_dataset, 'test' : test_dataset}
    ########################################################################################

    for odx, file_path in enumerate(datasets[dataset_type], 1):
        
        ## 파일 이름에서 필요한 대분류의 인덱스 값만 추출 ##
        ## 'Internal_content', 'Echogenicity', 'Shape', 'Orientation', 'Margin', 'Calcification', 'spongiform' ##
        feature_label = file_path.split('_')[3: -2]
        
        ########################################### feature_label 출력 결과 ###################################
        # ['1', '1', '1', '2', '1', '4', '0'] => 해당 파일 아래 7개의 대분류에 해당하는 소분류 인덱스 값들.
        # 'Internal_content', 'Echogenicity', 'Shape', 'Orientation', 'Margin', 'Calcification', 'spongiform'
        # e.g. '1', '1', '1', ... => Internal_content : 1, Echogenicity : 1, Shape : 1, ...

        print(f'[{grade}-{odx}] file name : {file_path}')
        print(f'[{grade}-{odx}] feature indexes : {feature_label}')

        ########################### filepaths에 있는 파일을 대분류, 소분류 별로 분류하여서 복사해주는 반복문 ###################
        for idx, (feat_lb, feat_name) in enumerate(zip(feature_label, main_category_bu), 1):
            ############################### 간혹 가다가 라벨 인덱스가 공백인 부분이 있어서 예외처리 ###########################
            try:
                label = labels[feat_name][int(feat_lb)]
                print(f'[{grade}-{odx}-{idx}] fature name : {feat_name}, label idx : {feat_lb}, label : {label}')
                
                ## 다른 날짜의 데이터 셋에서도 동일한 이름을 가진 파일이 있으면, 파일 이름이 겹치지 않도록  파일 이름에 오늘 날짜 추가 ##
                file_name, file_ext = file_path.split('.')[0], file_path.split('.')[1]
                file_name = f'{file_name}_{YEAR}_{str(MONTH).zfill(2)}_{str(DAY).zfill(2)}.{file_ext}'
                ###################################################################################################################

                os.makedirs(f'{SAVE_PATH}/{feat_name}/{dataset_type}/{label}', exist_ok = True)
                #os.makedirs(f'{ONEBONE_PATH}/{feat_name}/{dataset_type}/{label}', exist_ok = True)
                shutil.copy2(filepaths + "/" + file_path, f'{SAVE_PATH}/{feat_name}/{dataset_type}/{label}/{file_name}')
                #shutil.copy2(filepaths + "/" + file_path, f'{ONEBONE_PATH}/{feat_name}/{dataset_type}/{label}/{file_name}')
                print(f'[ok] {file_name}')
            except Exception as e:
                print(f'[Error] {e}')
            ################################################################################################################
        ####################################################################################################################

        print('\n')


# 학습용과 검증용으로 나누어진 데이터 셋을 옮겨주는 함수
def file_move_for_train_valid(dataset, data_type = 'test'):

    save_path = f'{DATASET_PATH}/{data_type}'
    for idx, data in enumerate(dataset):

        print('\n\n\n', data)
        label_name = data.split(os.path.sep)[-2]
        file_name = data.split(os.path.sep)[-1]

        [os.makedirs(f'{save_path}/{label_name}', exist_ok = True) for data_type in ['train', 'valid']]
        print(f'[{data_type}-{idx}]. {data}')
        shutil.move(data, f'{save_path}/{label_name}/{file_name}')
        




for nodule_grade in ['C3','C4','C5']: # 중간에 오류나면 이미 된거 빼고 돌리기
    file_rename(nodule_grade)

    file_move(nodule_grade)
    file_move(nodule_grade, dataset_type = 'test')

# 전체 데이터 셋을 7:3 비율로 학습용, 검증용으로 나누어 주는 부분 
# image_paths = sorted(paths.list_images(DATASET_PATH))
# image_labels = [image_path.split(os.path.sep)[-2] for image_path in image_paths]
# train_data, valid_data = train_test_split(image_paths, test_size = TEST_SIZE, shuffle = True, stratify = image_labels)

# datasets = {'train' : train_data, 'valid' : valid_data}
# for idx, (d_type, dataset) in enumerate(datasets.items()):
#     print(f'{idx}. {d_type} 데이터 셋 진행중...')
#     file_move(dataset, data_type = d_type)

    

