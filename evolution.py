import random
from fish import Fish

class Evolution:

    def __init__(self, mutateChance, fishOrigin, fishTotalPoints):
        self.mutateChance = mutateChance
        self.fishOrigin = fishOrigin
        self.fishTotalPoints = fishTotalPoints

    def calcWeights(self, fishList):
        totalScore = 0
        for fish in fishList:
            totalScore += fish.score + 1
            weights = [(fish.score + 1) / totalScore for fish in fishList]
        return weights

    def pickParent(self, prevGen, weights):
        pick = random.random()
        cdf = 0
        for w, fish in zip(weights, prevGen):
            cdf += w
            if pick <= cdf:
                return fish

    def crossBreed(self, parent1, parent2):
        pick_vision = random.randint(1, 2)
        if pick_vision == 1:
               vision = parent1.vision
        else:
            vision = parent2.vision
        pick_speed = random.randint(1, 2)
        if pick_speed == 1:
            speed = parent1.speed
        else:
            speed = parent2.speed
        pick_risk = random.randint(1, 2)
        if pick_risk == 1:
            risk = parent1.riskAwareness
        else:
            risk = parent2.riskAwareness
        pick_tier = random.randint(1, 2)
        if pick_tier == 1:
            initTier = parent1.initTier
        else:
            initTier = parent2.initTier
        return Fish(self.fishOrigin, vision, speed, risk, initTier, fishType = "training")

    def mutate(self, fish):
        chance = random.random()
        if chance <= self.mutateChance:
            return Fish.randomFishGenerator(self.fishOrigin, fish.fishType, self.fishTotalPoints)
        else:
            return fish

    def createGeneration(self, prevGen):
        weights = self.calcWeights(prevGen)
        # print("Weights: " + str(weights))
        parents = [(self.pickParent(prevGen, weights), self.pickParent(prevGen, weights)) for fish in prevGen]
        generation = list()
        for p1, p2 in parents:
            generation.append(self.mutate(self.crossBreed(p1, p2)))
        return generation
