import random
import pygame, sys
from aquarium import Aquarium
from fish import Fish
from PyAquarium.PyGameObject import PyFish
from PyAquarium.PyGameObject import PyFood

class View():

    def __init__(self, grid_size, viewSize):
        pygame.init()
        self.HEIGHT = viewSize
        self.WIDTH = self.HEIGHT

        self.grid_size = grid_size
        #display view
        self.setUpGame()
        self.displayMain()

    def setUpGame(self):
        self.setGridScale()
        self.BACKGROUND_COLOR = (52, 192, 235)
        self.setFonts()
        self.setTrainingVars()
        self.setDisplay()
        #sprites must first have a display initialized
        self.setUpSprites()
        self.setVisionView()

    # possible move locations on board will be a factor of cells in array/grid
    # const_dist is critical variable allowing us to print sprites in correct location
    def setGridScale(self):
        # determine where to draw objects on grid
        start_pos = self.HEIGHT / self.grid_size  # start position
        self.const_dist = start_pos  # with add equal **distance from each line**

    def setDisplay(self):
        pygame.display.set_caption('Aquarium')
        self.grid = pygame.display.set_mode((self.HEIGHT, self.HEIGHT))
        self.grid.fill(self.BACKGROUND_COLOR)

    def setUpSprites(self):
        # object will be a constant fraction of screen size
        self.OBJ_SIZE = self.HEIGHT * .067
        self.CORRECTION = self.HEIGHT * .0067

        #greenEel, worm, redCarp <- move these arrays to pyGameObject
        self.sheet1SpriteLoc = [(3.8, 5.3), (8.2, 2.6), (.9, 1.9)]
        self.sheet2SpriteLoc = [(1,3)]
        self.trainingFish = PyFish(self.OBJ_SIZE, self.OBJ_SIZE, 'PyAquarium/Sprites/FishSheet2.png', self.sheet2SpriteLoc[0])
        self.npc = PyFood(self.OBJ_SIZE, self.OBJ_SIZE, 'PyAquarium/Sprites/FishSheet1.png', self.sheet1SpriteLoc[2])
        self.food = PyFood(self.OBJ_SIZE, self.OBJ_SIZE, 'PyAquarium/Sprites/FishSheet1.png', self.sheet1SpriteLoc[1])

    def setVisionView(self):
        self.CIRCLE_RADIUS = self.HEIGHT / self.grid_size #must be initialized from fish object in game logic
        self.CIRCLE_WIDTH = int(self.HEIGHT / self.grid_size / 8.75)
        self.circleColor = (9, 74, 115)

    def setFonts(self):
        self.font = pygame.font.SysFont(None, 32)

    def setTrainingVars(self):
        self.origin = (10, 10)  # starting point for the training fish
        self.possibleX = [1, 3, 5, 7, 13, 15, 17, 19]
        self.possibleY = [1, 3, 5, 7, 13, 15, 17, 19]
        self.training_fishes = [Fish.randomFishGenerator(self.origin, "training") for i in range(10)]

    def displayObject(self, loc, type, vision = None):
        row = loc[0]
        col = loc [1]

        #training fish
        if type == "training":
            #location translate based on grid/array size
            translatedLoc = (col * self.const_dist - self.CORRECTION, row * self.const_dist - self.CORRECTION)
            self.grid.blit(self.trainingFish.sprite, translatedLoc)

            pygame.draw.circle(self.grid, self.circleColor, (col * self.const_dist + (self.const_dist/1.8),
                                row * self.const_dist + (self.const_dist/1.3)), self.CIRCLE_RADIUS * vision, self.CIRCLE_WIDTH)

        #food
        if type == "food":
            # location translate based on grid/array size
            translatedLoc = (col * self.const_dist - self.CORRECTION, row * self.const_dist - self.CORRECTION)
            self.grid.blit(self.food.sprite, translatedLoc)

        #enmey
        if type == "npc":
            translatedLoc = (col * self.const_dist - self.CORRECTION, row * self.const_dist - self.CORRECTION)
            self.grid.blit(self.npc.sprite, translatedLoc)

    def displayStats(self, fish):
        padding = 25
        # show training fish score
        counting_text = self.font.render("Score: " + str(fish.score), 1, (0, 0, 0))
        self.grid.blit(counting_text, (1, self.grid_size / 10))
        vision_text = self.font.render("Vision: " + str(fish.vision), 1, (0, 0, 0))
        self.grid.blit(vision_text, (1, self.grid_size/10 + padding))
        risk_text = self.font.render("Risk: " + str(fish.riskAwareness), 1, (0, 0, 0))
        self.grid.blit(risk_text, (1, self.grid_size/10 + padding * 2))
        speed_text = self.font.render("Speed: " + str(fish.speed), 1, (0, 0, 0))
        self.grid.blit(speed_text, (1, self.grid_size/10 + padding * 3))

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
            aquarium = Aquarium(self.grid_size, fishes)
            while aquarium.lifetime < 100 and fishes[-1].status == 1:
                #slow down tics to viewable rate
                pygame.time.wait(300)

                # if press exit button
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                aquarium.updateSim()
                # get type (fish/food) and their locations from backend
                # this will update each tic of display
                for fish in aquarium.fishes:
                    if(fish.fishType == "training"):
                        self.displayObject(fish.loc, fish.fishType, fish.vision)
                        self.displayStats(fish)
                    else:
                        self.displayObject(fish.loc, fish.fishType)

                pygame.display.update()
                #cover up previous sprites
                self.grid.fill(self.BACKGROUND_COLOR)

            scores.append(i.score)
