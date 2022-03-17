import pygame
from globalVariables2 import *

def loadImages():
    iconsName = ['wp','bp','wR','wB','wN','wQ','wK','bR','bB','bN','bQ','bK']
    pngs = {}
    for i in iconsName:
        pngs.update({i: pygame.image.load('icons/'+i+".png")})
    return pngs

icon = loadImages()

def drawBoard(screen,board,view,highlightSq):
    sq = squareDimentions
    color = [black_color,white_color]

    for t in range(Nwidth*Nheight):
        
        y=t//Nwidth
        x=t%Nwidth
        finalColor = color[(x+y+1)%2]

        if x+y*Nwidth in highlightSq: 
            finalColor = highlightColor[(x+y+1)%2]
            

        if view!=1: #draw the squares
            y=Nheight-y-1
            x=Nwidth-x-1
        
        
        

        pygame.draw.rect(screen,finalColor,(x*sq[1]+topleftpointofboard[0],(7-y)*sq[0]+topleftpointofboard[1],sq[1],sq[0]))

    for t in range(Nwidth*Nheight):
        y=t//Nwidth
        x=t%Nwidth

        

        if board[x+y*Nwidth]!=None:
            disp_icon = icon[board[x+y*Nwidth][:2]]
            if view!=1: #draw the squares
                y=Nheight-y-1
                x=Nwidth-x-1
                
            screen.blit(pygame.transform.scale(disp_icon,(sq[0],sq[0])), (x*sq[0]+topleftpointofboard[0],(7-y)*sq[1]+topleftpointofboard[1]))

    pygame.display.flip()          

def getMouseSq(view):
    x,y = pygame.mouse.get_pos()
    
    if x<topleftpointofboard[0] or y<topleftpointofboard[1]: return None

    x=(x-topleftpointofboard[0])//squareDimentions[0]
    y=(squareDimentions[1]*Nheight-y+topleftpointofboard[1])//squareDimentions[1]

    #print(x,y)
    if view!=1:
        x=7-x
        y=7-y

    if x<0 or y<0 or x>Nwidth-1 or y>Nheight-1:
        return None

    return x+Nwidth*y 

def createWindow():    
    screen = pygame.display.set_mode(windowDimentions)
    screen.fill(background_colour)
    pygame.display.set_caption(captionText)
    return screen

