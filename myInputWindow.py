import pstats
import sys
import tkinter as tk
import tkinter.ttk as ttk
import time


class InputWindow(tk.Frame):

    @property
    def InputPressure(self):
        return self.__pressure

    @InputPressure.setter
    def InputPressure(self, value):
        if value != '':
            self.__pressure = value

    @property
    def InputDeltaTime(self):
        return self.__deltatime

    @InputDeltaTime.setter
    def InputDeltaTime(self, value):
        if value != '':
            self.__deltatime = value

    FRAME_PADX: int = 30
    FRAME_PADY: int = 15
    FRAME_SIZEX: int = 1000
    FRAME_SIZEY: int = 300
    BUTTON_SIZEX: int = 10
    BUTTON_SIZEY: int = 30

    def __init__(self, root, mySerial):
        super().__init__(root)

        self.__root = root
        self.__mySerial = mySerial
        self.__pressure: float = 0.0
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
            self.tf1, text='データ送信', bg='lightpink', bd=4, width=15)
        self.sendDataButton.grid(
            padx=10, pady=10, column=0, row=0, sticky='w')
        self.sendDataButton.bind(
            "<Button-1>", self.EditSendedDataStateLabelEventHandler)

        # 1,送信状態表示ラベル
        self.sendDataStateLabel = tk.Label(
            self.tf1, text='無効な入力値が入力されました', fg="red")
        self.sendDataStateLabel.grid(
            padx=10, pady=10, column=1, columnspan=2, row=0, sticky='w')

        # 入力圧力の設定
        self.pLabel = tk.Label(self.tf1, text='設定圧力[pa]')
        self.pLabel.grid(padx=10, pady=10, column=0, row=1, sticky='e')

        self.pEntry = tk.StringVar()
        self.pEntry.set('0')
        self.pEntryBox = tk.Entry(
            self.tf1, textvariable=self.pEntry, bd=5, relief='groove')
        # self.pEntry.bind('<Return>', self.entf1unc)
        self.pEntryBox.grid(column=1, row=1)

        # 入力時間の設定
        self.dtLabel = tk.Label(
            self.tf1, text='設定時間[ms]')
        self.dtLabel.grid(padx=10, pady=10, column=0, row=2, sticky='e')

        self.dtEntry = tk.StringVar()
        self.dtEntry.set('0')
        self.dtEntryBox = tk.Entry(
            self.tf1, textvariable=self.dtEntry, bd=5, relief='groove')
        # self.dtEntry.bind('<Return>', self.entf1unc)
        self.dtEntryBox.grid(column=1, row=2)

        # border1 = ttk.Separator(root, orient="horizontal")
        # border1.grid(column=0, columnspan=2, row=3, sticky="ew")

        # 設定
        self.tf2 = tk.Frame(root, relief='groove', bd=5)
        self.tf2.grid(column=0, row=1, padx=self.FRAME_PADX,
                      pady=self.FRAME_PADY, sticky=tk.E + tk.W)

        # 2,計測開始ボタン
        self.startButton = tk.Button(
            self.tf2, text='計測開始', bg='lightgreen', bd=4, width=15)
        self.startButton.grid(padx=10, pady=10, column=0, row=4, sticky='w')
        self.startButton.bind("<Button-1>", self.StartButtonEventHandler)

        # 2,計測状態表示ラベル
        self.sendDataStateLabel = tk.Label(
            self.tf2, text='無効な入力値が入力されました', fg="red")
        self.sendDataStateLabel.grid(
            padx=10, pady=10, column=1, columnspan=2, row=4, sticky='w')

        # 3,計測終了ボタン
        self.stopButton = tk.Button(
            self.tf2, text='計測終了', bg='lightyellow', bd=4, width=15)
        self.stopButton.grid(padx=10, pady=10, column=0, row=5, sticky='w')
        self.stopButton.bind("<Button-1>", self.StopButtonEventHandler)

        # 設定
        self.tf3 = tk.Frame(root, relief='groove', bd=5)
        self.tf3.grid(column=0, row=2, padx=self.FRAME_PADX,
                      pady=self.FRAME_PADY, sticky=tk.E + tk.W)

        # 4,空気発射ボタン
        self.injectAirButton = tk.Button(
            self.tf3, text='空気発射', bg='lightblue', bd=4, width=15)
        self.injectAirButton.grid(
            padx=10, pady=10, column=0, row=0, sticky='w')
        self.injectAirButton.bind("<Button-1>", self.InjectAirEventHandler)

    def SendButtonEventHandler(self, event):
        self.InputPressure = self.pEntry.get()
        self.InputDeltaTime = self.dtEntry.get()
        self.__mySerial.WriteSerialData(self.__pressure, self.__deltatime)

    def StartButtonEventHandler(self, event):
        pass

    def StopButtonEventHandler(self, event):
        pass

    def InjectAirEventHandler(self, event):
        pass

    def EditSendedDataStateLabelEventHandler(self, event):
        pass

    def __del__(self):
        self.__root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    myapp = InputWindow(root)
    myapp.mainloop()
