import pygame
from visuals2 import *
import time
from chessPositions import *
from functions2 import *
from AI import *

board = Nheight*Nwidth*[None]
pygame.init()

#Create pieces
Pieces = ['wR0','wN1','wB2','wQ3','wK4','wB5','wN6','wR7']
Pieces += ['wp8','wp9','wp10','wp11','wp12','wp13','wp14','wp15']

Pieces += ['bp48','bp49','bp50','bp51','bp52','bp53','bp54','bp55']
Pieces += ['bR56','bN57','bB58','bQ59','bK60','bB61','bN62','bR63']

#Place the pieces in the board
for piece in Pieces: board[int(piece[2:])] = piece[:2]

#################
# Main program
#################
screen=createWindow()
myGame = ChessGame(board,Pieces,[None,True,True,True,True]) #None: no pawn 2 moves before, ,True,True,True,True for each roke

#chessPosition1(screen,myGame)
click=0

#GUI 
Button1 = button(screen,click,pos=[2.9*chessBoardDim//8,1.5*topleftpointofboard[1]+chessBoardDim],dimentions = [chessBoardDim//8,chessBoardDim//16],font=18,text="<<",color=[[57, 40, 28],[91, 83, 69]])
Button2 = button(screen,click,pos=[4.2*chessBoardDim//8,1.5*topleftpointofboard[1]+chessBoardDim],dimentions = [chessBoardDim//8,chessBoardDim//16],font=18,text="<",color=[[57, 40, 28],[91, 83, 69]])
Button3 = button(screen,click,pos=[5.5*chessBoardDim//8,1.5*topleftpointofboard[1]+chessBoardDim],dimentions = [chessBoardDim//8,chessBoardDim//16],font=18,text="DEL",color=[[254, 100, 107],[254, 21, 60]])
Button4 = button(screen,click,pos=[6.8*chessBoardDim//8,1.5*topleftpointofboard[1]+chessBoardDim],dimentions = [chessBoardDim//8,chessBoardDim//16],font=18,text=">",color=[[57, 40, 28],[91, 83, 69]])
Button5 = button(screen,click,pos=[8.1*chessBoardDim//8,1.5*topleftpointofboard[1]+chessBoardDim],dimentions = [chessBoardDim//8,chessBoardDim//16],font=18,text=">>",color=[[57, 40, 28],[91, 83, 69]])

Button6 = button_togle(screen,click,pos=[1.5*chessBoardDim,topleftpointofboard[1]],dimentions = [chessBoardDim//8,chessBoardDim//16],font=18,text="AI",color=[[254, 100, 107],[91, 186, 69]])

Button7 = button_togle(screen,click,pos=[5.5*chessBoardDim//8,chessBoardDim//8+1.5*topleftpointofboard[1]+chessBoardDim],dimentions = [chessBoardDim//8,chessBoardDim//16],font=18,text="Rotate",color=[[50, 50, 50],[255, 255, 255]])


running = True
AI=0
whiteToPlay=True
AIColor= not whiteToPlay
startPos=None
highlightSq=[]
while running:
    assets.update()
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
            if click==0: click=1

            pos = getMouseSq(view)
            if pos==None: break
            if startPos!=None:
                if pos in highlightSq:
                    movePiece(myGame.current_Node.current_board[startPos]+str(startPos),pos,myGame)
                    whiteToPlay=not whiteToPlay
                    #print("Pieces: ",Pieces)
                    startPos = None
                    highlightSq=[]
                    break
                
            if myGame.current_Node.current_board[pos]!=None:
                ok = False
                if whiteToPlay:
                    if myGame.current_Node.current_board[pos][0]=='w': ok = True
                elif myGame.current_Node.current_board[pos][0]=='b': ok = True

                if ok:
                    startPos = pos
                    highlightSq=leagalMoves(myGame.current_Node.current_board[pos]+str(pos),myGame)
                else:
                    startPos = None
                    highlightSq=[]
            else:
                startPos = None
                highlightSq=[]

    
    if Button1.returnValue(click): #display the start position
        click=0
        myGame.goToStartNode()

    if Button2.returnValue(click): #display the prev node of the tree
        click=0
        if myGame.current_Node.parent!=None:
            myGame.goOnelayerUp()
        
    if Button3.returnValue(click):#del move #add the hole tree of moves when i add it
        click=0
        if myGame.current_Node.parent!=None:
            print("Deleting Tree...")
            tmp = myGame.current_Node.parent
            delNode(myGame.current_Node) #fix
            myGame.current_Node = tmp


    if Button4.returnValue(click):
        click=0
        myGame.goToTheNextNode() #fix

    if Button5.returnValue(click):
        click=0
        myGame.goToTheFinalPosition()

    if Button6.returnValue(click):
        click=0
        AI=Button6.mode
        AIColor = whiteToPlay
        #print("True")

    if Button7.returnValue(click):
        click=0
        view*=-1

    mytext = ''''''

    '''
    label(screen,pos=[750,400],dimentions = [200,100],font=12,text=mytext,bg_color=[203, 246, 255])

    '''

    if whiteToPlay==AIColor and AI==1:
        #print(whiteToPlay==False)
        AI_player(myGame,whiteToPlay)
        whiteToPlay=not whiteToPlay
        


    drawBoard(screen,myGame.current_Node.current_board,view,highlightSq)

    