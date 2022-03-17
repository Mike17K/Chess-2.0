import time
from visuals2 import *
from functions2 import *


def chessPosition1(screen,myGame):
    Pieces = myGame.current_Pieces
    board = myGame.current_board

    dt = 0.5
    movePiece('wp12',28,myGame)
    drawBoard(screen,myGame.current_board,view,[])
    time.sleep(dt)
    movePiece('bp52',36,myGame)
    drawBoard(screen,myGame.current_board,view,[])
    time.sleep(dt)
    movePiece('wB5',26,myGame)
    drawBoard(screen,myGame.current_board,view,[])
    time.sleep(dt)
    movePiece('bN57',42,myGame)
    drawBoard(screen,myGame.current_board,view,[])
    time.sleep(dt)
    movePiece('wQ3',21,myGame)
    drawBoard(screen,myGame.current_board,view,[])
    time.sleep(dt)