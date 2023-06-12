import copy
import itertools


class Solver:
    def solve(self,board,total_bombs):
        self.click = []
        self.rows = len(board)
        self.columns = len(board[0])
        self.flag_and_open(board)
        if self.click:
            return set(self.click)
        if self.click:
            return set(self.click)
        self.set_theory(board)
        if self.click:
            return set(self.click)
        self.test_borders(board)
        if self.click:
            return set(self.click)
        self.combinatorics(board, total_bombs)
        return self.click

    def flag_and_open(self, board):
        for i in range(self.rows):
            for j in range(self.columns):
                if board[i][j]!='' and board[i][j]!='f' and board[i][j]!=0:
                    if board[i][j]-self.count_neighbors(board,(i,j),'f')==self.count_neighbors(board, (i,j),''):
                        self.click_neighbors(board, (i,j), 3)
                    if board[i][j]==self.count_neighbors(board, (i,j),'f'):
                        self.click_neighbors(board, (i,j), 1)    
   
    def set_theory(self, board):
        positions_open = set()
        positions_flag = set()
        coborders = self.find_coborder(board)
        for (first, second) in itertools.combinations(coborders, 2):
            first_neighbors = self.list_neighbors(board, first, '')
            second_neighbors = self.list_neighbors(board, second, '')
            first_flags = self.count_neighbors(board, first, 'f')
            second_flags = self.count_neighbors(board, second, 'f')
            if board[first[0]][first[1]]-first_flags-len(first_neighbors.difference(second_neighbors))==board[second[0]][second[1]]-second_flags:
                positions_open = positions_open.union(second_neighbors.difference(first_neighbors))
                positions_flag = positions_flag.union(first_neighbors.difference(second_neighbors))
            if board[second[0]][second[1]]-second_flags-len(second_neighbors.difference(first_neighbors))==board[first[0]][first[1]]-first_flags:
                positions_open = positions_open.union(first_neighbors.difference(second_neighbors))
                positions_flag = positions_flag.union(second_neighbors.difference(first_neighbors))
        for pos in positions_open:
            self.click.append((pos[0],pos[1],1))
        for pos in positions_flag:
            self.click.append((pos[0],pos[1],3))

    def test_borders(self, board):
        border = self.find_border(board)
        x = len(border)
        if x==0:
            return []
        print('Borders: n = '+str(x))
        if x>=15:
            print("Would take too long, skipping")
            return []
        subsets = self.powerset(border)
        flag = (1 << x)-1
        click = (1 << x)-1
        progress = 0
        print('['+' '*10+']', end='')
        for subset in subsets:
            progress = (subset*10)//((1 << x)-1)
            if progress-(subset-1)*10//((1 << x)-1)>=1:
                print('\r['+'❚'*progress +' '*(10-progress)+']', end='')
            test_board = copy.deepcopy(board)
            test_board = self.add_flag(test_board, subsets[subset])
            if self.is_valid_board(test_board):
                flag = flag & subset
                click = click & ~subset
        print('\n'+bin(flag))
        print(bin(click))
        for tile in subsets[flag]:
            self.click.append((tile[0],tile[1],3))
        for tile in subsets[click]:
            self.click.append((tile[0],tile[1],1))
    
    def combinatorics(self, board, total_bombs):
        current_bombs = self.count_bombs(board)
        free_spaces = self.list_free(board)
        x = len(free_spaces)
        if x == 0:
            return []
        print('Combinatorics: n = '+str(x)+', b = '+str(total_bombs-current_bombs))
        if x>=15:
            print('Would take too long, skipping')
            return []
        flag = set(free_spaces)
        click = set(free_spaces)
        for subset in itertools.combinations(free_spaces, total_bombs-current_bombs):
            test_board = copy.deepcopy(board)
            test_board = self.add_flag(test_board, subset)
            if self.is_valid_board(test_board):
                flag = flag.intersection(set(subset))
                click = click.intersection(set(free_spaces).difference(set(subset)))
        print(flag)
        print(click)
        for tile in flag:
            self.click.append((tile[0],tile[1],3))
        for tile in click:
            self.click.append((tile[0],tile[1],1))

    def click_neighbors(self, board, coords, event_num):
        for (x,y) in self.valid_neighbors(coords):
            if board[x][y] == '':
                self.click.append((x,y,event_num))

    def count_neighbors(self, board, coords, tile_type):
        count = 0
        for (x, y) in self.valid_neighbors(coords):
            if board[x][y] == tile_type:
                count+=1
        return count
    
    def list_neighbors(self, board, coords, tile_type):
        neighbors = []
        for (x,y) in self.valid_neighbors(coords):
            if board[x][y] == tile_type:
                neighbors.append((x,y))
        return set(neighbors)

    def valid_neighbors(self, coords):
        (i, j) = coords
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
        valid = []
        for pos in neighbors:
            if pos[0] >= 0 and pos[1] >= 0 and pos[0]<self.rows and pos[1]<self.columns:
                valid.append(pos)
        return valid

    def is_coborder(self, board, coords):
        (i, j) = coords
        if isinstance(board[i][j],int) and board[i][j]!=0:
            neighbors = self.valid_neighbors(coords)
            for (x,y) in neighbors:
                if board[x][y]=='':
                    return True
        return False

    def find_coborder(self, board):
        coborder = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.is_coborder(board, (i, j)):
                    coborder.append((i,j))
        return coborder

    def is_border(self, board, coords):
        if board[coords[0]][coords[1]]!='':
            return False
        for (x, y) in self.valid_neighbors(coords):
            if isinstance(board[x][y],int):
                return True
        return False
    
    def find_border(self, board):
        border = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.is_border(board, (i, j)):
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
                if type(test_board[i][j])==int and test_board[i][j]!=self.count_neighbors(test_board, (i, j), 'f'):
                    return False
        return True

    def powerset(self,full_set):
        x = len(full_set)
        subsets = {}
        for i in range(1 << x):
            subsets[i]=[full_set[j] for j in range(x) if (i & (1 << j))]
        return subsets

    def count_bombs(self, board):
        count=0
        for i in range(self.rows):
            for j in range(self.columns):
                if board[i][j] == 'f':
                    count+=1
        return count

    def list_free(self, board):
        free_tiles = []
        for i in range(self.rows):
            for j in range(self.columns):
                if board[i][j] == '':
                    free_tiles.append((i,j))
        return free_tiles
