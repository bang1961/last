# last
2021.04~
프로젝트 별 유용한 코드 및 실용코드입니다
/custom ---- 유용/실용코드
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
/prepro ---- 전처리(사용법.txt 필독)
  || prepro/AUCTEST.py : 민감도, 특이도, PPV, NPV, f1score AUC 출력
  ||
  || prepro/C2nk_Tireds.py : C2는 라벨이 다르기 때문에 따로 처리할 필요가 있음 C2용 Manage_custom.py
  ||
  || prepro/Manage_custom.py : C3~C5 엑셀파일 별로 