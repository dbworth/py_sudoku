
def list_diff(lst1, lst2):
    """Return lst1 - lst2.

    list_diff(list<X>, list<X>) -> list<X>
    The result is the list of entries in lst1 that are not in lst2.

    """
    diff = []
    for e in lst1:
        if not e in lst2:
            diff.append(e)
    return diff

def list_intersection(lst1, lst2):
    """Return the intersection.

    list_intersection(list<X>, list<X>) -> list<X>
    The result is the list of all entries in both lst1 and lst2.

    """
    inter = []
    for e in lst1:
        if e in lst2:
            inter.append(e)
    return inter

def row2list(str):
    """Convert a row string into a list

    row2list(string) -> list<char>
    Precondition: str is a string representation of a row i.e. every
    second char is an entry of the row and there are 9 entries

    """
    row = []
    for i in range(0, 18, 2):
        row.append(str[i])
    return row


class Sudoku:
    """A Sudoku game"""

    # all the valid choices
    all_choices = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    def _read_game(self, filename):
        """Return a list representation of the game.

        _read_game(string) -> void
        Precondition: The file can be opened for reading and contains 9
        lines with each line representing a row of the game.

        """
        f = open(filename, 'r')
        for line in f:
            self._game.append(row2list(line))
        f.close()

    def __init__(self, filename, autofill = False):
        """Constructor: Sudoku(filename, autofill) loads the game from 
        the given file and sets the autofill flag.

        Precondition: Assumes filename is a valid Sudoku game file.

        """
        self._game = []
        self._read_game(filename)
        self._undo_stack = []  # keeps move info for later undos
        self._do_auto_fill = autofill  # determine if auto fill should be used

    def write_game(self, filename):
        f = open(filename, 'w')
        for row in self._game:
            f.write(' '.join(row) + '\n')
        f.close()

    def get_row(self, r):
        """Get the r'th row of game

        get_row(integer) -> list<char>
        Precondition: 0 <= r <= 8.

        """
        return self._game[r]

    def get_column(self, c):
        """Get the c'th column of game

        get_column(integer) -> list<char>
        Precondition: 0 <= c <= 8.

        """
        column = []
        for r in self._game:
            column.append(r[c])   
        return column

    def get_block(self, r, c):
        """Get the (r,c) block of game.

        get_block(integer, integer) -> list<char>
        Precondition: 0 <= r < 3 and 0 <= c < 3.

        """
        block = []
        for row in range(3*r, 3*r+3):
            block.extend(self._game[row][3*c:3*c+3])
        return block

    def get_entry(self, r, c):
        """Get the entry at row r and column c

        get_entry(int, int) -> char
        """

        return self._game[r][c]

    def set_entry(self, r, c, v):
        """Set the entry at row r and column c to v

        set_entry(int, int, char) -> void
        """

        self._game[r][c] = v
        entries = [(r,c)]
        if self._do_auto_fill:
            auto = self.auto_fill()
            entries.extend(auto)
        self._undo_stack.append(entries)

    def undo(self):
        """Undo the last move."""
        if self._undo_stack != []:
            entries = self._undo_stack.pop()
            for r,c in entries:
                self._game[r][c] = ' '
        
    ### Below is the "pythonic" way of accessing the game info instead of the
    ### above 2 methods. By defining the special class methods __setitem__
    ### and __getitem__ you can access and update info from a Sudoku object x
    ### as follows
    ### x[r,c]        - the same as x.get_entry(r,c)
    ### x[r,c] = v    - the same as x.set_entry(r,c,v)

    def __getitem__(self, key):
        r,c = key
        return self._game[r][c]

    def __setitem__(self, key, val):
        r,c = key
        self.set_entry(r,c,val)
   
    def choices(self, r, c):
        """Return the choices for position (r,c)

        choices(integer, integer) -> list<char>
        Precondition: 0 <= r <= 8 and 0 <= c <= 8
        and _game[r][c] == ' '

        This function returns all the possible choices that are possible 
        at (r,c) in game - i.e. each choice should not occur in row r, 
        column c or in the block containing this position.

        """
        block_row = r / 3
        block_col = c / 3
        row_choices = list_diff(Sudoku.all_choices, self.get_row(r))
        col_choices = list_diff(Sudoku.all_choices, self.get_column(c))
        block_choices = list_diff(Sudoku.all_choices, 
                                  self.get_block(block_row, block_col))
        choices = list_intersection(row_choices, col_choices)
        choices = list_intersection(choices, block_choices)
        return choices

    def game_status(self):
        status = "Finished"
        game = self._game
        for row in range(9):
            for col in range(9):
               if game[row][col] == ' ':
                   status = ""
                   ch = self.choices(row, col)
                   if not ch:
                       return "Unsolvable"
        return status

    def flip_af(self):
        """ Flip between doing and not doing auto fill """

        self._do_auto_fill = not self._do_auto_fill
        return self._do_auto_fill

    def auto_fill(self):
        """Autofill - update squares and return (r,c) pairs where square
        have been filled"""
        fill = []
        found = True
        game = self._game
        while found:
            found = False
            for row in range(9):
                for col in range(9):
                    if game[row][col] != ' ': continue
                    ch = self.choices(row, col)
                    if len(ch) == 1:
                        found = True
                        fill.append((row,col))
                        game[row][col] = ch[0]
        return fill

    def __repr__(self):
        result = ''
        for row in self._game:
            result = result + ''.join(row) + '\n'
        return result

