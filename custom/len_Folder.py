import os 
from imutils import paths

ROOT_PATH = '/home/super/projects/thyroid/datasets/Axial'

image_list = os.listdir(ROOT_PATH)

images_list = []

label = ['C2','C3','C4','C5']

def lenlist(labels):

    for images in sorted(image_list):
        images = f'{ROOT_PATH}/{images}/{labels}'
        image = paths.list_images(images)
        ll = []
        cnt =0
        for im in image:
            ll.append(im)
            cnt += len(ll)
        print(f'{images} 이미지의 개수는  {len(ll)}개 입니다\n\n')
        
    print(f"총이미지개수 {cnt}개")
        

for labels in label:
    lenlist(labels)