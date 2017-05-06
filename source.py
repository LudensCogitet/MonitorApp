import random
import time

class RandSource:
    def __init__(self, name, interval = 1):
        self.name = name
        self.value = random.randint(50,100)
        self.deltaTime = time.time()
        self.interval = interval
        self.changeRange = 2

        self.changeVal()

    def checkVal(self):
        #print(time.time(), self.deltaTime)
        if time.time() - self.deltaTime > self.interval:
            self.changeVal()
            self.deltaTime = time.time()

        return (self.deltaTime,self.name,self.value)

    def changeVal(self):
        self.value = self.value + random.randint(-self.changeRange,self.changeRange)
        return self.value

    def printVal(self):
        print(self.value)

if __name__ == '__main__':
    source = RandSource()
    done = False
    while(done == False):
        source.checkVal()
