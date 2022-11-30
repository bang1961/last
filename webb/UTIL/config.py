import datetime
import logging
import os

## 분당 서울대 병원 용으로 경로 설정
## False : 사내 테스트 용, True: 분당 서울대 용
SNUBH = False

## 사내 3번째 서버인지 아닌지 설정
## False : 3번째 서버 아님 | True : 3번째 서버임
MK3   = True

## 환자 동의서 표시 설정
## False : 표시 안함, True : 표시함.
AGREE = False

ROOT_PATH = '/home/lt4/lt4/' if SNUBH else '/home/super/바탕화면/share/lt4/'
ROOT_PATH = '/home/super/projects/thyroid/WebPlatform/lt4/' if MK3 else ROOT_PATH

today = datetime.date.today()
year = today.year
month = str(today.month).zfill(2)
day = str(today.day).zfill(2)
os.makedirs(f'{ROOT_PATH}/media/log', exist_ok = True)

## media/log 폴더에 로그 남겨주는 코드.
def log_writer(message, level = 'err'):
    
    ## 로그 파일 이름은 log-(현재 연월일).log로 생성됨.
    ## 로그 내용은 [로그 등급] (이벤트가 발생한 시간) 로그 메시지와 같이 저장됨.
    logging.basicConfig(filename=f'{ROOT_PATH}/media/log/log-{year}{month}{day}.log',
                                format='[%(levelname)s] (%(asctime)s) %(message)s', level = logging.DEBUG)
    
    print(message)
    
    ## 로그의 등급 (error, info, warning)에 따라 다른 내용으로 저장됨.
    if 'err' in level.lower(): logging.error(message)
    elif 'info' in level.lower(): logging.info(message)
    elif 'warn' in level.lower(): logging.warning(message)

if __name__ == '__main__':
    log_writer('에러 테스트')
    log_writer('정보 테스트', level = 'info')
    log_writer('경고 테스트', level = 'warn')