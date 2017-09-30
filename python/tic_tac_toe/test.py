from functools import reduce
from copy import copy

import random

class TicTacToe():
    def __init__(self):       
        self.o_player, self.x_player, self.space = 'O', 'X', '.'
        self.win_lines = [[0,1,2],[3,4,5],[6,7,8], [0,3,6],[1,4,7],[2,5,8], [0,4,8],[2,4,6]]
        self.space_board =   [self.space for i in range(3*3)]
        
    def game_loop(self, board, player_list):
        (player, turn_func) = player_list[0]

        coord = turn_func(board, self.putable_coords(board))

        next_board = self.put_to_board(board, coord ,player)
        if next_board == False:
            #self.game_loop(board, player_list)
            next_board = board

        if self.is_player_win(next_board, player=player) :
            print("player %s won the game" % player)
            self.print_board(next_board)
        elif self.is_draw(next_board):
            print("the game was draw")
            self.print_board(next_board)
        else :
            self.game_loop(next_board, player_list[1:]+[player_list[0]])


                
    def is_draw(self, board):
        return len(self.putable_coords(board))==0

    def is_player_win(self, board, player="."):
        return []!=list(filter(lambda line: all(board[i]==player for i in line),
                                   self.win_lines))

    def putable_coords(self, board):
        return list(filter(lambda i : board[i]==self.space, range(len(board))))
            

    def put_to_board(self, board, coord, player):
        next_board = copy(board)
        if coord in self.putable_coords(board):
            next_board[coord] = player
            return next_board
        else :
            return False
        
    def print_board(self, board):
        print("y\\x 0 1 2 ")
        for i in range(len(board)):
            print("%s%s%s" % (" "+str(int(i/3))+"  " if i%3==0 else "",
                              board[i] + " ",
                              "\n" if i%3==2  else "")
                      ,end = "")

## AIs who play this game
    
def player_turn(board, putables):
    # its you
    print("\n====== Player Turn ======")
    TicTacToe.print_board(TicTacToe,board)
    print("put able coordinates is :")        
    print("n:(x,y)  ")
    for i, able in zip(range(len(putables)), putables):
        print("%s : (%s,%s)  " % (i, int(able/3), able%3 ))
            
    in_str = input(">> ")
        
    try :    return putables[int(in_str)]
    except : return player_turn(board, putables)

def randomist(board, putables):
    # random player
    return random.choice(putables)

def passest (board, putables):
    # passes all time
    return "aaaa"

def mcts (board, putables):
    pass


            
if __name__=="__main__":
    game = TicTacToe()
    game.game_loop(game.space_board,
                       [(game.o_player, player_turn),
                            #(game.x_player, game.player_turn)])
                       (game.x_player, passest)])
    
