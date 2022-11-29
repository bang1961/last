from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import torchvision
from torchvision import transforms
import cv2
import os
##### 학습 모델 알고리즘 #####
from keras_preprocessing.image.utils import img_to_array
from numpy.lib.function_base import average
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img 
from tensorflow import keras
from tensorflow.keras import applications, models, layers,optimizers
#from datetime import datetime
import matplotlib.pyplot as plt
import glob,os
import shutil
import tensorflow.keras.callbacks
from tensorflow.python.keras import callbacks
from tensorflow.keras.callbacks import ReduceLROnPlateau
import numpy as np
#import tensorflow as tf
from tensorflow.python.keras.preprocessing.image_dataset import load_image
from tensorflow.python.ops.gen_batch_ops import batch
import sys
from tensorflow.keras.applications.resnet import ResNet101
from tensorflow.keras.applications.densenet import DenseNet169
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_resnet_v2 import InceptionResNetV2
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import plot_model
import shutil
from imutils import paths
from sklearn.model_selection import train_test_split
from tensorflow.python.ops import random_ops
from absl import flags
import tensorflow.compat.v1 as tf
from torchvision.utils import save_image
import PIL
from imutils import paths
import matplotlib as cm
ROOT_PATH = '/home/super/301.Personal_Folder/01.bang/22.11.02'

SAVE_PATH = '/home/super/301.Personal_Folder/01.bang/central'


tf.app.flags.DEFINE_float(
    'cb_distortion_range', 0.1, 'Cb distortion range +/-')

tf.app.flags.DEFINE_float(
    'cr_distortion_range', 0.1, 'Cr distortion range +/-')

tf.app.flags.DEFINE_boolean(
    'use_fast_color_distort', True,
    'apply fast color/chroma distortion if True, else apply'
    'brightness/saturation/hue/contrast distortion')

tf.app.flags.DEFINE_float(
    'learning_rate',0.0001, 'learning_rate +/-'
)

FLAGS = tf.app.flags.FLAGS

def preprocess_for_eval(image, height, width, central_fraction=0.975):
  with tf.name_scope('eval_image'):
    image = Image.open(image)
    image = np.array(image)
    if image.dtype != tf.float32:
      image = tf.image.convert_image_dtype(image, dtype=tf.float32)
    image = tf.image.central_crop(image, central_fraction=central_fraction)
    image = tf.expand_dims(image, 0)
    image = tf.compat.v1.image.resize_bilinear(image, [height, width], align_corners=False)
    image = tf.squeeze(image, [0])
    image = tf.subtract(image, 0.5)
    image = tf.multiply(image, 2.0)
    image.set_shape([height, width, 3])
    #image = np.expand_dims(image, axis=0)
    np_arr = image.numpy()
    img = PIL.Image.fromarray((np_arr*255).astype(np.uint8))
    return img



def distort_color_fast(image, scope=None):
  with tf.name_scope('distort_color'):
    br_delta = random_ops.random_uniform([], -32./255., 32./255., seed=None)
    cb_factor = random_ops.random_uniform(
        [], -FLAGS.cb_distortion_range, FLAGS.cb_distortion_range, seed=None)
    cr_factor = random_ops.random_uniform(
        [], -FLAGS.cr_distortion_range, FLAGS.cr_distortion_range, seed=None)


    channels = tf.split(axis=2, num_or_size_splits=3, value=image)
    red_offset = 1.402 * cr_factor + br_delta
    green_offset = -0.344136 * cb_factor - 0.714136 * cr_factor + br_delta
    blue_offset = 1.772 * cb_factor + br_delta
    channels[0] += red_offset
    channels[1] += green_offset
    channels[2] += blue_offset
    image = tf.concat(axis=2, values=channels)
    image = tf.clip_by_value(image, 0., 1.)
    np_arr = image.numpy()
    img = PIL.Image.fromarray((np_arr*255).astype(np.uint8))
    
    return img


for idx, i in enumerate(paths.list_images(ROOT_PATH),0):
    #print("문제찾기",i)
    
    img     = (preprocess_for_eval(i,299,299))
    image   = i.split(os.path.sep)[-1]
    label   = i.split(os.path.sep)[-2]
    Datatype = i.split(os.path.sep)[-3]
    os.makedirs(f'{SAVE_PATH}/{Datatype}/{label}', exist_ok = True)
    img.save(f'{SAVE_PATH}/{Datatype}/{label}/{image}')
    print(f'{idx} 번째 --> {i} 이미지저장')


# def image_to_np(path,grade,central_fraction=0.96):
#     print(f"{SAVE_PATH}/{grade}")
#     os.makedirs(f"{SAVE_PATH}/{grade}", exist_ok = True)
#     image_np = sorted(os.listdir(path))
#     for idx,image_to in enumerate(image_np):
#         basename = image_to
#         image_to = Image.open(f'{ROOT_PATH}/{grade}/{image_to}')
#         _np = np.array(image_to)
#         image_height, image_width, image_channel = _np.shape
#         if central_fraction:
#             bbox_start_h = int(image_height * (1 - central_fraction)/2)
#             bbox_end_h = int(image_height - bbox_start_h)
#             bbox_start_w = int(image_width * (1 - central_fraction)/2)
#             bbox_end_w = int(image_width - bbox_start_w)
#             _np = _np[bbox_start_h:bbox_end_h, bbox_start_w:bbox_end_w]
        
#         cv2.imwrite(f"{SAVE_PATH}/{grade}/{basename}",_np)
        
#     return _np

# for grade in ['C2','C3','C4','C5']:
#     image_to_np(f'/home/super/bang/Datasets/train/{grade}',grade)