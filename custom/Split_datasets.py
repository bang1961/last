from ast import Or
import os,shutil
from imutils import paths
from UTIL import config
from sklearn.model_selection import train_test_split
import splitfolders

ROOT_PATH = config.ROOT_PATH
ORIGIN_PATH = '/home/super/301.Personal_Folder/01.bang/22.11.02/train'
SEED = 1004
LIST_IMAGE = sorted(paths.list_images(ORIGIN_PATH))
OUTPUT = '/home/super/301.Personal_Folder/01.bang/Axial'
[os.makedirs('/'.join(OUTPUT,SET), exist_ok= True) for SET in ['train','test','val']]
splitfolders.ratio(ORIGIN_PATH ,output= OUTPUT, seed =SEED , ratio = (0.7, 0.2, 0.1))