from qtinter import *

window = Tk()


def mouseClick(event):
    print("In", event) #  <ButtonPress event state=Mod2 num=1 x=24 y=11>

    print("mouse clicked")


label = Label(window, text="Click me")
label.pack()

label.bind("<Button>", mouseClick)

window.mainloop()