import tkinter as tk
from tkinter import ttk

def click(event):
    y=event.widget.grid_info()['row']
    x=event.widget.grid_info()['column']
    print(event.num,x,y)



#Creates window, defines dimensions and title.
window = tk.Tk()
window.geometry("400x400")
window.title("Test")

#Creates buttons' frames
frame_button = tk.Frame(window,
                        width = 20,
                        height = 20,
                        bg = "blue",
                        highlightbackground = "black",
                        highlightthickness = "1"
                        )

frame_button.pack_propagate(False)
frame_button.pack(
                  expand=True
                  )
frame_button.grid(column = 0,
                  row = 0)

frame_button2 = tk.Frame(window,
                        width = 20,
                        height = 20,
                        bg = "blue",
                        highlightbackground = "black",
                        highlightthickness = "1"
                        )

frame_button2.pack_propagate(False)
frame_button2.grid(column = 1,
                  row = 0)

#Set buttons' use
frame_button.bind("<Button>", click)
frame_button2.bind("<Button>", click)

#Keeps the window open untill closure
window.mainloop()
