from time import time

import cv2
cam = cv2.VideoCapture(0)  #사진 찍을 준비

import serial
ser = serial.Serial("COM3",9600)  #아두이노 시리얼통신
    #TODO 다른 센서 추가!!


import telegram
telegram_token = "5449822461:AAERJ9ZWoMMpGZa5MpMf7Va0ng4a3moi1Ns"  #텔레그램 메시지 준비
telegram_channel_id = "@shop08281"
bot = telegram.Bot(token=telegram_token)



def track():  #센서 코드
    sensor=[]  #사람이 지나간 센서 순서
    t=[]  # 센서와 센서 사이의 시간
    stop=False
    while not stop:
        if ser.readable():

            try:
                num = int(ser.read().decode())
                sensor.append(num)                        # 센서 번호를 리스트에 저장

                if len(sensor) > 1:        # 이미 다른 센서에 감지되었을때
                    tNow = time()
                    t.append(round(tNow - tBefore , 2))
                    tBefore = tNow

                    if num == 1 :      # 상점을 나갔으면
                        stop=True
                        tEnd = time()

                elif len(sensor) == 1 :                   # 처음 상점에 들어왔을때
                    takephoto()
                    tBefore = time()
                    tStart = time()

                print(sensor)
                print(t)
            except:
                pass
    return sensor, t, tStart, tEnd


def outlier(a):  #이상탐지
    return True
    #TODO 이상치 탐지 구현 (기준별로 다르게 해야 할수도 있음)


def takephoto():  #사진찍기
    ret, frame = cam.read()
    cv2.imwrite("allert.png", frame)

def alert(st): #상점 주인에게 사진, 시간 보내기
    photopath="allert.png"
    bot.sendMessage(chat_id=telegram_channel_id,text=f"Alert!! >>> time:{st}")
    bot.sendPhoto(chat_id=telegram_channel_id, photo=open(photopath, 'rb'))


run=True
while run: #반복
    print("tracking start")
    sensorList, timeList, startTime, endTime=track()
    print("tracking end")
    if outlier(sensorList) or outlier(timeList) or outlier(round(endTime - startTime , 2)): #세가지 기준 중 하나라도 이상치가 있으면:
        alert(startTime)
        print("alerted")
