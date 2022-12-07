# last
2021.04~
프로젝트 별 유용한 코드 및 실용코드입니다
1. custom ---- 유용/실용코드
  || custom/central_fraction.py : 갑상선 학습을 위해 스칼라를 활용하여, 전처리한 코드
  ||
  || custom/custom_detect_test.py : 웹 프레임워크 AI서빙용 더미이미지 생성 및 테스트
  ||
  || custom/Dataset_classification.py : 날짜별 데이터셋을 Train,test,validation 의 일정비율로 복사
  ||
  || custom/len_Folder.py : 해당경로를 기점으로 이미지가 존재하는 폴더의 모든 이미지 개수를 출력
  ||
  || custom/Normal_Distribution.py : 특성별로 개수와 데이터편향을 확인할 수 있음
  ||
  || custom/numpy_to_histogram.py : 히스토그램 정규화 변환
  ||
  || custom/Sagittal_classifi.py : 날짜별데이터셋을 타 폴더로 옮겨줌 '/',split[-3]기준
  ||
  || custom/Split_datasets.py : 전체데이터셋 기준 비율에 맞춰 학습셋팅해줌 ex) total/totals-> Train,test,validation datasets for ratio

2. prepro ---- 전처리(사용법.txt 필독)
  || prepro/AUCTEST.py : 민감도, 특이도, PPV, NPV, f1score AUC 출력
  ||
  || prepro/C2nk_Tirads.py : C2는 라벨이 다르기 때문에 따로 처리할 필요가 있음 C2용 Manage_custom.py
  ||
  || prepro/Manage_custom.py : C3~C5 별로 라벨링 및 폴더 분류
  || 
  || prepro/Manage_custom_v2.py : Manage_custom.py + C2nk_Tirads.py


데이터가 왔을 때의 순서

1. 폴더 분류

1-1 서버에 업로드해야함 업로드는 /home/super/projects/thyroid/datasets에 원본데이터(total), 알집형태의 데이터(zips), Axial크롭이미지(Axial), 전체크롭이미지(cropped)를 업로드함.
    /media/super/Backup/dataset/thyroid/thyroid/datasets(백업폴더)에도 업로드함
    초기 크롭이미지의 이름은 :"사본 -1_1.jpg"등의 형태가 되어야함

1-2  Manage_custom_v2.py로 DATASET_PATH,SAVE_PATH에 분류된 Axial이미지의 경로와 저장경로를 설정하여 실행함.


2. 성능지표

2-1 이미지 전처리
    위의 폴더 분류를 하면 (기존경로의 데이터셋, K-TIRADS 데이터셋, 특성분류 데이터셋) 총 3개의 폴더로 나뉨.
    기존경로의 데이터셋에 central_fraction.py를 사용하여, 전처리함.
2-2 성능지표 결과
    AUC_TEST.py 에 데이터셋 경로와 모델경로를 설정하고 실행하여 성능지표 출력.

3. K-TIRADS 및 특성분류 모델생성
3-1 학습데이터셋 업로드
    Split_datasets.py 함수 실행하여 데이터셋 일정비율로 넣고 실행하여 전처리된 이미지를 학습데이터셋에 분류함
    Dataset_classification.py 를 사용하면 날짜별로 모든데이터셋을 K-TIRADS로 나눠줄수 있음
3-2 학습
    Train_K-TIRADS에 경로를 기입하여 현재날짜 모델 업데이트