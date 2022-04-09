import pygame
from visuals2 import *
import time
from chessPositions import *
from functions2 import *
from AI import *

board = Nheight*Nwidth*[None]
pygame.init()
whiteToPlay=True

#Create pieces
#Pieces = {'wR': [0,7],'wN':[1,6],'wB':[2,5],'wQ':[3],'wK':[4],'wp':[8,9,10,11,12,13,14,15],
#'bR': [56,63],'bN': [57,62],'bB': [58,61],'bQ': [59],'bK': [60],'bp': [48,49,50,51,52,53,54,55]}


Pieces = ['wR0','wN1','wB2','wQ3','wK4','wB5','wN6','wR7']
Pieces += ['wp8','wp9','wp10','wp11','wp12','wp13','wp14','wp15']

Pieces += ['bp48','bp49','bp50','bp51','bp52','bp53','bp54','bp55']
Pieces += ['bR56','bN57','bB58','bQ59','bK60','bB61','bN62','bR63']

#short list for increasing the speed of the alpha beta minimax
Pieces.sort(key = lambda x: pieceWeight[x[1]],reverse=True)


#Place the pieces in the board
for piece in Pieces: board[int(piece[2:])] = piece[:2]

#################
# Main program
#################

myGame = ChessGame(board,Pieces,[None,True,True,True,True],whiteToPlay) #None: no pawn 2 moves before, ,True,True,True,True for each roke

#chessPosition1(screen,myGame)
click=0

#GUI 
Button1 = button(screen,click,pos=[2.9*chessBoardDim//8,1.5*topleftpointofboard[1]+chessBoardDim],dimentions = [chessBoardDim//8,chessBoardDim//16],font=18,text="<<",color=[[57, 40, 28],[91, 83, 69]])
Button2 = button(screen,click,pos=[4.2*chessBoardDim//8,1.5*topleftpointofboard[1]+chessBoardDim],dimentions = [chessBoardDim//8,chessBoardDim//16],font=18,text="<",color=[[57, 40, 28],[91, 83, 69]])
Button3 = button(screen,click,pos=[5.5*chessBoardDim//8,1.5*topleftpointofboard[1]+chessBoardDim],dimentions = [chessBoardDim//8,chessBoardDim//16],font=18,text="DEL",color=[[254, 100, 107],[254, 21, 60]])
Button4 = button(screen,click,pos=[6.8*chessBoardDim//8,1.5*topleftpointofboard[1]+chessBoardDim],dimentions = [chessBoardDim//8,chessBoardDim//16],font=18,text=">",color=[[57, 40, 28],[91, 83, 69]])
Button5 = button(screen,click,pos=[8.1*chessBoardDim//8,1.5*topleftpointofboard[1]+chessBoardDim],dimentions = [chessBoardDim//8,chessBoardDim//16],font=18,text=">>",color=[[57, 40, 28],[91, 83, 69]])
Button6 = button_togle(screen,click,pos=[1.5*chessBoardDim,topleftpointofboard[1]],dimentions = [chessBoardDim//8,chessBoardDim//16],font=18,text="AI On-Off",color=[[91, 186, 69],[254, 100, 107]])
Button6.mode = 1
Button8 = button_togle(screen,click,pos=[1.5*chessBoardDim+1.5*chessBoardDim//8,topleftpointofboard[1]],dimentions = [chessBoardDim//8,chessBoardDim//16],font=18,text="AI color",color=[[50, 50, 50],[255, 255, 255]])
Button8.mode = 1
Button7 = button_togle(screen,click,pos=[5.5*chessBoardDim//8,chessBoardDim//8+1.5*topleftpointofboard[1]+chessBoardDim],dimentions = [chessBoardDim//8,chessBoardDim//16],font=18,text="Rotate",color=[[50, 50, 50],[255, 255, 255]])

#program loop
running = True
AI=Button6.mode
AIColor=not (Button8.mode==1)
startPos=None
highlightSq=[]
leagal_Moves=[]
while running:
    for event in pygame.event.get():
 
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:                    
            if event.key == pygame.K_p:
                print("Total Node Tree: ")
                printNodeTree(myGame.root,0)
                #print(myGame.board_history)

                #find current path going bacwards the path and then disp it
                path=[]
                tmp = myGame.current_Node
                while True:
                    if tmp.move==None: break
                    path.append(tmp.move)
                    tmp = tmp.parent
                path.reverse()
                myGame.current_Node = myGame.root
                for i in path:
                    myGame.goToTheNextNode(i)
                    #pygame.event.get()
                    time.sleep(0.3)
                    drawBoard(screen,myGame.current_Node.current_board,view,highlightSq)

        if event.type == pygame.MOUSEBUTTONUP: click=0 #click handle kai move
        if event.type == pygame.MOUSEBUTTONDOWN: #click handle kai move
            click=1
            
            pos = getMouseSq(view)
            if pos==None: break
            if startPos!=None:
                if pos in leagal_Moves:
                    newNode = movePiece(myGame.current_Node.current_board[startPos]+str(startPos),pos,myGame.current_Node)
                    myGame.update(newNode)

                    whiteToPlay=myGame.current_Node.whiteToPlay
                    #print("Pieces: ",Pieces)
                    startPos = None
                    leagal_Moves=[]
                    highlightSq=[]
                    break
            if myGame.current_Node.current_board[pos]!=None:
                ok = False
                if whiteToPlay:
                    if myGame.current_Node.current_board[pos][0]=='w': ok = True
                elif myGame.current_Node.current_board[pos][0]=='b': ok = True
                if ok:
                    startPos = pos
                    leagal_Moves=leagalMoves(myGame.current_Node.current_board[pos]+str(pos),myGame.current_Node)
                    highlightSq = leagal_Moves
                else:
                    startPos = None
                    leagal_Moves=[]
                    highlightSq=[]
            else:
                startPos = None
                leagal_Moves=[]
                highlightSq=[]

    assets.update()

    if Button1.returnValue(click): #display the start position
        click=0
        myGame.goToStartNode()
        whiteToPlay = myGame.current_Node.whiteToPlay

    if Button2.returnValue(click): #display the prev node of the tree
        click=0
        if myGame.current_Node.parent!=None:
            myGame.goOnelayerUp()

            Button6.mode=0

            AI=0
            
            whiteToPlay = myGame.current_Node.whiteToPlay
        highlightSq=[]
        
    if Button3.returnValue(click):#del move #add the hole tree of moves when i add it
        click=0
        highlightSq=[]
        if myGame.current_Node.parent!=None:
            delNode(myGame.current_Node)

    if Button4.returnValue(click): myGame.goToTheNextNode() #fix
    if Button5.returnValue(click): myGame.goToTheFinalPosition()
    if Button7.returnValue(click): view*=-1

    if Button6.returnValue(click): #activate AI
        AI=Button6.mode
        highlightSq = []

    #print(click,Button6.click,Button6.mode,Button6.hover)

    if Button8.returnValue(click): #choose AI color
        AIColor=(Button8.mode==0)
        highlightSq = []
    
    '''
    Button8.mode=1-Button8.mode
    AIColor=whiteToPlay
    AI=1
    '''
    
    drawBoard(screen,myGame.current_Node.current_board,view,highlightSq)
    
    if whiteToPlay==AIColor and AI==1:
        if AI_player(myGame,whiteToPlay)==0:
            whiteToPlay=not whiteToPlay
        else:
            AI=0
            Button6.mode=0
    
    #add labels


    