from asyncio.windows_events import NULL
import pstats
import sys
import tkinter as tk
import tkinter.ttk as ttk
import time


class InputWindow(tk.Frame):

    FRAME_PADX: int = 30
    FRAME_PADY: int = 15
    FRAME_SIZEX: int = 1000
    FRAME_SIZEY: int = 300
    BUTTON_SIZEX: int = 10
    BUTTON_SIZEY: int = 30
    BUTTON_DISABLED_BG_COLOR: str = "whitesmoke"
    INJECTEAIR_BUTTON_BG_COLOR: str = "lightblue"
    SENDDATA_BUTTON_BG_COLOR: str = "lightpink"
    START_BUTTON_BG_COLOR: str = "lightgreen"
    STOP_BUTTON_BG_COLOR: str = "lemonchiffon"

    @property
    def InputPressure(self):
        return self.__pressure

    @InputPressure.setter
    def InputPressure(self, value):
        if value == '':
            self.__pressure = 0
            self.sendDataStateLabel["text"] += '[設定圧力に無効な入力]'
        elif int(value) > 1000:
            self.__pressure = 0
            self.sendDataStateLabel["text"] += '[設定圧力は1000pa以下]'
        elif int(value) < 0:
            self.__pressure = 0
            self.sendDataStateLabel["text"] += '[設定圧力は正値]'
        else:
            self.__pressure = value

    @property
    def InputDeltaTime(self):
        return self.__deltatime

    @InputDeltaTime.setter
    def InputDeltaTime(self, value):
        if value == '':
            self.__deltatime = 0
            self.sendDataStateLabel["text"] += '[設定時間に無効な入力]'
        elif int(value) > 1000:
            self.__deltatime = 0
            self.sendDataStateLabel["text"] += '[設定時間は1000s以下]'
        elif int(value) < 0:
            self.__deltatime = 0
            self.sendDataStateLabel["text"] += '[設定時間は正値]'
        else:
            self.__deltatime = value

    def __init__(self, root, mySerial, myAnalyze):
        super().__init__(root)

        self.__myAnalyze = myAnalyze
        self.__root = root
        self.__mySerial = mySerial
        self.__pressure: int = 0
        self.__deltatime: int = 0

        root.option_add('*font', 'ＭＳゴシック 22')
        root.title("装置との通信用窓")

        # ウィンドウの閉じるボタンは無効にする
        root.protocol('WM_DELETE_WINDOW', (lambda: 'pass')())

        # 設定
        self.tf1 = tk.Frame(root, relief='groove',
                            bd=5)
        self.tf1.grid(column=0, row=0, padx=self.FRAME_PADX,
                      pady=self.FRAME_PADY, sticky=tk.E + tk.W)
        # self.tf1.place(height=200, width=500)

        # 1,送信ボタン
        self.sendDataButton = tk.Button(
            self.tf1, text='データ送信', bg=self.SENDDATA_BUTTON_BG_COLOR, bd=4, width=15)
        self.sendDataButton.grid(
            padx=10, pady=10, column=0, row=0, sticky='w')
        self.sendDataButton.bind(
            "<Button-1>", self.DataSendButtonEventHandler)

        # 1,送信状態表示ラベル
        self.sendDataStateLabel = tk.Label(
            self.tf1, text='', fg="red")
        self.sendDataStateLabel.grid(
            padx=10, pady=10, column=1, columnspan=2, row=0, sticky='w')

        # 入力圧力の設定
        self.pLabel = tk.Label(self.tf1, text='設定圧力[pa]')
        self.pLabel.grid(padx=10, pady=10, column=0, row=1, sticky='e')

        self.pEntry = tk.StringVar()
        self.pEntry.set('')
        self.pEntryBox = tk.Entry(
            self.tf1, textvariable=self.pEntry, bd=5, relief='groove')
        # self.pEntry.bind('<Return>', self.entf1unc)
        self.pEntryBox.grid(padx=10, column=1, row=1, sticky='w')

        # 入力時間の設定
        self.dtLabel = tk.Label(
            self.tf1, text='設定時間[ms]')
        self.dtLabel.grid(padx=10, pady=10, column=0, row=2, sticky='e')

        self.dtEntry = tk.StringVar()
        self.dtEntry.set('')
        self.dtEntryBox = tk.Entry(
            self.tf1, textvariable=self.dtEntry, bd=5, relief='groove')
        # self.dtEntry.bind('<Return>', self.entf1unc)
        self.dtEntryBox.grid(padx=10, column=1, row=2, sticky='w')

        # border1 = ttk.Separator(root, orient="horizontal")
        # border1.grid(column=0, columnspan=2, row=3, sticky="ew")

        # 設定
        self.tf2 = tk.Frame(root, relief='groove', bd=5)
        self.tf2.grid(column=0, row=1, padx=self.FRAME_PADX,
                      pady=self.FRAME_PADY, sticky=tk.E + tk.W)

        # 2,計測開始ボタン
        self.startButton = tk.Button(
            self.tf2, text='計測開始', bg=self.BUTTON_DISABLED_BG_COLOR, bd=4, width=15)
        self.startButton.grid(padx=10, pady=10, column=0, row=0, sticky='w')
        self.startButton.bind("<Button-1>", self.StartButtonEventHandler)
        self.startButton["state"] = "disabled"

        # 　ファイル名ラベル
        self.fileNameLabel = tk.Label(
            self.tf2, text='ファイル名')
        self.fileNameLabel.grid(padx=10, pady=10, column=0, row=1, sticky='e')

        # 2,計測状態表示ラベル
        self.measuringStateLabel = tk.Label(
            self.tf2, text='', fg="black")
        self.measuringStateLabel.grid(
            padx=10, pady=10, column=1, columnspan=2, row=1, sticky='w')

        # 3,計測終了ボタン
        self.stopButton = tk.Button(
            self.tf2, text='計測終了', bg=self.BUTTON_DISABLED_BG_COLOR, bd=4, width=15)
        self.stopButton.grid(padx=10, pady=10, column=0, row=5, sticky='w')
        self.stopButton.bind("<Button-1>", self.StopButtonEventHandler)
        self.stopButton["state"] = "disabled"

        # 設定
        self.tf3 = tk.Frame(root, relief='groove', bd=5)
        self.tf3.grid(column=0, row=2, padx=self.FRAME_PADX,
                      pady=self.FRAME_PADY, sticky=tk.E + tk.W)

        # 4,空気発射ボタン
        self.injectAirButton = tk.Button(
            self.tf3, text='空気発射', bg=self.BUTTON_DISABLED_BG_COLOR, bd=4, width=15)
        self.injectAirButton.grid(
            padx=10, pady=10, column=0, row=0, sticky='w')
        self.injectAirButton.bind("<Button-1>", self.InjectAirEventHandler)
        self.injectAirButton["state"] = "disable"

    def DataSendButtonEventHandler(self, event):
        if self.sendDataButton["state"] == "disabled":
            return NULL

        self.sendDataStateLabel["text"] = ''
        self.InputPressure = self.pEntry.get()
        self.InputDeltaTime = self.dtEntry.get()
        if (int(self.InputPressure) == 0) or (int(self.InputDeltaTime) == 0):
            self.stopButton["state"] = "disabled"
            self.stopButton["bg"] = self.BUTTON_DISABLED_BG_COLOR
            self.startButton["state"] = "disabled"
            self.startButton["bg"] = self.BUTTON_DISABLED_BG_COLOR
            self.injectAirButton["state"] = "disabled"
            self.injectAirButton["bg"] = self.BUTTON_DISABLED_BG_COLOR
            return NULL

        self.__mySerial.SendSerialData(self.InputPressure, self.InputDeltaTime)

        self.startButton["state"] = "normal"
        self.startButton["bg"] = self.START_BUTTON_BG_COLOR
        self.injectAirButton["state"] = "normal"
        self.injectAirButton["bg"] = self.INJECTEAIR_BUTTON_BG_COLOR

    def StartButtonEventHandler(self, event):
        if self.startButton["state"] == "disabled":
            return NULL

        print("[I'm measuring now...]")
        filename = self.__myAnalyze.MakeFile(
            self.InputPressure, self.InputDeltaTime)
        self.measuringStateLabel["text"] = filename

        self.sendDataButton["state"] = "disabled"
        self.sendDataButton["bg"] = self.BUTTON_DISABLED_BG_COLOR
        self.startButton["state"] = "disabled"
        self.startButton["bg"] = self.BUTTON_DISABLED_BG_COLOR
        self.stopButton["state"] = "normal"
        self.stopButton["bg"] = self.STOP_BUTTON_BG_COLOR

    def StopButtonEventHandler(self, event):
        if self.stopButton["state"] == "disabled":
            return NULL

        print("[Stop measuring]")
        self.sendDataButton["state"] = "normal"
        self.sendDataButton["bg"] = self.SENDDATA_BUTTON_BG_COLOR

        if self.__myAnalyze.IsFileOpened():
            self.__myAnalyze.CloseFile()

        self.stopButton["state"] = "disabled"
        self.stopButton["bg"] = self.BUTTON_DISABLED_BG_COLOR

    def InjectAirEventHandler(self, event):
        if self.injectAirButton["state"] == "disabled":
            return NULL
        elif self.injectAirButton["state"] == "normal":
            self.injectAirButton["bg"] = self.INJECTEAIR_BUTTON_BG_COLOR
            print("[Inject Air!]")

    def __del__(self):
        self.__root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    myapp = InputWindow(root)
    myapp.mainloop()
