import pygame, sys
from aquarium import Aquarium
from fish import Fish

class View():

    def __init__(self, grid_size):
        pygame.init()
        self.HIEGHT = grid_size
        self.WIDTH = self.HIEGHT

        self.BACKGROUND_COLOR = (52, 192, 235)

        #display screen
        pygame.display.set_caption('Aquarium')
        screen = pygame.display.set_mode((self.HIEGHT, self.WIDTH))
        screen.fill(self.BACKGROUND_COLOR)

        #display view
        self.displayView()

    #todo add case for what sprite will populate at loc x
    def updateSprites(self, loc, type):

        #translate based on pygame size and aquarium array size
        self.translateLoc(loc)
        pass

    #todo
    def translateLoc(self,loc):
        pass

    def displayView(self):
        while True:
            event = pygame.event.wait()
            # if press exit button
            if event.type == pygame.QUIT:
                sys.exit()

            #todo get type (fish/food) and their locations from backend
            # this will update each tic of display
            loc = (0,0)
            type = 'unknown'
            self.updateSprites(loc, type)

            pygame.display.update()