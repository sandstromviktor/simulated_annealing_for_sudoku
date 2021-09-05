import numpy as np

class Sudoku():
    def __init__(self, size, beta=0.5):
        self.size = size
        self.box_size = int(np.sqrt(size))
        self.board = np.zeros(shape=(size,size))
        self.ref_board = np.zeros(shape=(size,size))
        self.__generate_ref_board__()
        self.clues = np.full((size,size),False, dtype=bool)
        self.__canonical_clues__(beta)
        self.board[self.clues] = self._ref_board[self.clues]

    def __repr__(self) -> str:
        repr = Sudoku.board_string(self.board)
        return repr


    @property
    def ref_board(self):
        print(Sudoku.board_string(self._ref_board))


    @ref_board.setter
    def ref_board(self, value):
        self._ref_board = value


    def __generate_ref_board__(self):
        ref_array = np.tile(np.arange(1,self.size+1, dtype=int),self.box_size)
        counter=0
        for i in range(self.box_size):
            for j in range(self.box_size):
                self._ref_board[counter] = ref_array[ j*self.box_size+i: self.size + j*self.box_size+i]
                counter+=1


    def __canonical_clues__(self, beta):
        linear_index = np.random.permutation(np.arange(0,self.size**2))[:int(beta*self.size**2)]
        for idx in [np.unravel_index(x,(self.size,self.size)) for x in linear_index]:
            self.clues[idx] = True
            #print(idx)


    def clear_board(self):
        self.board = np.empty(shape=(self.size,self.size))
        self.board[:] = np.NaN


    def place_number(self, num, row, col):
        if (num > self.size) | (num < 0):
            print('Must be a number between 0 and ', self.size)
            raise(ValueError)
        self.board[row, col] = int(num)


    def error_count(self):
        f = Sudoku.count_errors_in_list
        n = self.box_size
        return f(self.board) + f(self.board.T) + f(self.board.reshape((n,n**2,n)).reshape((n**2,n**2),order='F'))


    def fill_columns_uniquely(self):
        for i in range(self.size):
            missing_vals = np.setdiff1d(np.arange(1,self.size+1), self.board[:,i], assume_unique=True)
            self.board[:,i][~self.clues[:,i]]= missing_vals if missing_vals.size != 0 else self.board[:,i][~self.clues[:,i]]


    def swap_two_elements_in_column(self, col):
        idx = np.where(~self.clues[:,col])[0]
        idx = np.random.permutation(idx)[:2] if len(idx) > 1 else []
        value_1 = self.board[idx[0],col]
        value_2 = self.board[idx[1],col]
        self.board[idx[0],col] = value_2
        self.board[idx[1],col] = value_1


    @staticmethod
    def board_string(board):
        repr = '-'*(len(str(board[0]))+ 8) + '\n'
        n = int(np.sqrt(board.shape[0]))
        for i,row in enumerate(board):
            repr += "| "
            for j in range(n):
                lst = row[j*n:(j+1)*n]
                repr += "".join(["{:^3}".format(str(int(x))) for x in lst]) + " |"
            repr += '\n'
            if (i+1) % n == 0:
                repr += '-'*(len(str(row))+ 8) + '\n'
        return repr

    @staticmethod
    def count_errors_in_list(board):
        error = 0
        for lst in board:
            _, count = np.unique(lst[lst > 0], return_counts=True)
            error += np.sum([x-1 for x in count if x > 1])
        return error

