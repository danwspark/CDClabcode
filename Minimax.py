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
        raise NotImplementedError("TODO")

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
        #base case
        if node.depth == self.depthLimit:
            return self.eval(node.board)
        
        #get all possible moves
        moves = self.game.getPossibleMoves(node.board)
        if len(moves) == 0:
            return self.eval(node.board)
        
        scores = []  #list of scores corresponding to moves
        for move in moves:
            nextBoard = self.game.getNextBoard(node.board, move, node.side)
            if node.side == 'B':
                side = 'W'
            else:
                side = 'B'
            nextNode = Node(nextBoard, move, node.depth+1, side)
            score = self.boundedMinimax(nextNode)
            scores.append(score)
        
        minimum = score[0]
        maximum = score[0]
        mins = [] #list storing indices of mins
        maxes = [] #list storing indices of maxes
        for i in range(len(scores)):
            if scores[i] <= minimum:
                minimum = scores[i]
                mins.append(i)
            if scores[i] >= maximum:
                maximum = scores[i]
                maxes.append(i)
                
        if node.side == 'B':
            if node.depth == 0:  #at root
                ind = choice(maxes)
                self.bestMove = moves[ind]
            return maximum
        else:
            if node.depth == 0:
                ind = choice(mins)
                self.bestMove = moves[ind]
            return minimum

            


    def alphaBetaMinimax(self, node, alpha, beta):
        """Works similarly to boundedMinimax, but cuts off search down branches
        that will not lead to better outcomes."""
        raise NotImplementedError("TODO")
        
                           
if __name__ == '__main__':
    main()
