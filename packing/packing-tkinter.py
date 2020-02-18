import tkinter as tk
from tkinter import LEFT, RAISED, BOTH,YES
from tkinter.ttk import Frame

class WindowWithDifferentLayouts(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.frame1 = Frame(self, relief=RAISED,
                            borderwidth=1)
        self.frame1.pack(fill=BOTH, expand=YES)

        self.closeBtn = tk.Button(self.frame1,
                                 text="Close1",
                                 command=root.destroy)
        self.closeBtn.pack(side=LEFT)

        self.closeBtn2 = tk.Button(self.frame1,
                                 text="Close2",
                                 command=root.destroy)
        self.closeBtn2.pack(side=LEFT)

        self.closeBtn3 = tk.Button(self.frame1,
                                 text="Close3",
                                 command=root.destroy)
        self.closeBtn3.pack(side=LEFT)

        self.closeBtn4 = tk.Button(self.frame1,
                                 text="Close4",
                                 command=root.destroy)
        self.closeBtn4.pack(side=LEFT)


        self.frame2 = Frame(self, relief=RAISED,
                            borderwidth=1)
        self.frame2.pack(fill=BOTH, expand=YES)

        self.closeBtnA = tk.Button(self.frame2,
                                 text="Close1",
                                 command=root.destroy)
        self.closeBtnA.pack()

        self.closeBtnB = tk.Button(self.frame2,
                                 text="Close2",
                                 command=root.destroy)
        self.closeBtnB.pack()

        self.closeBtnC = tk.Button(self.frame2,
                                 text="Close3",
                                 command=root.destroy)
        self.closeBtnC.pack()

        self.closeBtnD = tk.Button(self.frame2,
                                 text="Close4",
                                 command=root.destroy)
        self.closeBtnD.pack()

if __name__ == '__main__':
    root = tk.Tk()
    app = WindowWithDifferentLayouts(master=root)
    app.mainloop()
