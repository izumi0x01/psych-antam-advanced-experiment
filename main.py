#クラスのインポート
from asyncio.windows_events import NULL
import myAnalyze
import myVision
import mySerial

_myVision = myVision.Vision()
_myVision.camera_window()

_mySerial = mySerial.Serial()