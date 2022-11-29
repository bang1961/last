from sklearn.model_selection import train_test_split

from collections import Counter
from datetime import datetime
import os, glob, natsort, cv2
from imutils import paths
import pandas as pd
import numpy as np
import shutil
from random import *
import tensorflow as tf
from sklearn.metrics import classification_report
from tensorflow.keras.utils import to_categorical

from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.applications.inception_v3 import InceptionV3
import keras
import tensorflow.keras.callbacks
from tensorflow.python.keras import callbacks
from tensorflow.keras.callbacks import ReduceLROnPlateau
from keras.applications.inception_v3 import preprocess_input
from tensorflow.keras import applications, models, layers,optimizers

from tensorflow.keras.preprocessing.image import ImageDataGenerator

Root_Path = '/home/super/bang/Datasets'
SEED = 999
TARGET_SIZE = (299,299)
BATCH_SIZE = 32
INPUT_SHAPE = (299, 299, 3)
SEED = 1024
num_classes=4
EPOCHS = 50

def mk_dataset(dataset_path):
    image_paths = sorted(paths.list_images(dataset_path))
    images, labels = [], []

    for idx, image_path in enumerate(image_paths, 1):

        #rint(f'\n\n[{idx}] {image_path}')
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, TARGET_SIZE)

        label = image_path.split(os.path.sep)[-2]
        images.append(image)
        labels.append(label)

    images = np.array(images)
    labels = np.array(labels)

    images = images / 255.
    
    lb = LabelEncoder()
    labels = lb.fit_transform(labels)
    labels = to_categorical(labels)

    #print(f'\n\n {lb.classes_} \n\n')
    (train_image, test_image, train_label, test_label) = train_test_split(images, labels, test_size = 0.3, 
                                                                        shuffle = True, stratify = labels, random_state = SEED)

    return (train_image,train_label), (test_image, test_label)


(dataset_tr, label_tr), (dataset_val, label_val) = mk_dataset(Root_Path)



base_model =InceptionV3(input_shape = INPUT_SHAPE,
                        weights='imagenet', include_top=False)

base_model.trainable = False
preprocess_input = keras.applications.inception_v3.preprocess_input

trainAug = ImageDataGenerator(
	rotation_range=0,
	zoom_range=0.0,
	width_shift_range=0.0,
	height_shift_range=0.0,
	shear_range=0.0,
	horizontal_flip=False,
	fill_mode="nearest")

valAug = ImageDataGenerator()

def make_model(INPUT_SHAPE, num_classes):
    regulizer = tf.keras.regularizers.l2(0.001)
    inputs = tf.keras.Input(shape=INPUT_SHAPE)
    x = layers.experimental.preprocessing.Rescaling(1.0 / 255)(inputs)
    x = base_model(x)
    #x = layers.Activation("relu")(x)
    x = layers.Dropout(0.4)(x)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.4)(x)
    outputs = layers.Dense(num_classes, activation="softmax", kernel_regularizer=regulizer)(x)
    
    return tf.keras.Model(inputs, outputs)

print(TARGET_SIZE + (3,))
model = make_model(INPUT_SHAPE=TARGET_SIZE + (3,), num_classes=num_classes)


def model_compile():
    CALLBACK = [
        tf.keras.callbacks.ModelCheckpoint(filepath=
        '/home/super/bang/model/weight/new_original_classification_adan.{epoch:02d}-{val_loss:.2f}.h5',save_best_only=True),
        tf.keras.callbacks.EarlyStopping(patience=90)
    ]

    model.compile(
        optimizer=optimizers.Adam(learning_rate = 5e-5),
        loss="categorical_crossentropy",
        metrics=["categorical_accuracy"],
    )

    history = model.fit(
    x = trainAug.flow(dataset_tr, label_tr, batch_size = BATCH_SIZE),
    steps_per_epoch=len(dataset_tr) // BATCH_SIZE,
    validation_data = valAug.flow(dataset_val, label_val),
    validation_steps = len(dataset_val) // BATCH_SIZE,
    epochs = EPOCHS
    )

model_compile()
# model.save('/home/lt4/Result/h5/new_original_classification_bang.h5')
model.save('/home/super/bang/model/h5/new_original_classification_adam.h5')
#keras.utils.plot_model(model,"/home/lt4/Result/Image/InceptionV3_Rmsprop.png")

predict = model.predict(dataset_val,steps=None)

print("----------------- Predict -----------------")
output_result = model.predict(
            test_ds,
            steps = test_len/32)