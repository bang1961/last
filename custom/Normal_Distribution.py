from imutils.paths import list_images
from collections import Counter
import os


ROOT_PATH = '/home/super/projects/thyroid/classification/onebone/model_Image'

def Normal_Distribution(path):
    for p in os.listdir(path):
        x = f'{ROOT_PATH}/{p}/train'
        
        ## 특성/train 폴더에 있는 데이터들 불러오기
        image_paths = sorted(list_images(x))
        
        ## 데이터 중에서 라벨만 가져오는 부분
        labels      = [lb.split(os.path.sep)[-2] for lb in image_paths]
        
        ## Counter | 리스트 안에 있는 요소별 갯수를 구해주는 함수
        ## 라벨별 갯수를 구해주는 부분
        lb_count    = Counter(labels)

        print(f'label : {p}')
        for k, v in lb_count.items(): print(f'{k} ==> {v} ({v * 100/ sum(lb_count.values()):.3f} %)')
        print('\n')

Normal_Distribution(ROOT_PATH)      