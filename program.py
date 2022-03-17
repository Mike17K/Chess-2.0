import pygame
from visuals2 import *
import time
from chessPositions import *
from functions2 import *
from AI import *

board = Nheight*Nwidth*[None]


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
myGame = ChessGame()
myGame.update(board,Pieces,[None,True,True,True,True]) #None: no pawn 2 moves before, ,True,True,True,True for each roke

#chessPosition1(screen,myGame)




running = True

whiteToPlay=True
startPos=None
highlightSq=[]
while running:
    for event in pygame.event.get():
 
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                view*=-1
            if event.key == pygame.K_LEFT:
                if len(myGame.board_history)>1:
                    myGame.undoMove()
            if event.key == pygame.K_p:
                #print(myGame.board_history)
                for i in myGame.board_history:
                    pygame.event.get()
                    drawBoard(screen,i,view,highlightSq)
                    time.sleep(0.3)
                
                


        if event.type == pygame.MOUSEBUTTONDOWN: #click handle kai move
            pos = getMouseSq(view)
            if pos==None: break
            if startPos!=None:
                if pos in highlightSq:
                    movePiece(myGame.current_board[startPos]+str(startPos),pos,myGame)
                    whiteToPlay=not whiteToPlay
                    #print("Pieces: ",Pieces)
                    startPos = None
                    highlightSq=[]
                    break
            
            if myGame.current_board[pos]!=None:
                ok = False
                if whiteToPlay:
                    if myGame.current_board[pos][0]=='w': ok = True
                elif myGame.current_board[pos][0]=='b': ok = True

                if ok:
                    startPos = pos
                    highlightSq=leagalMoves(myGame.current_board[pos]+str(pos),myGame)
                else:
                    startPos = None
                    highlightSq=[]
            else:
                startPos = None
                highlightSq=[]

    
    if whiteToPlay==False and False:
        #print(whiteToPlay==False)
        AI_player(myGame,whiteToPlay)
        whiteToPlay=not whiteToPlay
        


    drawBoard(screen,myGame.current_board,view,highlightSq)

    