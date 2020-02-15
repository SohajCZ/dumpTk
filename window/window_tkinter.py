import middleware as tk

class SimpleWindow(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('200x100+50+150')

    app = SimpleWindow(master=root)

    app.mainloop()
			
