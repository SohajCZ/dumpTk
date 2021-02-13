import qtinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()
        self.state = 0
        self.states = [tk.N + tk.S + tk.W,   # left stretched vertically
                       tk.N + tk.S,          # cent and stret vertically
                       tk.N + tk.S + tk.E,   # right stretched vertically
                       tk.N + tk.W + tk.E,   # top stretched horizontally
                       tk.W + tk.E,          # center and stretch horizontally
                       tk.S + tk.W + tk.E,   # bottom stretched horizontally
                       tk.N + tk.S + tk.E + tk.W,  # stretch all
                       tk.NW, tk.N,  tk.NE,  # first row
                       tk.W,  '',    tk.E,   # second row, '' = center
                       tk.SW, tk.S,  tk.SE]   # last row

    def create_widgets(self):
        self.buttons = []

        for i in range(0, 5):
            buttons2 = []
            for j in range(0, 5):
                if ((i < 1 or i > 3) or (j < 1 or j > 3)) and \
                        (i != 4 or j != 4):
                    button = tk.Button(self, text="Hi")
                    button.grid(column=i, row=j)
                    buttons2.append(button)

            self.buttons.append(buttons2)

        self.main_button = tk.Button(self, text="", command=self.reposition)
        self.main_button.grid(column=1, row=1, columnspan=3, rowspan=3)

        self.quit = tk.Button(self, text="Hi", fg="red",
                              command=self.master.destroy)
        self.quit.grid(column=4, row=4)

    def reposition(self):
        # self.main_button.forget() TODO for later
        stick_str = self.states[self.state % len(self.states)]
        self.main_button['text'] = stick_str
        self.main_button.grid(sticky=stick_str)
        self.state += 1


root = tk.Tk()
app = Application(master=root)
app.mainloop()
