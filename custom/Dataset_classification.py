import os
from imutils import paths
import shutil
import random
ROOT_PATH = '/home/super/projects/thyroid/datasets'

DATE_DATA = f'{ROOT_PATH}/Axial'
save_path = f'{ROOT_PATH}/total/totals'
DATE_PATH = os.listdir(DATE_DATA)
def file_move(DATE, image, dataset_type = 'train', percentage = 0.3):
    image = image
    label_name = image.split(os.path.sep)[-2]
    file_name = image.split(os.path.sep)[-1]
    name, file_ext = file_name.split('.')[0], file_name.split('.')[1]
    os.makedirs(f'{save_path}/{label_name}', exist_ok = True)
    [os.makedirs(f'{save_path}/{label_name}', exist_ok = True) for dataset_type in ['train', 'valid']]
    #print(f'[{dataset_type}-{idx}]. {filepaths}')
    shutil.copy2(filepaths +"/"+ file_name, f'{save_path}/{label_name}/{name}{rd}_{idx}_.{file_ext}')
    print(filepaths +"/"+ file_name,"=====>", f'{save_path}/{label_name}/{name}{rd}_{idx}_.{file_ext}\n\n')


for DATE in sorted(DATE_PATH):
    rd = random.randrange(1,7777)

    for idx, nodule_grade in enumerate(['C2','C3','C4','C5'],0):
        filepaths = f'{DATE_DATA}/{DATE}/{nodule_grade.upper()}'
        image_file_paths = paths.list_images(filepaths)
        
        for idx,image in enumerate(image_file_paths,0):
            file_move(idx,image)
            