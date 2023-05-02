import tkinter as tk
from tkinter import ttk

#Creates window, defines dimensions and title.
window = tk.Tk()
window.config(width=400, height=400)
window.title("Test")

#Creates button with base (window), text and command
button = ttk.Button(
        window,
        text="")

#Positions button
button.place(x=300,y=200)

#button.pack(
#        ipadx=5,
#        ipady=5,
#        expand=True)


#Keeps the window open untill closure
window.mainloop()
