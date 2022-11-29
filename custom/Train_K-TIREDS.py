##### 학습 모델 알고리즘 #####
from keras_preprocessing.image.utils import img_to_array
from numpy.lib.function_base import average
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img 
from tensorflow import keras
from tensorflow.keras import applications, models, layers,optimizers
#from datetime import datetime
import matplotlib.pyplot as plt
import glob
import tensorflow.keras.callbacks
from tensorflow.python.keras import callbacks
from tensorflow.keras.callbacks import ReduceLROnPlateau
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.preprocessing.image_dataset import load_image
from tensorflow.python.ops.gen_batch_ops import batch
from tensorflow.keras.applications.resnet import ResNet101
from tensorflow.keras.applications.densenet import DenseNet169
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_resnet_v2 import InceptionResNetV2
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import plot_model
from imutils import paths
from sklearn.model_selection import train_test_split
import tensorflow.keras.callbacks
from tensorflow.python.keras import callbacks
from tensorflow.keras.callbacks import ReduceLROnPlateau
import math
import datetime,os
from UTIL import config
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True 
sess = tf.compat.v1.Session(config=config)

today = datetime.date.today()
month= str(today.month).zfill(2)
day= str(today.day).zfill(2)

ROOT_PATH = '/home/super/301.Personal_Folder/01.bang'

TARGET_SIZE = (299,299)
BATCH_SIZE = 32
INPUT_SHAPE = (299, 299, 3)
SEED = 1024

epoch = 50 

train_len = (len(glob.glob(f'{ROOT_PATH}/Axial_central/train/*/*')))
val_len = (len(glob.glob(f'{ROOT_PATH}/Axial_central/val/*/*'))) 
train_dir = f'{ROOT_PATH}/Axial_central/train'
val_dir = f'{ROOT_PATH}/Axial_central/val'
print(f'{ROOT_PATH}/model/h5/{today.year}/{month}/{day}')

os.makedirs(f'{ROOT_PATH}/model/weight/{today.year}/{month}/{day}', exist_ok=True)
os.makedirs(f'{ROOT_PATH}/model/h5/{today.year}/{month}/{day}', exist_ok=True)
os.makedirs(f'{ROOT_PATH}/model/Result/{today.year}/{month}/{day}', exist_ok=True)


train_ds = tf.keras.preprocessing.image_dataset_from_directory(
                 train_dir,
                 seed=SEED,
                 labels="inferred",
                 class_names=None,
                 shuffle=True,
                 image_size = TARGET_SIZE,
                 batch_size = BATCH_SIZE,                      
                 label_mode = 'categorical')

validation_ds = tf.keras.preprocessing.image_dataset_from_directory(
                 val_dir,
                 seed=SEED,                 
                 labels="inferred",
                 class_names=None,
                 shuffle=True,
                 image_size = TARGET_SIZE,
                 batch_size = BATCH_SIZE,
                 label_mode = 'categorical')

# 라벨 갯수
classes = train_ds.class_names
#======================InceptionV3==========================
base_model =InceptionV3(input_shape = INPUT_SHAPE,
                        weights='imagenet', include_top=False)
#base_model.trainable = False

initial_learning_rate = 5e-4
decay = initial_learning_rate / epoch

def lr_time_based_decay(epoch,lr):

        return lr * 1/ (1 + decay * epoch)

def lr_exp_decay(epoch, lr):
    k = 0.1
    return initial_learning_rate * math.exp(-k*epoch)
    
def make_model(INPUT_SHAPE, num_classes):
    regulizer = tf.keras.regularizers.L2(0.001)
    inputs = tf.keras.Input(shape=INPUT_SHAPE)
    x = layers.experimental.preprocessing.Rescaling(1.0 / 255)(inputs)
    x = base_model(x)
    #x = layers.Activation("relu")(x)
    x = layers.Dropout(0.35)(x)
    x = layers.GlobalAveragePooling2D()(x) 
    x = layers.Dropout(0.35)(x)
    outputs = layers.Dense(num_classes, activation="softmax",kernel_regularizer='l2')(x)
    
    return tf.keras.Model(inputs, outputs)

print(TARGET_SIZE + (3,))
model = make_model(INPUT_SHAPE=TARGET_SIZE + (3,), num_classes=len(classes))

model.summary()


ok =True

if ok:
    # Parameters
    EPOCHS = epoch
    CALLBACK = [
        tf.keras.callbacks.ModelCheckpoint(filepath=
        f'/{ROOT_PATH}/model/weight/{today.year}/{month}/{day}/callback.' + '{epoch:02d}-{val_loss:.2f}.h5',save_best_only=True),
        tf.keras.callbacks.EarlyStopping(patience=90)
    ]
    
    model.compile(
        optimizer=optimizers.Adam(learning_rate = 5e-4),
        loss="categorical_crossentropy",
        metrics=["categorical_accuracy"],
    )
    
    history = model.fit(
        train_ds,
        epochs          = EPOCHS,
        validation_data = validation_ds,
        callbacks       = [tf.keras.callbacks.LearningRateScheduler(lr_exp_decay, verbose = 1)]
    )
    
else:
    # model = tf.keras.models.load_model('/home/lt4/Result/h5/new_original_classification_bang.h5')
    model = tf.keras.models.load_model(f'/{ROOT_PATH}/model/h5/{today.year}_{month}_{day}_{month}_{day}_Axial.h5')

print(f'{ROOT_PATH}/model/h5/{month}_{day}_{month}_{day}.h5')
model.save(f'/{ROOT_PATH}/model/h5/{today.year}_{month}_{day}_{month}_{day}.h5')
# keras.utils.plot_model(model,"/home/lt4/Result/Image/InceptionV3_Rmsprop.png")

predict = model.predict(validation_ds,steps=None)

print("----------------- Predict -----------------")
output_result = model.predict(
            validation_ds,
            steps = val_len/32)

np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
print(output_result)
results = model.evaluate(validation_ds, batch_size=BATCH_SIZE)

print("----------------- Predict2 -----------------")
print("val_loss, val_acc:", results)

acc = history.history['categorical_accuracy']
val_acc = history.history['val_categorical_accuracy']

loss = history.history['loss'] 
val_loss = history.history['val_loss']

plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.ylabel('Accuracy')
plt.ylim([min(plt.ylim()),1])
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.ylabel('Cross Entropy')
plt.ylim([0,1.0])
plt.title('Training and Validation Loss')
plt.xlabel('epoch')
# plt.savefig("/home/lt4/Result/Image/new_original_classification_bang.png")
plt.savefig(f'/{ROOT_PATH}/model/Result/{today.year}/{month}/{day}/{month}_{day}.png')