import numpy as np
from copy import deepcopy
import pygame
import random

class Pixel:
    def __init__(self,state):
        self.state = state
        self.deadage = 10
    def birth(self):
        self.state = 1
        self.deadage = 0
    def die(self):
        self.state = 0
        self.deadage = 0
    def deader(self):
        self.deadage += 1
    def checkState(self):
        return self.state
    def show(self):
        smolbox = pygame.Surface((10,10))
        if self.state:
            smolbox.fill((255,255,255))
        elif self.deadage < 10:
            smolbox.fill((0,255*(10-self.deadage)/30,0))
        else:
            smolbox.fill((0,0,0))
        return smolbox



class Play:
    def __init__(self,beginState):
        self.height, self.width = np.shape(beginState)
        self.height += 2
        self.width += 2 #edges
        self.playarea = [[0 for x in range(self.width)] for y in range(self.height)]
        pygame.init()
        global screen
        screen = pygame.display.set_mode([10*self.width,10*self.height])
        for y in range(self.height-2):
                for x in range(self.width-2):
                    self.playarea[y+1][x+1] = Pixel(beginState[y][x])
                self.playarea[y+1][0] = Pixel(0)
                self.playarea[y+1][self.width-1] = Pixel(0) #edges
        for x in range(self.width):
            self.playarea[0][x] = Pixel(0)
            self.playarea[self.height-1][x] = Pixel(0) #top and bottom
    def tick(self):
        self.currentState = deepcopy(self.playarea)
        for y in range(1,self.height-1):
            for x in range(1,self.width-1):
                self.neighbours = self.currentState[y  ][x+1].checkState() \
                                + self.currentState[y+1][x+1].checkState() \
                                + self.currentState[y+1][x  ].checkState() \
                                + self.currentState[y+1][x-1].checkState() \
                                + self.currentState[y  ][x-1].checkState() \
                                + self.currentState[y-1][x-1].checkState() \
                                + self.currentState[y-1][x  ].checkState() \
                                + self.currentState[y-1][x+1].checkState() #processing is cool 
                if self.currentState[y][x].checkState():
                    if self.neighbours in [0,1,4,5,6,7,8]: #THE RULES
                        self.playarea[y][x].die()
                else:
                    if self.neighbours == 3:               #ALSO THE RULES
                        self.playarea[y][x].birth()
                    else:
                        self.playarea[y][x].deader()
    def screenShow(self):
        global screen
        for y in range(1,self.height-1):
            for x in range(1,self.width-1):
      
                screen.blit(self.playarea[y][x].show(),(10*x,10*y))
        pygame.display.flip()

    # def jankShow(self):
    #     string = ""
    #     for y in range(1,self.height-1):
    #         for x in range(1,self.width-1):
    #             string += self.playarea[y][x].show()
    #         string += "\n"
    #     print(string)


class Game:
    def __init__(self):
        self.ran = False
        self.height = int(input("How tall? "))
        self.width  = int(input("How w i d e? "))
        self.start = [[0 for x in range(self.width)] for y in range(self.height)]
        for line in range(self.height):
            self.text = input(f'Line {line+1}: Enter up to {self.width} characters (0 is dead, 1 is alive)  ')
            if self.text == "go":
                break

            if self.text == "random":
                self.ran = True
                break

            if not self.text.isnumeric():
                self.text = "0"*self.width

            elif len(self.text) < self.width:
                self.steps = 0
                self.text  = str(self.text)
                while len(self.text) < self.width:
                    if self.steps%2:
                        self.text += "0" #right padding
                        self.steps += 1
                    else:
                        self.text = "0" + self.text #left padding, alternating so the input is centred
                        self.steps += 1
            self.start[line][0:self.width] = [int(num) for num in self.text]

        if self.ran:
            self.start = [[random.randint(0,1) for x in range(self.width)] for y in range(self.height)]
        self.s = Play(self.start) #initialise screen area


    def go(self):
        self.turn = 0
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.s.screenShow()
            #time.sleep(.1)
            self.s.tick()

    def show(self):
        self.s.jankShow()
Game().go()