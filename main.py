import tkinter as tk
import random
import time

class Game:
    def __init__(self, rows, columns, n_bombs):
        self.difficulty = [rows,columns,n_bombs]
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
        return count


class Button:
    color = {0: 'lightgrey',
            1: 'green',
            2: 'yellow',
            3: 'pink',
            4: 'orange',
            5: 'red',
            6: 'red',
            7: 'red',
            8: 'red'}
    def __init__(self, b, x, y):
        self.pressed = False
        self.flag = False
        self.bombCount = game.countBombs(x,y)
        self.butt = tk.Frame(b.fr,
                             bg = "grey",
                             highlightbackground = "black",
                             highlightcolor = "orange",
                             highlightthickness  = "1"
                             )
        self.butt.pack_propagate(False)
        self.butt.grid(column=x,
                  row=y,sticky=tk.N+tk.S+tk.E+tk.W)
        b.fr.columnconfigure(x,weight=1)
        b.fr.rowconfigure(y,weight=1)
        self.butt.bind("<Button>", self.click)
        self.butt.bind('<Up>',b.move_cursor)
        self.butt.bind('<Down>',b.move_cursor)
        self.butt.bind('<Left>',b.move_cursor)
        self.butt.bind('<Right>',b.move_cursor)
        self.butt.bind('<space>',lambda event: self.click2(x,y,1))
        self.butt.bind('<Control-space>', lambda event: self.click2(x,y,3))
    def click(self,event):
        x = event.widget.grid_info()['column']
        y = event.widget.grid_info()['row']
        self.click2(x,y,event.num)
    def click2(self,x,y,event_num):
        if self.pressed:
            if board.countFlags(x,y)==self.bombCount:
                openNeighbors(x,y)
            return 0
        elif(event_num == 2 or event_num == 3):
            if self.flag:
                self.butt.config(bg = "grey")
            else:
                self.butt.config(bg = "red")
            self.flag = not self.flag
        elif (event_num == 1 and not self.flag):
            self.pressed = True
            self.butt.config(bg = self.color[self.bombCount],relief=tk.SUNKEN)
            if game.table[y][x]:
                gameOver()
            else:
                tk.Label(self.butt, text=self.bombCount, bg = self.color[self.bombCount]).pack(expand=True)
                if self.bombCount == 0:
                    openNeighbors(x,y)
                game.running -= 1
            if not game.running:
                gameWin()
        


class Display:
    lasttime = time.time()
    def __init__(self, window, rows, columns):
        self.fr = tk.Frame(window,
                           highlightbackground='red',
                           highlightthickness=2
                           )
        self.fr.grid(row=0,column=0,sticky='news')
        self.fr.columnconfigure(0,weight=1)
        self.fr.pack_propagate(False)
        self.buttons = [[Button(self,i,j) for i in range(columns)] for j in range(rows)]
        self.cursor_x = 0
        self.cursor_y = 0
        self.buttons[self.cursor_y][self.cursor_x].butt.focus_set()
    def countFlags(self,x,y):
        count = 0
        if (x>0):
            if (self.buttons[y][x-1].flag):
                count+=1
            if (y>0 and self.buttons[y-1][x-1].flag):
                count+=1
            if (y<len(self.buttons)-1 and self.buttons[y+1][x-1].flag):
                count+=1
        if (x<len(self.buttons[0])-1):
            if (self.buttons[y][x+1].flag):
                count+=1
            if (y>0 and self.buttons[y-1][x+1].flag):
                count+=1
            if (y<len(self.buttons)-1 and self.buttons[y+1][x+1].flag):
                count+=1
        if (y>0 and self.buttons[y-1][x].flag):
            count+=1
        if (y<len(self.buttons)-1 and self.buttons[y+1][x].flag):
            count+=1
        return count
    def move_cursor(self,event):
        if event.keysym == 'Up':
            self.cursor_y-=1
            self.cursor_y%=len(self.buttons)
        elif event.keysym == 'Down':
            self.cursor_y+=1
            self.cursor_y%=len(self.buttons)
        elif event.keysym == 'Left':
            self.cursor_x-=1
            self.cursor_y%=len(self.buttons[0])
        elif event.keysym == 'Right':
            self.cursor_x+=1
            self.cursor_y%=len(self.buttons[0])
        self.buttons[self.cursor_y][self.cursor_x].butt.focus_set()


def gameOver():
    for child in board.fr.winfo_children():
        child.destroy()
    gameover = tk.Frame(board.fr,
                        width = board.fr.winfo_width(),
                        height = board.fr.winfo_height()/2,
                        highlightbackground = 'black',
                        highlightthickness = 1
                        )
    startover = tk.Frame(board.fr,
                         height = board.fr.winfo_height()/2,
                         highlightbackground = 'black',
                         highlightthickness = 1)
    change = tk.Frame(board.fr,
                      highlightbackground = 'black',
                      highlightthickness = 1)
    gameover.pack_propagate(False)
    startover.pack_propagate(False)
    change.pack_propagate(False)
    gameover.grid(column=0,row=0,columnspan=2,sticky=tk.N+tk.S+tk.W+tk.E)
    startover.grid(column=0,row=1,sticky=tk.N+tk.S+tk.W+tk.E)
    change.grid(column=1,row=1,sticky=tk.N+tk.S+tk.W+tk.E)
    board.fr.columnconfigure(0,weight=1)
    board.fr.columnconfigure(1,weight=1)
    board.fr.rowconfigure(0,weight=1)
    board.fr.rowconfigure(1,weight=1)
    tk.Label(gameover, text = "Game Over").pack(expand=True)
    startover.bind("<Button-1>",lambda event, dif=game.difficulty: newGame(dif))
    tk.Label(startover, text="New Game").pack(expand=True)
    change.bind("<Button-1>",setDifficulty)
    tk.Label(change, text = "Change Difficulty").pack(expand=True)
    def gameOverConf(event):
        gameover.config(width=board.fr.winfo_width(),
                        height = board.fr.winfo_height()/2)
        startover.config(height = board.fr.winfo_height()/2)
    board.fr.bind('<Configure>',gameOverConf)

def gameWin():
    for child in board.fr.winfo_children():
        child.destroy()
    gamewin = tk.Frame(board.fr,
                        width = board.fr.winfo_width(),
                        height = board.fr.winfo_height()/2,
                        highlightbackground = 'black',
                        highlightthickness = 1
                        )
    startover = tk.Frame(board.fr,
                         height = board.fr.winfo_height()/2,
                         highlightbackground = 'black',
                         highlightthickness = 1)
    change = tk.Frame(board.fr,
                      highlightbackground = 'black',
                      highlightthickness = 1)
    gamewin.pack_propagate(False)
    startover.pack_propagate(False)
    change.pack_propagate(False)
    gamewin.grid(column=0,row=0,columnspan=2,sticky=tk.N+tk.S+tk.W+tk.E)
    startover.grid(column=0,row=1,sticky=tk.N+tk.S+tk.W+tk.E)
    change.grid(column=1,row=1,sticky=tk.N+tk.S+tk.W+tk.E)
    board.fr.columnconfigure(0,weight=1)
    board.fr.columnconfigure(1,weight=1)
    board.fr.rowconfigure(0,weight=1)
    board.fr.rowconfigure(1,weight=1)
    tk.Label(gamewin, text = "Congratulations!").pack(expand=True)
    startover.bind("<Button-1>",lambda event, dif=game.difficulty: newGame(dif))
    tk.Label(startover, text="New Game").pack(expand=True)
    change.bind("<Button-1>",setDifficulty)
    tk.Label(change, text = "Change Difficulty").pack(expand=True)
    def gameWinConf(event):
        gamewin.config(width=board.fr.winfo_width(),
                        height = board.fr.winfo_height()/2)
        startover.config(height = board.fr.winfo_height()/2)
    board.fr.bind('<Configure>',gameWinConf)


   
def openNeighbors(x,y):
    if (x>0):
        if game.running and not board.buttons[y][x-1].pressed:
            board.buttons[y][x-1].butt.event_generate("<Button-1>")
        if (game.running and y>0 and not board.buttons[y-1][x-1].pressed):
            board.buttons[y-1][x-1].butt.event_generate("<Button-1>")
        if (game.running and y<len(game.table)-1 and not board.buttons[y+1][x-1].pressed):
            board.buttons[y+1][x-1].butt.event_generate("<Button-1>")
    if (x<len(game.table[0])-1):
        if  game.running and not board.buttons[y][x+1].pressed:
            board.buttons[y][x+1].butt.event_generate("<Button-1>")
        if (game.running and y>0 and not board.buttons[y-1][x+1].pressed):
            board.buttons[y-1][x+1].butt.event_generate("<Button-1>")
        if (game.running and y<len(game.table)-1 and not board.buttons[y+1][x+1].pressed):
            board.buttons[y+1][x+1].butt.event_generate("<Button-1>")
    if (game.running and y>0 and not board.buttons[y-1][x].pressed):
        board.buttons[y-1][x].butt.event_generate("<Button-1>")
    if (game.running and y<len(game.table)-1 and not board.buttons[y+1][x].pressed):
        board.buttons[y+1][x].butt.event_generate("<Button-1>")
 

def newGame(difficulty):
    global game
    global board
    for child in window.winfo_children():
        child.destroy()
    game = Game(*difficulty)
    for i in range(len(game.table)):
        print(game.table[i])
    board = Display(window, difficulty[0], difficulty[1])
    window.bind("<Control-Key-r>", lambda event, dif=game.difficulty: newGame(dif))


def setDifficulty(event):
    board.fr.unbind('<Configure>')
    for child in board.fr.winfo_children():
        child.destroy()
    board.fr.columnconfigure(0,weight=1)
    board.fr.rowconfigure(0,weight=1)
    board.fr.rowconfigure(1,weight=1)
    board.fr.rowconfigure(2,weight=1)
    easyFrame = tk.Frame(board.fr,
                        width = board.fr.winfo_width(),
                        height = board.fr.winfo_height()/3,
                        highlightbackground = 'black',
                        highlightthickness = 1
                        )
    easyFrame.grid(row=0,column=0,sticky=tk.NW+tk.NE+tk.S)
    easyFrame.pack_propagate(False)
    easyFrame.bind("<Button-1>", lambda event, dif=[8,8,10]: newGame(dif))
    Easy = tk.Label(easyFrame, text = "8x8\n10 mines")
    Easy.pack(expand=True)
    Easy.bind("<Button-1>", lambda event, dif=[8,8,10]: newGame(dif))
    mediumFrame = tk.Frame(board.fr,
                         width = board.fr.winfo_width(),
                         height = board.fr.winfo_height()/3,
                         highlightbackground = 'black',
                         highlightthickness = 1)
    mediumFrame.grid(row=1,column=0,sticky=tk.NW+tk.NE+tk.S)
    mediumFrame.pack_propagate(False)
    mediumFrame.bind("<Button-1>", lambda event, dif=[16,16,40]: newGame(dif))
    Medium = tk.Label(mediumFrame, text = "16x16\n40 mines")
    Medium.pack(expand=True)
    Medium.bind("<Button-1>", lambda event, dif=[16,16,40]: newGame(dif))
    hardFrame = tk.Frame(board.fr,
                      width = board.fr.winfo_width(),
                      height = board.fr.winfo_height()/3,
                      highlightbackground = 'black',
                      highlightthickness = 1)
    hardFrame.grid(row=2,column=0,sticky=tk.NW+tk.NE+tk.S)
    hardFrame.pack_propagate(False)
    hardFrame.bind("<Button-1>", lambda event, dif=[16,30,99]: newGame(dif))
    Hard = tk.Label(hardFrame, text = "16x30\n99 mines")
    Hard.pack(expand=True)
    Hard.bind("<Button-1>", lambda event, dif=[16,30,99]: newGame(dif))
    def setDifConf(event):
        if time.time()-board.lasttime>2:
            print('Conf')
            easyFrame.config(width = board.fr.winfo_width(),
                             height = board.fr.winfo_height()/3)
            mediumFrame.config(width = board.fr.winfo_width(),
                             height = board.fr.winfo_height()/3)
            hardFrame.config(width = board.fr.winfo_width(),
                             height = board.fr.winfo_height()/3)
#        board.lasttime = time.time()
    board.fr.bind('<Configure>', setDifConf) 

def conf(event):
    board.fr.config(height=window.winfo_height(), width=window.winfo_width())

window = tk.Tk()
window.geometry("400x400")


game = Game(1,1,1)


board = Display(window,1,1)

setDifficulty('<Button>')

#Keeps the window open untill closure
window.bind('<Configure>',conf)
window.bind("<Control-Key-w>", lambda event: window.destroy())
window.mainloop()
