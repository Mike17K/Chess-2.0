from cv2 import fastNlMeansDenoising
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
                
            screen.blit(pygame.transform.scale(disp_icon,(int(sq[0]),int(sq[0]))), (int(x*sq[0]+topleftpointofboard[0]),int((7-y)*sq[1]+topleftpointofboard[1])))

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

    return int(x+Nwidth*y )

def createWindow():    
    screen = pygame.display.set_mode(windowDimentions)
    screen.fill((102, 65, 45))
    pygame.display.set_caption(captionText)
    return screen

class assets:
    items=[]
    def __init__(self):
        self.type=None

    @staticmethod
    def update():
                    
        x,y = pygame.mouse.get_pos()

        for asset in assets.items:
            asset.hover = False
            if x<=asset.pos[0]+asset.dimentions[0] and x>=asset.pos[0]:
                if y<=asset.pos[1]+asset.dimentions[1] and y>=asset.pos[1]:
                    asset.hover = True

            if asset.type=='button':
                if asset.hover:  
                    color = asset.color[1]
                    bg_color = [color[0],color[1],color[2]]
                else:
                    color = asset.color[0]
                    bg_color = [color[0],color[1],color[2]]
            elif asset.type=='button_togle':
                if asset.hover and asset.click==1:  
                    asset.mode=(asset.mode+1)%2
                    #print(asset.mode)

                if asset.mode==0: 
                    color = asset.color[1]
                elif asset.mode==1: 
                    color = asset.color[0]

                bg_color = [color[0],color[1],color[2]]
                

            font = pygame.font.Font('freesansbold.ttf', asset.font)
            text = font.render(asset.text, True, [0,0,0], bg_color)
            textRect = text.get_rect()
            pygame.draw.rect(asset.screen,bg_color,(asset.pos[0],asset.pos[1],asset.dimentions[0],asset.dimentions[1]))

            if asset.type=='button':
                asset.screen.blit(text, [asset.pos[0]+asset.dimentions[0]/2-textRect[2]/2,asset.pos[1]+asset.dimentions[1]/2-textRect[3]/2])
            elif asset.type=='button_togle':
                asset.screen.blit(text, [asset.pos[0]+asset.dimentions[0]/2-textRect[2]/2,asset.pos[1]+asset.dimentions[1]/2-textRect[3]/2])
            elif asset.type=='label':
                asset.screen.blit(text, [asset.pos[0]+20,asset.pos[1]+20])#draw text


class button(assets):
    def __init__(self,screen,click,pos=[None,None],dimentions = [100,50],font=18,text='',color=[100,100,100]):
        self.type='button'
        
        self.screen = screen
        self.pos=pos
        self.dimentions=dimentions
        self.font=font
        self.text=text
        self.color=color

        self.hover=False
        assets.items.append(self)
    
    def returnValue(self,click):
        if click==1 and self.hover:
            click=0
            return True
        return False

class button_togle(assets):
    def __init__(self,screen,click,pos=[None,None],dimentions = [100,50],font=18,text='',color=[100,100,100]):
        self.type='button_togle'
        self.mode=0
        self.click=0

        self.screen = screen
        self.pos=pos
        self.dimentions=dimentions
        self.font=font
        self.text=text
        self.color=color

        self.hover=False
        assets.items.append(self)
    
    def returnValue(self,click):
        self.click=click
        if click==1 and self.hover:
            click=0
            return True
        return False

'''
def button(screen,click,pos=[None,None],dimentions = [100,50],font=18,text='',color=[100,100,100]):
            
    x,y = pygame.mouse.get_pos()
    hover = False
    if x<=pos[0]+dimentions[0] and x>=pos[0]:
        if y<=pos[1]+dimentions[1] and y>=pos[1]:
            hover = True
            
    if hover:  
        bg_color = [color[0],color[1],color[2]]
    else:
        bg_color = [color[0],color[1]/4,color[2]/4]
        
    
    font = pygame.font.Font('freesansbold.ttf', font)
    text = font.render(text, True, [0,0,0], bg_color)
    textRect = text.get_rect()
    pygame.draw.rect(screen,bg_color,(pos[0],pos[1],dimentions[0],dimentions[1]))#draw rect
    screen.blit(text, [pos[0]+dimentions[0]/2-textRect[2]/2,pos[1]+dimentions[1]/2-textRect[3]/2])#draw text
    
    if click==1 and hover:
        return True
    return False

def label(screen,pos=[None,None],dimentions = [100,50],font=18,text='',bg_color=[100,100,100]):
    font = pygame.font.Font('freesansbold.ttf', font)
    text = font.render(text, True, [0,0,0], bg_color)
    textRect = text.get_rect()
    pygame.draw.rect(screen,bg_color,(pos[0],pos[1],dimentions[0],dimentions[1]))#draw rect
    screen.blit(text, [pos[0]+20,pos[1]+20])#draw text

'''