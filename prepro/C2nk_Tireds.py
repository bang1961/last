# 두번째 전처리 코드 ==> C2 특성라벨 이동 *histogram 제외
## 파일이동시 수정사항 : PATH, len(dst)
from sklearn.model_selection import train_test_split
from collections import Counter
from datetime import datetime
import os, glob, cv2
from imutils import paths
import pandas as pd
import numpy as np
import shutil
from random import *

## 전처리된 C2를 특성별로 분류하는 코드.
## C2는 라벨이 모두 통일 되기때문에 구현함.

ROOT_PATH = '/home/super'

DATASET_PATH = f'{ROOT_PATH}/jong/어치'
SAVE_PATH = f'{ROOT_PATH}/jong/어치'

YEAR, MONTH, DAY = datetime.today().year, datetime.today().month, datetime.today().day

def renameC2():
    file_path = f"{DATASET_PATH}/train/C2"
    file_names =os.listdir(f"{DATASET_PATH}/train/C2")
    
    for idx,name in enumerate(file_names):
            
        src = os.path.join(file_path, name)
        dst = str(name).replace('batch_', '')
        dst = str(dst[4:])
        dst = os.path.join(file_path, dst)
        number = randrange(1,1000)
        if len(dst) == 39:
            new_name = os.path.join(file_path, '0' +str(number)+ os.path.basename(dst))
            print(new_name)
            os.rename(src, new_name)
        else:
            new_name = os.path.join(file_path, '00'+ str(number)+ os.path.basename(dst))
            print(new_name)
            os.rename(src, new_name)
                
                
                
def C2(dataset_type = 'train', percentage = 0.3):          
    file_path = f"{DATASET_PATH}/train/C2"
    file_names =os.listdir(f"{DATASET_PATH}/train/C2")
    train_dataset, test_dataset = train_test_split(file_names, random_state = 999, 
                                                    shuffle = True, test_size = percentage)
    datasets = {'train' : train_dataset, 'test' : test_dataset}
    for odx, file_name in enumerate(datasets[dataset_type], 1):

        shutil.copy2(f'{file_path}/{file_name}',f'{SAVE_PATH}/Orientation/{dataset_type}/Parallel/{file_name}')
        shutil.copy2(f'{file_path}/{file_name}',f'{SAVE_PATH}/Shape/{dataset_type}/Round_to_oval/{file_name}')
        shutil.copy2(f'{file_path}/{file_name}',f'{SAVE_PATH}/Margin/{dataset_type}/Smooth/{file_name}')
        shutil.copy2(f'{file_path}/{file_name}',f'{SAVE_PATH}/Calcification/{dataset_type}/absent/{file_name}')


renameC2()  
C2()
C2(dataset_type = 'test')


def K_split(path):
    klist = os.listdir(path)

    for k in klist:
        full_name = os.path.join(path + '/',k)

        label_name = full_name.split(os.path.sep)[-2]
        file_name = full_name.split(os.path.sep)[-1]

        #os.makedirs(f'{SAVE_PATH}/Original_classifcation/train/{label_name}', exist_ok = True)
        os.makedirs(f'{SAVE_PATH}/Original_classifcation/train/{label_name}', exist_ok = True)

        #shutil.copy2(f'{DATASET_PATH}/train/{label_name}/{file_name}',f'{SAVE_PATH}/Original_classifcation/train/{label_name}/{file_name}')
        shutil.copy2(f'{DATASET_PATH}/train/{label_name}/{file_name}',f'{SAVE_PATH}/Original_classifcation/train/{label_name}/{file_name}')

        #print(f'{DATASET_PATH}/train/{label_name}/{file_name} ==> {SAVE_PATH}/Original_classifcation/train/{label_name}/{file_name}')
        print(f'{DATASET_PATH}/train/{label_name}/{file_name} ==> {SAVE_PATH}/Original_classifcation/train/{label_name}/{file_name}\n\n')



grade = ['C2','C3','C4','C5']
for g in grade:
    K_split(f'{DATASET_PATH}/train/{g}')
    
