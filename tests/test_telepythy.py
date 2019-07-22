import unittest
import TelePythy as t

class TestGameStartup(unittest.TestCase):

    def test_cell_state_descriptions_are_enumerated(self):
        self.assertEqual(t.CELL_STATE.Eliminated.value, 1)
        self.assertEqual(t.CELL_STATE.Retained.value, 2)
        self.assertEqual(t.CELL_STATE.Unknown.value, 3)
        self.assertEqual(t.CELL_STATE.Correct.value, 4)

    def test_have_4_cell_states(self):
        self.assertEqual(len(t.CELL_STATE), 4)
        
    def test_board_board_is_18_square(self):
        board = t.Board()
        self.assertEqual(18,board.size())
    
    def test_game_has_a_board(self):
        game = t.Game()
        self.assertIsInstance(game.board,t.Board)
        
    def test_9_colors(self):
        board = t.Board()
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
            self.assertIn(shape,t.Board().shapes, shape)

    def test_board_has_equal_numbers_of_each_combo(self):
        b = t.Board()
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
        game = t.Game()
        game._set_answer('A',17) # A17 pink heart
        self.assertEqual(game._answer.col,17)
        self.assertEqual(game._answer.shape,game.board.shapes['heart'])
        
class TestGamePlay(unittest.TestCase):
    def test_guess_with_matching_attributes_returns_true(self):
        game = t.Game()
        game._set_answer('A',17) # A17 pink heart
        self.assertEqual(game.guess(game.get_cell('A',  0))[0],True)  # blue bolt (matches 'A')
        self.assertEqual(game.guess(game.get_cell('D', 17))[0],True) # blue circle (matches 18)
        self.assertEqual(game.guess(game.get_cell('B', 11))[0],True) # pink star (matches pink)
        self.assertEqual(game.guess(game.get_cell('Q',  7))[0],True)  # green heart (matches heart)
        self.assertEqual(game.guess(game.get_cell('R',  5))[0],True)  # pink heart (matches pink, heart) 

    def test_guess_with_no_matching_attributes_returns_false(self):
        game = t.Game()
        game._set_answer('A',17) # A17 pink heart
        self.assertEqual(game.guess(game.get_cell('K',  3))[0],False) # K 3  Blue Diamond
        self.assertEqual(game.guess(game.get_cell('I', 13))[0],False) # I 13 White Diamond
        self.assertEqual(game.guess(game.get_cell('R', 10))[0],False) # R 17 Pink Heart
        
    def test_tracks_each_guess_in_order(self):
        game = t.Game()
        game._set_answer('R',17) # R17 red sun
        game.guess(game.get_cell('A',0)) # blue bolt
        game.guess(game.get_cell('B',11)) # pink star
        self.assertEqual(len(game.guesses()),2)
        self.assertEqual(game.guesses()[1].color, game.board.colors['pink'])
        
    def test_try_solve_compares_guess_to_set_answer(self):
        game = t.Game()
        game._set_answer('R',17) # R18 red sun
        self.assertTrue(game.guess(game.get_cell('R',17),True))
        self.assertFalse(game.guess(game.get_cell('R',5), True))
        
# Render board
    def test_get_cell_data_returns_correct_values(self):
        game = t.Game()
        self.assertEqual(game.get_cell_data(0),('blue', 'bolt',t.CELL_STATE.Unknown))
