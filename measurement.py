#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import re
import csv
import datetime
import time

x=y=x1=x2=x3=y1=y2=y3=0
t1=t2=mx1=mx2=mx3=my1=my2=my3=0

# 日時の取得
now = datetime.datetime.now()
# ディレクトリの指定はここ
filename = './output/log_' + now.strftime('%Y%m%d_%H%M%S') + '.csv'
#file = open('new.csv', 'w')
with open(filename, 'w') as f:
    writer = csv.writer(f)
    #writer.writerow(['time', 'dx1', 'dy1', 'dx2', 'dy2', 'x', 'y'])
    writer.writerow(['time', '0', '0', '0', '0', '0', '0', '0', '0'])

while 1:
    perf_s = time.perf_counter()
    open1 = serial.Serial('/dev/ttyACM0',115200,timeout=None)
    open2 = serial.Serial('/dev/ttyACM1',115200,timeout=None)
    open3 = serial.Serial('/dev/ttyACM2',115200,timeout=None)
    open1.write(str.encode('o'))
    open2.write(str.encode('o'))
    open3.write(str.encode('o'))
    read1 = open1.readline()
    read2 = open2.readline()
    read3 = open3.readline()

    s1 = read1.decode()
    s2 = read2.decode()
    s3 = read3.decode()
    mx1 = re.search('aaa(.+?)bbb', s1).group(1)
    my1 = re.search('bbb(.+?)ccc', s1).group(1)
    mx2 = re.search('aaa(.+?)bbb', s2).group(1)
    my2 = re.search('bbb(.+?)ccc', s2).group(1)
    mx3 = re.search('aaa(.+?)bbb', s3).group(1)
    my3 = re.search('bbb(.+?)ccc', s3).group(1)

    print(mx1)
    print(my1)
    print(mx2)
    print(my2)
    print(mx3)
    print(my3)
    dx1 = int(mx1) * 0.08623663#* 0.10622929#* 0.13655233#* 0.02396472392638
    dy1 = int(my1) * 0.09190501#* 0.16020506#* 0.13544996#* 0.02396472392638
    dx2 = int(mx2) * 0.08467042#* 0.10727312#* 0.10288701#* 0.02396472392638
    dy2 = int(my2) * 0.09252234#* 0.1502449#* 0.11575682#* 0.02396472392638
    dx3 = int(mx3) * 0.08535701#* 0.12157463#* 0.15569776#* 0.02396472392638
    dy3 = int(my3) * 0.09904913#* 0.24527839#* 0.14964235#* 0.02396472392638
    
    if dx1 == 0 and dy1 == 0:
        x1 += dx2
        y1 += dy2
        if dx2 == 0 and dy2 == 0:
            x += dx3
            y += dy3
            x1 += dx3
            y1 += dy3
            x2 += dx3
            y2 += dy3
        elif dx3 == 0 and dy3 == 0:
            x += dx2
            y += dy2
            x3 += dx2
            y3 += dy2
        else:
            x += float((dx2 + dx3) / 2.0)
            y += float((dy2 + dy3) / 2.0)
    elif dx2 == 0 and dy2 == 0:
        x2 += dx3
        y2 += dy3
        if dx3 == 0 and dy3 == 0:
            x += dx1
            y += dy1
            x2 += dx1
            y2 += dy1
        else:
            x += float((dx1 + dx3) / 2.0)
            y += float((dy1 + dy3) / 2.0)
    elif dx3 == 0 and dy3 == 0:
        x += float((dx1 + dx2) / 2.0)
        y += float((dy1 + dy2) / 2.0)
        x3 += dx1
        y3 += dy1
    else:
        x += float((dx1 + dx2 + dx3) / 3.0)
        y += float((dy1 + dy2 + dy3) / 3.0)
        
        x1 += dx1
        x2 += dx2
        y1 += dy1
        y2 += dy2
        x3 += dx3
        y3 += dy3

    now_str = datetime.datetime.now().strftime('%H:%M:%S.%f')

    # writer.writerowでlistをcsvに書き込む
    with open(filename, 'a', newline="") as f:
        writer = csv.writer(f)
        writer.writerow([perf_t, x1, y1, x2, y2, x3, y3, x, y])
    
    perf_t = time.perf_counter() - perf_s
    while perf_t < 100:
        perf_t = time.perf_counter() - perf_s
    
    open1.close()
    open2.close()
    open3.close()