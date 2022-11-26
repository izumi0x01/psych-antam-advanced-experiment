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
    mySerial = mySerial.Serial()
    mySerial.ConfirmateComPort()
    # myAnalyze = myAnalyze.Analyze()
    root = tk.Tk()
    myapp = myInputWindow.InputWindow(root, mySerial)
    # myVision = myVision.Vision()

    print("[I'm measuring now...]")

    while True:

        myapp.update_idletasks()
        myapp.update()

        # mySerial.WriteSerialData()

        # data: dict = mySerial.GetSerialData()
        # if data != NULL:
        #     myAnalyze.writeRowToCSV(data)

    # Ctrl-Cでプログラムの終了

except KeyboardInterrupt:
    print("[exit](Ctrl-C interrupted)")
    sys.exit()

myVision.camera_window()
