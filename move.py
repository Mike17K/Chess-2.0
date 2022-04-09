from globalVariables2 import *
import copy
import numpy as np

def movePiece(piece,new_Pos,node,enable_calculate_next_leagal_moves=True): 
    #start = time.time()

    #first things to do
    move = piece+" "+str(new_Pos) #define move
    if str(move) in node.children.keys(): return node.children[str(move)] #if child already exists go to it
    
    pieces = np.array(node.current_Pieces) #copy of node array
    board = np.array(node.current_board) #copy of node array
    info = np.array(node.current_info) #copy of node array
    kingPositions = np.array(node.kingPositions) #copy of kingPositions array
    #

    #defining the _capturedPiece ...
    _capturedPiece = board[new_Pos] + str(new_Pos) if board[new_Pos]!=None else None #defining captured piece
    if piece[1]=='p' and _capturedPiece==None and abs(new_Pos-int(piece[2:]))%8!=0: _capturedPiece  = board[new_Pos + (-1 if piece[0]=='w' else 1)*Nwidth] + str(new_Pos + (-1 if piece[0]=='w' else 1)*Nwidth)  #defining captured piece if unpassun happend

    #update board , pieces , info for the _capturedPiece
    if _capturedPiece!=None: 
        pieces = np.delete(pieces,np.where(np.array([int(x[2:]) for x in pieces]) == new_Pos)) #delete it from pieces
        if new_Pos in [0,7,56,63] and _capturedPiece[1]=='R': info[(2,1,4,3)[np.where(np.array((0,7,56,63))==new_Pos)[0][0]]]=False #if rook captured handle roke logic baced on board position -> info position changes    
        board[int(_capturedPiece[2:])] = None #update board for the _capturedPiece

    #update info , kingPositions for moved p->2sq ,K ,R
    info[0] = int(piece[2:])%Nwidth if abs(int(piece[2:])//Nwidth-new_Pos//Nwidth)==2 and piece[1]=='p' else None #pawn 2 sq move
    if piece[1] =="K": info[3 if piece[0]=='b' else 1:5 if piece[0]=='b' else 3] , kingPositions[0 if piece[0]=='w' else 1] = [False,False] , new_Pos #king move
    elif piece in ['wR0','wR7','bR56','bR63']: info[1+np.where(np.array(['wR7','wR0','bR63','bR56'])==piece)[0][0]] = False #rook move
    
    #update board with moved piece
    board[new_Pos] , board[int(piece[2:])] = piece[:2] , None 
    #update board for pawn promotion -> Q   
    if piece[1]=='p' and new_Pos//Nwidth in [7,0]: board[new_Pos]=piece[0]+'Q' 
    #update list pieces for the moved piece also working for promotion
    pieces[np.where(pieces == piece)[0][0]] = board[new_Pos]+str(new_Pos) 

    #update board , pieces for casling (R)
    if abs(new_Pos%Nwidth - int(piece[2:])%Nwidth)==2 and piece[1]=='K':
        if new_Pos%Nwidth==6: 
            board[5 if piece[0]=='w' else 61] , board[7 if piece[0]=='w' else 63] = piece[0]+'R' , None #small casles
            pieces[np.where(pieces == piece[0]+'R'+str(7 if piece[0]=='w' else 63))[0][0]] = piece[0]+'R' + str(5 if piece[0]=='w' else 61) #update pieces for R small casling
        else: 
            board[3 if piece[0]=='w' else 59] , board[0 if piece[0]=='w' else 56] = piece[0]+'R' , None #big casles
            pieces[np.where(pieces == piece[0]+'R'+str(0 if piece[0]=='w' else 56))[0][0]] = piece[0]+'R' + str(3 if piece[0]=='w' else 59) #update pieces for R big casling


    #defining new Node 
    newNode = Node(move,board,pieces,info,not node.whiteToPlay)
    #update the king position in new Node
    newNode.kingPositions = kingPositions
    #update the isCheck arg of newNode  ################needs change to not use the function for attacking sq but have them already in the node as an arg
    newNode.isCheck = True if isCheck('w' if piece[0]=='b' else 'b',attacking_Squares_Total('w' if piece[0]=='b' else 'b',newNode),newNode) else False
    
    #handle the new leagal moves of the new Node
    if enable_calculate_next_leagal_moves:
        newNode.current_leagalMoves = find_new_leagal_moves(piece,new_Pos,node,newNode,capturedPiece = _capturedPiece)
        node.addChild(newNode)

    #print("time: ",time.time()-start)
    return newNode

def isCheck(color ,aSq,node):
    pos = 0 if color=='w' else 1 #if is white the value is on the first column #else one second column

    if node.kingPositions[pos] in aSq:
        return True
    return False

def attacking_Squares_Total(color,node): #track the before attacking sq and redefine bace on the diff of the move
    _Pieces = node.current_Pieces
    board = node.current_board

    squares = []
    for piece in _Pieces:
        if piece[0]!=color:
            tmp=attacking_Squares(piece,board)
            squares+=tmp
    return list(set(squares)) #αμα θελω σε καθε νοδε να κραταω την διαφορα στα attacking squares για ποιο γρήγορα δε το θελω σε set αλλα append πρεπει να εγω και το ποσες φορες απειλείται το καθε square

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

def find_new_leagal_moves(piece,new_Pos,node,newNode,capturedPiece = None):
    tmp_leagal_moves = copy.deepcopy(node.current_leagalMoves)
    
    #update tmp_leagal_moves for moved piece 
    del tmp_leagal_moves[piece] #removing from dictionarry the before state
    tmp_leagal_moves[piece[:2] + str(new_Pos)] = leagalMoves(piece[:2] + str(new_Pos),newNode) #adding the new state

    #update tmp_leagal_moves for capturedPiece
    if capturedPiece!=None: del tmp_leagal_moves[capturedPiece]
    
    #update tmp_leagal_moves for roke (extra rook new moves)
    if piece[1]=='K' and abs(int(piece[2:])-new_Pos)==2: #handle roke
        y = new_Pos//Nwidth
        x = new_Pos%Nwidth
        if y==0: #white side
            if x >4: #small roke
                del tmp_leagal_moves['wR7']
                tmp_leagal_moves['wR5'] = leagalMoves('wR5',newNode)
            else: #big roke
                del tmp_leagal_moves['wR0']
                tmp_leagal_moves['wR3'] = leagalMoves('wR3',newNode)
        else: #black side
            if x >4: #small roke
                del tmp_leagal_moves['bR63']
                tmp_leagal_moves['bR61'] = leagalMoves('bR61',newNode)
            else: #big roke
                del tmp_leagal_moves['bR56']
                tmp_leagal_moves['bR59'] = leagalMoves('bR59',newNode)

    
    check_positions = [] #positions for the updated pieces 
    for horseMove in [[2,-1],[2,1],[1,2],[-1,2],[-2,-1],[-2,1],[-1,-2],[1,-2]]:
        run , tmp_pos =newPos(int(piece[2:]),horseMove[0],horseMove[1])
        if not run: continue
        if newNode.current_board[tmp_pos]!=None:
            if newNode.current_board[tmp_pos][1]=='N' and tmp_pos!=new_Pos: 
                #print("N: ",horseMove," ",int(piece[2:])," ",newNode.current_board[tmp_pos]," pos: ",tmp_pos," ",tmp_pos)
                check_positions.append(tmp_pos)

    for direction in [[0,1],[1,1],[1,0],[0,-1],[-1,-1],[-1,0],[1,-1],[-1,1]]: 
        step = 0 
        run=True
        while run:
            step += 1 
            dx = step*direction[0]
            dy = step*direction[1]
            run , tmp_pos = newPos(int(piece[2:]),dx,dy)
            if tmp_pos == new_Pos: continue
            if run and newNode.current_board[tmp_pos]!=None:
                run = False
                check_positions.append(tmp_pos)
    for direction in [[0,1],[1,1],[1,0],[0,-1],[-1,-1],[-1,0],[1,-1],[-1,1]]: 
        step = 0 
        run=True
        while run:
            step += 1 
            dx = step*direction[0]
            dy = step*direction[1]
            run , tmp_pos = newPos(new_Pos,dx,dy)
            if tmp_pos == new_Pos: continue
            if run and newNode.current_board[tmp_pos]!=None:
                run = False
                check_positions.append(tmp_pos)

    
    #if check update check_positions for all the pieces of the attacked color
    if newNode.isCheck: check_positions += [ int(key[2:]) for key in tmp_leagal_moves.keys() if tmp_leagal_moves[key]!=[]]

    # update check_positions for all the pieces of the attacked color if newNode left from check
    if node.isCheck and not newNode.isCheck: check_positions += [ int(key[2:]) for key in tmp_leagal_moves.keys()]

    #delete the multiple same values for the array using set() data type
    check_positions = set(check_positions) 

    for position in check_positions: #replace the new moves in newNode.current_leagalMoves
        _piece = newNode.current_board[position]+str(position)
        
        del tmp_leagal_moves[_piece]
        tmp_leagal_moves[_piece] = leagalMoves(_piece,newNode)
    
   
    #print(tmp_leagal_moves)
    return tmp_leagal_moves

def newPos(t,dx,dy):
    if t>=Nwidth*Nheight: return False, None

    if (t//Nwidth<Nheight-abs(dy) and dy>=0) or (t//Nwidth>=abs(dy) and dy<0):
        if (t%Nwidth<Nwidth-abs(dx) and dx>=0) or (t%Nwidth>=abs(dx) and dx<0):
            return True, t+dy*Nwidth+dx
    return False, None

def leagalMoves(piece,node): #piece : my moving piece, pieces all the pieces of the board , board : the arr of the board
    #start = time.time()
    pieces = node.current_Pieces
    board = node.current_board

    aSq=attacking_Squares_Total(piece[0],node)
    posibleMove = posibleMoves(piece,node)
    
    logic , directions , pSq = pinnedSquares(pieces,piece[0],board)
    
    finalSq=[]
    
    if int(piece[2:]) in pSq and logic: #handle pinned Pieces
        for i in range(len(pSq)):
            if int(piece[2:])==pSq[i]:
                break

        for sq in posibleMove:
            sq_X=sq%Nwidth
            sq_Y=sq//Nwidth
            P_X=int(piece[2:])%Nwidth
            P_Y=int(piece[2:])//Nwidth
            if (sign([sq_X-P_X,sq_Y-P_Y]) == directions[i]) or (sign([P_X-sq_X,P_Y-sq_Y]) == directions[i]):
                finalSq.append(sq)

    elif piece[1]=='K':
        for move in posibleMove:
            if move not in aSq: finalSq.append(move)
    else:
        finalSq=posibleMove[:]        


    #check case
    if node.isCheck: 
        finalSq_output = []
        for move in finalSq:
            newNode = movePiece(piece,move,node,enable_calculate_next_leagal_moves=False) #do the move 
            aSq = attacking_Squares_Total(piece[0],newNode) #find the new attackted sq
            if isCheck(piece[0],aSq,newNode)==False: #see again if is in check
                finalSq_output.append(move)
        #print("out: ",finalSq_output)
        return finalSq_output

    
    #print("time: ",time.time()-start)
    return finalSq

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

def sign(x):
    a,b = None,None
    if abs(x[0])==abs(x[1]):
        if x[0]==0: a=0 
        else: a=x[0]/abs(x[0])
        if x[1]==0: b=0 
        else: b=x[1]/abs(x[1])
        return [a,b]
    else:
        return [0,0]

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
