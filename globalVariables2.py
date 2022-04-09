import numpy as np

colors={
    "background_colour": (234, 212, 252),

    
}

pieceWeight = {
    "p":1,
    "R":5,
    "N":3,
    "B":3,
    "Q":9,
    "K":300
}

class Node:
    def __init__(self,move,board,pieces :dict,info,whiteToPlay): #add self.king positions = [w pos,b pos] to remove some loops
        # elements
        self.whiteToPlay = whiteToPlay
        self.move = move

        self.current_board = np.copy(board)
        self.current_Pieces = np.copy(pieces)
        self.current_info = np.copy(info)

        self.parent=None
        self.children = {}

        self.kingPositions = [None,None]
        self.current_leagalMoves = {}
        self.isCheck = False
        #


    def setParent(self,parent): self.parent = parent

    def addChild(self,child):
        child.setParent(self) #def the childs parent the curent node
        self.children[str(child.move)]=child #add the child to child list
    
    def removeChild(self,node):
        del self.children[str(node.move)]
        
    def copy(self):
        return Node(self.move,self.board,self.pieces,self.info,self.whiteToPlay)


background_colour = (234, 212, 252)

windowDimentions = (1200,1000)

topleftpointofboard=(windowDimentions[0]//8,windowDimentions[1]//8)

chessBoardDim = windowDimentions[0]/2
sqMax = chessBoardDim//8
squareDimentions = [min(windowDimentions[0]//8,windowDimentions[1]//8,sqMax),min(windowDimentions[0]//8,windowDimentions[1]//8,sqMax)]
captionText = "Atomic Chess Atempt"

whiteToMoveStart = True

black_color = (144,88,45)
white_color = (230,219,210)
highlightColor = [(51, 153, 0),(153, 255, 102)]

Nwidth = 8
Nheight = 8
view=1

import pygame
def createWindow():    
    screen = pygame.display.set_mode(windowDimentions)
    screen.fill((102, 65, 45))
    pygame.display.set_caption(captionText)
    return screen

screen=createWindow()