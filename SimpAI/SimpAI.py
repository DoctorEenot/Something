from keras.models import Sequential
from keras.layers import Dense, Activation
import keras.backend as K
import tensorflow as tf
import keras
import random
import pygame
from agent import Agent
from enemy import Enemy
import math
import threading 
import numpy as np
import time

tick = 0 
model = Sequential([
    Dense(200, input_dim=7),
    Activation('relu'),
    Dense(500),
    Activation('tanh'),
    Dense(1),
    Activation('sigmoid'),])
        #self.wnd.update()
model.compile(optimizer='adam',
              loss='mean_absolute_error',
              metrics=['accuracy'])

pygame.init()
window = pygame.display.set_mode((900,700))
pygame.display.set_caption("Game")
qmat = []
reward = 0
agent = Agent()
enemy = Enemy()
# = ()
act = 4
delta = 0.1
prevacts = []
prevact = 0

def Learn():
    global model,delta
    #pygame.display.update()
    input = [agent.prevcoord[0]/100,agent.prevcoord[1]/100,enemy.prevcoord[0]/100,enemy.prevcoord[1]/100,act,tick,delta]
    #pygame.display.update()
    model.fit(np.array([input]),np.array([[reward]]),epochs = 10,batch_size = 32)
    #pygame.display.update()

def Predict():
    global model,qmat,act,delta
    for i in range(len(qmat)):
        #pygame.display.update()
        if [agent.coord[0],agent.coord[1],enemy.coord[0],enemy.coord[1]] in qmat[i]:
            act = qmat[i][1].index(max(qmat[i][1]))
            return
    out = []
    for i in range(8):

        #pygame.display.update()
        input_ = [agent.coord[0]/100,agent.coord[1]/100,enemy.coord[0]/100,enemy.coord[1]/100,i,tick,delta]
        out.append(model.predict(np.array([input_])))
        #pygame.display.update()
    #pygame.display.update()
    act = out.index(max(out))

def CalcReward():
    global reward,delta
    if not agent.alive:
        reward = -10
        n = 0
        for i in range(len(qmat)):
            if n == len(prevacts):    
                return
            elif prevacts[n] in qmat[i]:
                try:
                    qmat[i][1][qmat[i][1].index(max(qmat[i][1]))] += (reward*n*delta*tick)
                except:
                    pass
                n+=1
            
    else:
        #reward = (math.sqrt((agent.coord[0]-enemy.coord[0])**2 + (agent.coord[1]-enemy.coord[1])**2)/20000 + tick)*delta
        reward = tick * delta
        #reward = math.fabs(math.sqrt((agent.coord[0]-enemy.coord[0])**2 + (agent.coord[1]-enemy.coord[1])**2)/100 - tick*1000)
        #reward = tick*100
def qUpdate():
    global reward,prevacts
    prevacts = []
    for i in range(len(qmat)):
        #pygame.display.update()
        if [agent.prevcoord[0],agent.prevcoord[1],enemy.prevcoord[0],enemy.prevcoord[1]] in qmat[i]:
            #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            prevacts.append(qmat[i].copy())
            qmat[i][1][act] += reward
            return
    qmat.append([])
    #pygame.display.update()
    qmat[len(qmat)-1].append([agent.prevcoord[0],agent.prevcoord[1],enemy.prevcoord[0],enemy.prevcoord[1]])
    qmat[len(qmat)-1].append([random.randint(0,7),random.randint(0,7),random.randint(0,7),random.randint(0,7),random.randint(0,7),random.randint(0,7),random.randint(0,7),random.randint(0,7)])
    #qmat[len(qmat)-1].append([0,0,0,0,0,0,0,0])
def R():
    pygame.display.update()
    #time.sleep(0.01)

e = threading.Event()
t = threading.Thread(target = R)

def main():
    global model,agent,enemy,act,delta
    count = 1
    t.start()
    e.set()
    while True:
        delta+=0.1
        prevacts = []
        tick = 0
        print("Started1")
        agent.coord = [500,100]
        enemy.coord = [300,600]
        #print(qmat)
        
        agent.alive = True
        
        time.sleep(0.5)

        while agent.alive:
            prevact = act
            window.fill((0,0,0))
            #pygame.display.update()
            print("Started")
            if count <2:
                
                agent.move(window,random.randint(0,7))
                enemy.prevcoord = enemy.coord.copy()
                enemy.move(window,agent.coord.copy())
                #enemy.prevcoord = enemy.coord.copy()
                qUpdate()
                count+=1
            else:
                Predict()
                
                agent.move(window,act)
                enemy.prevcoord = enemy.coord.copy()
                enemy.move(window,agent.coord.copy())
            pygame.display.update()
            if agent.coord[0]+agent.width > 900 or agent.coord[0] < 0 or agent.coord[1]+agent.hight > 700 or agent.coord[1] < 0 or (math.fabs((agent.coord[0]+agent.width)-(enemy.coord[0]+enemy.width)) < enemy.width and math.fabs((agent.coord[1]+agent.hight)-(enemy.coord[1]+enemy.hight)) < enemy.hight):
                agent.alive = False
            
            CalcReward()
            Learn()
            print(agent.coord,agent.prevcoord)
            qUpdate()
            tick+=1
    #e.set()
    t.join()



#e.set()
main()
