import time

import os
import datetime

from imutils.paths import list_images
import custom_detect
from yolov5.utils.torch_utils import select_device
from yolov5.models.common import DetectMultiBackend
from UTIL import config

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ModuleNotFoundError as e:
    print (e)
    os.system("pip install watchdog")


today = datetime.date.today()
month= str(today.month).zfill(2)
day= str(today.day).zfill(2)
dt = os.path.join(f'{today.year}/{month}/{day}')

ROOT_PATH = config.ROOT_PATH
os.makedirs(f'{ROOT_PATH}/media/{today.year}/{month}/{day}', exist_ok=True)

## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
config.log_writer('Watchdogs 실행 중.', level = 'info')

# weight_path = f'{ROOT_PATH}/_yolov5_/weight/best.pt'
# device = select_device('')
# model = DetectMultiBackend(weights = weight_path, device = device)
def load_model():
    weight_path = f'{ROOT_PATH}/models/yolo.pt'
    device = select_device('')
    model = DetectMultiBackend(weights = weight_path, device = device)
    return model, device

model, device = load_model()
# ------------------------------------------------
class Handler(FileSystemEventHandler):
    def __init__(self):
        pass 
    
    def on_created(self, event): # 파일 생성시
        Isdir = os.path.exists(event.src_path)
        print (f'event type : {event.event_type}\n')
        print("첫번째", Isdir)
        if event.is_directory:
            print ("폴더 생성",event.src_path)
            print("두번째", Isdir)
            _, ext = os.path.splitext(os.path.basename(event.src_path))
            Fname = event.src_path.split(os.path.sep)[-1]

            if os.path.isdir(event.src_path):
                custom_detect.run(save_path = event.src_path,file_name = f'{dt}/{Fname}', model= model, device= device)
                #subprocess.run(text,shell=True)
        else: # not event.is_directory
            """
            Fname : 파일 이름
            Extension : 파일 확장자 
            """
            Fname, Extension = os.path.splitext(os.path.basename(event.src_path))
            '''
            1. zip 파일
            2. exe 파일
            3. lnk 파일
            '''
            if Extension == '.zip':
                print (".zip 압축 파일 입니다.")
            elif Extension == '.exe':
                print (".exe 실행 파일 입니다.")
                os.remove(Fname + Extension)   # _파일 삭제 event 발생
            elif Extension == '.lnk':
                print (".lnk 링크 파일 입니다.")
        return Fname

    def on_deleted(self, event):
        print ("삭제 이벤트 발생")

    def on_moved(self, event): # 파일 이동시
        print (f'event type : {event.event_type}\n')

class Watcher:
    # 생성자
    def __init__(self, path):
        print ("감시 중 ...")
        self.event_handler = None      # Handler
        self.observer = Observer()     # Observer 객체 생성
        self.target_directory = path   # 감시대상 경로
        self.currentDirectorySetting() # instance method 호출 func(1)

    # func (1) 현재 작업 디렉토리
    def currentDirectorySetting(self):
        
        print ("====================================")
        print ("현재 작업 디렉토리:  ", end=" ")
        os.chdir(self.target_directory)
        print ("{cwd}".format(cwd = os.getcwd()))
        print ("====================================")

    # func (2)
    def run(self):
        self.event_handler = Handler() # 이벤트 핸들러 객체 생성
        self.observer.schedule(
            self.event_handler,
            self.target_directory,
            recursive=False
        )

        self.observer.start() # 감시 시작
        try:
            while True: # 무한 루프
                time.sleep(1) # 1초 마다 대상 디렉토리 감시
        except KeyboardInterrupt as e: # 사용자에 의해 "ctrl + z" 발생시
            print ("감시 중지...")
            
            ## media/log 폴더에 로그 작성해주는 코드 자세한 코드는 UTIL/config.py 참조
            config.log_writer('Watch Dogs 감시 종료', level='warn')
            self.observer.stop() # 감시 중단

myWatcher = Watcher(f'{ROOT_PATH}/media/{today.year}/{month}/{day}')
myWatcher.run()
