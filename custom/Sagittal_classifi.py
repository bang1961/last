import os
from imutils.paths import list_images
import shutil
ROOT_PATH = '/home/super/projects/thyroid/datasets/cropped/22.04.22'

def Sagittal_class(path):
    for p in os.listdir(path):
        
        x = f'{ROOT_PATH}/{p}'
        
        image_paths = sorted(list_images(x))
        for sagittal in image_paths:
            label_name = sagittal.split(os.path.sep)[-2]
            file_name = sagittal.split(os.path.sep)[-1]
            os.makedirs(f'/home/super/projects/thyroid/datasets/Axial/22.04.22/{label_name}', exist_ok = True)
            
            if sagittal.split('__')[1] == '1_.jpg' or sagittal.split('__')[1] =='2_.jpg':
                print(f'{x}/{file_name} =>>/home/super/projects/thyroid/datasets/Axial/22.04.22/{label_name}/{file_name}')
                shutil.copy2(f'{x}/{file_name}',f'/home/super/projects/thyroid/datasets/횡단만/22.04.22/{label_name}/{file_name}')

Sagittal_class(ROOT_PATH)