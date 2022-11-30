from yolov5.utils.general import (check_img_size, non_max_suppression, scale_coords, xywh2xyxy, xyxy2xywh,  clip_coords, increment_path)
from tensorflow.keras.models import load_model
from yolov5.utils.plots import Annotator, colors
from yolov5.utils.datasets import LoadImages
from imutils.paths import list_images
from pathlib import Path
from UTIL import config
import numpy as np
import traceback
import datetime
import cv2, os
import torch
import json
import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
    # Memory growth must be set before GPUs have been initialized
        print(e)


## 필요 설정 값
TODAY = datetime.date.today()
YEAR = TODAY.year
MONTH= str(TODAY.month).zfill(2)
DAY= str(TODAY.day).zfill(2)

ROOT_PATH = config.ROOT_PATH
label_dict = {
    'k-tirads' : {0 : 'C2', 1 : 'C3', 2 : 'C4', 3 : 'C5'},
    'internal content' : {0 : 'Solid', 1 : 'Predominantly_solid'},
    'echogenicity' : {0 : 'Hyperechogenicity', 1 : 'Hypoechogenicity', 2 : 'Isoechogenicity'},
    'shape' : {0 : 'Round_to_oval', 1 : 'Irregular'}, 
    'orientation' : {0 : 'Parallel', 1 : 'NonParallel'},
    'margin' : {0 : 'Ill-defined', 1 : 'Smooth', 2 : 'Spiculated_microlobulated'},
    'calcification' : {0 : 'absent', 1 : 'Microcalcification', 2 : 'Macrocalcification'},
    'spongiform' : {0 : 'absent', 1 : 'present'}, 
    'internal content2' : {0 : 'Benign', 1 : 'Colloid', 2 : 'Spongiform'}}


## 분류모델 로딩하는 함수
def classi_model_load():
    print('K-TIRADS 분류 모델 로딩중 입니다.')
    k_model = load_model(f'{ROOT_PATH}/models/2022_10_21_10_21.h5')

    print('Echogenicity 분류 모델 로딩중 입니다.')
    e_model = load_model(f'{ROOT_PATH}/models/echogenicity.h5')

    print('Margin 분류 모델 로딩중 입니다.')
    m_model = load_model(f'{ROOT_PATH}/models/margin.h5')

    print('sponfiform 분류 모델 로딩중 입니다.')
    s_model = load_model(f'{ROOT_PATH}/models/spongiform.h5')

    print('orientation 분류 모델 로딩중 입니다.')
    o_model = load_model(f'{ROOT_PATH}/models/orientation.h5')

    print('calcification 분류 모델 로딩중 입니다.')
    c_model = load_model(f'{ROOT_PATH}/models/calcification.h5')

    print('shape 분류 모델 로딩중 입니다.')
    h_model = load_model(f'{ROOT_PATH}/models/shape.h5')

    print('internal content 분류 모델 로딩중 입니다.')
    i_model = load_model(f'{ROOT_PATH}/models/internal.h5')

    print('internal content C2 분류 모델 로딩중 입니다.')
    i2_model = load_model(f'{ROOT_PATH}/models/C2_internal.h5')
    ## 모델 로딩 후 첫 번째 검증에 시간이 가장 오래 걸려 numpy에서 더미 이미지를 생성해 첫 검증 수행

    print('분류 모델 첫 번째 검증 중입니다.')
    dummy_image = np.zeros((299, 299, 3), dtype = np.uint8)
    orientation_image = cv2.cvtColor(dummy_image,cv2.COLOR_BGR2GRAY)
    dummy_image = np.expand_dims(dummy_image, axis = 0)

    ori_median = cv2.medianBlur(orientation_image,3)
    ori_img = cv2.cvtColor(ori_median, cv2.COLOR_GRAY2BGR)
    ori_img = np.expand_dims(ori_img, axis=0)

    k_model.predict(dummy_image)
    e_model.predict(dummy_image)
    m_model.predict(dummy_image)
    s_model.predict(dummy_image)
    o_model.predict(ori_img)
    c_model.predict(dummy_image)
    h_model.predict(dummy_image)
    i_model.predict(dummy_image)
    i2_model.predict(dummy_image)
    print('분류 모델 로딩이 완료 되었습니다.')
    return k_model, e_model, m_model,s_model, o_model, c_model, h_model, i_model, i2_model


k_model, e_model, m_model, s_model, o_model, c_model, h_model, i_model, i2_model = classi_model_load()

## 분류 모델에 입력 전 전처리 해주는 함수
def preprocessing(image, save_path):

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_gray  = cv2.equalizeHist(image_gray)

    clahe = cv2.createCLAHE(clipLimit = 2.0, tileGridSize=(8, 8))
    image_gray = clahe.apply(image_gray)

    image_gray = cv2.cvtColor(image_gray, cv2.COLOR_BGR2RGB)
    cv2.imwrite(save_path, image_gray)

    print('전처리 된 이미지가 저장되었습니다.')
    return image_gray


## 분류 모델 검증을 실행하는 함수
def classification(image):
    try:
        print(f'입력 받은 데이터 셋 : {image.shape}')

        ori = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (299, 299))
        ori = cv2.resize(ori, (299,299))
        ori_blur = cv2.medianBlur(ori, 3)
        ori_img = cv2.cvtColor(ori_blur, cv2.COLOR_GRAY2BGR)
        image = np.expand_dims(image, axis=0)
        ori_img =np.expand_dims(ori_img,axis=0)
        print('분류모델 검증 중 입니다.')
        pred_k = k_model.predict(image)
        pred_m = m_model.predict(image)
        pred_e = e_model.predict(image)
        pred_s = s_model.predict(image)
        pred_o = o_model.predict(ori_img)
        pred_h = h_model.predict(image)
        pred_i2 = i2_model.predict(image)
        ## calcification과 internal_content는 학습 진행할때 이미지를 정규화하여 진행시킴.
        image = image / 255.
        pred_c = c_model.predict(image)
        pred_i = i_model.predict(image)

        print('분류모델 검증 완료 되었습니다. \n')

        return pred_k, pred_e, pred_m, pred_s, pred_o, pred_c, pred_h, pred_i, pred_i2

    except Exception as e:
        ERR  = f'[ERR] 에러 발생 - {e} \n디테일 : {traceback.format_exc()}'
        config.log_writer(ERR)


## 검사 결과를 json 및 text 파일로 저장해주는 함수
def save_result(results, **kwargs):
        np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
        
        try:
            ## 인자값을 너무 많이 받으면 코드가 지저분해 질 것 같아 kwargs로 딕셔너리 형태로 받아오도록 함. (357번째 라인 참조 / kwargs 변수 선언 부분)
            ##                   index : 검증 결과  저장 인덱스 값 (결과 텍스트 파일 저장하는 과정에서 문제가 있어 사용)
            ##               file_name : 이미지 이름
            ##               visit_date : 방문 날짜
            ##              patient_id : 환자 id 
            ##         detected_path : 바운딩 박스가 그려진 이미지가 저장된 경로
            ##  nodule_image_path : 결절이 크롭된 이미지가 저장된 경로
            ## original_image_path : 입력받은 원본 이미지 경로
            
            index               = kwargs['index']
            file_name           = kwargs['file_name']
            visit_date          = kwargs['visit_date']
            original_image_path = kwargs['original_image_path']
            detected_path       = kwargs['detected_image_path']
            nodule_image_path   = kwargs['nodule_image_path']
            patient_id          = kwargs['patient_id']
            json_save_path      = kwargs['json_path']
            width, height       = kwargs['width'], kwargs['height']
            print("input save_result1")
        except Exception as e:
            ERR = f'[ERR] 인자값으로 전달 받지 못한 값이 있습니다. - {e} \n자세한 내용 : {traceback.format_exc()}'
            config.log_writer(ERR)
            index               = None
            file_name           = None
            visit_date          = None
            detected_path       = None
            nodule_image_path   = None
            original_image_path = None
            width, height       = 0, 0

        try:
            print("Axial 이미지에 결절이 있을때 두번째 과정")
            pred_k, pred_e, pred_m, pred_s, pred_o, pred_c, pred_h, pred_i, pred_i2 = results
            json_file = {"patient id" : patient_id, "visit date" : visit_date,
                            "original image path" : original_image_path,
                            "inspection image path" : detected_path,
                            "model complete" : "complete",
                            "result" : {}}

            predictions = zip(pred_k, pred_e, pred_m, pred_s, pred_o, pred_c, pred_h, pred_i, pred_i2)
            
            ## json 과 text로 반환하는 부분
            #! 반복문에서는 변수 이름을 겹쳐 사용하지 않는게 좋아요 !#
            for odx, (result_k, result_e, result_m, result_s, result_o, result_c, result_h, result_i, result_i2) in enumerate(predictions):
                pre_ans1 = result_k.argmax()
                pre_ans2 = result_e.argmax()
                pre_ans3 = result_m.argmax()
                pre_ans4 = result_s.argmax()
                pre_ans5 = result_o.argmax()
                pre_ans6 = result_c.argmax()
                pre_ans7 = result_h.argmax()
                pre_ans8 = result_i.argmax()
                pre_ans9 = result_i2.argmax()

                result_text = ''
                k_tirads_label = ''
                echo_label = ''
                margin_label = ''
                spongiform_label = ''
                orientation_label = ''
                calcification_label = ''
                shape_label = ''
                internal_label = ''
                internal2_label = ''


                try:
                    k_tirads_label = label_dict['k-tirads'][pre_ans1]
                    echo_label = label_dict['echogenicity'][pre_ans2]
                    margin_label = label_dict['margin'][pre_ans3]
                    spongiform_label = label_dict['spongiform'][pre_ans4]
                    orientation_label = label_dict['orientation'][pre_ans5]
                    calcification_label = label_dict['calcification'][pre_ans6]
                    shape_label = label_dict['shape'][pre_ans7]
                    internal_label = label_dict['internal content'][pre_ans8]
                    internal2_label = label_dict['internal content2'][pre_ans9]
                    
                    ## 0 ~ 1 사이의 값 중에서 랜덤하게 생성
                    dummy_score   = np.random.random_sample()

                    ## 하나는 랜덤하게 생성된 값으로, 다른 하나는 1에서 생성된 값을 뺀 값으로 생성
                    ## e.g | 랜덤하게 생성된 값 : 0.275 -> 다른 하나의 값 : 0.725
                    max_o, min_o  = sorted([dummy_score, 1 - dummy_score], reverse = True)

                    ## 가로가 세로 길이보다 길다면 Parallel 점수가 크게, 반대인 경우 Non-Parallel 점수가 크게
                    orientation   = [max_o, min_o] if width > height else [min_o, max_o]
                    orientation   = f'[{orientation[0]:.3f} {orientation[1]:.3f}]'

                except KeyError as ke:
                    ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
                    config.log_writer('라벨 정보가 존재하지 않습니다. - {ke}')
                    print(f'라벨 정보가 존재하지 않습니다 . {ke}')

                result_text += f'nodule name : {odx}, percent : {pred_k[odx]}, label_name : {k_tirads_label} \n'
                result_text += f'nodule name : {odx}, percent : {pred_e[odx]}, label_name : {echo_label} \n'
                result_text += f'nodule name : {odx}, percent : {pred_m[odx]}, label_name : {margin_label} \n'
                result_text += f'nodule name : {odx}, percent : {pred_s[odx]}, label_name : {spongiform_label} \n'
                result_text += f'nodule name : {odx}, percent : {orientation}, label_name : {orientation_label} \n'
                result_text += f'nodule name : {odx}, percent : {pred_c[odx]}, label_name : {calcification_label} \n'
                result_text += f'nodule name : {odx}, percent : {pred_h[odx]}, label_name : {shape_label} \n'
                result_text += f'nodule name : {odx}, percent : {pred_i[odx]}, label_name : {internal_label} \n'
                result_text += f'nodule name : {odx}, percent : {pred_i2[odx]}, label_name : {internal2_label} \n'


            crop_image_paths = sorted(list_images(f'{nodule_image_path}'))
            crop_image_paths = [crop_image_path for crop_image_path in crop_image_paths if 'hst' not in crop_image_path]
            json_file['result']['ncount'] = len(crop_image_paths)

            print("Axial 이미지에 결절이 있을때 세번째 json 생성중")
            for idx, nodule_image in enumerate(crop_image_paths, 1):
                text_file_name, _ = os.path.splitext(crop_image_paths[idx-1])
                text_file_name = f'{text_file_name}.txt'

                json_file['result'][f'nodule{idx}'] = {
                                    "nodule image path" : nodule_image,
                                    "classi_text_path" : text_file_name,
                                    "Shape" : None,
                                    "Margin" : None,
                                    "Calcification" : None,
                                    "Spongiform" : None,
                                    "Internal content" : None,
                                    "Echogenicity" : None,
                                    "Orientation" : None,
                                    "comet tail" : None
                                }

            ## idx 변수로 사용할 경우 결절을 여러개 검출할 경우에 모든 텍스트 파일이 같은 결과값으로 저장되어 함수 인자값으로 받은 index 변수 사용
            print(Path(f'{nodule_image_path}/{file_name}_nodule_{index}.txt'))
            open(Path(f'{nodule_image_path}/{file_name}_nodule_{index}.txt'), 'w').write(result_text)    

            json.dump(json_file, open(Path(f'{json_save_path}/{file_name}_nodule.json'),'w'),ensure_ascii=False, indent =4)

        except Exception as e:
            config.log_writer(f'검출된 결절 이미지가 존재하지 않습니다. - {traceback.format_exc()}')
            print(traceback.format_exc())
            

        return result_text


## YOLO v5 검출 함수
@torch.no_grad()
def run(save_path, file_name,  model, device):
    image_paths = sorted(list_images(f'{ROOT_PATH}/media/{file_name}'))
    folder_name = file_name.split(os.path.sep)[-1]

    visit_date = '/'.join(file_name.split(os.path.sep)[:-1])
    print(f'방문 날짜 : {visit_date} \n\n')

    ## YOLO v5 검증에 필요한 부분 설정 중
    stride, names, pt, jit, engine = model.stride, model.names, model.pt, model.jit, model.engine
    imgsz = check_img_size((480, 480), s = stride)

    half = False and ((pt or jit or engine) and device.type != 'cpu')
    model.model.half() if half else model.model.float()

    print(f'검증할 이미지가 있는 경로 입니다. {ROOT_PATH}/media/{file_name}\n')
    for odx, image_path in enumerate(image_paths, 1):
        print(f'\n\n\n {odx}번 째 검증 중입니다......')
        ## odx | 입력받은 이미지의 인덱스 값
        ## odx = 1 → Axial 이미지 | odx = 2 → Sagittal 이미지

        print(f'[{odx}] {image_path}, {type(image_path)}')
        image_name, _ = os.path.splitext(image_path.split(os.path.sep)[-1])
        ## 크롭된 결절 이미지가 저장되는 폴더
        ## /home/super/바탕화면/share/lt4/media/2022/04/25/dove/nodule/dove처럼 구성됨.
        nodule_image_path = '/'.join(image_path.split(os.path.sep)[:-1]) + f'/nodule/{image_name}'
        json_image_path = '/'.join(image_path.split(os.path.sep)[:-1]) + '/jsons'
        os.makedirs(nodule_image_path, exist_ok = True)

        ## 바운딩 박스가 그려진 이미지가 저장되는 폴더
        ## /home/super/바탕화면/share/lt4/media/2022/04/25/dove/detected처럼 구성됨.
        detected_image_path = '/'.join(image_path.split(os.path.sep)[:-1]) + '/detected'
        os.makedirs(detected_image_path, exist_ok = True)

        ## 횡단, 종단 검사 json 파일들이 저장되는 폴더
        ## /home/super/바탕화면/share/lt4/media/2022/04/25/dove/jsons 처럼구성됨.
        
        json_save_path = '/'.join(image_path.split(os.path.sep)[:-1]) + '/jsons'
        os.makedirs(json_save_path, exist_ok = True)
        dataset = LoadImages(image_path, img_size = imgsz, stride = stride, auto = pt)

        ## 검증시간 및 검출 갯수 측정 용 변수
        dt, seen = [0.0, 0.0, 0.0], 0

        print("Json path",json_image_path)
        for path, image, original_image, _, s in dataset:

            image = torch.from_numpy(image).to(device)
            image = image.half() if half else image.float()
            image /= 255.
            
            if len(image.shape) == 3: image = image[None]
            boxes = model(image)
            boxes = non_max_suppression(boxes, 0.6, 0.5)

            ## 검출된 박스 갯수대로 작업해주는 코드
            for box in boxes:
                seen += 1
                ##         path_ : string 형태가 아닌 YOLO v5에서 사용하는 경로 자료형으로 이루어진 이미지 경로
                ## image_copy : 검출된 결절에 바운딩 박스 그리기 용으로 복사한 이미지 
                path_, image_copy = Path(path), original_image.copy()
                file_name = path.split(os.path.sep)[-1]

                print(f'데이터 경로 : {path_}, {path_.stem} {type(path_)} \n파일 이름 : {file_name} \n')
                name, ext = os.path.splitext(file_name)

                ## detected_save_path : 바운딩 박스가 그려진 이미지가 저장되는 폴더
                detected_save_path = f'{detected_image_path}/{name}_detected{ext}'
                nodule_image_path = Path(nodule_image_path)

                print(f'바운딩 박스가 그려진 이미지 경로s : {detected_save_path}')

                s += f'{image.shape[2]} x {image.shape[3]}'

                ## 검출한 내용대로 크롭하기 위한 이미지
                image_for_crop = image_copy.copy()

                ## 바운딩 박스를 그리기 위한 Annotator 클래스 호출
                annotator = Annotator(image_copy, line_width = 3, example = str(names))
                print("학습된 클래스",box)
                print("학습된 클래스 개수",len(box))
                if len(box) >= 1:
                    print(f"박싱된 결절의 개수가 {len(box)}개 일때\n\n ")
                    ## YOLO v5에서 검출한 좌표를 입력한 이미지의 좌표에 맞게 변경해주는 부분
                    box[:, :4] = scale_coords(image.shape[2: ], box[:, :4], image_copy.shape).round()

                    for idx, (*xyxy, conf, cls) in enumerate(reversed(box)):
                        class_idx = int(cls)
                        label = f'{names[class_idx]} {conf:.2f}'

                        print(f'\n\n detected : {idx} - {names[class_idx]}\n\n')

                        ## 경동맥, 협부, 결절 중 결절만 표시되도록 해주는 코드
                        if 'nodule' not in names[class_idx].lower(): continue
                        
                        file_path = Path(f'{nodule_image_path}/{name}_nodule_{idx}.jpg')

                        ## 이미지에 바운딩 박스하고 라벨 정보 입력해주는 부분
                        annotator.box_label(xyxy, label, color = colors(class_idx, True))

                        ## 크롭한 결절 이미지 저장
                        crop, (w, h) = save_one_box(xyxy, image_for_crop, file=file_path, BGR=True)

                        #! 횡단면 이미지만 분류 모델을 적용하므로, 횡단면 이미지 이외의 이미지는 전처리 및 분류모델을 적용하지 않음.
                        #sagittal만 들어왔을때 파일이름에 sagittal이 들어가있으면 예외처리
                        
                        if odx == 1:
                            print(f"Axial 이미지에 결절이 있을때 {idx}번째 과정")
                            ## histogram 평준화가 이루어진 이미지가 저장되는 폴더
                            ## /home/super/바탕화면/share/lt4/media/2022/04/25/dove/  nodule/dove/hst처럼 구성됨.
                            #! 횡단면 이미지만 분류 모델을 적용하므로, 횡단면 이미지 이외의 이미지는 histogram 폴더를 만들지 않음.
                            histogram_image_path = '/'.join(image_path.split(os.path.sep)[:-1]) + f'/nodule/{image_name}/hst'
                            os.makedirs(histogram_image_path, exist_ok = True)
                            
                            histogram_save_path = f'{histogram_image_path}/{name}_hst_{idx}.jpg'
                            histogram_image = preprocessing(crop, histogram_save_path)

                            ## 특성별 분류 모델 검증 부분
                            #pred_k, pred_e, pred_m, pred_s, pred_o, pred_c, pred_h, pred_i, pred_i2 = classification(histogram_image)

                            ## 결과 저장에 필요한 파라미터들을 딕셔너리 형태로 save_result 함수에 전달
                            kwargs = { 'index' : idx, 'file_name' : name, 'visit_date' : visit_date, 'original_image_path' : image_path, 'patient_id' : folder_name,
                                        'width' : w, 'height' : h, 'detected_image_path' : detected_save_path, 'nodule_image_path' : nodule_image_path, 
                                        'json_path' : json_save_path
                                    }
                            save_result(classification(histogram_image), **kwargs)

                            first_filename = name
                        
                        else:
                            if idx == 0:
                                print(f"Sagittal 이미지에 결절이 있을때 첫번째 과정{idx}\n\n")
                                json_file1 = {"patient id" : name, "visit date" : visit_date,
                                "original image path" : image_path,
                                "inspection image path" : image_path,
                                "model complete" : "complete",
                                "result" : {}}

                                json_file1['result']['ncount'] = 0
                                # 결절이 detect 되지않았을 때 json
                                json_file1['result'][f'nodule{idx}'] = {
                                                    "nodule image path" : image_path,
                                                    "classi_text_path" : detected_image_path,
                                                    "Shape" : None,
                                                    "Margin" : None,
                                                    "Calcification" : None,
                                                    "Spongiform" : None,
                                                    "Internal content" : None,
                                                    "Echogenicity" : None,
                                                    "Orientation" : None,
                                                    "comet tail" : None
                                                }
                                print("똬똬1",json_file1)

                                json.dump(json_file1, open(Path(f'{json_image_path}/{name}_nodule.json'),'w'),ensure_ascii=False, indent =4)



                    ## 종단면 이미지의 분루 모델 결과는 횡단면 이미지 검사결과의 json 파일을 불러와서 일부만 수정한다.
                        if odx != 1:
                            try:
                                print("Axial 이미지에 결절이 여러개 있을때 첫번째 과정")
                                json_file = json.loads(open(f'{json_save_path}/{first_filename}_nodule.json', 'rb').read())

                            except Exception as e:
                                    ERR = f'[ERR]횡단면 검사 json 파일이 존재하지 않습니다. 확인 부탁드립니다. {e} \n상세 : {traceback.format_exc()}'
                                    config.log_writer(ERR)
                                    json_file = {}

                            try:
                                print("\n\n똬똬3",json_file)
                                nodule_image_paths = sorted(list_images(f'{nodule_image_path}'))
                                #json_file['result']['ncount'] = len(nodule_image_paths)

                                ## 종단에서 검출한 결절의 수 보다 횡단에서 검출한 결절의 수가 많은 경우
                                ##  json 파일에서 key값을 제거해주는 부분

                                ## 종단에서 검출한 결절 갯수 만큼 nodule1, nodule2, ... 가 저장된 리스트 생성
                                nodule_count = [f'nodule{idx}' for idx, _ in enumerate(nodule_image_paths, 1)]

                                ## 횡단 검사 json에서 검출한 결절 갯수 만큼 nodule1, nodule2, ... 가 저장된 리스트(json_file['result'].keys())에서
                                ## nodule이라는 문자열이 들어가고, 위에 생성한 nodule_count에는 없는 값만 추출
                                json_keys = [json_key for json_key in json_file['result'].keys() 
                                                    if ('nodule' in json_key) and (json_key not in nodule_count)]

                                ## json_file['result']에서 종단면에서 검출한 갯수 보다 많은 만큼 삭제
                                #for json_key in json_keys: del json_file['result'][json_key]

                                for idx, nodule_image_path in enumerate(nodule_image_paths, 1):
                                    json_file['original image path'] = image_path
                                    json_file['inspection image path'] = detected_save_path

                                    ## Axial 이미지 보다 Sagittal 이미지에서 결절을 더 많이 검출한 경우에 예외처리
                                    try:
                                        
                                        
                                        json_file['result'][f'nodule{idx}'] = {}
                                        json_file['result'][f'nodule{idx}']['nodule image path'] = nodule_image_path
                                        print("\n\n똬똬4",json_file)
                                    except Exception as e:
                                        WARN = f'[WARN] 횡단면 이미지에서 종단면 보다 많은 결절이 검출되었습니다. {e} \n상세 : {traceback.format_exc()}'
                                        config.log_writer(WARN, level = 'warn')
                                        
                                json.dump(json_file, open(f'{json_save_path}/{name}_nodule.json', 'w'), ensure_ascii=False, indent=4)
                                print("\n\n똬똬2",json_file['result'])
                            except Exception as e:
                                ERR = f'[ERR]종단면 검사 json 파일 저장에 실패하였습니다. 확인 부탁드립니다. {e} \n상세 : {traceback.format_exc()}'
                                config.log_writer(ERR)
                if len(box) < 1:
                    print(f'\n\n no nodule images - \n\n')
                    json_file1 = {"patient id" : name, "visit date" : visit_date,
                    "original image path" : image_path,
                    "inspection image path" : image_path,
                    "model complete" : "complete",
                    "result" : {}}

                    json_file1['result']['ncount'] = 0
                    # 결절이 detect 되지않았을 때 json
                    json_file1['result'][f'nodule1'] = {
                                        "nodule image path" : image_path,
                                        "classi_text_path" : None,
                                        "Shape" : None,
                                        "Margin" : None,
                                        "Calcification" : None,
                                        "Spongiform" : None,
                                        "Internal content" : None,
                                        "Echogenicity" : None,
                                        "Orientation" : None,
                                        "comet tail" : None
                                    }
                    print("confirm",json_file1,image_path)
                    json.dump(json_file1, open(Path(f'{json_save_path}/{name}_nodule.json'),'w'),ensure_ascii=False, indent =4)
                    

            ## 바운딩 박스 그려진 이미지 저장해주는 부분
            cv2.imwrite(detected_save_path, image_copy)
            config.log_writer('[INFO] 검출, 분류 모델 검증이 완료 되었습니다.')
                    

## 좌표 정보를 이용하여 검출한 객체만 크롭하여 저장해주는 함수
def save_one_box(xyxy, im, file='image.jpg', gain=1.02, pad=10, square=False, BGR=False, save=True):
    # Save image crop as {file} with crop size multiple {gain} and {pad} pixels. Save and/or return crop
    xyxy = torch.tensor(xyxy).view(-1, 4)
    b = xyxy2xywh(xyxy)  # boxes
    if square:
        b[:, 2:] = b[:, 2:].max(1)[0].unsqueeze(1)  # attempt rectangle to square
    b[:, 2:] = b[:, 2:] * gain + pad  # box wh * gain + pad
    xyxy = xywh2xyxy(b).long()
    clip_coords(xyxy, im.shape)
    crop = im[int(xyxy[0, 1]):int(xyxy[0, 3]), int(xyxy[0, 0]):int(xyxy[0, 2]), ::(1 if BGR else -1)]

    try:
        if save:
            file.parent.mkdir(parents=True, exist_ok=True) 
            cv2.imwrite(str(increment_path(file).with_suffix('.jpg')), crop)
    except:
        pass
    ## 크롭한 이미지의 width와 height도 계산하여 반환
    w = int(xyxy[0, 2]) - int(xyxy[0, 0])
    h = int(xyxy[0, 3]) - int(xyxy[0, 1])

    return crop, (w, h)

## 테스트 용 코드
if __name__ == '__main__':
    from yolov5.models.common import DetectMultiBackend
    from yolov5.utils.torch_utils import select_device

    def load_model():
        weight_path = f'{ROOT_PATH}/models/yolo.pt'
        device = select_device('')

        print('디텍션 모델 로딩 중 입니다.')
        model = DetectMultiBackend(weights = weight_path, device = device)
        print('디텍션 모델 로딩 완료 하였습니다.')
        return model, device

    model, device = load_model()
    run(save_path = 'save', file_name = '2022/04/26/dove', model = model, device = device)