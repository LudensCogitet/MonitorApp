from os import system
import time
import random
from multiprocessing import Process, Manager

clear = lambda: system('cls')

class Source(Process):
    def __init__(self,name,values):
        super(Source,self).__init__()

        self.name = name
        self.values = values

        self.values[self.name] = {'value': random.randint(0,100), 'timestamp': 0}

    def run(self):
        while True:
            time.sleep(1)
            oldVal = self.values[self.name]['value']
            if oldVal == 'kill':
                break
            self.values[self.name] = {'value': oldVal+random.randint(-1,1), 'timestamp': time.time()}

    def kill(self):
        self.values[self.name] = {'value': 'kill'}

class SourceManager:
    def __init__(self,sources):
        self.manager = Manager()
        self.values = self.manager.dict()
        self.sources = []

        for source in sources:
            self.sources.append(Source(source,self.values))

    def start(self):
        for source in self.sources:
            source.start()

    def stop(self):
        for source in self.sources:
            source.kill()
            source.join()

    def poll(self):
        returnDict = {}
        for source in self.sources:
            name = source.name
            value = self.values[source.name]['value']
            timestamp = self.values[source.name]['timestamp']

            returnDict[name] = {'name': name, 'value': value, 'timestamp': timestamp}

        return returnDict

if __name__ == '__main__'
    sourceManager = SourceManager(['source1','source2','source3'])

    sourceManager.start()

    done = False
    while not done:
        command = input()

        if command == 'kill':
            done = True
        elif command == 'poll':
            print(sourceManager.poll())

    sourceManager.stop()
