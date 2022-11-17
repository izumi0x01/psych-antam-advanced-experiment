# クラスのインポート
from asyncio.windows_events import NULL
import myAnalyze
import myVision
import mySerial
import sys

# initialize
myVision = myVision.Vision()
myAnalyze = myAnalyze.Analyze()
mySerial = mySerial.Serial()

try:
    print("[measuring]")
    while True:
        # serial通信でデータを取ってくる
        data: dict = mySerial.GetSerialData()
        # コンソール画面でデータの流れを見たい場合は、以下のコメントをコメントアウトする
        # mySerial.PrintSerialData()
        myAnalyze.writeRowToCSV(data)
except KeyboardInterrupt:
    # Ctrl-Cでプログラムの終了
    print("[exit](Ctrl-C interrupted)")
    sys.exit()

myVision.camera_window()
