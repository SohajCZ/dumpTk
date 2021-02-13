from qtinter import *

window = Tk()


def print_event(event):
    for attr in ["serial","num","focus","height","width","keycode","state",
                 "time","x","y","x_root","y_root","char","send_event",
                 "keysym","keysym_num","type","widget","delta"]:
        print("Attribute:", attr, "=", getattr(event, attr, "not set/found"))


def mouse_click_1(event):
    print("mouse clicked -", event.num)


def mouse_click_3(event):
    print("mouse clicked -", event.num)


def s_clicked(event):
    print("s clicked")


def bind_all_clicked(event):
    print("bind all -", event.char)


frame = Frame()
frame.pack()

label = Label(frame, text="Click me")
label.pack()

label.bind("<1>", mouse_click_1)
label.bind("<3>", mouse_click_3)
label.bind_all("<Key>", bind_all_clicked)



window.mainloop()