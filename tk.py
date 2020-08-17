from tkinter import *

root = Tk()

myLabel = Label(root, text="Hello World")
myLabel.pack()
cc = colorchooser.askcolor(root, title='Select a color')
cc.pack()

root.mainloop()