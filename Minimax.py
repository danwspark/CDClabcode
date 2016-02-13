########################################
# CS63: Artificial Intelligence, Lab 3
# Spring 2016, Swarthmore College
########################################

from Players import *
from HexGame import *
from random import choice
import time

def main():
    game = HexGame(6)
    p1 = BoundedMinimaxPlayer(game,2)
    p2 = RandomChoicePlayer(game)
    #game.playOneGame(p1,p2)
    sTime = time.time()
    game.playNGames(100,p1,p2)
    eTime = time.time()
    print "time Elapsed: ", eTime-sTime

class Node(object):
    """Node used in minimax search"""
    def __init__(self, board, move, depth, side):
        self.board = board
        self.move = move
        self.depth = depth
        self.side = side # 'B' or 'W'

class ABNode(object):
    #Node used in Alpha Beta pruning algorithm
    def __init__(self, board, move, depth, side, alpha, beta):
        self.board = board
        self.move = move
        self.depth = depth
        self.side = side
        self.alpha = alpha
        self.beta = beta



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
        if self.game.whiteWins(board):
            return -100  #some large negative number

        elif self.game.blackWins(board):
            return 100  #some large positive number

        blackCount = self.game.countConnected(board,"B")
        whiteCount = -self.game.countConnected(board,"W")

        return blackCount + whiteCount
        
    def betterEval(self, board):
        """Invent a better evaluator than the one above."""
        raise NotImplementedError("TODO")

    def getMove(self, board): 
        """Given a board, creates the root node of the search tree and calls
        either boundedMinimax or alphaBetaMinimax. Returns the best
        move found."""
        newNode = ABNode(board,None,0,self.side,-float('inf'),float('inf'))
        #newNode = Node(board,None,0,self.side)
        value = self.alphaBetaMinimax(newNode) #can be alphaBetaMinimax
        #print "TEST: current value of node: ",value
        return self.bestMove
        
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
        minimum = float('inf')
        maximum = -float('inf')
        for move in moves:
            nextBoard = self.game.getNextBoard(node.board, move, node.side)
            if node.side == 'B':
                side = 'W'
            else:
                side = 'B'
            nextNode = Node(nextBoard, move, node.depth+1, side)
            score = self.boundedMinimax(nextNode)
            scores.append(score)
            if score < minimum:
                minimum = score
            if score > maximum:
                maximum = score
        
        mins = [] #list storing indices of mins
        maxes = [] #list storing indices of maxes
        for i in range(len(scores)):
            if scores[i] == minimum:
                mins.append(i)
            if scores[i] == maximum:
                maxes.append(i)
        
        if node.side == 'B':
            if node.depth == 0:  #at root
                """
                print "scores ",scores
                print "minimum& mins: ",minimum, mins
                print "maximum& maxes: ",maximum, maxes
                """
                ind = choice(maxes)
                #print "index of choice: ",ind
                self.bestMove = moves[ind]
            return maximum
        else:
            if node.depth == 0:
                """
                print scores
                print minimum, mins
                print maximum, maxes
                """
                ind = choice(mins)
                #print ind
                self.bestMove = moves[ind]
            return minimum
           

    def alphaBetaMinimax(self, node):
        """Works similarly to boundedMinimax, but cuts off search down branches
        that will not lead to better outcomes."""
        #base case
        if node.depth == self.depthLimit:
            return self.eval(node.board)
                    
        #get all possible moves
        moves = self.game.getPossibleMoves(node.board)
        if len(moves) == 0:
            return self.eval(node.board)
        
        scores = []  #list of scores corresponding to moves
        minimum = float('inf')
        maximum = -float('inf')
        for move in moves:
            nextBoard = self.game.getNextBoard(node.board, move, node.side)
            if node.side == 'B':
                side = 'W'
            else:
                side = 'B'

            #print "alpha, beta: ", node.alpha, node.beta
            nextNode = ABNode(nextBoard, move, node.depth+1, side,node.alpha, node.beta)
            score = self.alphaBetaMinimax(nextNode)
            scores.append(score)
            
            if node.side == 'B':
                if node.alpha < score:
                    node.alpha = score
            elif node.side == 'W':
                if node.beta > score:
                    node.beta = score
            
            if score < minimum:
                minimum = score
            if score > maximum:
                maximum = score

            if node.alpha > node.beta:
                break
                
        mins = [] #list storing indices of mins
        maxes = [] #list storing indices of maxes
        for i in range(len(scores)):
            if scores[i] == minimum:
                mins.append(i)
            if scores[i] == maximum:
                maxes.append(i)
        
        if node.side == 'B':
            if node.depth == 0:  #at root
                """
                print "scores ",scores
                print "minimum& mins: ",minimum, mins
                print "maximum& maxes: ",maximum, maxes
                """
                ind = choice(maxes)
                #print "index of choice: ",ind
                self.bestMove = moves[ind]
            return maximum
        else:
            if node.depth == 0:
                """
                print scores
                print minimum, mins
                print maximum, maxes
                """
                ind = choice(mins)
                #print ind
                self.bestMove = moves[ind]
            return minimum

        
                           
if __name__ == '__main__':
    main()
