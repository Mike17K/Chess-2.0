from functions2 import *
import math as m
from visuals2 import *

class Counter:
    G=0

def genChoices(node):
    Pieces = node.current_Pieces
    color = 'b'
    if node.whiteToPlay: color = 'w'
    
    
    choices = []
    for piece in Pieces:
        if piece[0]==color:
            moves = leagalMoves(piece,node)
            if len(moves)>0:
                choices.append([piece,moves]) 
    return choices
    



def minimax_ab(node,a,b,depth,eval_function,min_max="max"):
    global screen
    Counter.G+=1
    
    #node shit
    choices = genChoices(node)

    if depth==0 or choices==[]: 
        tmp = eval_function(node)
        #drawBoard(screen,node.current_board,1,[])
        #time.sleep(0.1)
        #print(a,b)
        return tmp,None

    if min_max=="max": #search max
        max_choice ,value = None , -m.inf
        for choice in choices:
            for move in choice[1]:
                
                newNode = movePiece(choice[0],move,node)
                current_evaluation,tmp_choice = minimax_ab(newNode,a,b,depth-1,eval_function,min_max="min") 
                
                if current_evaluation>value: # value = max(value,current_evaluation)
                    value=current_evaluation
                    max_choice=[choice[0],move]

                a = max(a,value)

                if b<=a: 
                    break
    
        return value,max_choice

    elif min_max=="min": #search min
        max_choice ,value = None , m.inf
        for choice in choices:
            for move in choice[1]:

                newNode = movePiece(choice[0],move,node)
                current_evaluation,tmp_choice = minimax_ab(newNode,a,b,depth-1,eval_function,min_max="max") 
                
                if current_evaluation<value: # value = imn(value,current_evaluatio
                    value=current_evaluation
                    min_choice=[choice[0],move]
                
                b = min(b,value)

                if b<=a:
                    break
                
                
                
        return value,min_choice



def evaluate_pos(node): 
    sum=0
    
    for piece in node.current_Pieces:
        mult=1
        if piece[0]=='b': mult=-1
        moves = leagalMoves(piece,node)
        
        
        aSq=attacking_Squares_Total(piece[0],node)
        is_ = isCheck(piece[0],aSq,node)
        #if is_: print(is_,node.move,aSq)
        if piece[1]=='K' and len(moves)==0 and is_: return -mult*m.inf 

        sum+=mult*0.01*len(moves)
    
    for piece in node.current_Pieces:
        mult=1
        if piece[0]=='b': mult=-1

        sum+=mult*pieceWeight[piece[1]]

    return sum
