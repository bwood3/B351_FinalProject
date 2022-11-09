from fish import Fish

if __name__ == '__main__':
    print("Running Main")

    f = Fish((0,5))
    f.updateLoc((1, 1))
    print(f.NORTHEAST)
