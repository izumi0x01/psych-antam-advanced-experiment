import sys
import tkinter as tk
import mySerial
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

    def __init__(self, root, _mySerial):
        super().__init__(root)

        self.__root = root
        self.__mySerial = _mySerial
        self.__pressure: float = 0.0
        self.__deltatime: int = 0

        root.option_add('*font', 'ＭＳゴシック 22')
        root.title("装置との通信用窓")

        # ウィンドウの閉じるボタンは無効にする
        root.protocol('WM_DELETE_WINDOW', (lambda: 'pass')())

        # 窓全体の設定
        self.tf = tk.Frame(root)
        self.tf.grid(column=0, row=0, padx=150, pady=100)

        # 入力圧力の設定
        self.pLabel = tk.Label(self.tf, text='設定圧力[pa] -> ')
        self.pLabel.grid(column=0, row=0, sticky='w')

        self.pEntry = tk.StringVar()
        self.pEntry.set('0')
        self.pEntryBox = tk.Entry(
            self.tf, textvariable=self.pEntry, bd=5, relief='groove')
        # self.pEntry.bind('<Return>', self.entfunc)
        self.pEntryBox.grid(column=1, row=0)

        # 入力時間の設定
        self.dtLabel = tk.Label(
            self.tf, text='設定時間[ms] -> ')
        self.dtLabel.grid(column=0, row=1, sticky='w')

        self.dtEntry = tk.StringVar()
        self.dtEntry.set('0')
        self.dtEntryBox = tk.Entry(
            self.tf, textvariable=self.dtEntry, bd=5, relief='groove')
        # self.dtEntry.bind('<Return>', self.entfunc)
        self.dtEntryBox.grid(column=1, row=1)

        # エラー表示ラベル
        self.errorLabel = tk.Label(
            self.tf, text='無効な入力値が入力されました', fg="red")
        self.errorLabel.grid(column=0, columnspan=2, row=2, sticky='e')

        # 送信ボタン
        self.Button = tk.Button(
            self.tf, text='送信', bg='lightpink', bd=2)
        self.Button.grid(column=0, columnspan=2, row=3, sticky='e')
        self.Button.bind("<Button-1>", self.SendButtonEventHandler)

    def SendButtonEventHandler(self, event):
        self.InputPressure = self.pEntry.get()
        self.InputDeltaTime = self.dtEntry.get()
        self.__mySerial.WriteSerialData(self.__pressure, self.__deltatime)

    def __del__(self):
        self.__root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    myapp = InputWindow(root)
    myapp.mainloop()
