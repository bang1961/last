from ast import Or
import os,shutil
from imutils import paths
from UTIL import config
from sklearn.model_selection import train_test_split
import splitfolders

ROOT_PATH = config.ROOT_PATH
ORIGIN_PATH = '/home/super/projects/thyroid/classification/Axail/Original_classifcation/train'
SEED = 1004
LIST_IMAGE = sorted(paths.list_images(ORIGIN_PATH))

splitfolders.ratio(ORIGIN_PATH ,output= '/home/super/bang/Axial', seed =SEED , ratio = (0.7, 0.3, 0.0))
