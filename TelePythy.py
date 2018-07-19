"""
# telepathy_game
 Development Steps:

 - Draw board
    - [sun star eye moon circle bolt diamond hand heart] - Use font-icons for symbols.
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

    import csv
    with open('board_squares.csv') as f:
        board_reader = csv.reader(f, delimiter=',')
        for line in board_reader:
            c = Cell(*line)
            c.col = int(c.col)
            cells.append(c) 

    
    def __init__(self):
        self._grid = [[[] for y in range(self._board_size)] for  x in range(self._board_size)]
        self.eliminated =  {'rows': [], 'cols': [], 'colors' : [], 'shapes': []}
        self.retained =  {'rows': [], 'cols': [], 'colors' : [], 'shapes': []}
    
    def size(self):
        return self._board_size
    
    def update_cell_statuses(self,cell,answer_true):
        if not answer_true:
            prior_eliminated = len([cell for cell in self.cells 
                                   if cell.state == CELL_STATE.Eliminated])
            # ToDo: test this for color, then follow for other attributes.
            if cell.color not in self.eliminated['colors']:
                # add to eliminated and set all relevant cell states to 
                if cell.color in self.retained['colors']:
                    self.retained['colors'].remove(cell.color)
                self.eliminated['colors'].append(cell.color)
                for c in self.cells:
                    if c.color == cell.color:
                        c.state = CELL_STATE.Eliminated
                        
            post_eliminated = len([cell for cell in self.cells if cell.state == CELL_STATE.Eliminated])
        
            return str('Eliminated ' + str(post_eliminated - prior_eliminated) + ' additional cells for a total of ' + str(post_eliminated))
        
        else: #add non-eliminated things to retained.
            if cell.color not in self.eliminated['colors']:
                if cell.color not in self.retained['colors']:
                    self.retained['colors'].append(cell.color)
                for c in self.cells:
                    if (c.color == cell.color) and (c.state != CELL_STATE.Eliminated):
                        c.state = CELL_STATE.Retained

class Game:

    def __init__(self):
        self.board = Board()
        self._answer = None
        self._guesses = list()
        
    def _set_answer(self, row, col):
        if self._answer is not None:
            self._answer.state = CELL_STATE.Unknown
        ndx = (ord(row) - ord('A')) * self.board.size() + (col - 1) # board columns are 1-based
        self._answer = self.board.cells[ndx]
        self.board.cells[ndx].state = CELL_STATE.Correct

                        
    def guess(self, row, col, color, shape, try_solve = False):
        if self._answer is None:
            # what to do here? Assign a random cell?
            raise AttributeError('Cannot guess until answer is set')
        ndx = (ord(row) - ord('A')) * self.board.size() + col-1
        cell = self.board.cells[ndx]
        if (cell.color != color) or (cell.shape != shape):
            raise ValueError('Error in cell values. Did you mean ' + cell.color + ' ' + cell.shape + '?')
        a = self._answer # just to save typing
        # board  col is 1-based
        self._guesses.append(cell)
        if try_solve:
            return a is cell
        
        
        answer_true =  ((row == a.row) or 
                        ((col - 1) == a.col) or 
                        (color == a.color ) or 
                        (shape == a.shape )
                        )
        results = self.board.update_cell_statuses(cell,answer_true)
        
        return answer_true, results
        # ToDo: return richer results
    def guesses(self):
        return self._guesses
    
    def get_cell_data(self, cell_index):
        # print("\033[1;32;43m Bright Green \n")
        cell = self.board.cells[cell_index]
        return (cell.color, cell.shape, cell.state)
        
import unittest

class TestGameStartup(unittest.TestCase):

    def test_cell_state_descriptions_are_enumerated(self):
        self.assertEqual(CELL_STATE.Eliminated.value, 1)
        self.assertEqual(CELL_STATE.Retained.value, 2)
        self.assertEqual(CELL_STATE.Unknown.value, 3)
        self.assertEqual(CELL_STATE.Correct.value, 4)

    def test_have_4_cell_states(self):
        self.assertEqual(len(CELL_STATE), 4)
        
    def test_board_board_is_18_square(self):
        board = Board()
        self.assertEqual(18,board.size())
    
    def test_game_has_a_boad(self):
        game = Game()
        self.assertIsInstance(game.board,Board)
        
    def test_9_colors(self):
        board = Board()
        self.assertIn('yellow', board.colors)
        self.assertIn('orange', board.colors)
        self.assertIn('red', board.colors)
        self.assertIn('purple', board.colors)
        self.assertIn('pink', board.colors)
        self.assertIn('blue', board.colors)
        self.assertIn('green', board.colors)
        self.assertIn('silver', board.colors)
        self.assertIn('white', board.colors)
    
    def test_9_shapes(self):
        
        for shape in ['sun', 'star', 'eye', 'moon', 'circle', 'bolt', 'diamond', 'hand', 'heart']:
            self.assertIn(shape,Board().shapes, shape)

    def test_board_has_equal_numbers_of_each_combo(self):
        b = Board()
        # 4 per combo on normal 18 x 18 board.
        cells_per_combo = 4 # (b.size * b.size) /(len(b.shapes) * len(b.colors))
        for clr in b.colors:
            for s in b.shapes:
                instances_count =  0
                for c in b.cells:
                    if c.color == clr and c.shape == s:
                        instances_count += 1
                self.assertEqual(cells_per_combo, instances_count,clr + " " + s)
        
    def test_set_answer_is_retreivable(self):
        game = Game()
        game._set_answer('A',18) # A18 pink heart
        self.assertEqual(game._answer.col,17)
        self.assertEqual(game._answer.shape,game.board.shapes['heart'])
        
class TestGamePlay(unittest.TestCase):
    def test_guess_with_matching_attributes_returns_true(self):
        game = Game()
        game._set_answer('A',18) # A18 pink heart
        self.assertEqual(game.guess('A',1,'blue','bolt')[0],True) # A
        self.assertEqual(game.guess('D',18,'blue','circle')[0],True) # 18
        self.assertEqual(game.guess('B',12,'pink','star')[0],True) # pink
        self.assertEqual(game.guess('Q',8,'green','heart')[0],True) # heart
        self.assertEqual(game.guess('R',6,'pink','heart')[0],True)   # another pink heart

    def test_guess_with_no_matching_attributes_returns_false(self):
        game = Game()
        game._set_answer('A',18) # A18 pink heart
        self.assertEqual(game.guess('K',3,'green','moon')[0],False)
        self.assertEqual(game.guess('I',13,'orange','sun')[0],False)
        self.assertEqual(game.guess('R',17,'purple','diamond')[0],False)
        
    def test_guess_with_inconsistent_values_rejected(self):
        game = Game()
        game._set_answer('A',18) # A18 pink heart
        with self.assertRaises(ValueError):
            game.guess('K',3,'green','star') # s/b green moon
        
        
    def test_tracks_each_guess_in_order(self):
        game = Game()
        game._set_answer('R',18) # R18 red sun
        game.guess('A',1,'blue','bolt')
        game.guess('B',12,'pink','star')
        self.assertEqual(len(game.guesses()),2)
        self.assertEqual(game.guesses()[1].color, game.board.colors['pink'])
        
    def test_try_solve_compares_guess_to_set_answer(self):
        game = Game()
        game._set_answer('R',18) # R18 red sun
        self.assertTrue(game.guess('R',18,'red','sun')[0])        
        self.assertFalse(game.guess('R',6,'pink','heart')[0])
        
# Render board
    def test_cell_has_color_background(self):
        game = Game()
        self.assertEqual(get_cell_string(0),('B',5))
        
if __name__ == '__main__':
    unittest.main()
    
