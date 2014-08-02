from random import *

class MapFeature:
    
    def __init__(self, y, x, begin = "start", identity = "random"):
        self.size = [y, x]

        self.startpoint = [0, 0]
        self.grid = []

        for row in range(self.size[0]):
            self.grid.append([])
            for col in range(self.size[1]):
                self.grid[row].append(".")
        
        if identity == "random":
            #adda mer senare
            rand = randint(0, 0)
            if rand == 0:
                self.identity = "room"
            elif rand == 1:
                self.identity = "corridor"
            elif rand == 2:
                self.identity = "maze"
        else:
            self.identity = identity

        self.generate(self.identity, begin)

    def generate(self, identity, begin):
        beginning = [-1, -1]

        if begin == "E":
            beginning[1] = 0
        elif begin == "S":
            beginning[0] = 0
        elif begin == "W":
            beginning[1] = self.size[1] - 1
        elif begin == "N":
            beginning[0] = self.size[0] - 1

        for i, v in enumerate(beginning):
            if v != -1:
                self.startpoint[i] = v
            else:
                self.startpoint[i] = randrange(1, self.size[i] - 2)

        if identity == "room":
            rectstart = list(self.startpoint)
            if begin == "E":
                rectstart[1] = 1
            elif begin == "S":
                rectstart[0] = 1
            elif begin == "W":
                rectstart[1] = self.size[1] - 2
            elif begin == "N":
                rectstart[0] = self.size[0] - 2

            firstrun = True
            while self.grid[randrange(1, self.size[0] -1)][randrange(1, self.size[1] -1)] in "#.":
                westspan = randint(0, rectstart[1] - 1)
                northspan = randint(0, rectstart[0] - 1)
                eastspan = randint(0, self.size[1] - rectstart[1] - 2)
                southspan = randint(0, self.size[0] - rectstart[0] - 2)
                
                if ((firstrun or 
                     self.grid[rectstart[0]][rectstart[1]] == " " or
                     self.grid[rectstart[0] - northspan][rectstart[1]] == " " or
                     self.grid[rectstart[0] + southspan][rectstart[1]] == " " or
                     self.grid[rectstart[0]][rectstart[1] - westspan] == " " or
                     self.grid[rectstart[0]][rectstart[1] + eastspan] == " ") and
                    (westspan + eastspan >= 1 and
                     northspan + southspan >= 1)):
                    self.floorrect(rectstart, westspan, northspan, eastspan, southspan)
                    firstrun = False
                    
                if not firstrun:
                    rectstart = [randrange(1, self.size[0] - 2), 
                                 randrange(1, self.size[1] - 2)]
            
        elif identity == "corridor":
            x = 0

        #Trim down the size of the feature to make it fit better
        #We do this by removing all outer columns and rows that do not contain
        #anything

        emptyrows = []
        emptycols = []

        for index, row in enumerate(self.grid):
            feature = False
            for sign in row:
                if sign != ".":
                    feature = True
                    break
            if not feature:
                emptyrows.append(index)

        for index in range(self.size[1]):
            feature = False
            for row in self.grid:
                if row[index] != ".":
                    feature = True
                    break
            if not feature:
                emptycols.append(index)

        emptyrows.sort(reverse = True)
        emptycols.sort(reverse = True)

        for index in emptyrows:
            del self.grid[index]
            self.size[0] -= 1
            if index < self.startpoint[0]:
                self.startpoint[0] -= 1

        for row in self.grid:
            for index in emptycols:
                del row[index]

        for index in emptycols:
            self.size[1] -= 1
            if index < self.startpoint[1]:
                self.startpoint[1] -= 1
            
    
            

    def display(self):
        for y in self.grid:
            row = ""
            for x in y:
                row += x
            print(row)

    def get_grid(self):
        return self.grid

    def get_startpoint(self):
        return self.startpoint

    def get_size(self):
        return self.size

    def get_floorcount(self):
        return self.floorcount

    def floorrect(self, start, west, north, east, south):
        #Define the wall positions.
        northwall = start[0] - north - 1
        southwall = start[0] + south + 1
        westwall = start[1] - west - 1
        eastwall = start[1] + east + 1

        #Place corner walls.
        self.add_wall(northwall, westwall)
        self.add_wall(northwall, eastwall)
        self.add_wall(southwall, westwall)
        self.add_wall(southwall, eastwall)

        firstrun = True
        for y in range(start[0] - north, start[0] + south + 1):
            self.add_wall(y, westwall)
            self.add_wall(y, eastwall)
            for x in range(start[1] - west, start[1] + east + 1):
                
                if firstrun:
                    self.add_wall(northwall, x)
                    self.add_wall(southwall, x)

                if self.grid[y][x] in ".#":
                    self.add_floor(y, x)
            
            firstrun = False

    def add_wall(self, y, x):
        if self.grid[y][x] == ".":
            self.grid[y][x] = "#"

    def add_floor(self, y, x):
        self.grid[y][x] = " "
    
    def add_door(self, y, x):
        self.grid[y][x] = "D"
