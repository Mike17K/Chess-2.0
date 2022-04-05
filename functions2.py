'''
ChessGame() #class that handles the game history

newPos(t,dx,dy) #u take the new position from the current position with moving dx at the x axis and y at the y axis
pinnedSquares(_Pieces,color,board) #returns a logic,list of squares with pinned pieces of the given color
printBoard(_board) #prints the board
movePiece(piece,newPos,board) #move a piece in the board
attacking_Squares(piece,board) #returns a list of squares thats attacked by a piece
attacking_Squares_Total(_Pieces,color,board) #returns a list of squares thats attacked by all pieces of the same color
posibleMoves(piece,board) #the posible moves of a piece
isCheck(color,aSq,myGame) #the color of the king we want to check if he is in check,the array of positions that are attackted by the other pieces, returns the logic True/False
sign(x) #the sign of the x
leagalMoves(piece,myGame) #all the legal squares from the piece
'''

from shutil import move
from traceback import print_tb
from globalVariables2 import *
import numpy as np

#consider add dictionarry instead of array for traking the pieces

class Node:
    def __init__(self,move,board,pieces,info,whiteToPlay): #add self.king positions = [w pos,b pos] to remove some loops
        # elements
        self.whiteToPlay = whiteToPlay
        self.move = move

        self.current_board = np.copy(board)
        self.current_Pieces = np.copy(pieces)
        self.current_info = np.copy(info)

        self.parent=None
        self.children = {}
        #

    def setParent(self,parent):
        self.parent = parent

    def addChild(self,child):
        child.setParent(self) #def the childs parent the curent node
        self.children[str(child.move)]=child #add the child to child list
    
    def removeChild(self,node):
        del self.children[str(node.move)]
        
    def copy(self):
        return Node(self.move,self.board,self.pieces,self.info,self.whiteToPlay)
       

def printNodeTree(node,layer):
    print(layer," value: ",node.move,node,node.current_info)
    
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
        self.root=Node(None,board,pieces,info,whiteToPlay)        

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
    

def newPos(t,dx,dy):
    if t>=Nwidth*Nheight: return False, None

    if (t//Nwidth<Nheight-abs(dy) and dy>=0) or (t//Nwidth>=abs(dy) and dy<0):
        if (t%Nwidth<Nwidth-abs(dx) and dx>=0) or (t%Nwidth>=abs(dx) and dx<0):
            return True, t+dy*Nwidth+dx
    return False, None

def pinnedSquares(_Pieces,color,board):
    squares = []
    directions = []
    
    posKing=None
    for piece in _Pieces:
        if piece[1]=='K' and piece[0]==color:
            posKing=int(piece[2:])
            break
    
    if posKing==None: return False,[],[]

    for direction in [[1,0],[-1,0],[0,1],[0,-1], [1,1],[-1,1],[1,-1],[-1,-1]]:
        logic=True
        sq=posKing
        mode=0
        pinnedPos=None
        while logic:
            logic , sq = newPos(sq,direction[0],direction[1])
            if logic: 
                if board[sq]!=None:

                    if board[sq][0]==color and mode==0: 
                        mode=1
                        pinnedPos=sq
                    elif board[sq][0]!=color and mode==0: break
                    elif board[sq][0]!=color and mode==1: 
                        if (board[sq][1] in ['B','Q'] and (abs(direction[0])+abs(direction[1])==2)) or (board[sq][1] in ['R','Q'] and (abs(direction[0])+abs(direction[1])==1)): 
                            squares.append(pinnedPos)
                            directions.append([direction[0],direction[1]])
                        break    
                    elif board[sq][0]==color and mode==1: break
    return True,directions,squares

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

def posibleMoves(piece,node):
    board = node.current_board
    info = node.current_info

    squares = []

    color = piece[0]
    type = piece[1]
    #print(piece)
    pos = int(piece[2:])

    if type =='p': #add unpassun
        if pos//Nwidth == 4 and color=='w': #white captures
            if info[0]==pos%Nwidth+1 and pos%Nwidth+1<Nwidth: #right unpassun
                squares.append(pos+9)
            elif info[0]==pos%Nwidth-1 and pos%Nwidth-1>=0: #left unpassun
                squares.append(pos+7)
        elif pos//Nwidth == 3 and color=='b': #black captures
            if info[0]==pos%Nwidth+1 and pos%Nwidth+1<Nwidth: #right unpassun
                squares.append(pos-7)
            elif info[0]==pos%Nwidth-1 and pos%Nwidth-1>=0: #left unpassun
                squares.append(pos-9) 

        if (pos//Nwidth==1 and color=='w') or (pos//Nwidth==Nheight-2 and color=='b'): #2squares front move
            logic , sq = newPos(pos,0,2*(color=='w')-1)
            if board[sq]==None and logic:
                logic , sq = newPos(pos,0,2*(2*(color=='w')-1))
                if board[sq]==None and logic: 
                    squares.append(sq)

        logic , sq = newPos(pos,0,2*(color=='w')-1) #front move
        if logic : 
            if board[sq]==None: 
                squares.append(sq)

        logic , sq = newPos(pos,1,2*(color=='w')-1) #capture right
        if logic:
            if board[sq]!=None:
                if board[sq][0]!=color: 
                    squares.append(sq)
        logic , sq = newPos(pos,-1,2*(color=='w')-1) #capture left
        if logic:
            if board[sq]!=None:
                if board[sq][0]!=color: 
                    squares.append(sq)

    if type =='N': 
        for i in [[2,-1],[2,1],[1,2],[-1,2],[-2,-1],[-2,1],[-1,-2],[1,-2]]:
            logic , sq = newPos(pos,i[0],i[1])
            if logic:
                if board[sq]!=None:
                    if board[sq][0]==color: 
                        continue
                squares.append(sq)

    if type =='R':
        for direction in [[1,0],[-1,0],[0,1],[0,-1]]:
            logic=True
            sq=pos
            while logic:
                logic , sq = newPos(sq,direction[0],direction[1])
                if logic: 
                    if board[sq]!=None:
                        if board[sq][0]!=color: 
                            squares.append(sq)
                        break
                    squares.append(sq)
                    continue
                break
    
    if type =='B':
        for direction in [[1,1],[-1,1],[1,-1],[-1,-1]]:
            logic=True
            sq=pos
            while logic:
                logic , sq = newPos(sq,direction[0],direction[1])
                if logic: 
                    if board[sq]!=None:
                        if board[sq][0]!=color: 
                            squares.append(sq)
                        break
                    squares.append(sq)
                    continue
                break
    
    if type =='Q':
        for direction in [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]:
            logic=True
            sq=pos
            while logic:
                logic , sq = newPos(sq,direction[0],direction[1])
                if logic: 
                    if board[sq]!=None:
                        if board[sq][0]!=color: 
                            squares.append(sq)
                        break
                    squares.append(sq)
                    continue
                break
    
    if type =='K': 
        for direction in [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]:
            logic , sq = newPos(pos,direction[0],direction[1])
            if logic: 
                if board[sq]!=None:
                    if board[sq][0]==color: continue
                squares.append(sq)
        
        #roke handle
        #white 
        aSq = attacking_Squares_Total(color,node)
        #print(aSq)
        if color == 'w' and pos==4:
            if info[1]: #small roke
                if board[6]==None and board[5]==None: 
                    if 6 not in aSq and 5 not in aSq and 4 not in aSq: 
                        squares.append(6)
            if info[2]: #big roke
                if board[1]==None and board[2]==None and board[3]==None:
                    if 2 not in aSq and 3 not in aSq and 4 not in aSq:
                        squares.append(2)
        elif color == 'b' and pos==60: #black
            if info[3]: #small roke
                if board[61]==None and board[62]==None:
                    if 61 not in aSq and 62 not in aSq and 60 not in aSq: 
                        squares.append(62)
            if info[4]: #big roke
                if board[57]==None and board[58]==None and board[59]==None :
                    if 58 not in aSq and 59 not in aSq and 60 not in aSq: 
                        squares.append(58)
            
    return squares
import time 

def movePiece(piece,newPos,node): 
    move = piece+" "+str(newPos)

    if str(move) in node.children.keys(): #if child already exists go to it
        nextNode = node.children[str(move)]
        return nextNode
    
    pieces = np.array(node.current_Pieces)
    board = np.array(node.current_board)
    info = np.array(node.current_info)
    

    tmp = np.array([int(x[2:]) for x in pieces])
    if board[newPos]!=None:#if in new position there is a piece del it from piece list
        pieces = np.delete(pieces,np.where(tmp == newPos)[0][0])
    
    tmp = np.array([int(x[2:]) for x in pieces])
    pos = np.where(tmp == int(piece[2:]))
    pieces[pos[0][0]]=piece[:2]+str(newPos) #update list pieces with new position


    if board[newPos]!=None:
        if board[newPos][1]=='R': #if rook captured handle roke logic
            if newPos==0: info[2]=False
            if newPos==7: info[1]=False
            if newPos==56: info[4]=False
            if newPos==63: info[3]=False

    if piece[1]=='p':

        if board[newPos]==None and abs(newPos-int(piece[2:]))%8!=0: #unpassun happend
            if piece[0]=='w': 
                target = newPos-Nwidth
            else:
                target = newPos+Nwidth
            board[target]=None
        

    board[newPos]=piece[:2]
    board[int(piece[2:])]=None

    if piece[1]=='p' and newPos//Nwidth in [7,0]: 
        board[newPos]=piece[0]+'Q' #promotion
        #print(board[newPos])


    # handle roke logic
    moved2Sq=None
    if piece[1]=='p':
        if abs(int(piece[2:])//Nwidth-newPos//Nwidth): moved2Sq = int(piece[2:])%Nwidth
    if piece[:2]=='wK':
        info[1]=False
        info[2]=False
    if piece[:2]=='bK':
        info[3]=False
        info[4]=False
    if piece == 'wR0':
        info[2]=False
    if piece == 'wR7':
        info[1]=False
    if piece == 'bR56':
        info[4]=False
    if piece == 'bR63':
        info[3]=False


    if abs(newPos%Nwidth - int(piece[2:])%Nwidth)==2 and piece[1]=='K':
        #casles
        if newPos%Nwidth==6: #small casles
            if newPos//Nwidth==0:#white
                board[5]='wR'
                board[7]=None
            else: #black
                board[61]='bR'
                board[63]=None
        else: #big casles
            if newPos//Nwidth==0:#white
                board[3]='wR'
                board[0]=None
            else: #black
                board[59]='bR'
                board[56]=None

    
    newNode = Node(move,board,pieces,[moved2Sq,info[1],info[2],info[3],info[4]],not node.whiteToPlay)
    node.addChild(newNode)

    return newNode
        
def attacking_Squares(piece,board):
    squares = []

    color = piece[0]
    type = piece[1]
    pos = int(piece[2:])

    if type =='p': 
        logic , sq = newPos(pos,1,2*(color=='w')-1)
        if logic: squares.append(sq)
        logic , sq = newPos(pos,-1,2*(color=='w')-1)
        if logic: squares.append(sq)

    if type =='N': 
        for i in [[2,-1],[2,1],[1,2],[-1,2],[-2,-1],[-2,1],[-1,-2],[1,-2]]:
            logic , sq = newPos(pos,i[0],i[1])
            if logic: squares.append(sq)

    if type =='R':
        for direction in [[1,0],[-1,0],[0,1],[0,-1]]:
            logic=True
            sq=pos
            while logic:
                logic , sq = newPos(sq,direction[0],direction[1])
                if logic: 
                    if board[sq]!=None:
                        squares.append(sq)
                        break
                    squares.append(sq)
                    continue
                break
    
    if type =='B':
        for direction in [[1,1],[-1,1],[1,-1],[-1,-1]]:
            logic=True
            sq=pos
            while logic:
                logic , sq = newPos(sq,direction[0],direction[1])
                if logic: 
                    if board[sq]!=None:
                        squares.append(sq)
                        break
                    squares.append(sq)
                    continue
                break
    
    if type =='Q':
        for direction in [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]:
            logic=True
            sq=pos
            while logic:
                logic , sq = newPos(sq,direction[0],direction[1])
                if logic: 
                    if board[sq]!=None:
                        squares.append(sq)
                        break
                    squares.append(sq)
                    continue
                break
    
    if type =='K':
        for direction in [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]:
            logic , sq = newPos(pos,direction[0],direction[1])
            if logic: squares.append(sq)

    return squares

def attacking_Squares_Total(color,node): #track the before attacking sq and redefine bace on the diff of the move
    _Pieces = node.current_Pieces
    board = node.current_board

    squares = []
    for piece in _Pieces:
        if piece[0]!=color:
            tmp=attacking_Squares(piece,board)
            squares+=tmp
    return list(set(squares)) #αμα θελω σε καθε νοδε να κραταω την διαφορα στα attacking squares για ποιο γρήγορα δε το θελω σε set αλλα append πρεπει να εγω και το ποσες φορες απειλείται το καθε square

def isCheck(color,aSq,node):
    pos = None
    for piece in node.current_Pieces:
        if piece[:2]==color+'K':
            pos = int(piece[2:])
    
    if pos in aSq:
        return True
    return False

def sign(x):
    a,b = None,None
    if abs(x[0])==abs(x[1]):
        #print(x)
        if x[0]==0: a=0 
        else: a=x[0]/abs(x[0])
        if x[1]==0: b=0 
        else: b=x[1]/abs(x[1])
        
        return [a,b]
    else:
        return [0,0]

def leagalMoves(piece,node): #piece : my moving piece, pieces all the pieces of the board , board : the arr of the board
    pieces = node.current_Pieces
    board = node.current_board

    posibleMove = posibleMoves(piece,node)
    aSq=attacking_Squares_Total(piece[0],node)
    
    #print("aSq: ",aSq)
    logic , directions , pSq = pinnedSquares(pieces,piece[0],board)
    
    finalSq=[]
    
    #print(pSq)
    if int(piece[2:]) in pSq and logic: #handle pinned Pieces
        for i in range(len(pSq)):
            if int(piece[2:])==pSq[i]:
                break

        for sq in posibleMove:
            sq_X=sq%Nwidth
            sq_Y=sq//Nwidth
            P_X=int(piece[2:])%Nwidth
            P_Y=int(piece[2:])//Nwidth
            #print([sq_X-P_X,sq_Y-P_Y],sign([sq_X-P_X,sq_Y-P_Y]),directions[i])
            if (sign([sq_X-P_X,sq_Y-P_Y]) == directions[i]) or (sign([P_X-sq_X,P_Y-sq_Y]) == directions[i]):
                finalSq.append(sq)
    elif piece[1]=='K':
        for move in posibleMove:
            if move not in aSq: finalSq.append(move)
    else:
        finalSq=posibleMove[:]            

    if isCheck(piece[0],aSq,node): #A BAD WAY OF FINDING THE MOVES THAT LEAD TO NO CHECK IF IS CHECK  IN THE FIRST PLACE
        #print("is in check!")
        finalSq_output = []

        for move in finalSq:
            #print("do the move: "+piece[:2]+str(move))
            newNode = movePiece(piece,move,node) #do the move 
            aSq = attacking_Squares_Total(piece[0],newNode) #find the new attackted sq
            if isCheck(piece[0],aSq,newNode)==False: #see again if is in check
                #print("Leagal!")
                finalSq_output.append(move)
            
        return finalSq_output

    return finalSq
