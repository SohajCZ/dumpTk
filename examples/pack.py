import qtinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(side="top", expand=1)

        self.hi_there = tk.Button(frame)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(frame, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom", fill="x")

        # ----------------------------------------

        frame2 = tk.Frame(frame)
        frame2.pack(side="top")

        self.hi_there2 = tk.Button(frame2)
        self.hi_there2["text"] = "Hello World\n(click me)"
        self.hi_there2["command"] = self.say_hi
        self.hi_there2.pack(side="top")

        self.quit2 = tk.Button(frame2, text="QUIT2", fg="red",
                              command=self.master.destroy)
        self.quit2.pack(side="bottom")

        # ----------------------------------------

        frame3 = tk.Frame(frame)
        frame3.pack(side="left")

        self.hi_there3 = tk.Button(frame3)
        self.hi_there3["text"] = "Hello World\n(click me)"
        self.hi_there3["command"] = self.say_hi
        self.hi_there3.pack(side="top")

        self.quit3 = tk.Button(frame3, text="QUIT3", fg="red",
                              command=self.master.destroy)
        self.quit3.pack(side="bottom")

        # ----------------------------------------

        frame4 = tk.Frame(frame)
        frame4.pack(side="right", expand=1)

        self.hi_there4 = tk.Button(frame4)
        self.hi_there4["text"] = "Hello World\n(click me)"
        self.hi_there4["command"] = self.say_hi
        self.hi_there4.pack(side="top")

        self.quit4 = tk.Button(frame4, text="QUIT4", fg="red",
                              command=self.master.destroy)
        self.quit4.pack(side="bottom", fill="x")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
