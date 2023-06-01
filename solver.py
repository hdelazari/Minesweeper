import copy
import itertools


class Solver:
    def solve(self,board):
        self.click = []
        self.rows = len(board)
        self.columns = len(board[0])
        self.flag_and_open(board)
        if self.click:
            return set(self.click)
#        self.check_ones(board)
        if self.click:
            return set(self.click)
        self.set_theory(board)
        if self.click:
            return set(self.click)
        self.test_borders(board)
        if self.click:
            return set(self.click)
        return []

    def flag_and_open(self, board):
        for i in range(self.rows):
            for j in range(self.columns):
                if board[i][j]!='' and board[i][j]!='f' and board[i][j]!=0:
                    if board[i][j]-self.count_neighbors(board,i,j,'f')==self.count_neighbors(board, i,j,''):
                        self.click_neighbors(board, i,j,3)
                    if board[i][j]==self.count_neighbors(board, i,j,'f'):
                        self.click_neighbors(board, i,j,1)
    
    def check_ones(self, board):
        positions = set()
        coborders = [(x,y) for (x,y) in self.find_coborder(board) if board[x][y]==1]
        for pair in itertools.combinations(coborders, 2):
            (first, second) = pair
            first_neighbors = self.list_neighbors(board, first, '')
            second_neighbors = self.list_neighbors(board, second, '')
            if first_neighbors.issubset(second_neighbors):
                positions = second_neighbors.difference(first_neighbors)
                break
            if second_neighbors.issubset(first_neighbors):
                positions = first_neighbors.difference(second_neighbors)
                break
        for pos in positions:
            self.click.append((pos[0],pos[1],1))
    
    def set_theory(self, board):
        positions = set()
        coborders = self.find_coborder(board)
        for (first, second) in itertools.combinations(coborders, 2):
            first_neighbors = self.list_neighbors(board, first, '')
            second_neighbors = self.list_neighbors(board, second, '')
            first_flags = self.list_neighbors(board, first, 'f')
            second_flags = self.list_neighbors(board, second, 'f')
            if board[first[0]][first[1]]-len(first_flags)-len(first_neighbors.difference(second_neighbors))==board[second[0]][second[1]]-len(second_flags):
                positions = positions.union(second_neighbors.difference(first_neighbors))
            if board[second[0]][second[1]]-len(second_flags)-len(second_neighbors.difference(first_neighbors))==board[first[0]][first[1]]-len(first_flags):
                positions = positions.union(first_neighbors.difference(second_neighbors))
        for pos in positions:
            self.click.append((pos[0],pos[1],1))

    def test_borders(self, board):
        border = self.find_border(board)
        x = len(border)
        print('n= '+str(x))
        if x>=20:
            print("Would take too long, skipping")
            return []
        subsets = self.powerset(border)
        flag = (1 << x)-1
        click = (1 << x)-1
        for subset in subsets:
            test_board = copy.deepcopy(board)
            test_board = self.add_flag(test_board, subsets[subset])
            if self.is_valid_board(test_board):
                print(subset)
                flag = flag & subset
                click = click & ~subset
        print(bin(flag))
        print(bin(click))
        for tile in subsets[flag]:
            self.click.append((tile[0],tile[1],3))
        for tile in subsets[click]:
            self.click.append((tile[0],tile[1],1))


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
    
    def list_neighbors(self, board, coords, tile_type):
        (i,j) = coords
        neighbors = []
        for (x,y) in self.find_neighbors(i, j):
            if board[x][y] == tile_type:
                neighbors.append((x,y))
        return set(neighbors)



    def find_neighbors(self, i, j):
        neighbors = [(i+1,j+1),
                     (i+1,j),
                     (i+1,j-1),
                     (i,j+1),
                     (i,j),
                     (i,j-1),
                     (i-1,j+1),
                     (i-1,j),
                     (i-1,j-1)
                     ]
        valid_neighbors = []
        for pos in neighbors:
            if pos[0] >= 0 and pos[1] >= 0 and pos[0]<self.rows and pos[1]<self.columns:
                valid_neighbors.append(pos)
        return valid_neighbors

    def is_coborder(self, board, i, j):
        if isinstance(board[i][j],int) and board[i][j]!=0:
            neighbors = self.find_neighbors(i, j)
            for (x,y) in neighbors:
                if board[x][y]=='':
                    return True
        return False

    def find_coborder(self, board):
        coborder = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.is_coborder(board, i, j):
                    coborder.append((i,j))
        return coborder

    def is_border(self, board, i, j):
        if board[i][j]!='':
            return False
        if i > 0:
            if type(board[i-1][j])==int:
                return True
            if j > 0 and type(board[i-1][j-1])==int:
                return True
            if j < self.columns - 1 and type(board[i-1][j+1])==int:
                return True
        if i < self.rows - 1:
            if type(board[i+1][j])==int:
                return True
            if j > 0 and type(board[i+1][j-1])==int:
                return True
            if j < self.columns - 1 and type(board[i+1][j+1])==int:
                return True
        if j > 0 and type(board[i][j-1])==int:
            return True
        if j < self.columns -1 and type(board[i][j+1])==int:
            return True
        return False
    
    def find_border(self, board):
        border = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.is_border(board, i, j):
                    border.append((i,j))
        return border

    def add_flag(self, test_board, flags):
        for flag in flags:
            if test_board[flag[0]][flag[1]]=='':
                test_board[flag[0]][flag[1]]='f'
            else:
                raise Exception("Tried to flag non empty tile at "+str(flag))
        return test_board

    def is_valid_board(self, test_board):
        for i in range(self.rows):
            for j in range(self.columns):
                if type(test_board[i][j])==int and test_board[i][j]!=self.count_neighbors(test_board, i, j, 'f'):
                    return False
        return True

    def powerset(self,full_set):
        x = len(full_set)
        subsets = {}
        for i in range(1 << x):
            subsets[i]=[full_set[j] for j in range(x) if (i & (1 << j))]
        return subsets
