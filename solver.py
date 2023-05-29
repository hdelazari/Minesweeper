

class Solver:
    def solve(self,board):
        self.click = []
        self.flag_and_open(board)
        if self.click:
            return set(self.click)
        return []

    def flag_and_open(self,board):
        self.rows = len(board)
        self.columns = len(board[0])
        for i in range(self.rows):
            for j in range(self.columns):
                if board[i][j]!='' and board[i][j]!='f' and board[i][j]!=0:
                    if board[i][j]-self.count_neighbors(board,i,j,'f')==self.count_neighbors(board, i,j,''):
                        self.click_neighbors(board, i,j,3)
                    if board[i][j]==self.count_neighbors(board, i,j,'f'):
                        self.click_neighbors(board, i,j,1)

    def click_neighbors(self, board, i, j, event_num):
        if i > 0:
            if board[i-1][j]=='':
                self.click.append((i-1,j,event_num))
            if j > 0 and board[i-1][j-1]=='':
                self.click.append((i-1,j-1,event_num))
            if j < self.columns - 1 and board[i-1][j+1]=='':
                self.click.append((i-1,j+1,event_num))
        if i < self.rows - 1:
            if board[i+1][j]=='':
                self.click.append((i+1,j,event_num))
            if j > 0 and board[i+1][j-1]=='':
                self.click.append((i+1,j-1,event_num))
            if j < self.columns - 1 and board[i+1][j+1]=='':
                self.click.append((i+1,j+1,event_num))
        if j > 0 and board[i][j-1]=='':
            self.click.append((i,j-1,event_num))
        if j < self.columns -1 and board[i][j+1]=='':
            self.click.append((i,j+1,event_num))

    def count_neighbors(self, board, i, j, tile_type):
        count = 0
        if i > 0:
            if board[i-1][j]==tile_type:
                count+=1
            if j > 0 and board[i-1][j-1]==tile_type:
                count+=1
            if j < self.columns - 1 and board[i-1][j+1]==tile_type:
                count+=1
        if i < self.rows - 1:
            if board[i+1][j]==tile_type:
                count+=1
            if j > 0 and board[i+1][j-1]==tile_type:
                count+=1
            if j < self.columns - 1 and board[i+1][j+1]==tile_type:
                count+=1
        if j > 0 and board[i][j-1]==tile_type:
            count+=1
        if j < self.columns -1 and board[i][j+1]==tile_type:
            count+=1
        return count



