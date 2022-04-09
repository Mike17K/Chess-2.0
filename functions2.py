'''
ChessGame() #class that handles the game history

newPos(t,dx,dy) #u take the new position from the current position with moving dx at the x axis and y at the y axis
pinnedSquares(_Pieces,color,board) #returns a logic,list of squares with pinned pieces of the given color
printBoard(_board) #prints the board
movePiece(piece,newPos,board) #move a piece in the board
attacking_Squares(piece,board) #returns a list of squares thats attacked by a piece
attacking_Squares_Total(_Pieces,color,board) #returns a list of squares thats attacked by all pieces of the same color
posibleMoves(piece,board) #the posible moves of a piece
isCheck(aSq,myGame) #the array of positions that are attackted by the other pieces, returns the logic True/False
sign(x) #the sign of the x
leagalMoves(piece,myGame) #all the legal squares from the piece
'''

from shutil import move
from traceback import print_tb
from globalVariables2 import *
import numpy as np
import copy
import time

from move import *



#consider add dictionarry instead of array for traking the pieces       

def printNodeTree(node,layer):
    print(layer," value: ",node.move," LeagalMoves: ",len(node.current_leagalMoves.keys()),node.current_info)
    
    if len(node.children.keys())== 0:
        return 0

    for move,child in node.children.items():
        printNodeTree(child,layer+1)


def delNode(node): 
    node.parent.removeChild(node)

    n = len(node.children)
    print("Deleteting Node: ",node.move,node)
    tmp = node.children
    
    for child in range(n):
        delNode(tmp[child])
    del tmp , n
    del node 
        

class ChessGame():
    def __init__(self,board,pieces,info,whiteToPlay):
        kingpos = [None,None]
        for piece in pieces:
            if piece[:2]=="wK": kingpos[0] = int(piece[2:])
            if piece[:2]=="bK": kingpos[1] = int(piece[2:])
        
        self.root=Node(None,board,pieces,info,whiteToPlay)   
        self.root.kingPositions = kingpos[:]

        genChoices(self.root)  #find for the start node manually the leagal moves 

        self.current_Node = self.root
        
    def goToStartNode(self):
        self.current_Node 
        while True:
            if self.current_Node .parent==None: break
            self.current_Node = self.current_Node .parent

    def goOnelayerUp(self):
        self.current_Node = self.current_Node.parent
    
    def goToTheNextNode(self,move):
        if str(move) in self.current_Node.children.keys(): 
            self.current_Node = self.current_Node.children[str(move)]
            return

        tmp = Node(move,self.current_Node.current_board,self.current_Node.current_Pieces,self.current_Node.current_info,not self.current_Node.whiteToPlay)
        self.current_Node.addChild(tmp)
        self.current_Node = tmp
    
    def goToTheFinalPosition(self):
        pass

    def update(self,node):        
        self.current_Node = node
    



def printBoard(_board):
    for j in range(Nheight):      
        for i in range(Nwidth):
            if _board[i+j*Nwidth]==None:
                if i+j*Nwidth<10:
                    print(" ",end='')
                print(i+j*Nwidth,end=' ')
            else:
                print(_board[i+j*Nwidth],end = ' ')
        print()
    print()


    






def genChoices(node):
    Pieces = node.current_Pieces
    
    _dict = {}
    for piece in Pieces:
        moves = leagalMoves(piece,node)
        _dict[piece] = moves
    
    node.current_leagalMoves = _dict

    

    