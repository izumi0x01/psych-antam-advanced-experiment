from asyncio.windows_events import NULL
from multiprocessing.sharedctypes import Value
# from urllib.request import HTTPPasswordMgrWithDefaultRealm
import serial
from serial.tools import list_ports
import json
import datetime
import sys
import glob
import copy


class Serial:
    BOUDRATE: int = 115200
    COMPORT: str = "COM15"
    SENDING_STATE: bool = False

    # RTS:Request to Send.送信要求。DSRと対になる信号でこちらの装置が正常に動作していること、すなわち電源が入っていることを相手に知らせるためのものです。正常に動作しているときには論理を"1"にします。
    # DTR:Data Terminal Ready。送信要求信号を意味します。相手からこちらにデータを送る要求を行います。論理を"0"にすると相手はデータを送ることを中断します

    @property
    def ArduinoPort(self):
        return self.__openSerial

    @ArduinoPort.setter
    def ArduinoPort(self, value):
        self.__openSerial = value

    def __init__(self):
        self._error: int = 0
        data: dict = NULL
        self.__openSerial = NULL

    def ConfirmateComPort(self):
        ports = list(list_ports.comports())
        print("\n[COMPORT_CONFIGURATION]")
        for p in ports:
            try:
                openserial = serial.Serial(p.device)
                print(p.device, "can use.")
                openserial.close()
                if p.manufacturer == "Arduino LLC (www.arduino.cc)":
                    self.__openSerial = serial.Serial(
                        p.device, self.BOUDRATE, timeout=None)
                    print("(", p.device, "is ready for arduino", ")")
            except (OSError, serial.SerialException):
                print(p.device, "can't use.")
        if self.__openSerial == NULL:
            print("[Arduino is not found]")
        print("\n")

    def SendInitializeData(self, inputPressure: int = 0, inputDeltaTime: int = 0):

        if self.__openSerial == NULL:
            print("[Port is not opened]")
            return NULL

        if (inputPressure == 0) or (inputDeltaTime == 0):
            print("[Value is Incorrect]")
            return NULL

        sendData = {'p': inputPressure, 'd': inputDeltaTime}
        sendDataString = str(sendData)

        self.__openSerial.reset_input_buffer()
        self.__openSerial.reset_output_buffer()

        # .writelineだとエラー出るっぽい。->.writeにする。
        self.__openSerial.write(bytes(sendDataString, 'utf-8'))
        print("[Success to send Deltatime, Pressure]\n")

        while self.__openSerial.out_waiting > 0:
            continue

        self.__openSerial.reset_output_buffer()

    def SendStartMeasuringSignal(self):
        if self.__openSerial == NULL:
            print("[Port is not opened]")
            return NULL

        self.__openSerial.reset_input_buffer()
        self.__openSerial.reset_output_buffer()

        print("[measuring start signal sended]\n")
        self.__openSerial.write(bytes('1', 'utf-8'))
        while self.__openSerial.out_waiting > 0:
            continue

        self.__openSerial.reset_output_buffer()

    def SendInjectAirSignalFromVision(self):
        if self.__openSerial == NULL:
            print("[Port is not opened]")
            return NULL

        self.__openSerial.reset_input_buffer()
        self.__openSerial.reset_output_buffer()

        print("[Inject Air signal sended]\n")
        self.__openSerial.write(bytes('2', 'utf-8'))
        while self.__openSerial.out_waiting > 0:
            continue

        self.__openSerial.reset_output_buffer()

    def SendStopMeasuringSignal(self):
        if self.__openSerial == NULL:
            print("[Port is not opened]")
            return NULL

        self.__openSerial.reset_input_buffer()
        self.__openSerial.reset_output_buffer()

        print("[measuring stop signal sended]\n")
        self.__openSerial.write(bytes('3', 'utf-8'))

        while self.__openSerial.out_waiting > 0:
            continue

        self.__openSerial.reset_output_buffer()

    def SendInjectAirSignalFromWindow(self):
        if self.__openSerial == NULL:
            print("[Port is not opened]")
            return NULL

        self.__openSerial.reset_input_buffer()
        self.__openSerial.reset_output_buffer()

        print("[Inject Air Signal sended]\n")
        self.__openSerial.write(bytes('9', 'utf-8'))

        while self.__openSerial.out_waiting > 0:
            continue

        self.__openSerial.reset_output_buffer()

    # マイコンからのシリアル通信のデータがあれば、それを読み取る.
    def ReadData(self):
        if self.__openSerial.in_waiting > 0:
            rawData = self.__openSerial.readline()
            try:
                decodedData = rawData.decode()
                data = json.loads(decodedData)
            except json.JSONDecodeError:
                # data: dict = {"RECIEVE_TEXT": str(decodedData)}
                data: dict = NULL
                return data
        else:
            data: dict = NULL

        return data

    def ReshapeData(self, data):
        if data != NULL:
            self._error = int(data['Err'])
            data.pop('Err')
            return data
        elif data == None:
            return NULL

    def PrintData(self, data):
        if (data != NULL) and (data != None):
            print("PC時間:", datetime.datetime.now(), ",生データ:", data)

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
            self.__openSerial.close()
        except AttributeError:
            pass


if __name__ == "__main__":
    s = Serial()

    # windowsで、ポートの利用状況を詳しく調べる。
    s.WinSerialPortsDescripition()

    # s.PrintData()
