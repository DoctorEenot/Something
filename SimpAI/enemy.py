import pygame
import math
class Enemy:
    def __init__(self):
        self.coord = [90,70]
        self.prevcoord = []
        #self.prevcoord = self.coord
        self.speed = 3
        self.color = (255,0,0)
        self.width = 20
        self.hight = 20
    def move(self,win,coords):
        #self.prevcoord = self.coord.copy()
        try:
            self.coord[0] = int(self.coord[0] - self.speed * ((self.coord[0]-coords[0])/math.fabs(coords[0]-self.coord[0])))
        except:
            pass
        try:
            self.coord[1] = int(self.coord[1] - self.speed * ((self.coord[1]-coords[1])/math.fabs(coords[1]-self.coord[1])))
        except:
            pass
        print((self.coord[1]-coords[1]))
        pygame.draw.rect(win,self.color,(self.coord[0],self.coord[1],self.width,self.hight))