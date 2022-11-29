## 이미지 histogram equalization 해주는 부분 AUCTEST시 마무리단계

from imutils import paths
import os, glob, natsort, cv2, shutil
import numpy as np

ROOT_PATH = '/home/super'

DATASET_PATH = f'{ROOT_PATH}/bang/Axial'


C = [2,3,4,5]
for i in C:
    file_path = f"{DATASET_PATH}/val/C{i}"
    file_names =os.listdir(f"{DATASET_PATH}/val/C{i}")
    onlyfiles = natsort.natsorted(file_names)
    images = np.empty(len(onlyfiles), dtype=object)

    for n in range(0,len(onlyfiles)):
            
            images[n] = cv2.imread(os.path.join(file_path, onlyfiles[n]), cv2.IMREAD_COLOR)
            imgray = cv2.cvtColor(images[n],cv2.COLOR_BGR2GRAY)

            img2 = cv2.equalizeHist(imgray)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            img2 = clahe.apply(img2)

            kernel_sharpen = np.array([[-1,-1,-1,-1,-1],[-1,2,2,2,-1],[-1,2,8,2,-1],[-1,2,2,2,-1],[-1,-1,-1,-1,-1]])/8.0
            thresh = cv2.filter2D(img2,-1,kernel_sharpen)
            # cv2.accumulateProduct
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            cv2.imwrite(file_path+f"/{onlyfiles[n]}",img2)