from asyncio.windows_events import NULL
# from urllib.request import HTTPPasswordMgrWithDefaultRealm
import serial
from serial.tools import list_ports
import json
import datetime
import sys
import glob


class Serial:
    BOUDRATE: int = 115200
    COMPORT: str = "COM15"

    # RTS:Request to Send.送信要求。DSRと対になる信号でこちらの装置が正常に動作していること、すなわち電源が入っていることを相手に知らせるためのものです。正常に動作しているときには論理を"1"にします。
    # DTR:Data Terminal Ready。送信要求信号を意味します。相手からこちらにデータを送る要求を行います。論理を"0"にすると相手はデータを送ることを中断します

    def __init__(self):
        self._data: dict = {}
        ports = list(list_ports.comports())
        print("--------COMPORT CONFIGURATION--------")
        for p in ports:
          try:
            openserial = serial.Serial(p.device)
            print(p.device , "can use.")
            openserial.close()
            if p.manufacturer == "Arduino LLC (www.arduino.cc)":
              #print("this is arduino.")
              self.openSerial = serial.Serial(
                p.device, self.BOUDRATE, timeout=None)
              print("(",p.device,"is ready for arduino",")")
            

          except(OSError, serial.SerialException):
            print(p.device, "can't use.")
        print("-------------------------------------")
        

    # データが一列ずつ送られてくる。その送られたデータを返り値として送る。
    # 送るべきデータがシリアルポートに到着すれば、文字列のデータを返り値として送る。

    def ReadSerialData(self):
        if self._openSerail.in_waiting > 0:
            rawData = self._openSerail.readline()
            decodedData = rawData.decode()
            self._data = json.loads(decodedData)
        else:
            self._data = NULL

    def PrintData(self):
        while 1:
            self.ReadSerialData()
            if self._data != NULL:
                print("PC時間:", end="")
                print(datetime.datetime.now(), end="")
                print(",生データ:", end="")
                print(self._data)
            else:
                continue

    def WinSerialPortsDescripition(self):
        comports = list_ports.comports()
        if not comports:
            print("ポートが見つかりません")
            return
        ports = list(comports)
        for p in ports:
            print(p)
            print(" device       :", p.device)
            print(" name         :", p.name)
            print(" description  :", p.description)
            print(" hwid         :", p.hwid)
            print(" vid          :", p.vid)
            print(" pid          :", p.pid)
            print(" serial_number:", p.serial_number)
            print(" location     :", p.location)
            print(" manufactuer  :", p.manufacturer)
            print(" product      :", p.product)
            print(" interface    :", p.interface)
            print("")

    def SerialPorts(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def __del__(self):
      try:
        self.openSerial.close()
      except AttributeError:
        pass


if __name__ == "__main__":
    s = Serial()
    
    # windowsで、ポートの利用状況を詳しく調べる。
    #s.WinSerialPortsDescripition()

    # s.PrintData()
