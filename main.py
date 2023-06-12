import tkinter as tk
import random
import time
from solver import Solver

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
    def __init__(self, b, x, y, is_bomb):
        self.is_bomb = is_bomb
        self.pressed = False
        self.flag = False
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
        self.butt.bind("<Button>", lambda event: self.click(x,y,event.num))
        self.butt.bind('<Up>',b.move_cursor)
        self.butt.bind('<Down>',b.move_cursor)
        self.butt.bind('<Left>',b.move_cursor)
        self.butt.bind('<Right>',b.move_cursor)
        self.butt.bind('<space>',lambda event: self.click(x,y,1))
        self.butt.bind('<Control-space>', lambda event: self.click(x,y,3))

    def click(self,x,y,event_num):
        self.bombCount= board.countBombs(x,y)
        if self.pressed:
            if board.countFlags(x,y)==self.bombCount and event_num==1:
                openNeighbors(x,y)
            return 0
        elif(event_num == 2 or event_num == 3):
            if self.flag:
                self.butt.config(bg = "grey")
                self.butt.winfo_children()[0].destroy()
            else:
                self.butt.config(bg = "red")
                tk.Label(self.butt, text='f')
            self.flag = not self.flag
        elif (event_num == 1 and not self.flag):
            self.pressed = True
            self.butt.config(bg = self.color[self.bombCount],relief=tk.SUNKEN)
            if self.is_bomb:
                gameOver()
            else:
                tk.Label(self.butt, text=self.bombCount, bg = self.color[self.bombCount]).pack(expand=True)
                if self.bombCount == 0:
                    openNeighbors(x,y)
                board.running -= 1
            if not board.running:
                gameWin()
        

class Display:
    lasttime = time.time()
    def __init__(self, window, rows, columns, n_bombs):
        self.difficulty = [rows,columns,n_bombs]
        self.running = rows*columns - n_bombs
        self.bombs = random.sample(range(rows*columns), n_bombs)
        self.fr = tk.Frame(window,
                           highlightbackground='red',
                           highlightthickness=2
                           )
        self.fr.grid(row=0,column=0,sticky='news')
        self.fr.columnconfigure(0,weight=1)
        self.fr.pack_propagate(False)
        self.buttons = [[Button(self,i,j, j*columns+i in self.bombs) for i in range(columns)] for j in range(rows)]
        self.cursor_x = 0
        self.cursor_y = 0
        self.buttons[self.cursor_y][self.cursor_x].butt.focus_set()
        self.game = [['_' for i in range(columns)] for j in range(rows)]

    def countBombs(self,x,y):
        count = 0
        if (x>0):
            if (self.buttons[y][x-1].is_bomb):
                count+=1
            if (y>0 and self.buttons[y-1][x-1].is_bomb):
                count+=1
            if (y<len(self.buttons)-1 and self.buttons[y+1][x-1].is_bomb):
                count+=1
        if (x<len(self.buttons[0])-1):
            if (self.buttons[y][x+1].is_bomb):
                count+=1
            if (y>0 and self.buttons[y-1][x+1].is_bomb):
                count+=1
            if (y<len(self.buttons)-1 and self.buttons[y+1][x+1].is_bomb):
                count+=1
        if (y>0 and self.buttons[y-1][x].is_bomb):
            count+=1
        if (y<len(self.buttons)-1 and self.buttons[y+1][x].is_bomb):
            count+=1
        return count

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
            self.cursor_x%=len(self.buttons[0])
        elif event.keysym == 'Right':
            self.cursor_x+=1
            self.cursor_x%=len(self.buttons[0])
        self.buttons[self.cursor_y][self.cursor_x].butt.focus_set()

    def click(self, y, x, event_num):
        self.buttons[y][x].click(x,y,event_num)
    
    def outside_view(self):
        for fr in self.fr.winfo_children():
            label = fr.winfo_children()
            self.game[fr.grid_info()['row']][fr.grid_info()['column']] = label[0].cget('text') if label else ''


def gameOver():
    GOscreen = tk.Toplevel(window)
    GOscreen.geometry('400x400')
    gameover = tk.Frame(GOscreen,
                        width = GOscreen.winfo_width(),
                        height = GOscreen.winfo_height()/2,
                        highlightbackground = 'black',
                        highlightthickness = 1
                        )
    startover = tk.Frame(GOscreen,
                         height = GOscreen.winfo_height()/2,
                         highlightbackground = 'black',
                         highlightthickness = 1)
    change = tk.Frame(GOscreen,
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
    startover.bind("<Button-1>",lambda event, dif=board.difficulty: newGame(dif))
    tk.Label(startover, text="New Game").pack(expand=True)
    change.bind("<Button-1>",setDifficulty)
    tk.Label(change, text = "Change Difficulty").pack(expand=True)
    def gameOverConf(event):
        gameover.config(width= GOscreen.winfo_width(),
                        height = GOscreen.winfo_height()/2)
        startover.config(height = GOscreen.winfo_height()/2)
    GOscreen.bind('<Configure>',gameOverConf)
    GOscreen.bind('<Control-Key-r>', lambda event, dif=board.difficulty: newGame(dif))
    GOscreen.bind("<Control-Key-w>", lambda event: window.destroy())

def gameWin():
    GWscreen = tk.Toplevel(window)
    GWscreen.geometry('400x400')
    gamewin = tk.Frame(GWscreen,
                        width = GWscreen.winfo_width(),
                        height = GWscreen.winfo_height()/2,
                        highlightbackground = 'black',
                        highlightthickness = 1
                        )
    startover = tk.Frame(GWscreen,
                         height = GWscreen.winfo_height()/2,
                         highlightbackground = 'black',
                         highlightthickness = 1)
    change = tk.Frame(GWscreen,
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
    startover.bind("<Button-1>",lambda event, dif=board.difficulty: newGame(dif))
    tk.Label(startover, text="New Game").pack(expand=True)
    change.bind("<Button-1>",setDifficulty)
    tk.Label(change, text = "Change Difficulty").pack(expand=True)
    def gameWinConf(event):
        gamewin.config(width=GWscreen.winfo_width(),
                        height = GWscreen.winfo_height()/2)
        startover.config(height = GWscreen.winfo_height()/2)
    GWscreen.bind('<Configure>',gameWinConf)
    GWscreen.bind('<Control-Key-r>', lambda event, dif=board.difficulty: newGame(dif))
    GWscreen.bind("<Control-Key-w>", lambda event: window.destroy())

   
def openNeighbors(x,y):
    if (x>0):
        if board.running and not board.buttons[y][x-1].pressed:
            board.buttons[y][x-1].click(x-1,y,1)
        if (board.running and y>0 and not board.buttons[y-1][x-1].pressed):
            board.buttons[y-1][x-1].click(x-1,y-1,1)
        if (board.running and y<len(board.buttons)-1 and not board.buttons[y+1][x-1].pressed):
            board.buttons[y+1][x-1].click(x-1,y+1,1)
    if (x<len(board.buttons[0])-1):
        if  board.running and not board.buttons[y][x+1].pressed:
            board.buttons[y][x+1].click(x+1,y,1)
        if (board.running and y>0 and not board.buttons[y-1][x+1].pressed):
            board.buttons[y-1][x+1].click(x+1,y-1,1)
        if (board.running and y<len(board.buttons)-1 and not board.buttons[y+1][x+1].pressed):
            board.buttons[y+1][x+1].click(x+1,y+1,1)
    if (board.running and y>0 and not board.buttons[y-1][x].pressed):
        board.buttons[y-1][x].click(x,y-1,1)
    if (board.running and y<len(board.buttons)-1 and not board.buttons[y+1][x].pressed):
        board.buttons[y+1][x].click(x,y+1,1)
 

def newGame(difficulty):
    global board
    for child in window.winfo_children():
        child.destroy()
    board = Display(window, *difficulty)
    window.bind("<Control-Key-r>", lambda event, dif=board.difficulty: newGame(dif))


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
            easyFrame.config(width = board.fr.winfo_width(),
                             height = board.fr.winfo_height()/3)
            mediumFrame.config(width = board.fr.winfo_width(),
                             height = board.fr.winfo_height()/3)
            hardFrame.config(width = board.fr.winfo_width(),
                             height = board.fr.winfo_height()/3)
    board.fr.bind('<Configure>', setDifConf) 

def conf(event):
    board.fr.config(height=window.winfo_height(), width=window.winfo_width())

def solve():
    solve = Solver()
    clicks = [(0,0,0)]
    while clicks:
        board.outside_view()
        clicks = solve.solve(board.game, board.difficulty[2])
        for click in clicks:
            board.click(*click)
#        clicks = []




window = tk.Tk()
window.geometry("400x400")


board = Display(window,1,1,1)

setDifficulty('<Button>')

#Keeps the window open untill closure
window.bind('<Control-Key-s>',lambda event: solve())
window.bind('<Configure>',conf)
window.bind("<Control-Key-w>", lambda event: window.destroy())
window.mainloop()
