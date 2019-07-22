"""
# telepathy_game
 Author: Bob Hiltner
 May, 2018
 
 Development Steps:

 - Draw board
    - [sun star eye moon circle bolt diamond hand heart] - Use font-icons, emoji or svg for symbols.
 [yellow orange red purple pink blue green silver white] - Standard or chosen constants for each color.
 [A..R] [1..18]
 - 1-Player game
     - Randomly select target square
     - Render Board
     - Offer player a chance to guess or solve
         - Entering in coordinates, fills out color and symbol, or
         - Click on square.
     - Compute results
         - Add guess to guesses list.
         - Compute Yes/No answer
         - Which squares are eliminated? (capture how many are eliminated with the guess, mark them)
         - Render Board
         - Provide Results
         - If player is solving, congratulate player and end game if correct, or show solution and wah-wah if incorrect.
"""

from enum import Enum
import csv

CELL_STATE = Enum('CELL_STATE', 'Eliminated Retained Unknown Correct')

# ToDo: Refactor opportunity- any advantage to making colors and shaps some sort of Enums as well?

class Colors(dict):
    # for now, key - value.  value should be object to have color value, shaded value, highlighted value
    _c = ['yellow', 'orange', 'red', 'purple', 'pink', 'blue', 'green', 'silver', 'white']
    colors = dict(zip(_c,_c))

class Shapes(dict):
    # for now, key -value. Later add graphic or visual font value to member shapes.
    _s = ['sun', 'star', 'eye', 'moon', 'circle', 'bolt', 'diamond', 'hand', 'heart']
    shapes = dict(zip(_s, _s))

class Cell:
    # row, col, color, shape, state

    def __init__(self, row, col, color, shape, state = CELL_STATE.Unknown):
        if color not in  Colors().colors:
            raise ValueError("Color '" + color + "'is not valid.")

        if shape not in Shapes().shapes:
            raise ValueError("Shape '" + shape + "' is not valid.")

        self.row = row
        self.col = col
        self.color = color
        self.shape = shape
        self.state = state

    def state_desc(self):
        return CELL_STATE        
    def __str__(self):
        # return self.row + str(self.col) + ', ' + self.color + ' ' + self.shape + ' state = ' + str(self.state)
        return 'Cell: "%s%s: %s %s %s' % (self.row, str(self.col), self.color, self.shape, str(self.state))
    def __repr__(self):
        return 'Cell(row="%s", col=%s, color="%s", shape="%s", state=%s)' % (self.row, self.col, self.color, self.shape, self.shape)        

class Board:
    _board_size = 18 
    colors = Colors().colors
    shapes = Shapes().shapes
    cells = list()
    
    with open('board_squares.csv') as f:
        board_reader = csv.reader(f, delimiter=',')
        # row letter,col number,color,shape
        for line in board_reader:
            c = Cell(*line)
            c.col = int(c.col)
            cells.append(c) 
        # is csv import overkill vs just readlines()?
        # for line in f.readlines():
        #     c = Cell(line.split(','))
        #     c.col=int(c.col)
        #     cells.append(c)
            
    def __init__(self):
        self._grid = [[[] for y in range(self._board_size)] for  x in range(self._board_size)]
        # Each cell will hold its state, and each trait will be tracked separetly
        self.eliminated =  {'rows': [], 'cols': [], 'colors' : [], 'shapes': []}
        self.retained =  {'rows': [], 'cols': [], 'colors' : [], 'shapes': []}
    
    def size(self):
        return self._board_size
    
    def update_cells(self, trait, trait_desc, status):
        #ToDo: is there a cleaner way to do this? (maybe refactor to use sets?)
        for c in self.cells: 
            if  ((trait_desc == 'colors' and c.color == trait) or 
                (trait_desc == 'shapes'and c.shape == trait) or
                (trait_desc == 'rows' and c.row == trait) or
                (trait_desc == 'cols' and c.col == trait)):
                    if c.state != CELL_STATE.Eliminated: #Final state--don't update
                        c.state = status
            elif trait_desc not in ('colors', 'shapes', 'rows', 'cols'):
                 raise AttributeError('Invalid trait_desc: ' + trait_desc)
                    
    def update_board_state(self,cell, guess_matches_traits):

        prior_eliminated = len([cell for cell in self.cells 
                               if cell.state == CELL_STATE.Eliminated])

        prior_retained = len([cell for cell in self.cells 
                           if cell.state == CELL_STATE.Retained])

        for (trait, trait_desc) in [(cell.color, 'colors'), (cell.shape, 'shapes'), (cell.row, 'rows'), (cell.col, 'cols')]:
            if not guess_matches_traits:
                if trait not in self.eliminated[trait_desc]:
                    # add trait to eliminated list and set all relevant cell states to eliminated.
                    if trait in self.retained[trait_desc]:
                        self.retained[trait_desc].remove(trait)
                    self.eliminated[trait_desc].append(trait)
                    
                    self.update_cells(trait, trait_desc, CELL_STATE.Eliminated)
                    post_eliminated = len([cell for cell in self.cells if cell.state == CELL_STATE.Eliminated])
                    return str('Eliminated ' + str(post_eliminated - prior_eliminated) + ' additional cells for a total of ' + str(post_eliminated))
                        
            else: #add non-eliminated things to retained.
                if trait not in self.eliminated[trait_desc]:
                    if trait not in self.retained[trait_desc]:
                        self.retained[trait_desc].append(trait)
                    self.update_cells(trait, trait_desc, CELL_STATE.Retained)
                post_retained = len([cell for cell in self.cells if cell.state == CELL_STATE.Retained])
                return str('Retained ' + str(post_retained - prior_retained) + ' additional cells for a total of ' + str(post_retained))
    

class Game:

    def __init__(self):
        self.board = Board()
        self._answer = None
        self._guesses = list()
    
    def get_cell_index(self, row, col):
        return (ord(row) - ord('A')) * self.board.size() + (col - 1) # board columns are 1-based
    
    def _set_answer(self, row, col):
        if self._answer is not None:
            self._answer.state = CELL_STATE.Unknown
        ndx = self.get_cell_index(row, col)
        self._answer = self.board.cells[ndx]
        self.board.cells[ndx].state = CELL_STATE.Correct

                        
    def guess(self, row, col, color, shape, try_solve = False):
        if self._answer is None:
            # what to do here? Assign a random cell?
            raise AttributeError('Cannot guess until answer is set')
        ndx = self.get_cell_index(row, col)
        cell = self.board.cells[ndx]
        if (cell.color != color) or (cell.shape != shape):
            raise ValueError('Error in cell values. Did you mean ' + cell.color + ' ' + cell.shape + '?')

        a = self._answer # just to save typing
        self._guesses.append(cell)
        if try_solve:
            return a is cell
        
        
        guess_matches_traits =  ((row == a.row) or 
                        ((col - 1) == a.col) or 
                        (color == a.color ) or 
                        (shape == a.shape )
                        )
        results = self.board.update_board_state(cell, guess_matches_traits)
        
        return guess_matches_traits, results
        # ToDo: return richer results
    def guesses(self):
        return self._guesses
    
    def get_cell_data(self, cell_index):
        # print("\033[1;32;43m Bright Green \n")
        cell = self.board.cells[cell_index]
        return (cell.color, cell.shape, cell.state)
        
