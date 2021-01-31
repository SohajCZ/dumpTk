from qtinter import *

window = Tk()


def mouseClick(event):
    print("In", event) #  <ButtonPress event state=Mod2 num=1 x=24 y=11>

    print("mouse clicked")

    for attr in ["serial","num","focus","height","width","keycode","state",
                 "time","x","y","x_root","y_root","char","send_event",
                 "keysym","keysym_num","type","widget","delta"]:
        print("Attribute:", attr, "=", getattr(event, attr, "not set/found"))


label = Label(window, text="Click me")
label.pack()

label.bind("<Button>", mouseClick)

window.mainloop()