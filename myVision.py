from ast import While
from asyncio.windows_events import NULL
from pickle import NONE
from turtle import distance, update
from cv2 import contourArea
import numpy as np
import cv2
from PIL import Image
import sys
import math
import copy
import datetime


class Vision:

    FPS = 10
    MAIN_WINDOW_NAME = "RAW"
    BINARY_WINDOW_NAME = "Binary"
    MASKED_WINDOW_NAME = "Masked"
    WINDOW_HEIGHT = 0
    WINDOW_WIDTH = 0

    def __init__(self):
        self.__threshold: int = 200
        self.distance = 0
        self.__railPointList = NULL

    def MakeWindow(self):
        cv2.namedWindow(self.BINARY_WINDOW_NAME)
        cv2.createTrackbar("slesh_hold", self.BINARY_WINDOW_NAME, self.__threshold,
                           255, self.SleshHoldChangedEventHandler)
        self.__cam = cv2.VideoCapture(1+cv2.CAP_DSHOW)  # 引数に番号だけ渡すのではダメだった模様
        if not self.__cam.isOpened():
            return print("failure video capture")
        self.__cam.set(cv2.CAP_PROP_FPS, self.FPS)
        self.WINDOW_HEIGHT = int(self.__cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.WINDOW_WIDTH = int(self.__cam.get(cv2.CAP_PROP_FRAME_WIDTH))

    def SleshHoldChangedEventHandler(self, position):
        self.__threshold = cv2.getTrackbarPos(
            "slesh_hold", self.BINARY_WINDOW_NAME)

    def UpdateWindow(self):
        # 描画の待ち時間設定
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            sys.exe()
        ret, frame = self.__cam.read()
        if not ret:
            return NULL
        # frame全体から画像の抽出
        grayImage = self.ToBinaryImage(frame)
        (grayImage, railPointList) = self.GetRailCountour(grayImage)
        if railPointList != NULL:
            (grayImage, railPointList) = self.SortRailPointList(
                grayImage, railPointList)
            self.__railPointList = copy.deepcopy(railPointList)

        if self.__railPointList != NULL:
            # print(str(datetime.datetime.now()) + str(self.__railPointList))
            self.CalcRailWidthDistance(frame, self.__railPointList)
            self.CalcRailHeightDistance(frame, self.__railPointList)
            self.DrawRailFlamePoint(frame, self.__railPointList)
            cv2.imshow(self.MAIN_WINDOW_NAME, frame)
            self.MakeRailMask(grayImage, frame, self.__railPointList)

        cv2.imshow(self.BINARY_WINDOW_NAME, grayImage)

    def ToBinaryImage(self, frame):
        ret, grayImage = cv2.threshold(
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), self.__threshold, 255, cv2.THRESH_BINARY_INV)
        grayImage = cv2.adaptiveThreshold(
            grayImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize=21, C=10)
        return grayImage

    def GetRailCountour(self, grayImage):
        contours, hierarchy = cv2.findContours(
            grayImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # approx_contours = []
        # for i, cnt in enumerate(contours):
        #     # 輪郭の周囲の長さを計算する。
        #     arclen = cv2.arcLength(cnt, True)
        #     # 輪郭を近似する。
        #     approx_cnt = cv2.approxPolyDP(
        #         cnt, epsilon=0.005 * arclen, closed=True)
        #     approx_contours.append(approx_cnt)
        # triangles = list(filter(lambda x: len(x) == 4, approx_contours))
        contours = list(filter(lambda x: (cv2.contourArea(
            x) > 8000 and cv2.contourArea(x) < 18000), contours))
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
        if distFromBaseList[1][2] <= distFromBaseList[2][2]:
            newlyRailPointList[2] = (
                distFromBaseList[1][1], distFromBaseList[1][2])
            newlyRailPointList[3] = (
                distFromBaseList[2][1], distFromBaseList[2][2])
        elif distFromBaseList[1][2] > distFromBaseList[2][2]:
            newlyRailPointList[3] = (
                distFromBaseList[1][1], distFromBaseList[1][2])
            newlyRailPointList[2] = (
                distFromBaseList[2][1], distFromBaseList[2][2])

        # print(newlyRailPointList)

        return grayImage, newlyRailPointList

    def DrawRailFlamePoint(self, grayImage, railPointList):
        grayImage = cv2.circle(
            grayImage, railPointList[0], 5, (255, 255, 0), -1)  # aqua
        grayImage = cv2.circle(
            grayImage, railPointList[1], 5, (0, 255, 0), -1)  # lime
        grayImage = cv2.circle(
            grayImage, railPointList[2], 5, (255, 0, 0), -1)  # blue
        grayImage = cv2.circle(
            grayImage, railPointList[3], 5, (0, 255, 255), -1)  # yellow

    def CalcCenterOfGravity(self):
        pass

    def CalcRailWidthDistance(self, grayImage, railPointList=[]):
        railWidthDistance = 0
        railWidthDistance: float = math.sqrt(
            abs(railPointList[2][0] - railPointList[0][0] + 1)**2 + abs(railPointList[2][1] - railPointList[1][1])**2 + 1)
        text = "rail width : " + \
            str(int(railWidthDistance))
        coordinates = (50, 50)
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (255, 0, 255)
        thickness = 2
        grayImage = cv2.putText(grayImage, text, coordinates,
                                font, fontScale, color, thickness, cv2.LINE_AA)
        return railWidthDistance

    def CalcRailHeightDistance(self, grayImage, railPointList=[]):
        railHeightDistance = 0
        railHeightDistance: float = math.sqrt(
            abs(railPointList[1][0] - railPointList[0][0] + 1)**2 + abs(railPointList[1][1] - railPointList[0][1])**2 + 1)
        text = "rail height pixel : " + str(int(railHeightDistance))
        coordinates = (50, 100)
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (255, 0, 255)
        thickness = 2
        grayImage = cv2.putText(grayImage, text, coordinates,
                                font, fontScale, color, thickness, cv2.LINE_AA)
        return railHeightDistance

    # ダンゴムシの重心を検出する
    def MakeRailMask(self, grayImage, rawImage, railPointList=[]):
        (x0, y0) = (min(railPointList[0][0], railPointList[1][0]),
                    min(railPointList[0][1], railPointList[2][1]))
        editedRawImage = rawImage[y0: max(railPointList[1][1], railPointList[3][1]),
                                  x0: max(railPointList[2][0], railPointList[3][0])]

        npbox = np.array([[railPointList[0][0], railPointList[0][1]],
                          [railPointList[2][0], railPointList[2][1]],
                          [railPointList[3][0], railPointList[3][1]],
                          [railPointList[1][0], railPointList[1][1]]])
        npbox = np.int0(npbox)
        # print(npbox)

        mask = np.ones_like(grayImage)
        cv2.drawContours(mask, [npbox], -1,
                         color=(255, 255, 255), thickness=-1)
        mask = mask[y0: max(railPointList[1][1], railPointList[3][1]),
                    x0: max(railPointList[2][0], railPointList[3][0])]
        # 背景画像のうち、合成する領域
        splitedMask = cv2.split(mask)
        if len(splitedMask) == 3:
            mask, g_, r_ = splitedMask
            editedRawImage[mask == 1] = [0, 0, 0]

        if editedRawImage.shape[0] != 0 and editedRawImage.shape[1] != 0:
            cv2.imshow(self.MASKED_WINDOW_NAME, editedRawImage)

    def CalcDangomusiMoment(self):
        pass
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
