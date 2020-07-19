import myTkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        for i in range(0,3):
            self.hi_there = tk.Button(self)
            self.hi_there["text"] = "LEFT"+str(i)+"\n(click me)"
            self.hi_there["command"] = self.say_hi
            self.hi_there.pack(side="left")

        for i in range(0,3):
            self.hi_there = tk.Button(self)
            self.hi_there["text"] = "BOTTOM"+str(i)+"\n(click me)"
            self.hi_there["command"] = self.say_hi
            self.hi_there.pack(side="bottom")

        self.quit = tk.Button(self, text="QUIT TOP", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="top")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
