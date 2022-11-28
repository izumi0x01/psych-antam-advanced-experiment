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
        self._error: int = 0
        self._data: dict = NULL
        self._openSerial = NULL

    def ConfirmateComPort(self):
        ports = list(list_ports.comports())
        print("[COMPORT_CONFIGURATION]")
        for p in ports:
            try:
                openserial = serial.Serial(p.device)
                print(p.device, "can use.")
                openserial.close()
                if p.manufacturer == "Arduino LLC (www.arduino.cc)":
                    self._openSerial = serial.Serial(
                        p.device, self.BOUDRATE, timeout=None)
                    print("(", p.device, "is ready for arduino", ")")
            except (OSError, serial.SerialException):
                print(p.device, "can'kt use.")
        if self._openSerial == NULL:
            print("[exit](Arduino is not found)")

    def SendSerialData(self, inputPressure=NULL, inputDeltaTime=NULL):

        if self._openSerial == NULL:
            print("[Port is not opened]")
            return NULL

        sendData = {'P': inputPressure, 'D': inputDeltaTime}
        self._openSerial.writelines(sendData)

        while self._openSerial.out_waiting > 0:
            continue

    def PrintSerialData(self):
        if self._openSerial == NULL:
            print("[Port is not opened]")
            return NULL

        while True:
            self.ReadSerialData()
            if self._data != NULL:
                print("PC時間:", datetime.datetime.now(), ",生データ:", self._data)
            else:
                continue

    def GetSerialData(self):
        if self._openSerial == NULL:
            print("[Port is not opened]")
            return NULL

        while True:
            self.ReadSerialData()
            if self._data != NULL:
                self._error = self._data['Err']
                self._data.pop('Err')
                return self._data
            else:
                return NULL

    # マイコンからのシリアル通信のデータがあれば、それを読み取る.
    def ReadSerialData(self):
        if self._openSerial.in_waiting > 0:
            rawData = self._openSerial.readline()
            decodedData = rawData.decode()
            self._data = json.loads(decodedData)
        else:
            self._data = NULL

    def WinSerialPortsDescripition(self):
        comports = list_ports.comports()
        if not comports:
            print("ポートが見つからない！残念！")
            return NULL
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
            self._openSerial.close()
        except AttributeError:
            pass


if __name__ == "__main__":
    s = Serial()

    # windowsで、ポートの利用状況を詳しく調べる。
    # s.WinSerialPortsDescripition()

    s.PrintSerialData()
