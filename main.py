import tkinter as tk
import random


class Game:
    def __init__(self, rows, columns, n_bombs):
        self.running = rows*columns - n_bombs
        self.bombs = random.sample(range(rows*columns), n_bombs)
        self.table = [[0 for i in range(columns)] for j in range(rows)]
        for i in range(columns):
            for j in range(rows):
                if j*columns+i in self.bombs:
                    self.table[j][i] = 1
    def countBombs(self,x,y):
        count = 0
        if (x>0):
            if (self.table[y][x-1]):
                count+=1
            if (y>0 and self.table[y-1][x-1]):
                count+=1
            if (y<len(self.table)-1 and self.table[y+1][x-1]):
                count+=1
        if (x<len(self.table[0])-1):
            if (self.table[y][x+1]):
                count+=1
            if (y>0 and self.table[y-1][x+1]):
                count+=1
            if (y<len(self.table)-1 and self.table[y+1][x+1]):
                count+=1
        if (y>0 and self.table[y-1][x]):
            count+=1
        if (y<len(self.table)-1 and self.table[y+1][x]):
            count+=1
        if (count==0):
            openNeighbors(x,y)
        return count


class Button:
    def __init__(self, b, x, y):
        self.pressed = False
        self.flag = False
        self.butt = tk.Frame(b,
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
        x = event.widget.grid_info()['column']
        y = event.widget.grid_info()['row']
        self.click2(x,y,event.num)
    def click2(self,x,y,event_num):
        if self.pressed:
            return 0
        elif(event_num == 2 or event_num == 3):
            if self.flag:
                self.butt.config(bg = "grey")
            else:
                self.butt.config(bg = "red")
            self.flag = not self.flag
        elif (event_num == 1 and not self.flag):
            self.pressed = True
            self.butt.config(bg = "lightgrey")
            if game.table[y][x]:
                gameOver()
            else:
                tk.Label(self.butt, text=game.countBombs(x,y)).pack()
                game.running -= 1
            if not game.running:
                gameWin()


class Display:
    def __init__(self, window, rows, columns):
        self.fr = tk.Frame(window)
        self.fr.pack(fill = "both")
        self.buttons = [[Button(self.fr,i,j) for i in range(columns)] for j in range(rows)]


def close(event):
    window.destroy()

def gameOver():
    for child in window.winfo_children():
        child.destroy()
    gameover = tk.Frame(window,
                        width = 400,
                        height = 200
                        )
    gameover.grid(row=0,column=0,columnspan = 2)
    gameover.pack_propagate(False)
    tk.Label(gameover, text = "Game Over",pady = 100).grid()
    startover = tk.Frame(window,
                         width = 200,
                         height = 200,
                         bg = 'green')
    startover.grid(row=1,column=0)
    startover.bind("<Button-1>",setDifficulty)
    change = tk.Frame(window,
                     width = 200,
                     height = 200,
                     bg = 'black')
    change.grid(row=1,column=1)

def gameWin():
    print('Yey')

def openNeighbors(x,y):
    if (x>0):
        board.buttons[y][x-1].butt.event_generate("<Button-1>")
        if (y>0):
            board.buttons[y-1][x-1].butt.event_generate("<Button-1>")
        if (y<len(game.table)-1):
            board.buttons[y+1][x-1].butt.event_generate("<Button-1>")
    if (x<len(game.table[0])-1):
        board.buttons[y][x+1].butt.event_generate("<Button-1>")
        if (y>0):
            board.buttons[y-1][x+1].butt.event_generate("<Button-1>")
        if (y<len(game.table)-1):
            board.buttons[y+1][x+1].butt.event_generate("<Button-1>")
    if (y>0):
        board.buttons[y-1][x].butt.event_generate("<Button-1>")
    if (y<len(game.table)-1):
        board.buttons[y+1][x].butt.event_generate("<Button-1>")
 

def newGame(event,difficulty):
    for child in window.winfo_children():
        child.destroy()
    global game
    global board
    game = Game(*difficulty)
    for i in range(len(game.table)):
        print(game.table[i])
    board = Display(window, difficulty[0], difficulty[1])


def setDifficulty(event):
    for child in window.winfo_children():
        child.destroy()
    easyFrame = tk.Frame(window,
                        width = 400,
                        height = 100,
                        highlightbackground = 'black',
                        highlightthickness = 1
                        )
    easyFrame.grid(row=0,column=0)
    easyFrame.pack_propagate(False)
    easyFrame.bind("<Button-1>", lambda event, dif=[8,8,10]: newGame(event,dif))
    Easy = tk.Label(easyFrame, text = "Easy")
    Easy.pack(expand=True)
    mediumFrame = tk.Frame(window,
                         width = 400,
                         height = 100,
                         highlightbackground = 'black',
                         highlightthickness = 1)
    mediumFrame.grid(row=1,column=0)
    mediumFrame.pack_propagate(False)
    mediumFrame.bind("<Button-1>", lambda event, dif=[16,16,40]: newGame(event,dif))
    Medium = tk.Label(mediumFrame, text = "Medium")
    Medium.pack(expand=True)
    hardFrame = tk.Frame(window,
                      width = 400,
                      height = 100,
                      highlightbackground = 'black',
                      highlightthickness = 1)
    hardFrame.grid(row=2,column=0)
    hardFrame.pack_propagate(False)
    hardFrame.bind("<Button-1>", lambda event, dif=[16,30,99]: newGame(event,dif))
    Hard = tk.Label(hardFrame, text = "Hard")
    Hard.pack(expand=True)
 
        

window = tk.Tk()
window.geometry("400x400")


game, board = Game(1,1,1), Display(window,1,1)

setDifficulty("<Button>")

#newGame("<Button>")


#Keeps the window open untill closure
window.bind("<Control-Key-w>", close)
window.bind("<Control-Key-r>", newGame)
window.mainloop()
