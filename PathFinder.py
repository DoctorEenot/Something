#This is simple Path finder
#Created by Doctor Eenot
import pygame
import math
from random import *
pygame.init()
#win size:
WX = 1920 #Window X
WY = 1000 #Window Y
#Destination params:
Xdest = randint(20,WX)
Ydest = randint(20,WY)
Dwidth = 20
Dheight = 20

#Player params:
X0 = 100
Y0 = 100
X1 = X0
Y1 = Y0
width = 5
height = 5
speed = 5
Point = 0
distance = float(math.sqrt((Xdest - X1) ** 2 + (Ydest - Y1) ** 2))
prevdist = distance
#vesa = [(random()*2*3.14)/10000000,(random()*2*3.14)/10000000,(random()*2*3.14)/10000000,(random()*2*3.14)/10000000,(random()*2*3.14)/10000000,(random()*2*3.14)/10000000,(random()*2*3.14)/10000000,(random()*2*3.14)/10000000]
#vesa = [0.0000001, 0.000000001, 0.0000002, 0.00000003,0.00000002, 0.0000000002, 0.00000002, 0.000000003]#will be random later
vesa = [0,0,0,0,0,0,0,0]
#ACTIVATION FUNC
def sigm(nums):
    ret = []
    for i in range(8):
        ret.append(1.0 / (1.0 + math.exp(-nums[i])))
    return ret
#AI func   
def AI():
    global X1,Y1,distance,prevdist
    prevdist = distance
    global vesa
    buf = []
    for i in range(8):
        buf.append(distance*vesa[i])
    
    decision = sigm(buf)
    
    ind = decision.index(max(decision))
    if ind == 0 and Y1 >= speed:
        print('UP')
        Y1 = Y1 - speed
    elif ind == 1 and X1 < WX - width:
        print('RIGHT')
        X1 = X1 + speed
    elif ind == 2 and Y1 < WY - height:
        print('DOWN')
        Y1 = Y1 + speed
    elif ind == 3 and X1 >= speed:
        print('LEFT')
        X1 = X1 - speed
    elif ind == 4 and Y1 >= speed and X1 < WX - width:
        print('UP-RIGHT')
        X1 = X1 + speed
        Y1 = Y1 - speed
    elif ind == 5 and Y1 < WY - height and X1 < WX - width:
        print('DOWN-RIGHT')
        X1 = X1 + speed
        Y1 = Y1 + speed
    elif ind == 6 and Y1 < WY - height and X1 >= speed:
        print('DOWN-LEFT')
        X1 = X1 - speed
        Y1 = Y1 + speed
    elif ind == 7 and Y1 >= speed and X1 >= speed :
        print('UP-LEFT')
        X1 = X1 - speed
        Y1 = Y1 - speed

    distance = float(math.sqrt((Xdest - X1) ** 2 + (Ydest - Y1) ** 2))
    print(decision)
    if distance > prevdist:
        vesa[ind] = vesa[ind] - (8 / 1000000)*8
    elif distance == prevdist:
        vesa[ind] = vesa[ind] - (1 / 1000000)*4
    else:
        if vesa[ind]<0:
            vesa[ind] = vesa[ind]*(-1)+(1 / 1000000)
        elif vesa[ind] == 0:
            vesa[ind] = vesa[ind]+(1 / 1000000)
        else:
            vesa[ind] = vesa[ind]+(1 / 1000000)
    prevdist = distance

def main():
    global X1
    global Y1,Point
    run = True
    win = pygame.display.set_mode((WX,WY))
    pygame.display.set_caption("PathFinder")
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #win.fill((0,0,0))
        if (X1+width) >= Xdest and (X1+width) <= Xdest + Dwidth and (Y1+height) <= Ydest+Dheight and (Y1+height) >= Ydest:
            win.fill((0,0,0))
            print("Done!")
            Point = Point + 1
            pygame.draw.rect(win, (0,255,0), (Xdest,Ydest,Dwidth,Dheight))#Draw dest    
            pygame.draw.rect(win, (255,125,0),(X1,Y1,width,height))#Draw Player
            pygame.display.update()
            return
        fontObj = pygame.font.Font('freesansbold.ttf', 20)
        WIN = fontObj.render("Point: "+str(Point), True, (0,0,255), (0,0,0))
        box = WIN.get_rect()
        box.center = (WX-100, WY-100)
        win.blit(WIN, box)
        textSurfaceObj = fontObj.render(str(distance), True, (0,0,255), (0,0,0))
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (200, WY-100)
        win.blit(textSurfaceObj, textRectObj)
        
        pygame.draw.rect(win, (0,255,0), (Xdest,Ydest,Dwidth,Dheight))#Draw dest    
        pygame.draw.rect(win, (255,125,0),(X1,Y1,width,height))#Draw Player

        dec = AI()
        
        pygame.display.update()
while True:
    main()
    #vesa = [0.0000001, 0.000000001, 0.0000002, 0.00000003,0.00000002, 0.0000000002, 0.00000002, 0.000000003]
    vesa = [0,0,0,0,0,0,0,0]    
    Xdest = randint(1,WX)
    Ydest = randint(1,WY)
    #X1 = randint(1,WX)
    #Y1 = randint(1,WY)
