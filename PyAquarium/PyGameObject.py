import math
import pygame

class GameObject():
    #all game objects will have a height width and image
    def __init__(self, height, width, png_image):
        self.height = height
        self.width = width
        self.png = png_image

class PyFish(GameObject):
    def __init__(self, height, width, png_sheet):
        super().__init__(height, width, png_sheet)

        # for FishSheet 1, each object is 31/31
        size = 31
        sheetFishLoc = (1,3)

        sheet = pygame.image.load(self.png).convert_alpha()
        sheet.set_clip(pygame.Rect(SpriteSheet.sheetTranslator(size, sheetFishLoc)))
        self.fish = sheet.subsurface(sheet.get_clip())
        self.fish = pygame.transform.scale(self.fish, (width, height))

#return array containing sprites for a game object
class SpriteSheet():
    @staticmethod
    #return tuple with sprite location arguments
    #location is location on sprite sheet (tuple)
    #size is how large each object on sprite sheet is (we are expect square sprites here)
    def sheetTranslator(size, loc, correction = None):
        if correction == None:
            correction = 0

        #we will think of col as row in pygame
        return (loc[1] * size - correction, loc[0] * size + math.sqrt(correction), size, size)

class PyFood(GameObject):
    def __init__(self,height, width, png_image):
        super().__init__(height, width, png_image)

        # for FishSheet 1, each object is 25/25
        #worm loc = (8,3), correction = 10 (notice bottom row in fish sheet one is off center)
        size = 25
        sheetFoodLoc = (8, 3)
        sheet = pygame.image.load(self.png).convert_alpha()
        sheet.set_clip(pygame.Rect(SpriteSheet.sheetTranslator(size, sheetFoodLoc, 10)))

        self.food = sheet.subsurface(sheet.get_clip())
        # self.delete = sheet.subsurface(sheet.get_clip())
        # self.delete.set_masks()
        self.food = pygame.transform.scale(self.food, (width, height))