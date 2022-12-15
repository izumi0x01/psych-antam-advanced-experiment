# クラスのインポート
from asyncio.windows_events import NULL
import myCSV
import myVision
import mySerial
import myWindow
import sys
import tkinter as tk
import copy

try:
    # initialize
    _mySerial = mySerial.Serial()
    _mySerial.ConfirmateComPort()
    _myCSV = myCSV.CSV()
    _myVision = myVision.Vision()
    root = tk.Tk()
    _myWindow = myWindow.Window(root, _mySerial, _myCSV, _myVision)
    _myVision.MakeWindow()

    while True:

        _myWindow.update_idletasks()
        _myWindow.update()

        _myVision.UpdateWindow()

        if _mySerial.ArduinoPort == NULL:
            continue

        # copy()メソッドで辞書を作らないと怒られる
        decodedData: dict = _mySerial.ReadData()

        if _myWindow.IsMeasuring == False:
            continue

        if (decodedData == None) or (decodedData == NULL):
            continue
        print(decodedData)
        reshapedData = _mySerial.ReshapeData(copy.copy(decodedData))

        # _mySerial.PrintData(copy.copy(reshapedData))

        if (reshapedData != None) and (reshapedData != NULL) and (_myCSV.IsFileOpened()):
            # _mySerial.PrintData(copy.copy(reshapedData))
            if (_myVision.DANGOMUSI_X == 0) or (_myVision.DANGOMUSI_Y == 0) or (_myVision.NOZLE_DANGOMUSI_DISTANCE == 0):
                continue
            _myCSV.AddRow(reshapedData, _myVision.DANGOMUSI_X,
                          _myVision.DANGOMUSI_Y, _myVision.NOZLE_DANGOMUSI_DISTANCE)

# Ctrl-Cでプログラムの終了
except KeyboardInterrupt:
    del _myCSV
    print("[exit](Ctrl-C interrupted)")
    sys.exit()

myVision.camera_window()
