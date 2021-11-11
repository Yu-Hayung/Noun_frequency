import requests
import urllib.request
import time
import os
from konlpy.tag import *

# 음성 데이터가 여러번 들어갔을때 누적으로 명사 빈도수 최종 상위 7개 도출


# 서강대 STT 실행 // 사용자 함수 정의
def send_api(method, file):
    url = 'http://auc.sogang.ac.kr/service/api/speech/recognize'

    if method == 'GET':
        response = requests.get(url)

        return response

    elif method == 'POST':
        try:
            start = time.time()
            FLIE = {'file': open(file, 'rb')}
            response = requests.post(url,
                             files=FLIE,
                             timeout=60)

            endtime = time.time() - start

            return response, endtime

        except requests.exceptions.Timeout:
            return ' <<< 60s  time out   >>> ', requests

        except Exception as ex:
            return 'ex >>', ex

def SKU_STT(url):
    wav_Name = "C:/Users/yuhay/Desktop/STT_test.wav"

    urllib.request.urlretrieve(url, wav_Name)
    response, endtime = send_api("POST", wav_Name)
    response_result_json = response.json()
    STT_txt = response_result_json.get('data')

    os.remove(wav_Name)  # 로컬 OS  저장된 WAV 삭제

    return STT_txt

def nouns_out(txt): # 명사추출 함수
    okt = Okt()  # Okt 객체 선언
    nouns = okt.nouns(txt)  # 명사 배열

    #1글자 명사(불용어) 삭제
    return_list = []
    for i in nouns:
        if len(i) != 1 :
            return_list.append(i)
        else:
            pass

    return return_list

def Noue_frequency(url):
    STT = SKU_STT(url)
    STT_nouns = []
    for i in STT:
        nouns = nouns_out(i)
        STT_nouns.append(nouns)

    STT_nouns = sum(STT_nouns, []) # 2차 -> 1차 리스트

    if os.path.isdir('C:/Users/yuhay/Desktop/None.text'):
        f = open('C:/Users/yuhay/Desktop/None.text', 'w')
        j = ' '.join(STT_nouns)
        f.write(j)
        f.close()
    else:
        f = open('C:/Users/yuhay/Desktop/None.text', 'a')
        j = ' '.join(STT_nouns)
        f.write(j)
        f.close()

    frequency = {}
    f = open('C:/Users/yuhay/Desktop/None.text', 'r')

    STT_nouns = []
    for line in f:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        STT_nouns.append(line_list)

    f.close()

    STT_nouns_list = sum(STT_nouns, []) # 2차 -> 1차 리스트

    for word in STT_nouns_list:
        count = frequency.get(word, 0)
        frequency[word] = count + 1

    frequency_list = frequency.keys()

    response_dict = {}
    for words in frequency_list:
        response = dict({words: frequency[words]})
        response_dict.update(response)

    sorted_by_value = sorted(response_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_by_value_7 = sorted_by_value[0:7]  # 빈도수 상위 7 개
    response_dict = dict((k, v) for k, v in sorted_by_value_7)
    response = list(response_dict.keys())

    result = dict({'result': response})

    return result
    # return JsonResponse(response_dict)

####################################################################################################################################################

start_time = time.time()

if __name__ == "__main__":
    file_name = '5.wav'
    url = 'https://withmind.cache.smilecdn.com//images/UHA/WAV/'+ file_name
    # url = 'C:/Users/yuhay/Desktop/module/noun_frequency/test.wav'
    frequency = Noue_frequency(url)

print('frequency >>>', frequency)
print("--- %s sec ---" % (time.time() - start_time))


