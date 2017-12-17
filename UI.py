import main
from tkinter import *


m = main.Runtime_io()


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)
        self.create_button_n_label('Left', 12, 0)
        self.create_button_n_label('Right', 12, 2)
        self.create_button_n_label('Up', 11, 1)
        self.create_button_n_label('Down', 13, 1)
        self.create_button_n_label('A', 12, 4)
        self.create_button_n_label('B', 13, 5)
        self.keyboard()
        self.textBox = Text(root, height=2, width=50)
        self.textBox.pack()
        self.outputtext = Text(root, height=8, width=50)
        self.outputtext.pack()
        self.outputtext.insert(END, 'bla')
        buttonCommit = Button(root, height=1, width=10, text="Commit", command=lambda: self.retrieve_input())
        buttonCommit.pack()

    def retrieve_input(self):
        inputValue=self.textBox.get("1.0","end-1c")
        print(inputValue)
        m.put_something_in(inputValue)

    def create_button_n_label(self, msxinput, row, col):
        set_input = lambda: m.change_control(msxinput.upper())
        text = msxinput.lower()
        button = Button(self, width=4, text=text, command=set_input).grid(row=row, column=col)
        return button

    def select(self, value):
        main.Runtime_io().change_keyboard(value, 'mylayer')
        return value

    def keyboard(self):
        varRow = 2
        varColumn = 0

        buttons = [
            'F1', 'F2', 'F3', 'F4', 'F5', 'HOME', 'STOP', 'INS', 'DEL',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '\\', 'BS',
            'TAB', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', 'RETURN',
            'CTRL', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':', '"', '~',
            'SHIFT', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'SHIFT', '^',
            'CAP', 'CODE', 'SPACE', 'CODE', 'GRAPH', 'SELECT'
        ]

        for button in buttons:

            Button(self, text=button, width=5, relief='raised', padx=2,
                           pady=1, bd=1, command=lambda x= button:self.select(x)).grid(row=varRow, column=varColumn)

            varColumn += 1

            if varColumn == 5 and varRow == 2:
                varColumn = 8
            if varColumn == 12 and varRow == 2:
                varColumn = 0
                varRow += 1
            if varColumn > 13 and varRow == 3:
                varColumn = 0
                varRow += 1
            if varColumn > 13 and varRow == 4:
                varColumn = 0
                varRow += 1
            if varColumn > 12 and varRow == 5:
                varColumn = 0
                varRow += 1
            if varColumn > 12 and varRow == 6:
                varColumn = 3
                varRow += 1

    def client_exit(self):
        exit()


root = Tk()
root.geometry("800x500")
app = Window(root)

root.mainloop()
