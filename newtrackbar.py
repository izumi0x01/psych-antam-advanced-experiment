#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
import sys
import math

def nothing(x):
    pass

def printing(position):
    print(position)

# 初期値を設定
threshold = 60
FPS = 10
#CAM_W = 240
#CAM_H = 240
CAM_W = 200
CAM_H = 200
KP_GAIN = 0.8
KD_GAIN = 0.001/FPS

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, FPS)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
video = cv2.VideoWriter('video.mp4', fourcc, FPS, (CAM_W, CAM_H))

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:                                                                                          
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import * # Uses Dynamixel SDK library

ADDR_TORQUE_ENABLE          = 64
ADDR_GOAL_VELOCITY          = 104
DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
BAUDRATE                    = 115200

# DYNAMIXEL Protocol Version (1.0 / 2.0)
# https://emanual.robotis.com/docs/en/dxl/protocol2/
PROTOCOL_VERSION            = 2.0

# Default setting
DXL1_ID                     = 1                 # Dynamixel#1 ID : 1
DXL2_ID                     = 2                 # Dynamixel#2 ID : 2
DXL3_ID                     = 3                 # Dynamixel#1 ID : 3

DEVICENAME1                 = '/dev/ttyUSB0'    # Check which port is being used on your controller

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

index = 0
error_x = 0
error_y = 0
x = y = 0
countor = 0

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler1 = PortHandler(DEVICENAME1)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port1
if portHandler1.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

# Set port1 baudrate
if portHandler1.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Enable Dynamixel#1 Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler1, DXL1_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel#%d has been successfully connected" % DXL1_ID)

# Enable Dynamixel#2 Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler1, DXL2_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel#%d has been successfully connected" % DXL2_ID)

# Enable Dynamixel#3 Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler1, DXL3_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel#%d has been successfully connected" % DXL3_ID)

# トラックバーを表示するウィンドウを作成
cv2.namedWindow("Masked")

# トラックバーを作成する
# トラックバーの名前、トラックバーをつけるウィンドウ名、初期値、トラックバーの最大値。コールバック関数
cv2.createTrackbar("track", "Masked", threshold, 255, printing)

while 1:
    ret, frame1 = cam.read()
    #x, y = 80, 0
    #h, w = 560, 480
    x, y = 120, 40
    h, w = 520, 440
    frame = frame1[y:y+h, x:x+w]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print(cam.get(cv2.CAP_PROP_FPS))

    ret, mask_image = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

    # トラックバーの位置をthreshholdに代入
    threshold = cv2.getTrackbarPos("track", "Masked")

    if cv2.waitKey(1) & 0xff == ord('r'):
        countor = 1

    if cv2.waitKey(1) & 0xff == ord('g'):
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler1, DXL1_ID, ADDR_GOAL_VELOCITY,0)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler1, DXL2_ID, ADDR_GOAL_VELOCITY,0)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler1, DXL3_ID, ADDR_GOAL_VELOCITY,0)
        countor = 0

    countors,hierarchy=cv2.findContours(mask_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(countors) != 0 :
        mu = cv2.moments(mask_image)  
        x,y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
        cv2.circle(mask_image,(x,y),5,(0,0,255),3)
    
    error_x = x - CAM_W
    error_y = y - CAM_H
    #print(error_x)
    #print(error_y)
    abs_x = abs(error_x)
    abs_y = abs(error_y)
    diff_error_x = CAM_W - error_x
    diff_error_y = CAM_H - error_y
    Vx = KP_GAIN * abs_x + KD_GAIN * diff_error_x
    Vy = KP_GAIN * abs_y + KD_GAIN * diff_error_y

    #print(Vx)
    #print(Vy)
    if Vx > 200:
        Vx = 200
    if Vy > 200:
        Vy = 200
    
    if countor == 1:

        if x >= CAM_W and y >= CAM_H:
            Vx = Vx
            Vy = -1 * Vy
        elif  x < CAM_W and y > CAM_H:
            Vx = -1 * Vx
            Vy = -1 * Vy
        elif  x <= CAM_W and y <= CAM_H:
            Vx = -1 * Vx
            Vy = Vy
        elif  x > CAM_W and y < CAM_H:
            Vx = Vx
            Vy = Vy
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler1, DXL1_ID, ADDR_GOAL_VELOCITY,int(-Vx))
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler1, DXL2_ID, ADDR_GOAL_VELOCITY,int(0.5*Vx-math.sqrt(3)*0.5*Vy))
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler1, DXL3_ID, ADDR_GOAL_VELOCITY,int(0.5*Vx+math.sqrt(3)*0.5*Vy))
    cv2.imshow('Input', frame)
    cv2.imshow('Masked', mask_image)

    print(x)
    print(y)
    print(error_x)

    key = cv2.waitKey(1)
    if key == 27:
        #stop
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler1, DXL1_ID, ADDR_GOAL_VELOCITY,0)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler1, DXL2_ID, ADDR_GOAL_VELOCITY,0)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler1, DXL3_ID, ADDR_GOAL_VELOCITY,0)

        # Disable Dynamixel#1 Torque
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler1, DXL1_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        # Disable Dynamixel#2 Torque
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler1, DXL2_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        # Disable Dynamixel#3 Torque
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler1, DXL3_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        # Close port1
        portHandler1.closePort()
        cam.release()
        cv2.destroyAllWindows()
        sys.exit()
