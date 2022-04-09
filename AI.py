import nntplib
from re import A
from secrets import choice
from time import time
from visuals2 import *
from functions2 import *

from globalVariables2 import *
import random
import math as m

from minimax import *
import time

def AI_player(myGame,whiteToPlay):
        
    ######################
    # AI logic
    ######################

    text='min'
    if whiteToPlay: text='max'
    
    
    #start = time.time()


    evaluation,finalChoice = minimax_ab(myGame.current_Node,-m.inf,m.inf,3,evaluate_pos,min_max=text)
    #print("time: ",time.time()-start)

    if finalChoice==None: 
        Pieces = myGame.current_Node.current_Pieces

        color = 'b'
        if whiteToPlay: color = 'w'

        choices = []
        for piece in Pieces:
            if piece[0]==color:
                moves = leagalMoves(piece,myGame.current_Node)
                #print(piece," : ",moves)
                if len(moves)>0:
                    choices.append([piece,moves])
        
        if len(choices)==0:   
            aSq=attacking_Squares_Total(color,myGame.current_Node)
            if isCheck(color,aSq,myGame.current_Node):
                print("Mate")
                return 1
            else: 
                print("Pat")
            whiteToPlay=not whiteToPlay
            return 1

    finalMove = finalChoice[1]

    
    #print(Counter.G)

    #print(choices)   

    print("Final choices: ",finalChoice[0],finalMove," evaluate: ",evaluation)
    
    myGame.current_Node = movePiece(finalChoice[0],finalMove,myGame.current_Node)
    

    return 0








