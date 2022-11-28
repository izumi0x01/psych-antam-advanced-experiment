# クラスのインポート
from asyncio.windows_events import NULL
import myAnalyze
import myVision
import mySerial
import myInputWindow
import sys
import tkinter as tk

try:
    # initialize
    _mySerial = mySerial.Serial()
    _mySerial.ConfirmateComPort()
    _myAnalyze = myAnalyze.Analyze()
    # myVision = myVision.Vision()
    root = tk.Tk()
    _myInputWindow = myInputWindow.InputWindow(root, _mySerial, _myAnalyze)

    while True:

        _myInputWindow.update_idletasks()
        _myInputWindow.update()

        # mySerial.SendSerialData()

        # data: dict = mySerial.GetSerialData()

        # if data != NULL & _myAnalyze.IsFileOpened():
        #     myAnalyze.AddRow(data)

    # Ctrl-Cでプログラムの終了

except KeyboardInterrupt:
    del _myAnalyze
    print("[exit](Ctrl-C interrupted)")
    sys.exit()

myVision.camera_window()
