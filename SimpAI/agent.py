import pygame

class Agent:
    def __init__(self):
        self.coord = [50,50]
        self.prevcoord = []
        self.speed = 15
        self.color = (0,255,0)
        self.width = 20
        self.hight = 20
        self.alive = True
    def move(self,wnd,act):
        self.prevcoord = self.coord.copy()
        if act == 0:
            self.coord[0]-=self.speed
        elif act == 1:
            self.coord[0]-=self.speed
            self.coord[1]-=self.speed
        elif act == 2:
            self.coord[1]-=self.speed
        elif act == 3:
            self.coord[0]+=self.speed
            self.coord[1]-=self.speed
        elif act == 4:
            self.coord[0]+=self.speed
        elif act == 5:
            self.coord[0]+=self.speed
            self.coord[1]+=self.speed
        elif act == 6:
            self.coord[1]+=self.speed
        elif act == 7:
            self.coord[0]-=self.speed
            self.coord[1]+=self.speed
        
        pygame.draw.rect(wnd,self.color,(self.coord[0],self.coord[1],self.width,self.hight))

