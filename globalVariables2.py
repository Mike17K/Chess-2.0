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