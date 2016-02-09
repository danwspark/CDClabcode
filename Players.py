########################################
# CS63: Artificial Intelligence, Lab 3
# Spring 2016, Swarthmore College
########################################

from HexGame import *
from random import choice, shuffle

class Player(object):
    """A base class for Hex players.  All players must implement the
    getMove method."""
    def __init__(self):
        self.name = None
        self.side = None
        self.game = None
        self.wins = 0
        self.losses = 0
    def setSide(self, side):
        self.side = side
    def otherSide(self, side):
        if side == 'W':
            return 'B'
        else:
            return 'W'
    def won(self):
        self.wins += 1
    def lost(self):
        self.losses += 1
    def results(self):
        result = self.name
        result += " Wins:" + str(self.wins)
        result += " Losses:" + str(self.losses)
        return result
    def getMove(self, board):
        """
        Given the current board, should return a valid move.
        """
        raise NotImplementedError()

class RandomChoicePlayer(Player):
    """Selects a random choice move."""
    def __init__(self, game):
        Player.__init__(self)
        self.name = "RandomChoicePlayer"
        self.game = game
    def getMove(self, board):
        return choice(self.game.getPossibleMoves(board))

class RandomShufflePlayer(Player):
    """Shuffles the possible moves, then selects the first possible move."""
    def __init__(self, game):
        Player.__init__(self)
        self.name = "RandomShufflePlayer"
        self.game = game
    def getMove(self, board):
        possible = self.game.getPossibleMoves(board)
        shuffle(possible)
        return possible[0]

class HumanPlayer(Player):
    """Selects a move chosen by the user."""
    def __init__(self, game, name="HumanPlayer"):
        Player.__init__(self)
        self.name = name
        self.game = game
    def getMove(self, board):
        print("\n%s's turn" % (self.name))
        while True:
            row, col = input("Enter row, col: ")
            if row >= self.game.size or col >= self.game.size or \
               row < 0 or col < 0:
                print("Invalid move: row and col must be on board")
            elif self.game.board[row][col] != '-':
                print("Invalid move: there is already a piece there")
            else:
                return (row, col)
