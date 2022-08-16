import serial
from time import time
ser = serial.Serial("COM3",9600)




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

            elif len(sensor) == 1 :                   # 처음 상점에 들어왔을때
                tBefore = time()

            print(sensor)
            print(t)
        except:
            pass