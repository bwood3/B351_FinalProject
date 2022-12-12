import random
import pygame, sys
from evolution import Evolution
from aquarium import Aquarium
from fish import Fish
from PyAquarium.PyGameObject import PyFish, PyFood

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
        # to know last blit location of fish within this class store there memory locations in dict
        self.fishPrevLocDict = {}
        self.fishSmoothDict = {}
        self.trainingTierCaptured = False

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
        self.fps = 40
        # object will be a constant fraction of screen size
        self.OBJ_SIZE = self.HEIGHT * .067
        self.CORRECTION = self.HEIGHT * .0067

        #greenEel (higher tier), worm (food), redCarp (lower tire), blue fish(equal tier) <- move these arrays to pyGameObject
        self.sheet1SpriteLoc = [(3.8, 5.3), (8.2, 2.6), (.9, 1.9), (3.8, 4.4)]
        #training fish sheet
        self.westMoves = [(1,3),(1,4),(1,5)]
        self.eastMove = [(2,3),(2,4),(2,5)]
        self.trainingFish = PyFish(self.OBJ_SIZE, self.OBJ_SIZE, 'PyAquarium/Sprites/FishSheet2.png', self.fps)
        self.npcLowerTier = PyFood(self.OBJ_SIZE, self.OBJ_SIZE, 'PyAquarium/Sprites/FishSheet1.png', self.sheet1SpriteLoc[2])
        self.npcSameTier = PyFood(self.OBJ_SIZE, self.OBJ_SIZE, 'PyAquarium/Sprites/FishSheet1.png', self.sheet1SpriteLoc[3])
        self.npcHigherTier = PyFood(self.OBJ_SIZE, self.OBJ_SIZE, 'PyAquarium/Sprites/FishSheet1.png', self.sheet1SpriteLoc[0])
        self.food = PyFood(self.OBJ_SIZE, self.OBJ_SIZE, 'PyAquarium/Sprites/FishSheet1.png', self.sheet1SpriteLoc[1])

    def setVisionView(self):
        self.CIRCLE_RADIUS = self.HEIGHT / self.grid_size
        self.CIRCLE_WIDTH = int(self.HEIGHT / self.grid_size / 8.75)
        self.circleColor = (9, 74, 115)

    def setFonts(self):
        self.font = pygame.font.SysFont(None, 32)

    def setTrainingVars(self):
        self.origin = (10, 10)  # starting point for the training fish
        self.mutationChance = 0.02
        self.maxAttributePoints = 15
        # locations that our fish may spawn
        self.possibleX = [1, 3, 5, 7, 13, 15, 17, 19]
        self.possibleY = [1, 3, 5, 7, 13, 15, 17, 19]
        self.evolution = Evolution(self.mutationChance, self.origin, self.maxAttributePoints)
        self.training_fishes = [Fish.randomFishGenerator(self.origin, "training", self.maxAttributePoints) for i in range(11)]

        #showning attribute of one of our best fish
        # 5,5,4,7
        self.overRideTrainingFish =[Fish(self.origin, 5, 5, 4, 7, "training"), Fish(self.origin, 5, 5, 4, 7, "training"),
                                    Fish(self.origin, 5, 5, 4, 7, "training")]

    # take N*N grid and translate its proportional location to py view
    def translateLoc(self, col, row):
        return (col * self.const_dist - self.CORRECTION, row * self.const_dist - self.CORRECTION)

    def smoothBlit(self, fish, targetLoc, fishIteration =None, generation=None):

        if (fish.fishType == "training"):
            self.grid.blit(self.trainingFish.getFrame(), targetLoc)
            self.displayFishStats(fish, fishIteration, generation)

        elif (fish.fishType == "npc"):
            # lower tier
            if(fish.getTier() < self.trainingTierCaptured):
                self.grid.blit(self.npcLowerTier.sprite, targetLoc)
            # higher tier
            elif(fish.getTier() > self.trainingTierCaptured):
                self.grid.blit(self.npcHigherTier.sprite, targetLoc)
            # same tier
            else:
                self.grid.blit(self.npcSameTier.sprite, targetLoc)

        elif (fish.fishType == "food"):
            self.grid.blit(self.food.sprite, targetLoc)

    def aquariumStats(self, time):
        yStart = 5
        counting_text = self.font.render("Aquarium ticks: " + str(time), 1, (0, 0, 0))
        self.grid.blit(counting_text, (self.HEIGHT/2 - counting_text.get_width()/2, yStart))

    def displayFishStats(self, fish, fishIteration, generation):
        padding = 25
        yStart = 5
        # show training fish score
        counting_text = self.font.render("Score: " + str(fish.score), 1, (0, 0, 0))
        self.grid.blit(counting_text, (1, yStart))
        vision_text = self.font.render("Vision: " + str(fish.vision), 1, (0, 0, 0))
        self.grid.blit(vision_text, (1, yStart + padding))
        risk_text = self.font.render("Risk: " + str(fish.riskAwareness), 1, (0, 0, 0))
        self.grid.blit(risk_text, (1, yStart + padding * 2))
        speed_text = self.font.render("Speed: " + str(fish.speed), 1, (0, 0, 0))
        self.grid.blit(speed_text, (1, yStart + padding * 3))
        fishTier_text = self.font.render("Tier: " + str(fish.initTier), 1, (0, 0, 0))
        self.grid.blit(fishTier_text, (1, yStart + padding * 4))

        #show generation
        gen_text = self.font.render("Generation: " + str(generation), 1, (0, 0, 0))
        self.grid.blit(gen_text, (self.WIDTH - gen_text.get_width() - yStart, yStart))
        #show fish iteration with generation
        fishIter_text = self.font.render("Fish # in Gen: " + str(fishIteration), 1, (0, 0, 0))
        self.grid.blit(fishIter_text, (self.WIDTH - fishIter_text.get_width()- yStart, yStart + padding))

    def trainingFishEaten(self, fish, i, g):
        self.displayFishStats(fish, i, g)
        death = pygame.font.SysFont(None, 50).render("Training fish eaten", 1, (0, 0, 0))
        self.grid.blit(death, (self.HEIGHT/2 - death.get_width()/2, self.HEIGHT/2))

    # this method has bugs and needs to be update (specifically, delta does not always indicate direction as expected)
    # if a direction has been perform for > %50 of steps, change to that direction
    def checkDirec(self, fish, delta):
        # for training fish determine if direction change needed
        if (fish.fishType == "training"):
            if (self.trainingFish.direction == "east" and delta < 0):
                self.trainingFish.direction = "west"
            elif (self.trainingFish.direction == "west"):
                self.trainingFish.direction = "east"

    # for efficiency, the training algorithm spawns fish into there next grid location while moving -
    # - additionally fish with high speed may jump grid location -
    # - this algorithm smooths the gap between jumps (Note: it is import fish Dict is update after this method)
    # STACK -> [t1, x1, y1, z1, t2, x2, y2, z2, t3, x3, y3, z3] -
    # - Leave n-1 open space between each t (where n is number of fish in aquarium)
    # Alternative to above (method used):
    # store dictionary of moves for each fish id (moves is a list with the split frames)
    # create x points between between current and target location
    # loop through them in succession
    def getSteps(self, fish, targetLoc, nFrames = 3):
        hashableID = id(fish)
        prevLoc = self.fishPrevLocDict.get(hashableID)

        # if just initialized, simply draw fish
        if(prevLoc == None):
            self.smoothBlit(fish, targetLoc)
        else:
            # get delta (x,y) between two points
            # split delta into equal parts (by nFrame)
            # for each nth part add onto step (current location -> final addition is target)
            delta = tuple(map(lambda x, y : x - y, targetLoc, prevLoc))
            splitRow = delta[0] / nFrames
            splitCol = delta[1] / nFrames
            #get list of nFrames to add between current location and target
            smoothPath = []
            for i in range(nFrames):
                # get each step partial (the sum of each step = distance to target)
                step = (splitRow * (i+1), splitCol * (i+1))
                # append the partial to prev loc to get each coordinate in between fish should move (i.e., frames expanded)
                stepN = tuple(map(sum, zip(prevLoc, step)))
                smoothPath.append(stepN)
            #add each step as list for that fish to complete is concurrence with all other fish
            self.fishSmoothDict.update({hashableID: smoothPath})
            self.checkDirec(fish, delta[1])

        # now that we have compared previous to current loc -
        # - update fish current loc in dict. using translated location
        self.fishPrevLocDict.update({hashableID: targetLoc})

    #print frames retrieve from getSteps
    def smoothMove(self, time, frames, fps, aquarium, fishIteration, generation):
        # if we are not on first frame
        if (len(self.fishSmoothDict) != 0):
            for n in range(frames):
                pygame.time.wait(fps)
                for fish in aquarium.fishes:
                    step = self.fishSmoothDict.get(id(fish))
                    #sometimes food is thrown into aquarium, so a step does not yet exist for it
                    if (step != None):
                        # print(self.fishFrameDict.get(id(fish)))
                        self.smoothBlit(fish, step[n], fishIteration, generation)

                # display aquarium ticks
                self.aquariumStats(time)
                # update for each step
                pygame.display.update()
                # cover up previous sprites
                self.grid.fill(self.BACKGROUND_COLOR)
                # print(aquarium)

    #get tier so we know how to blit other fish
    def getTraininingTier(self, fish):
        if (fish.fishType == "training" and not self.trainingTierCaptured):
            self.trainingTierCaptured = fish.getTier()

    def resetGameVars(self):
        # reset fish dictionaries for new generation
        self.fishPrevLocDict.clear()
        self.fishSmoothDict.clear()
        # capture next iteration
        self.trainingTierCaptured = False
        self.speedUp = 1

    #todo this logic will need to be updated with new code
    def displayMain(self):
        generation = 0
        self.speedUp = 1
        wait = int(1000/self.fps/(1+self.speedUp))
        # aquarium demonstration variables (Note: can pres -> or <- to slow/speed up a generation)
        generationToView = [0, 10]
        numOfGenerations = 10
        while (generation < numOfGenerations):
            scores = []
            bestFish = None
            bestScore = -1
            fishIteration = -1
            for trainingFish in self.training_fishes:
                fishIteration += 1
                fishes = []
                for j in range(0, 10):
                    x = random.randint(0, 7)
                    y = random.randint(0, 7)
                    loc = (self.possibleX[x], self.possibleY[y])
                    f = Fish.randomFishGenerator(loc, "npc", self.maxAttributePoints)
                    fishes.append(f)

                x = random.randint(0, 7)
                y = random.randint(0, 7)
                loc = (self.possibleX[x], self.possibleY[y])
                f = Fish(loc, 2, 2, 0, 20, "npc")  # adds a predator npc
                fishes.append(f)
                # i.score = 100
                fishes.append(trainingFish)
                aquarium = Aquarium(20, fishes)

                while aquarium.lifetime < 100 and trainingFish.status == 1:
                    # update fish locations
                    aquarium.updateSim()

                    if(generation in generationToView):
                        # slow down tics to viewable rate
                        # if press exit button
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                            #allow speed up of current generation
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RIGHT:
                                    self.speedUp += 10
                                    wait = int(1000/self.fps/(1+self.speedUp))
                                if event.key == pygame.K_LEFT:
                                    self.speedUp =1
                                    wait = int(1000 / self.fps / (1 + self.speedUp))
                                if event.key == pygame.K_UP:
                                    self.training_fishes = self.overRideTrainingFish
                                    self.displayMain()

                            # get type (fish/food) and their locations from backend
                        # this will update each tic of display
                        for fish in aquarium.fishes:
                            # get tier so we know how to blit other fish
                            self.getTraininingTier(fish)
                            # for each fish produce n more frames (steps) to target location
                            self.getSteps(fish, self.translateLoc(fish.loc[1], fish.loc[0]), self.fps)

                        # distribute added frames evenly across each fish (this is where we display our fish)
                        self.smoothMove(aquarium.lifetime, self.fps, wait, aquarium, fishIteration, generation)

                        # if training fish has been eaten, show it
                        if (trainingFish.status == 0):
                            self.trainingFishEaten(trainingFish, fishIteration, generation)
                            pygame.display.update()
                            pygame.time.wait(int(1500/self.speedUp))

                if(generation in generationToView):
                    self.resetGameVars()

                # capture data from cycle each iteration
                trainingFish.score += aquarium.lifetime
                scores.append(trainingFish.score)
                if (trainingFish.score > bestScore):
                    bestFish = trainingFish
                    bestScore = trainingFish.score

            # from our last 10 cycles who had the best score:
            if(generation not in generationToView):
                print("Best fish had: " + bestFish.strAttributes())
                print("With score: " + str(bestScore))
                # print(scores)
                print("Average: " + str(sum(scores) / 10))
            # crossbreed
            self.training_fishes = self.evolution.createGeneration(self.training_fishes)
            generation += 1

