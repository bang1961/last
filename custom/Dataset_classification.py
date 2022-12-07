import os
from imutils import paths
import shutil
import random
from UTIL import config
import splitfolders

ROOT_PATH = '/home/super/projects/thyroid/datasets'
SEED = 1004
DATE_DATA = f'{ROOT_PATH}/Axial'
total_save_path = f'{ROOT_PATH}/total/totals'

date_path_list = os.listdir(DATE_DATA)

def file_move(idx, image,filepaths,rd):
    label_name = image.split(os.path.sep)[-2]
    file_name = image.split(os.path.sep)[-1]

    name, file_ext = file_name.split('.')[0], file_name.split('.')[1]
    os.makedirs(f'{total_save_path}/{label_name}', exist_ok = True)

    shutil.copy2(filepaths +"/"+ file_name, f'{total_save_path}/{label_name}/{name}{rd}_{idx}_.{file_ext}')
    print(filepaths +"/"+ file_name,"=====>", f'{total_save_path}/{label_name}/{name}{rd}_{idx}_.{file_ext}\n\n')


def classification(output,ratio):
    os.makedirs(output,exist_ok= True)
    for DATE in sorted(date_path_list):
        rd = random.randrange(1,7777)

        for idx, nodule_grade in enumerate(['C2','C3','C4','C5'],0):
            filepaths = f'{DATE_DATA}/{DATE}/{nodule_grade.upper()}'
            image_file_paths = paths.list_images(filepaths)
            
            for idx,image in enumerate(image_file_paths,0):
                file_move(idx,image,filepaths,rd)
                
    splitfolders.ratio(total_save_path ,output= output, seed =SEED , ratio = ratio)

classification('/home/super/301.Personal_Folder/01.bang/backup_python',(0.7, 0.3, 0.0))