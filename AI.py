from visuals2 import *
from functions2 import *

import random

def AI_player(myGame,whiteToPlay):
    Pieces = myGame.current_Pieces
    board = myGame.current_board

    color = 'b'
    if whiteToPlay: color = 'w'

    choices = []
    for piece in Pieces:
        if piece[0]==color:
            moves = leagalMoves(piece,myGame)
            #print(piece," : ",moves)
            if len(moves)>1:
                choices.append([piece,moves])
    

    finalChoice = choices[random.randint(0,len(choices)-1)]
    finalMove = finalChoice[1][random.randint(0,len(finalChoice[1])-1)]

    #print(finalChoice)
    movePiece(finalChoice[0],finalMove,myGame)

    