from visuals2 import *
from functions2 import *

import random

def AI_player(myGame,whiteToPlay):
    Pieces = myGame.current_Node.current_Pieces
    board = myGame.current_Node.current_board

    color = 'b'
    if whiteToPlay: color = 'w'

    choices = []
    for piece in Pieces:
        if piece[0]==color:
            moves = leagalMoves(piece,myGame)
            #print(piece," : ",moves)
            if len(moves)>0:
                choices.append([piece,moves])
    
    if len(choices)==0: 
        print("Mate")
        whiteToPlay=not whiteToPlay
        return 1
        

    finalChoice = choices[random.randint(0,len(choices)-1)]
    finalMove = finalChoice[1][random.randint(0,len(finalChoice[1])-1)]

    #print(finalChoice)
    movePiece(finalChoice[0],finalMove,myGame)

    return 0
    