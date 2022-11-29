import cv2, os
import numpy as np
from natsort import natsort
from imutils.paths import list_images

DATASET_PATH = "/home/super/projects/thyroid/classification/Axail/Original_classifcation"

def histogram(path):
    image_paths = sorted(list_images(path))
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

    for idx,image_path in enumerate(image_paths,1):
        print(f'{idx}-{image_path}')
        label = image_path.split(os.path.sep)[-2]
        file_names = image_path.split(os.path.sep)[-1]
        os.makedirs(f'/home/super/bang/Datasets/{label}', exist_ok =True)

        images = cv2.imread(image_path,cv2.IMREAD_COLOR)
        imgray = cv2.cvtColor(images,cv2.COLOR_BGR2GRAY)
        image_equal = cv2.equalizeHist(imgray)
        image_clahe = clahe.apply(image_equal)

        image_Blur = cv2.medianBlur(image_clahe,3)
        img = cv2.resize(image_Blur, (299,299), cv2.INTER_AREA)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.imwrite(f'/home/super/bang/Datasets/{label}/{file_names}',img)


histogram(DATASET_PATH)



