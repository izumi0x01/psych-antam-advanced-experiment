from ast import While
import unicurses 
import cv2
import sys

class Vision:

  def __init__(self):
    self.distance = 0


  def getDistance(self):
    return self.distance

  # ノズルとダンゴムシとの重心距離を計算して距離を返す。
  def calc_distance(self,center_of_nozzle,center_of_gravity):
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
    cam = cv2.VideoCapture(1+cv2.CAP_DSHOW) #引数に番号だけ渡すのではダメだった模様
    
    if not cam.isOpened():
      return print("failure video capture")

    while(True):
      ret, frame = cam.read()
      cv2.imshow(window_name,frame)
      if not ret:
        continue
      if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

    cv2.destroyWindow(window_name)
    cam.release()

v = Vision()
v.camera_window()
    