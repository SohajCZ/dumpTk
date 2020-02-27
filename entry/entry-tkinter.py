import middleware as tk

class WindowWithEntryField(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        defaultStrVar = tk.StringVar()
        defaultStrVar.set("text")
        self.fieldEntry = tk.Entry(self, textvariable = defaultStrVar)
        self.fieldEntry.pack()

if __name__ == '__main__':
    root = tk.Tk()
    app = WindowWithEntryField(master=root)
    app.mainloop()
