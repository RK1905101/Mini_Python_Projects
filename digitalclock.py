from tkinter import *
import time

root= Tk()
root.geometry("400x100")
root.config(bg='black')

def update():
    clock.config(text=time.strftime("%I:%M:%S"))
    clock.after(1000,update)

clock = Label(root, background = 'black',foreground = 'white', font = ('arial', 40, 'bold'))
clock.pack()
update()
root.title('clock')
root.mainloop()
