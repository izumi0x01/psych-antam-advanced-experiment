from ast import While
from turtle import update
from cv2 import contourArea
import unicurses
import numpy as np
import cv2
import sys


class Vision:

    X0, Y0 = 0, 0
    X1, Y1 = 0, 0
    FPS = 10
    MAIN_WINDOW_NAME = "RAW"
    MASKED_WINDOW_NAME = "Masked"

    def __init__(self):
        self.__threshold: int = 60
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
        ret, Frame = self.__cam.read()
        cv2.imshow(self.MAIN_WINDOW_NAME, Frame)
        # 描画の待ち時間設定
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            sys.exe()
        # frame全体から画像の抽出
        # Frame = Frame1[self.Y0:self.Y1, self.X0:self.X1]
        grayFrame = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
        ret, mask_image = cv2.threshold(
            grayFrame, self.__threshold, 255, cv2.THRESH_BINARY_INV)
        mask_image = self.GetRailCountour(mask_image)
        # cv2.imshow(self.MASKED_WINDOW_NAME, mask_image)

    def GetRailCountour(self, mask_image):
        # contours, hierarchy = cv2.findContours(
        #     grayFrame, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
        # for i, cnt in enumerate(contours):
        #     # print(f"contours[{i}].shape: {cnt.shape}")
        #     rect = cv2.minAreaRect(contours[i])
        #     box = cv2.boxPoints(rect)
        #     box = np.int0(box)
        #     grayFrame = cv2.drawContours(grayFrame, [box], 0, (0, 0, 255), 2)
        # return
        contours, hierarchy = cv2.findContours(
            mask_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return mask_image

        rect = cv2.minAreaRect(contours[0])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        print(box)
        mask_image = cv2.cvtColor(mask_image, cv2.COLOR_GRAY2BGR)
        mask_image = cv2.drawContours(mask_image, [box], 0, (0, 0, 255), 10)
        # cv2.rectangle(mask_image, (384, 0), (510, 128), (0, 255, 255), 3)

        cv2.imshow(self.MASKED_WINDOW_NAME, mask_image)
        return mask_image

    def CalcCenterOfGravity(self):
        pass

    def getDistance(self):
        return self.distance

    # ノズルとダンゴムシとの重心距離を計算して距離を返す。
    def calc_distance(self, center_of_nozzle, center_of_gravity):
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
