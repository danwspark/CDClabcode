########################################
# CS63: Artificial Intelligence, Lab 3
# Spring 2016, Swarthmore College
########################################

from Queues import FIFO_Queue
from copy import deepcopy
from Players import *

def main():
    game = HexGame(6)
    p1 = RandomChoicePlayer(game)
    p2 = HumanPlayer(game)
    game.playOneGame(p1, p2)

class HexGame(object):
    def __init__(self, size):
        """The board is represented as a list of lists with length
        size. Blank locations are represented by the character '-'.
        The players locations are represented as 'B' and 'W'."""
        self.size = size
        self.turn = None # should be either 'B' or 'W'
        self.reset()

    def reset(self):
        """Resets the board to the starting configuration."""
        self.board = []
        for i in range(self.size):
            self.board.append(['-']*self.size)

    def __str__(self):
        """Returns a string representing the board."""
        result = "\n"
        side = "black   "
        result += " "*self.size +  "white\n"
        for i in range(self.size):
            result +=  " " * i + side[i] + "  "
            for j in range(self.size-1):
                result += self.board[i][j] + " "
            result += self.board[i][self.size-1] + "  " + side[i] + "\n"
        result += " "*(int(2*self.size)) + "white"
        return result

    def playOneGame(self, player1, player2, show=True):
        """Plays a game and returns winner."""
        self.reset()
        player1.setSide('B')
        player2.setSide('W')
        print("%s vs %s" % (player1.name, player2.name))
        while True:
            if show:
                print(self)
                print("Player B's turn")
            self.turn = 'B'
            row, col = player1.getMove(self.board)
            self.board[row][col] = self.turn
            print "score for black: ",player1.eval(self.board)#
            #connected = self.countConnected(self.board, self.turn)
            #print "%s connected: %d" % (self.turn, connected)
            if show:
                print("Made move (%d, %d)" % (row, col))
            if self.blackWins(self.board): 
                winner = 'B'
                break
            if show:
                print(self)
                print("Player W's turn")
            self.turn = "W"
            row, col = player2.getMove(self.board)
            
            self.board[row][col] = self.turn
            #connected = self.countConnected(self.board, self.turn)
            #print "%s connected: %d" % (self.turn, connected)
            if self.whiteWins(self.board): 
                winner = 'W'
                break
        if show:
            print(self)
            print("%s wins" % self.turn)
        return winner

    def playNGames(self, n, player1, player2, show=False):
        """
        Will play out n games between player1 and player2.
        The players alternate going first.  Prints the total
        number of games won by each player.
        """
        first = player1
        second = player2
        for i in range(n):
            print "Game", i
            winner = self.playOneGame(first, second, show)
            if winner == 'B':
                first.won()
                second.lost()
                print first.name, "wins"
            else:
                first.lost()
                second.won()
                print second.name, "wins"
            first, second = second, first
        print first.results()
        print second.results()

    def getPossibleMoves(self, board):
        """Returns a list of all possible moves on the given board."""
        possible = []
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == '-':
                    possible.append((row, col))
        return possible

    def getNextBoard(self, board, move, player):
        """Returns a new board showing how the given board would look after
        the move by player."""
        row, col = move
        if board[row][col] != '-':
            print("Error invalid move: %s" % (move))
            exit()
        nextBoard = deepcopy(board)
        nextBoard[row][col] = player
        return nextBoard

    def getNeighbors(self, row, col):
        """Returns a list of neighboring cells to the given row and col."""
        ls = []
        if row > 0:
            ls.append((row-1, col))
        if row < self.size-1:
            ls.append((row+1, col))
        if col > 0:
            ls.append((row, col-1))
        if col < self.size-1:
            ls.append((row, col+1))
        if row > 0 and col < self.size-1:
            ls.append((row-1, col+1))
        if row < self.size-1 and col > 0:
            ls.append((row+1, col-1))
        return ls

    def blackWins(self, board):
        """Returns True if black player wins, otherwise False."""
        queue = FIFO_Queue()
        visited = set()
        # Add all locations of black pieces in the leftmost col to queue
        for row in range(self.size):
            if board[row][0] == 'B':
                queue.add((row, 0))
        # Try to find a path to the rightmost col
        while len(queue) > 0:
            row, col = queue.get()
            visited.add((row, col))
            for n in self.getNeighbors(row, col):
                r, c = n
                if board[r][c] != 'B': continue
                if c == self.size-1: return True
                if n in visited or n in queue:
                    continue
                queue.add(n)
        return False

    def whiteWins(self, board):
        """Returns True if white player wins, otherwise False."""
        queue = FIFO_Queue()
        visited = set()
        # Add all locations of white pieces n the top row to queue
        for col in range(self.size):
            if board[0][col] == 'W':
                queue.add((0, col))
        # Try to find a path to the bottom row
        while len(queue) > 0:
            row, col = queue.get()
            visited.add((row, col))
            for n in self.getNeighbors(row, col):
                r, c = n
                if board[r][c] != 'W': continue
                if r == self.size-1: return True
                if n in visited or n in queue:
                    continue
                queue.add(n)
        return False

    def countConnected(self, board, side):
        """Counts how many pieces for the given side touch another piece
        of the same side."""
        q = FIFO_Queue()
        visited = set()
        connected = 0

        #get all pieces of one color on the board
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == side:
                    q.add( (row,col) )

        while len(q) > 0:
            row, col = q.get()
            if (row,col) not in visited:
                visited.add( (row,col) )
                isConnected = False
                for neighbor in self.getNeighbors(row,col):
                    if board[ neighbor[0] ][ neighbor[1] ] == side:
                        isConnected = True
                if isConnected:
                    connected += 1

        return connected

if __name__ == '__main__':
    main()
