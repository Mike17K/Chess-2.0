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

class Node():
    def __init__(self,move,board,pieces,info):#,value):
        self.move = move

        itm1 = board
        tmp1 = len(itm1)*[None]
        for sq in range(len(itm1)): 
            tmp1[sq]=itm1[sq]
        self.current_board = tmp1

        itm2 = pieces
        tmp2 = len(itm2)*[None]
        for sq in range(len(itm2)): 
            tmp2[sq]=itm2[sq]
        self.current_Pieces = tmp2

        itm3 = info
        tmp3 = len(itm3)*[None]
        for sq in range(len(itm3)): 
            tmp3[sq]=itm3[sq]
        self.current_info = tmp3

        self.parent=None
        self.children = []
    
    def setParent(self,parent):
        self.parent = parent

    def addChild(self,child):
        child.setParent(self) #def the childs parent the curent node
        self.children.append(child) #add the child to child list
   

def printNodeTree(node,layer):
    print(layer," value: ",node.move)
    
    if len(node.children)== 0:
        return 0

    for child in node.children:
        printNodeTree(child,layer+1)


def delNode(node): ##not working fixxxxxxxx
    n = len(node.children)
    for child in range(n):
        delNode(node.children[child])
    

    print("Deleteting Node: ",node.move)
    del node
    


class ChessGame():
    def __init__(self,board,pieces,info):
        self.root=Node(None,board,pieces,info)        

        self.current_Node = self.root
        
    def goToStartNode(self):
        self.current_Node = self.root

    def goOnelayerUp(self):
        self.current_Node = self.current_Node.parent
    
    def goToTheNextNode(self,move):
        for child in self.current_Node.children:
            if child.move==move:
                self.current_Node = child
                return
        self.current_Node.addChild(Node(move,self.current_Node.current_board,self.current_Node.current_Pieces,self.current_Node.current_info))
        self.current_Node = self.current_Node.children[-1]
    
    def goToTheFinalPosition(self):
        pass

    def update(self,move,board,Pieces,info):
        tmp1 = len(board)*[None]
        for sq in range(len(board)): 
            tmp1[sq]=board[sq]
        
        
        tmp2 = len(Pieces)*[None]
        for piece in range(len(Pieces)): 
            tmp2[piece]=Pieces[piece]
        

        tmp3 = len(info)*[None]
        for i in range(len(info)): 
            tmp3[i]=info[i]
        
        
        '''
        self.current_Node.current_board = tmp1
        self.current_Node.current_Pieces = tmp2
        self.current_Node.current_info = tmp3
        '''
        for child in self.current_Node.children:
            if child.move==move:
                self.current_Node = child
                return
        self.current_Node.addChild(Node(move,tmp1,tmp2,tmp3))
        self.current_Node = self.current_Node.children[-1]

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

def posibleMoves(piece,myGame):
    board = myGame.current_board
    info = myGame.current_info

    squares = []

    color = piece[0]
    type = piece[1]
    #print(piece)
    pos = int(piece[2:])

    if type =='p': #add unpassun
        if pos//Nwidth == 4 and color=='w': #white captures
            if myGame.current_info[0]==pos%Nwidth+1 and pos%Nwidth+1<Nwidth: #right unpassun
                squares.append(pos+9)
            elif myGame.current_info[0]==pos%Nwidth-1 and pos%Nwidth-1>=0: #left unpassun
                squares.append(pos+7)
        elif pos//Nwidth == 3 and color=='b': #black captures
            if myGame.current_info[0]==pos%Nwidth+1 and pos%Nwidth+1<Nwidth: #right unpassun
                squares.append(pos-7)
            elif myGame.current_info[0]==pos%Nwidth-1 and pos%Nwidth-1>=0: #left unpassun
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
        aSq = attacking_Squares_Total(color,myGame)
        #print(aSq)
        if color == 'w' and pos==4:
            if info[1]: #small roke
                if board[6]==None and board[5]==None: 
                    if 6 not in aSq and 5 not in aSq: 
                        squares.append(6)
            if info[2]: #big roke
                if board[1]==None and board[2]==None and board[3]==None:
                    if 2 not in aSq and 3 not in aSq:
                        squares.append(2)
        elif color == 'b' and pos==60: #black
            if info[3]: #small roke
                if board[61]==None and board[62]==None:
                    if 61 not in aSq and 62 not in aSq: 
                        squares.append(62)
            if info[4]: #big roke
                if board[57]==None and board[58]==None and board[59]==None:
                    if 58 not in aSq and 59 not in aSq:
                        squares.append(58)
            
    return squares

def movePiece(piece,newPos,myGame): #add casles
    pieces = myGame.current_Node.current_Pieces
    board = myGame.current_Node.current_board

    #print(pieces)
    for p in range(len(pieces)):
        if int(pieces[p][2:])==newPos:
            del pieces[p]
            break

    for p in range(len(pieces)):
        if int(pieces[p][2:])==int(piece[2:]):
            pieces[p]=piece[:2]+str(newPos)
            break

    if board[newPos]!=None:
        if board[newPos][1]=='R': #if rook captured handle roke logic
            if newPos==0: myGame.current_Node.current_info[2]=False
            if newPos==7: myGame.current_Node.current_info[1]=False
            if newPos==56: myGame.current_Node.current_info[4]=False
            if newPos==63: myGame.current_Node.current_info[3]=False

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
    
    
    '''
    print("movePiece('"+piece+"',"+str(newPos)+",myGame)")
    print("drawBoard(screen,myGame.current_board,view,[])")
    print("time.sleep(dt)")
    '''

    # handle roke logic
    moved2Sq=None
    if piece[1]=='p':
        if abs(int(piece[2:])//Nwidth-newPos//Nwidth): moved2Sq = int(piece[2:])%Nwidth
    if piece[:2]=='wK':
        myGame.current_Node.current_info[1]=False
        myGame.current_Node.current_info[2]=False
    if piece[:2]=='bK':
        myGame.current_Node.current_info[3]=False
        myGame.current_Node.current_info[4]=False
    if piece == 'wR0':
        myGame.current_Node.current_info[1]=False
    if piece == 'wR7':
        myGame.current_Node.current_info[2]=False
    if piece == 'bR56':
        myGame.current_Node.current_info[3]=False
    if piece == 'bR63':
        myGame.current_Node.current_info[4]=False


    if abs(newPos%Nwidth - int(piece[2:])%Nwidth)==2 and piece[1]=='K':
        #casles
        if newPos%Nwidth==6: #small casles
            if newPos//Nwidth==0:#white
                movePiece('wR7',5,myGame)
            else: #black
                movePiece('bR63',61,myGame)
        else: #big casles
            if newPos//Nwidth==0:#white
                movePiece('wR0',3,myGame)
            else: #black
                movePiece('bR56',59,myGame)
    

    myGame.update(piece+" "+str(newPos),board,pieces,[moved2Sq,myGame.current_Node.current_info[1],myGame.current_Node.current_info[2],myGame.current_Node.current_info[3],myGame.current_Node.current_info[4]])
    #print(myGame.current_info)
        
def attacking_Squares(piece,board):
    squares = []

    color = piece[0]
    type = piece[1]
    pos = int(piece[2:])

    if type =='p': #add unpassun
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

def attacking_Squares_Total(color,myGame):
    _Pieces = myGame.current_Pieces
    board = myGame.current_board

    squares = []
    for piece in _Pieces:
        if piece[0]!=color:
            tmp=attacking_Squares(piece,board)
            squares+=tmp
            #print(piece,tmp)
    return list(set(squares))

def isCheck(color,aSq,myGame):
    pos = None
    for piece in myGame.current_Pieces:
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

def leagalMoves(piece,myGame): #piece : my moving piece, pieces all the pieces of the board , board : the arr of the board
    pieces = myGame.current_Node.current_Pieces
    board = myGame.current_Node.current_board

    posibleMove = posibleMoves(piece,myGame.current_Node)
    aSq=attacking_Squares_Total(piece[0],myGame.current_Node)
    
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

    if isCheck(piece[0],aSq,myGame.current_Node): #A BAD WAY OF FINDING THE MOVES THAT LEAD TO NO CHECK IF IS CHECK  IN THE FIRST PLACE
        finalSq_output = []
        for move in finalSq:
            #print("do the move: "+piece[:2]+str(move))
            movePiece(piece,move,myGame) #do the move 
            aSq = attacking_Squares_Total(piece[0],myGame.current_Node) #find the new attackted sq
            if isCheck(piece[0],aSq,myGame.current_Node)==False: #see again if is in check
                #print("Leagal!")
                finalSq_output.append(move)
            #undo move
            myGame.goOnelayerUp()
        return finalSq_output

    return finalSq



#check , unpasan 
