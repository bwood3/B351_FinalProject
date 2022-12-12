import random
from fish import Fish

class Evolution:

    # Creates an Evolution object.
    # mutateChance - a decimal value between 0 and 1 that is the chance of random mutation
    # fishOrigin - a tuple location required for this object to create new fish objects.
    # fishTotalPoints - the total number of points fish may use to generate attributes.
    def __init__(self, mutateChance, fishOrigin, fishTotalPoints):
        self.mutateChance = mutateChance
        self.fishOrigin = fishOrigin
        self.fishTotalPoints = fishTotalPoints

    # Calculates the percent chance a fish will be picked as a parent for the -
    # - next generation. This is always a non-zero value.
    # A fish's weight is its score divided by the total score of all fish.
    # The calculation adds one to each fish's score to ensure it is not zero -
    # - and the total score between all fish is not zero.
    def calcWeights(self, fishList):
        totalScore = 0
        for fish in fishList:
            totalScore += fish.score + 1
            weights = [(fish.score + 1) / totalScore for fish in fishList]
        return weights

    # Generates a number between 0 and 1 to pick a parent at random.
    # Since the sum of all fishs' weights is 1, the distribution of fish weights -
    # - is effectively a cumulative distribution function and can be calculated -
    # - as such to determine which fish is picked as the parent.
    # The received list of fish (prevGen) and weights for fish (weights) are in -
    # - respective order to each other.
    def pickParent(self, prevGen, weights):
        pick = random.random()
        cdf = 0
        for w, fish in zip(weights, prevGen):
            cdf += w
            if pick <= cdf:
                return fish

    # Creates a new fish with two parent fish as input.
    # For each attribute of the new fish, an attribute score is randomly chosen -
    # - from one of the two parent fish. The chance is 50% for either parent.
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

    # An experimental way to mutate fish. This mutate method will randomly increase, -
    # - decrease, or do nothing to a randomly chosen attribute of the fish.
    # This mutation method is not used in the final implementation
    def mutateAttrIncr(self, fish):
        chance = random.random()
        if chance <= self.mutateChance:
            attributes = [fish.vision, fish.speed, fish.riskAwareness, fish.initTier]
            attr = random.randint(0, 3)
            change = random.randint(-1, 1)
            attributes[attr] += change
            return Fish(self.fishOrigin, attributes[0], attributes[1], attributes[2], attributes[3], fish.fishType)
        else:
            return fish

    # This is the mutation method most similar to typical implementations of genetic -
    # - algorithms. It randomly picks an attribute from the fish, then randomizes it -
    # - within the maximum allowed attribute range. This unfortunately breaks the -
    # - constraint of limited attribute points we impose on the fish. For this -
    # - reason it is not used in the final implementation.
    def mutateAttribute(self, fish):
        chance = random.random()
        if chance <= self.mutateChance:
            attributes = [fish.vision, fish.speed, fish.riskAwareness, fish.initTier]
            attributes[random.randint(0, 3)] = random.randint(0, self.fishTotalPoints)
            return Fish(self.fishOrigin, attributes[0], attributes[1], attributes[2], attributes[3], fish.fishType)
        else:
            return fish

    # This mutation method takes a fish, then returns a new randomly generated -
    # - fish instead. Altough this mutation method is substantially more random -
    # - then the other methods, it maintains the limited attribute constraint -
    # - that is imposed on the fish. Mutation chance was lowered to compensate -
    # - for its increased randomness.
    # This mutation method is used.
    def mutate(self, fish):
        chance = random.random()
        if chance <= self.mutateChance:
            return Fish.randomFishGenerator(self.fishOrigin, fish.fishType, self.fishTotalPoints)
        else:
            return fish

    # This is the method called from the main method whenever a new generation is needed.
    # It takes the previous generation of fish, calculates their weights, then -
    # - creates a list of tuples, each tuple being the two parents for one of - 
    # - the new fish. A loop is run where each tuple is used to create one fish-
    # - in the next generation. This fish is passed through the mutate method -
    # - where it has a chance of mutating before being added to the next generation list.
    def createGeneration(self, prevGen):
        weights = self.calcWeights(prevGen)
        parents = [(self.pickParent(prevGen, weights), self.pickParent(prevGen, weights)) for fish in prevGen]
        generation = list()
        for p1, p2 in parents:
            generation.append(self.mutate(self.crossBreed(p1, p2)))
        return generation
