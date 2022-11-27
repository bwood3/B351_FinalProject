import pygame

class GameObject():
    #all game objects will have a height width and image
    def __init__(self, height, width, png_image):
        self.height = height
        self.width = width
        self.png = png_image

class PyFish(GameObject):
    def __init__(self, height, width, png_sheet, sheetLoc):
        super().__init__(height, width, png_sheet)

        # for FishSheet 2, each object is 31/31
        sqaureSize = 31

        sheet = pygame.image.load(self.png).convert_alpha()
        sheet.set_clip(pygame.Rect(SpriteSheet.sheetTranslator(sqaureSize, sheetLoc)))
        self.sprite = sheet.subsurface(sheet.get_clip())
        self.sprite = pygame.transform.scale(self.sprite, (width, height))

#return array containing sprites for a game object
class SpriteSheet():
    @staticmethod
    #return tuple with sprite location arguments
    #location is location on sprite sheet (tuple)
    #size is how large each object on sprite sheet is (we are expect square sprites here)
    def sheetTranslator(size, loc):
        #we will think of col as row in pygame
        return (loc[1] * size, loc[0] * size, size, size)

class PyFood(GameObject):
    def __init__(self,height, width, png_image, sheetLoc):
        super().__init__(height, width, png_image)

        # for FishSheet 1, each object is 25/25
        sqaureSize = 25

        sheet = pygame.image.load(self.png).convert_alpha()
        sheet.set_clip(pygame.Rect(SpriteSheet.sheetTranslator(sqaureSize, sheetLoc)))

        self.sprite = sheet.subsurface(sheet.get_clip())
        self.sprite = pygame.transform.scale(self.sprite, (width, height))