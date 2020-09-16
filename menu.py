from qtinter import *
import qtfiledialog as filedialog

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu)
        fileMenu.add_command(label="Item", command=self.say_hi)
        fileMenu.add_command(label="Exit", command=self.exitProgram)
        menu.add_cascade(label="File", menu=fileMenu)
        
        editMenu = Menu(menu)
        editMenu.add_command(label="Undo")
        editMenu.add_command(label="Redo")
        menu.add_cascade(label="Edit", menu=editMenu)

        dialogMenu = Menu(menu)
        dialogMenu.add_command(label="Open", command=self.print_file_name)
        dialogMenu.add_command(label="Save", command=filedialog.asksaveasfilename)
        menu.add_cascade(label="Dialog", menu=dialogMenu)

    def exitProgram(self):
        exit()

    def say_hi(self):
        print('chello')

    def print_file_name(self):
        print(filedialog.askopenfilename())
        
root = Tk()
app = Window(root)
root.wm_title("Tkinter window")
root.mainloop()
