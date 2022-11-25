import tkinter as tk


class InputWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        root.option_add('*font', 'ＭＳゴシック 22')
        root.title("装置との通信用窓")

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
        self.Button.bind("<Button-1>", self.print_contents)

    def print_contents(self, event):
        print("Hi. The current entry content is:")

    def InputPressureHandler():
        pass

    def InputDeltaTimeHandler():
        pass


if __name__ == '__main__':
    root = tk.Tk()
    myapp = InputWindow(root)
    myapp.mainloop()
