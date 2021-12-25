import numpy as np
from copy import deepcopy
import pygame
import random
import time

class Pixel:
    def __init__(self,state):
        self.state = state
        self.deadage = 10
    def birth(self):
        self.state = 1
    def die(self):
        self.state = 0
        self.deadage = 0
    def deader(self):
        self.deadage += 1
    def checkState(self):
        return self.state
    def show(self,t):
        smolbox = pygame.Surface((10,10))
        if self.state:
            smolbox.fill((255,255,255))
        elif self.deadage < 10:
            colour = (10-self.deadage)/20*np.abs(np.array([(255*np.sin(t)),255*np.sin(t+2*np.pi/3),255*np.sin(t+4*np.pi/3)]))
            smolbox.fill(colour)
        else:
            smolbox.fill((0,0,0))
        return smolbox

    # def jankShow(self):
    #     string = ""
    #     for y in range(1,self.height-1):
    #         for x in range(1,self.width-1):
    #             string += self.playarea[y][x].show()
    #         string += "\n"
    #     print(string)


def Game(path="",padding = 10):
    t=0
    if path:
        pathdict = {".":"0","O":"1"}
        f = open(path, "r")
        code = f.readlines()
        width = 2*padding
        height = 2*padding
        for line in code:
            if line[0] != "!":
                height += 1
                if len(line)+2*padding > width:
                    width = len(line)+2*padding
        height += 2
        width += 2
        start = [[0 for x in range(width-2)] for y in range(height-2)]
        p = 0
        for line in code:
            if line[0] != "!":            
                text = "0"*padding+"".join([pathdict[a] for a in line[:-1]]) #left padding 10, -1 kills \n, which is 1 character somehow
                while len(text)<width:
                    text+="0"                                      #right padding 10 plus bonus
                start[p+padding][0:width-2] = [int(num) for num in text]
                print(text)
                p += 1


    else:
        ran = False
        height = int(input("How tall? ")) + 2 #extra for dead cells at edge
        width  = int(input("How w i d e? ")) + 2
        start = [[0 for x in range(width-2)] for y in range(height-2)]

        for line in range(height-2):
            text = input(f'Line {line+1}: Enter up to {width-2} characters (0 is dead, 1 is alive)  ')
            if text == "go":
                break

            if text == "random":
                ran = True
                break

            if not text.isnumeric():
                text = "0"*width

            elif len(text) < width:
                steps = 0
                text  = str(text)
                while len(text) < width:
                    if steps%2:
                        text += "0" #right padding
                        steps += 1
                    else:
                        text = "0" + text #left padding, alternating so the input is centred
                        steps += 1
            start[line][0:width-2] = [int(num) for num in text]

        if ran:
            start = [[random.randint(0,1) for x in range(width)] for y in range(height)]

    pygame.init()
    screen = pygame.display.set_mode([10*width-20,10*height-20]) #-20 here
    playarea = [[0 for x in range(width)] for y in range(height)] #define a h+2*w+2 matrix to store data from now on

    for y in range(height-2):
            for x in range(width-2):
                playarea[y+1][x+1] = Pixel(start[y][x])

            playarea[y+1][0] = Pixel(0)
            playarea[y+1][width-1] = Pixel(0) #edges dead

    for x in range(width):
        playarea[0][x] = Pixel(0)
        playarea[-1][x] = Pixel(0) #top and bottom dead
    turn = 0
    running = True

    #the main loop!
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #show screen and flip
        for y in range(0,height):
            for x in range(0,width):
                screen.blit(playarea[y][x].show(t),(10*x-10,10*y-10))
        pygame.display.flip()

        #progress one tick
        #time.sleep(.5)
        t += 0.1
        currentState = deepcopy(playarea)
        for y in range(1,height-1):
            for x in range(1,width-1):
                neighbours = currentState[y  ][x+1].checkState() \
                           + currentState[y+1][x+1].checkState() \
                           + currentState[y+1][x  ].checkState() \
                           + currentState[y+1][x-1].checkState() \
                           + currentState[y  ][x-1].checkState() \
                           + currentState[y-1][x-1].checkState() \
                           + currentState[y-1][x  ].checkState() \
                           + currentState[y-1][x+1].checkState() #processing is cool 
                if currentState[y][x].checkState():   #is alive
                    if neighbours not in [2,3]:       #THE RULES
                        playarea[y][x].die()
                else:                                 #is dead
                    if neighbours == 3:               #ALSO THE RULES
                        playarea[y][x].birth()
                    else:
                        playarea[y][x].deader()       #add 1 to how long dead
#Game()
Game("D:\\Coding\\Life Files\\orion.cells.txt",20)



