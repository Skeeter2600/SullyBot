from abc import ABC, abstractmethod
import random

# playersPerGame = 4
# smashers = None
# sample = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
# # sample = ['a', 'b', 'c', 'd']


# Class for Each Fighter in the Queue
class Fighter():
    PLAYEDWEIGHT = 1.0
    FOUGHTWEIGHT = 0.6
    TEAMEDWEIGHT = 0.5

    def __init__(self, player, players):
        self.__user = player
        self.fought = dict()
        self.teamed = dict()
        self.lastPlayed = 0
        self.__fs = 0.0
        self.__ts = 0.0
        
        for i in players:
            if i != self.__user:
                self.fought[i] = 0
                self.teamed[i] = 0

    def foughtScore(self, player):
        self.__fs = (self.lastPlayed * self.PLAYEDWEIGHT) + (self.fought[player.getUser()] * self.FOUGHTWEIGHT)
        return self.__fs

    def getFoughtScore(self):
        return self.__fs

    def teamScore(self, player):
        self.__ts = (self.lastPlayed * self.PLAYEDWEIGHT) + (self.teamed[player.getUser()] * self.TEAMEDWEIGHT)
        return self.__ts

    def getTeamScore(self):
        return self.__ts

    def getUser(self):
        return self.__user

        
# Class to hold all of the fighters in the queue
# Abstract Class
class Fighters(ABC):
    # loadout = []        # Stores all of the players currently in the arena
    # lastGames = []      # Stores who played in the last few games
    # currentGame = 0     # Stores the current game # as an int
    # currentQueue = []   # Container for list of fighters playing in current game
    # MAXNOPLAY = 2       # Maximum number of games a player can sit out

    def __init__(self, players):
        self.currentGame = 0
        self.loadout = []
        self.currentQueue = []

        for i in players:
            self.loadout.append(Fighter(i, players))

        random.shuffle(self.loadout)

        # self.currentQueue.clear()

    # def refreshLastGames(self, lastGame):
    #     self.lastGames.append(lastGame)
    #     if len(self.lastGames) > 4:
    #         self.lastGames.pop(0)

    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def generate(self):
        pass


            
# Fighters Class with logic for Singles
class Singles(Fighters):
    fightersPerGame = 0

    def __init__(self, players, playersPerGame):
        super().__init__(players)
        self.fightersPerGame = playersPerGame


    def generate(self):
        self.currentQueue.clear() #clears the current queue
        print("Current Round: " + str(self.currentGame))

        tempQueue = self.loadout[:] #copies loadout to tempQueue

        target = self.loadout[self.currentGame % len(self.loadout)]
        tempQueue.remove(target)
        self.currentQueue.append(target)

        tempQueue.sort(key = lambda x: x.teamScore(target))

        preQ = [tempQueue[0]]
        tempQueue.pop(0)
        for i in tempQueue:
            if i.getFoughtScore() == preQ[-1].getFoughtScore() or len(preQ) < self.fightersPerGame:
                preQ.append(i)

        random.shuffle(preQ)

        counter = 1
        while len(self.currentQueue) < self.fightersPerGame:
            self.currentQueue.append(preQ[counter])
            counter += 1

        self.update()

        return self.currentQueue


    def update(self):
        for i in self.currentQueue:
            for j in self.currentQueue:
                if i != j:
                    i.fought[j.getUser()] += 1
            i.lastPlayed = self.currentGame

        self.currentGame += 1
                


#Fighters Class with logic for Doubles
class Doubles(Fighters):
    FIGHTERSPERGAME = 4

    def __init__(self, players):
        super().__init__(players)

    def __breakTieTeam(self, target, queue):
        q = queue[:]

        q.sort(key = lambda x: x.teamScore(target))

        pQ = []
        for i in q:
            if len(pQ) == 0:
                pQ.append(i)
            elif i.getTeamScore() == pQ[-1].getTeamScore():
                pQ.append(i)

        return random.choice(pQ)

    def __breakTieFought(self, target, queue):
        q = queue[:]

        q.sort(key = lambda x: x.foughtScore(target))

        pQ = []
        for i in q:
            if len(pQ) == 0:
                pQ.append(i)
            elif i.getFoughtScore() == pQ[-1].getFoughtScore():
                pQ.append(i)

        return random.choice(pQ)


    def generate(self):
        self.currentQueue.clear() #clears the current queue
        print("Current Round: " + str(self.currentGame))

        tempQueue = self.loadout[:] #copies loadout to tempQueue

        target = self.loadout[self.currentGame % len(self.loadout)]
        tempQueue.remove(target)
        self.currentQueue.append(target)

        # Sort to find most suitable teammate for target
        tempQueue.sort(key = lambda x: x.teamScore(target))

        # Logic: From target, find teammate & opponent;  from opponent, find teammate

        # Find teammate for target
        targetTeam = self.__breakTieTeam(target, tempQueue)
        self.currentQueue.append(targetTeam)
        tempQueue.remove(targetTeam)

        # Find opponent for target
        counterTarget = self.__breakTieFought(target, tempQueue)
        self.currentQueue.append(counterTarget)
        tempQueue.remove(counterTarget)

        # Find teammate for opponent
        counterTeam = self.__breakTieTeam(counterTarget, tempQueue)
        self.currentQueue.append(counterTeam)
        tempQueue.remove(counterTeam)

        self.update()

        return self.currentQueue

    def update(self):
        # 2 Teams
        t1 = [self.currentQueue[0], self.currentQueue[1]]
        t2 = [self.currentQueue[2], self.currentQueue[3]]

        c = 0 # Counter
        while c < 2:
            t1[c].teamed[t1[(c + 1) % 2].getUser()] += 1
            t1[c].lastPlayed = self.currentGame

            t2[c].teamed[t2[(c + 1) % 2].getUser()] += 1
            t2[c].lastPlayed = self.currentGame
            
            cc = 0
            while cc < 2:
                t1[c].fought[t2[cc].getUser()] += 1
                t2[c].fought[t1[cc].getUser()] += 1
                cc += 1
            
            c += 1

        self.currentGame += 1
        

# # Fake Fight Command (Sets up the queues for the first time)
# def fight(gamemode):
#     global smashers
#     global sample
#     global playersPerGame

#     if gamemode == "singles":
#         smashers = Singles(sample, playersPerGame)
#     elif gamemode == "doubles":
#         smashers = Doubles(sample)
#     else:
#         raise NameError("Incorrect Gamemode")

#     return next_fight()


# # Fake Next Fight Command (Generates the next queue)
# def next_fight():
#     global smashers
#     next_queue = smashers.generate()

#     pQ = []
#     for i in next_queue:
#         pQ.append(i.user)
#     return pQ


# def main():
#     print(fight("doubles"))
#     c = 12
#     for i in range(c):
#         print(next_fight())
    
# if __name__ == "__main__":
#     main()