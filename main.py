# クラスのインポート
from asyncio.windows_events import NULL
import myCSV
import myVision
import mySerial
import myWindow
import sys
import tkinter as tk

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

        # mySerial.SendSerialData()

        # data: dict = mySerial.GetSerialData()

        # if data != NULL & _myCSV.IsFileOpened():
        #     myCSV.AddRow(data)

    # Ctrl-Cでプログラムの終了

except KeyboardInterrupt:
    del _myCSV
    print("[exit](Ctrl-C interrupted)")
    sys.exit()

myVision.camera_window()
