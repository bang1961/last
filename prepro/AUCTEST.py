##### 양성/음성 예측도 #####
from tensorflow.keras.models import load_model
from tensorflow.keras import optimizers
from scipy.stats import chisquare
import matplotlib.pyplot as plt
from sklearn import metrics
from numpy import linspace
from imutils import paths
from numpy import argmax
import tensorflow as tf
import numpy as np
import cv2, os
import shutil
# /home/super/projects/thyroid/datasets/cropped/22.09.01
ROOT_PATH = '/home/super/301.Personal_Folder/01.bang'
DATASET_PATH = f'{ROOT_PATH}/Axial_central/val'
print(DATASET_PATH)

MODEL_PATH = f'{ROOT_PATH}/model/h5/2022_11_28_11_28.h5'
#MODEL_PATH = f'{ROOT_PATH}/projects/thyroid/WebPlatform/lt4/models/k-tirads.h5'
class_names = ["C2", "C3", "C4", "C5"]
#class_names = ["C","Pc","Ps","S"]
TPR, FPR, LIST = [], [], []
TP= FN = TN = FP = 1
LR =  0.00005
ground_truth, predicted, scores = [], [], []

image_paths = sorted(paths.list_images(DATASET_PATH))
model = load_model(MODEL_PATH)  #학습모델 load

#load한 model compile
# model.compile(loss='categorical_crossentropy',
#               optimizer=optimizers.Adam(lr = LR),
#               metrics=['accuracy'])

# model.summary()

for idx, image_path in enumerate(image_paths):

    print(f'[{idx}] - {image_path}')
    # file_name = image_path.split(os.path.sep)[-1]
    # ground_truth_label = f'C{image_path[66]}'
    ground_truth_label = image_path.split(os.path.sep)[-2]

    conf_ground_truth_label = 1 if ground_truth_label in ['C2', 'C3'] else 0
    ground_truth.append(conf_ground_truth_label)
    
    image = cv2.imread(image_path)
    image = cv2.resize(image,(299,299))
    image = np.reshape(image,[1,299,299,3])

    predicted_scores = model.predict(image)
    predicted_idx = np.argmax(predicted_scores, axis = -1)[0]
    predicted_label = class_names[predicted_idx]
    conf_predicted_label = 1 if predicted_label in ['C2', 'C3'] else 0

    predicted_proba = predicted_scores[0][predicted_idx]
    predicted.append(conf_predicted_label)

    print(f'실제 라벨 : {conf_ground_truth_label} \n검증 라벨 : {conf_predicted_label}\n검증 점수 : {predicted_proba:.2f}\n')


confusion_mat = metrics.confusion_matrix(ground_truth, predicted)
TP, FP = confusion_mat[0][0], confusion_mat[0][1]
FN, TN = confusion_mat[1][0], confusion_mat[1][1]

print(f'민감도 : {TP/(TP+FN)*100:.2f} 특이도 : {TN / (FP + TN)*100:.2f}\nPPV : {TP / (TP + FP)*100:.2f} NPV : {TN / (FN + TN)*100:.2f}\n\n\n')
print('classification report\n', metrics.classification_report(ground_truth, predicted))
print(f'AUC score : {metrics.roc_auc_score(ground_truth, predicted)*100}')
print(confusion_mat)