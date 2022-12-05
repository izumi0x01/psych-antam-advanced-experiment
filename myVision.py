from ast import While
from asyncio.windows_events import NULL
from turtle import distance, update
from cv2 import contourArea
import unicurses
import numpy as np
import cv2
import sys
import math
import copy


class Vision:

    X0, Y0 = 0, 0
    X1, Y1 = 0, 0
    FPS = 10
    MAIN_WINDOW_NAME = "RAW"
    MASKED_WINDOW_NAME = "Masked"

    def __init__(self):
        self.__threshold: int = 145
        self.distance = 0

    def MakeWindow(self):
        cv2.namedWindow(self.MASKED_WINDOW_NAME)
        cv2.createTrackbar("slesh_hold", self.MASKED_WINDOW_NAME, self.__threshold,
                           255, self.SleshHoldChangedEventHandler)
        self.__cam = cv2.VideoCapture(1+cv2.CAP_DSHOW)  # 引数に番号だけ渡すのではダメだった模様
        if not self.__cam.isOpened():
            return print("failure video capture")
        self.__cam.set(cv2.CAP_PROP_FPS, self.FPS)
        cv2.createTrackbar("height", self.MASKED_WINDOW_NAME, 0,
                           int(self.__cam.get(cv2.CAP_PROP_FRAME_HEIGHT) * 0.5), self.Y0ChangedEventHandler)
        cv2.createTrackbar("width", self.MASKED_WINDOW_NAME, 0,
                           int(self.__cam.get(cv2.CAP_PROP_FRAME_WIDTH) * 0.5), self.X0ChangedEventHandler)

    def SleshHoldChangedEventHandler(self, position):
        self.__threshold = cv2.getTrackbarPos(
            "slesh_hold", self.MASKED_WINDOW_NAME)

    def X0ChangedEventHandler(self, position):
        self.X0 = cv2.getTrackbarPos("width", self.MASKED_WINDOW_NAME)

    def Y0ChangedEventHandler(self, position):
        self.Y0 = cv2.getTrackbarPos("height", self.MASKED_WINDOW_NAME)

    def X1ChangedEventHandler(self, position):
        self.X1 = int(self.__cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        - cv2.getTrackbarPos("width", self.MASKED_WINDOW_NAME)

    def Y1ChangedEventHandler(self, position):
        self.Y1 = int(self.__cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        - cv2.getTrackbarPos("height", self.MASKED_WINDOW_NAME)

    def UpdateWindow(self):
        # 描画の待ち時間設定
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            sys.exe()
        ret, Frame = self.__cam.read()
        if not ret:
            return NULL
        cv2.imshow(self.MAIN_WINDOW_NAME, Frame)
        # frame全体から画像の抽出
        # Frame = Frame1[self.Y0:self.Y1, self.X0:self.X1]
        ret, grayImage = cv2.threshold(
            cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY), self.__threshold, 255, cv2.THRESH_BINARY_INV)
        grayImage, railPointList = self.GetRailCountour(grayImage)
        if railPointList != NULL:
            grayImage, railPointList = self.SortRailPointList(
                grayImage, railPointList)
        cv2.imshow(self.MASKED_WINDOW_NAME, grayImage)

    def GetRailCountour(self, grayImage):
        contours, hierarchy = cv2.findContours(
            grayImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return grayImage, NULL

        rect = cv2.minAreaRect(contours[0])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        grayImage = cv2.cvtColor(grayImage, cv2.COLOR_GRAY2BGR)
        grayImage = cv2.drawContours(grayImage, [box], 0, (0, 0, 255), 2)

        railPointList = []
        for elm in box:
            railPointList.append(((elm.tolist())[0], (elm.tolist())[1]))

        return grayImage, railPointList

    def SortRailPointList(self, grayImage, railPointList):

        p0x, p0y = railPointList[0]
        p1x, p1y = railPointList[1]
        p2x, p2y = railPointList[2]
        p3x, p3y = railPointList[3]

        distFromOriginList = [0] * 4
        distFromOriginList[0] = (
            math.sqrt(abs(p0x)**2 + abs(p0y)**2), p0x, p0y)
        distFromOriginList[1] = (
            math.sqrt(abs(p1x)**2 + abs(p1y)**2), p1x, p1y)
        distFromOriginList[2] = (
            math.sqrt(abs(p2x)**2 + abs(p2y)**2), p2x, p2y)
        distFromOriginList[3] = (
            math.sqrt(abs(p3x)**2 + abs(p3y)**2), p3x, p3y)
        distFromOriginList = sorted(distFromOriginList)

        var, x, y = distFromOriginList[0]
        newlyRailPointList = [0] * 4
        newlyRailPointList[0] = (x, y)

        distFromBaseList = [0] * 4
        distFromBaseList[0] = (
            math.sqrt(abs(x - p0x)**2 + abs(y - p0y)**2), p0x, p0y)
        distFromBaseList[1] = (
            math.sqrt(abs(x - p1x)**2 + abs(y - p1y)**2), p1x, p1y)
        distFromBaseList[2] = (
            math.sqrt(abs(x - p2x)**2 + abs(y - p2y)**2), p2x, p2y)
        distFromBaseList[3] = (
            math.sqrt(abs(x - p3x)**2 + abs(y - p3y)**2), p3x, p3y)
        distFromBaseList = sorted(distFromBaseList)
        distFromBaseList.pop(0)

        newlyRailPointList[1] = (
            distFromBaseList[0][1], distFromBaseList[0][2])
        newlyRailPointList[2] = (
            distFromBaseList[1][1], distFromBaseList[1][2])
        newlyRailPointList[3] = (
            distFromBaseList[2][1], distFromBaseList[2][2])

        print(newlyRailPointList)

        grayImage = cv2.circle(
            grayImage, newlyRailPointList[0], 5, (255, 255, 0), -1)  # aqua
        grayImage = cv2.circle(
            grayImage, newlyRailPointList[1], 5, (0, 255, 0), -1)  # lime
        grayImage = cv2.circle(
            grayImage, newlyRailPointList[2], 5, (255, 0, 0), -1)  # blue
        grayImage = cv2.circle(
            grayImage, newlyRailPointList[3], 5, (0, 255, 255), -1)  # yellow

        return grayImage, newlyRailPointList

    def CalcCenterOfGravity(self):
        pass

    def CalcRailDistance(self, railPointList):

        railDistance = 0
        return railDistance

    # ノズルとダンゴムシとの重心距離を計算して距離を返す。
    def CalcDistance(self, center_of_nozzle, center_of_gravity):
        _distance = 0
        self.distance = _distance

    # ダンゴムシの中心を計算する
    def calc_center_of_gravity(self):
        _center_of_gravity = 0
        return _center_of_gravity

    # ノズルの中心位置を計算する
    def calc_center_of_nozzle(self):
        _calc_center_of_nozzle = 0
        return _calc_center_of_nozzle

    # cameraの映像を表示する
    def camera_window(self):
        delay = 1
        window_name = "frame"
        self.__cam = cv2.VideoCapture(1+cv2.CAP_DSHOW)  # 引数に番号だけ渡すのではダメだった模様

        if not self.__cam.isOpened():
            return print("failure video capture")

        while (True):
            ret, frame = self.__cam.read()
            cv2.imshow(window_name, frame)
            if not ret:
                continue
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

        cv2.destroyWindow(window_name)
        self.__cam.release()

    def __del__(self):
        self.__cam.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    v = Vision()
    # v.camera_window()
    v.MakeWindow()
    while (True):
        v.UpdateWindow()
