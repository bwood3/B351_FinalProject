import random
import pygame, sys
from aquarium import Aquarium
from fish import Fish
from PyAquarium.PyGameObject import PyFish
from PyAquarium.PyGameObject import PyFood

class View():

    def __init__(self, grid_size, viewSize):
        pygame.init()
        self.HEIGHT = height = viewSize
        self.WIDTH = height
        # object will be a constant fraction of screen size
        self.OBJ_SIZE = self.HEIGHT * .067
        self.CORRECTION = self.HEIGHT * .0067
        # to know where to translate objects
        self.grid_size = grid_size
        #deterime where to draw objects on grid
        self.start_pos = self.HEIGHT / self.grid_size  # start position
        self.const_dist = self.start_pos  # with add equal **distance from each line**

        self.BACKGROUND_COLOR = (52, 192, 235)

        # display screen
        pygame.display.set_caption('Aquarium')
        self.grid = pygame.display.set_mode((height, height))
        self.grid.fill(self.BACKGROUND_COLOR)

        # game objects
        self.trainingFish = PyFish(self.OBJ_SIZE, self.OBJ_SIZE, 'PyAquarium/Sprites/FishSheet2.png')
        self.food = PyFood(self.OBJ_SIZE, self.OBJ_SIZE, 'PyAquarium/Sprites/FishSheet1.png')
        #todo import get enemy fish

        self.font = pygame.font.SysFont(None, 32)

        self.setUpLogic()
        #display view
        self.displayMain()

    def setUpLogic(self):
        self.origin = (10, 10)  # starting point for the training fish
        self.possibleX = [1, 3, 5, 7, 13, 15, 17, 19]
        self.possibleY = [1, 3, 5, 7, 13, 15, 17, 19]
        self.training_fishes = [Fish.randomFishGenerator(self.origin, "training") for i in range(10)]

    def displayObject(self, loc, type):
        row = loc[0]
        col = loc [1]

        #training fish
        if type == "training":
            #location translate based on grid/array size
            translatedLoc = (col * self.const_dist - self.CORRECTION, row * self.const_dist - self.CORRECTION)
            self.grid.blit(self.trainingFish.fish, translatedLoc)

        #food
        if type == "npc": #todo -> this is actually food display
            # location translate based on grid/array size
            translatedLoc = (col * self.const_dist - self.CORRECTION, row * self.const_dist - self.CORRECTION)
            self.grid.blit(self.food.food, translatedLoc)

        #enmey
        if type == "npc":
            pass

    #todo this logic will need to be updated with new code
    def displayMain(self):
        scores = []
        cycleCount = 0
        for i in self.training_fishes:
            print("Iteration #: {0}".format(cycleCount))
            cycleCount = cycleCount+1
            fishes = []
            for j in range(0, 10):
                x = random.randint(0, 7)
                y = random.randint(0, 7)
                loc = (self.possibleX[x], self.possibleY[y])
                f = Fish.randomFishGenerator(loc, "npc")
                fishes.append(f)
            i.score = 100
            fishes.append(i)
            aquarium = Aquarium(20, fishes)
            while aquarium.lifetime < 100 and fishes[-1].status == 1:
                #slow down tics to viewable rate
                pygame.time.wait(300)

                # if press exit button
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                aquarium.updateSim()
                #get type (fish/food) and their locations from backend
                # this will update each tic of display
                for fish in aquarium.fishes:
                    self.displayObject(fish.loc, fish.fishType)
                    if(fish.fishType == "training"):
                        # show training fish score
                        counting_text = self.font.render("Score: " + str(fish.score), 1, (0, 0, 0))
                        self.grid.blit(counting_text,(1,2))



                pygame.display.update()
                #cover up previous sprites
                self.grid.fill(self.BACKGROUND_COLOR)

            scores.append(i.score)
