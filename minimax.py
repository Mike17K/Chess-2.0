from functions2 import *
import math as m
from visuals2 import *

class Counter:
    G=0

def minimax_ab(node,a,b,depth,eval_function,min_max="max"):
    global screen
    Counter.G+=1
    
    choices = [[piece , moves] for piece , moves in node.current_leagalMoves.items() if piece[0]== ('w' if node.whiteToPlay else 'b') and len(moves)!=0]

    #sorting options for better performance
    choices.sort(key = lambda x: pieceWeight[x[0][1]],reverse=True)    

    

    if depth==0 or choices==[]: 
        tmp = eval_function(node)
        #drawBoard(screen,node.current_board,1,[])
        #time.sleep(0.1)
        #print("temp evaluation: ",int(tmp*1000)/1000," move: ",node.move)
        return tmp,None

    if min_max=="max": #search max
        max_choice ,value = None , -m.inf
        for piece , moves in choices:
            for move in moves:
                newNode = movePiece(piece,move,node)

                current_evaluation,tmp_choice = minimax_ab(newNode,a,b,depth-1,eval_function,min_max="min") 
                
                if current_evaluation>value: # value = max(value,current_evaluation)
                    value=current_evaluation
                    max_choice=[piece,move]

                a = max(a,value)

                if b<=a: 
                    break
    
        return value,max_choice

    elif min_max=="min": #search min
        max_choice ,value = None , m.inf
        for piece , moves in choices:
            for move in moves:

                newNode = movePiece(piece,move,node)
                current_evaluation,tmp_choice = minimax_ab(newNode,a,b,depth-1,eval_function,min_max="max") 
                
                if current_evaluation<value: # value = imn(value,current_evaluatio
                    value=current_evaluation
                    min_choice=[piece,move]
                
                b = min(b,value)

                if b<=a:
                    break
            
            
            
        return value,min_choice



def evaluate_pos(node): 
    start = time.time()
    sum=0
    
    '''totalMoves = [0,0]
    for piece in node.current_Pieces:
        mult=1
        if piece[0]=='b': mult=-1

        moves = leagalMoves(piece,node)
        
        totalMoves[0 if piece[0]=='w' else 1] +=len(moves)
        
        

        sum+=mult*0.01*len(moves)

    '''

    totalMoves = [0,0]
    for piece , moves in node.current_leagalMoves.items():
        totalMoves[0 if piece[0]=='w' else 1] += len(moves)


    if node.isCheck and totalMoves[0 if piece[0]=='w' else 1] == 0: return mult*1000

    

    
    for piece in node.current_Pieces:
        mult = -1 if piece[0]=='b' else 1

        sum+=mult*pieceWeight[piece[1]]


    print("time: ",time.time()-start)
    return sum
