from ast import While
from turtle import update
import unicurses
import cv2
import sys


class Vision:

    X, Y = 120, 40
    H, W = 520, 440
    FPS = 10
    MAIN_WINDOW_NAME = "RAW"
    MASKED_WINDOW_NAME = "Masked"

    def __init__(self):
        self.__threshold: int = 60
        self.distance = 0

    def MakeWindow(self):
        cv2.namedWindow(self.MASKED_WINDOW_NAME)
        cv2.createTrackbar("slesh_hold", self.MASKED_WINDOW_NAME, self.__threshold,
                           255, self.TrackBarChangedEvent)
        self.__cam = cv2.VideoCapture(1+cv2.CAP_DSHOW)  # 引数に番号だけ渡すのではダメだった模様
        if not self.__cam.isOpened():
            return print("failure video capture")
        self.__cam.set(cv2.CAP_PROP_FPS, self.FPS)

    def TrackBarChangedEvent(self, position):
        self.__threshold = cv2.getTrackbarPos(
            "slesh_hold", self.MASKED_WINDOW_NAME)

    def UpdateWindow(self):
        ret, frame1 = self.__cam.read()
        k = cv2.waitKey(1) & 0xFF  # 描画の待ち時間設定
        frame = frame1[self.Y:self.Y+self.H,
                       self.X:self.X+self.W]  # frame全体から画像の抽出
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, mask_image = cv2.threshold(
            gray, self.__threshold, 255, cv2.THRESH_BINARY_INV)

        cv2.imshow(self.MASKED_WINDOW_NAME, mask_image)
        cv2.imshow(self.MAIN_WINDOW_NAME, frame)

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
