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
    # myVision = myVision.Vision()
    root = tk.Tk()
    _myWindow = myWindow.Window(root, _mySerial, _myCSV)

    while True:

        _myWindow.update_idletasks()
        _myWindow.update()

        if _mySerial.ArduinoPort == NULL:
            continue

        # copy()メソッドで辞書を作らないと怒られる
        decodedData: dict = _mySerial.ReadData()
        reshapedData = _mySerial.ReshapeData(copy.copy(decodedData))
        # _mySerial.PrintData(copy.copy(reshapedData))

        if _myWindow.IsMeasuring == False:
            continue

        if (reshapedData != None) and (reshapedData != NULL) and (_myCSV.IsFileOpened()):
            # _mySerial.PrintData(copy.copy(reshapedData))
            print(reshapedData)
            _myCSV.AddRow(reshapedData)

# Ctrl-Cでプログラムの終了
except KeyboardInterrupt:
    del _myCSV
    print("[exit](Ctrl-C interrupted)")
    sys.exit()

myVision.camera_window()
