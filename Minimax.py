########################################
# CS63: Artificial Intelligence, Lab 3
# Spring 2016, Swarthmore College
########################################

from Players import *
from HexGame import *

class Node(object):
    """Node used in minimax search"""
    def __init__(self, board, move, depth, side):
        self.board = board
        self.move = move
        self.depth = depth
        self.side = side # 'B' or 'W'

class BoundedMinimaxPlayer(Player):
    """Uses depth-bounded minimax to choose a move"""
    def __init__(self, game, depthLimit):
        Player.__init__(self)
        self.game = game
        self.name = "BoundedMinimaxDepth"+str(depthLimit)
        self.depthLimit = depthLimit
        self.bestMove = None

    def eval(self, board):
        """Black is the maximizer, so we want positive scores when board is
        good for black and negative scores when board is good for
        white. Should return highest score when black wins. Should
        return lowest score when white wins.  Otherwise should return
        number of black's connected pieces minus the number of white's
        connected pieces."""
        if whiteWins(board):
            return -100

        elif blackWins(board):
            return 100

        blackCount = countConnected(board,"B")
        whiteCount = countConnected(board,"W")

        return blackCount + whiteCount
        
    def betterEval(self, board):
        """Invent a better evaluator than the one above."""
        raise NotImplementedError("TODO")

    def getMove(self, board):
        """Given a board, creates the root node of the search tree and calls
        either boundedMinimax or alphaBetaMinimax. Returns the best
        move found."""
        raise NotImplementedError("TODO")
        
    def boundedMinimax(self, node):
        """Returns the value of the given node. Also sets self.bestMove to
        the best move found from the root node at depth 0."""
        raise NotImplementedError("TODO")

    def alphaBetaMinimax(self, node, alpha, beta):
        """Works similarly to boundedMinimax, but cuts off search down branches
        that will not lead to better outcomes."""
        raise NotImplementedError("TODO")
        
                           
if __name__ == '__main__':
    main()
