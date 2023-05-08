import tkinter as tk



class Button:
    def __init__(self,board,x,y):
        self.pressed = False
        self.flag = False
        self.butt = tk.Frame(board,
                width = 20,
                height = 20,
                bg = "grey",
                highlightbackground = "black",
                highlightthickness  = "1"
                )
        self.butt.pack_propagate(False)
        self.butt.grid(column=x,
                  row=y)
        self.butt.bind("<Button>", self.click)
    def click(self,event):
        if self.pressed:
            return 0
        y=event.widget.grid_info()['row']
        x=event.widget.grid_info()['column']
        print(event.num,x,y,self.pressed)
        if (event.num == 2 or event.num == 3):
            if self.flag:
                self.butt.config(bg = "grey")
            else:
                self.butt.config(bg = "red")
            self.flag = not self.flag
        elif (event.num == 1 and not self.flag):
            self.butt.config(bg = "blue")
            self.pressed = True


class Display:
    buttons = []

    def __init__(self,window,rows,columns):
        self.board = tk.Frame(window)
        self.board.pack(fill = "both")
        for i in range(rows):
            for j in range(columns):
                self.button(i,j)


    def button(self,x,y):
        self.buttons.append(Button(self.board,x,y))

def close(event):
    window.destroy()

window = tk.Tk()
window.geometry("400x400")


b = Display(window,20,10)

#Keeps the window open untill closure
window.bind("<Control-Key-w>", close)
window.mainloop()
