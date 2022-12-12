import pygame

class GameObject():
    #all game objects will have a height width and image
    def __init__(self, height, width, png_image):
        self.height = height
        self.width = width
        self.png = png_image

#training fish uses this class
class PyFish(GameObject):

    def __init__(self, height, width, png_sheet, fps):
        super().__init__(height, width, png_sheet)

        self.width = width
        self.height = height

        # for FishSheet 2, each object is 31/31
        self.sqaureSize = 31

        # animation frame count
        #if 60 fps we do not want fish completing animation 60 times per second (spread out)
        self.fps = fps
        cycleSpeed = 3
        self.cycle = cycleSpeed/fps
        self.setCLips()
        # default direction
        self.direction = "west"

    #eating clip is frame 3
    def getFrame(self):
        if(self.direction == "west"):
            clip = self.westMoves[int(self.cycle%2)]
        else:
            clip = self.eastMoves[int(self.cycle%2)]
        self.cycle += 1/self.fps
        return clip

    def setCLips(self):
        self.setEastClips()
        self.setWestClips()

    def setEastClips(self):
        # locations on sprite sheet
        eastLoc = [(2, 3.1), (2, 4.1), (2, 5.1)]

        #1
        east = pygame.image.load(self.png).convert_alpha()
        east.set_clip(pygame.Rect(SpriteSheet.sheetTranslator(self.sqaureSize, eastLoc[0])))
        east0 = east.subsurface(east.get_clip())
        east0 = pygame.transform.scale(east0, (int(self.width), int(self.height)))
        #2
        east.set_clip(pygame.Rect(SpriteSheet.sheetTranslator(self.sqaureSize, eastLoc[1])))
        east1 = east.subsurface(east.get_clip())
        east1 = pygame.transform.scale(east1, (int(self.width), int(self.height)))
        #3
        east.set_clip(pygame.Rect(SpriteSheet.sheetTranslator(self.sqaureSize, eastLoc[2])))
        east2 = east.subsurface(east.get_clip())
        east2 = pygame.transform.scale(east1, (int(self.width), int(self.height)))

        self.eastMoves = [east0, east1, east2]

    def setWestClips(self):
        # locations on sprite sheet
        westLoc = [(1, 3), (1, 4.1), (1, 5.1)]

        # 1
        west = pygame.image.load(self.png).convert_alpha()
        west.set_clip(pygame.Rect(SpriteSheet.sheetTranslator(self.sqaureSize, westLoc[0])))
        west0 = west.subsurface(west.get_clip())
        west0 = pygame.transform.scale(west0, (int(self.width), int(self.height)))
        # 2
        west.set_clip(pygame.Rect(SpriteSheet.sheetTranslator(self.sqaureSize, westLoc[1])))
        west1 = west.subsurface(west.get_clip())
        west1 = pygame.transform.scale(west1, (int(self.width), int(self.height)))
        # 3
        west.set_clip(pygame.Rect(SpriteSheet.sheetTranslator(self.sqaureSize, westLoc[2])))
        west2 = west.subsurface(west.get_clip())
        west2 = pygame.transform.scale(west2, (int(self.width), int(self.height)))

        self.westMoves = [west0, west1, west2]


#return array containing sprites for a game object
#will be approximate array location on sprite sheet (this will not be the case if grid location are not all equal)
class SpriteSheet():
    @staticmethod
    #return tuple with sprite location arguments
    #location is location on sprite sheet (tuple)
    #size is how large each object on sprite sheet is (we are expect square sprites here)
    def sheetTranslator(size, loc):
        #we will think of col as row in pygame
        return (loc[1] * size, loc[0] * size, size, size)

# all other fish/food use this class
class PyFood(GameObject):
    def __init__(self,height, width, png_image, sheetLoc):
        super().__init__(height, width, png_image)

        # for FishSheet 1, each object is 25/25
        sqaureSize = 25

        sheet = pygame.image.load(self.png).convert_alpha()
        sheet.set_clip(pygame.Rect(SpriteSheet.sheetTranslator(sqaureSize, sheetLoc)))

        self.sprite = sheet.subsurface(sheet.get_clip())
        self.sprite = pygame.transform.scale(self.sprite, (int(width), int(height)))