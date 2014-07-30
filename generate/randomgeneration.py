from random import *

class GameMap:
    
    def __init__(self, x, y):
        self.size = [y, x]
        self.grid = []
        self.wallcount = self.size[0]*self.size[1]
        self.walls = set()

        for row in range(self.size[0]):
            self.grid.append([])
            for sign in range(self.size[1]):
                self.grid[row].append(".")

        self.generate()

    def generate(self):
        while True:
            roomstart = (randrange(1, self.size[0] - 2), 
                         randrange(1, self.size[1] - 2))
            room = MapFeature(randrange(5, 21), randrange(5, 21))
            if self.fit_feature(room, roomstart):
                break
        
        x = 0
        while x < 10:
            self.display()
            testcoord = sample(self.walls, 1)[0]
            orientation = self.checkwall(testcoord)

            if orientation != None:
                room = MapFeature(randrange(5, 21), randrange(5, 21), orientation)
                if self.fit_feature(room, testcoord):
                    self.grid[testcoord[0]][testcoord[1]] = "D"
                    x += 1
            else:
                #In this case, features cannot be placed from this wall.
                #Hence, it is removed from the wall set.
                self.walls.discard(testcoord)

    def checkwall(self, coord):
        valid = []
        if self.grid[coord[0] - 1][coord[1]] == " ":
            valid.append("north")
        if self.grid[coord[0] + 1][coord[1]] == " ":
            valid.append("south")
        if self.grid[coord[0]][coord[1] - 1] == " ":
            valid.append("west")
        if self.grid[coord[0]][coord[1] + 1] == " ":
            valid.append("east")

        if len(valid) == 1:
            return valid[0]
        else:
            return None

    def fit_feature(self, feature, featurestart):
        offset = feature.get_startpoint()
        featuregrid = feature.get_grid()
        size = feature.get_size()
        y = featurestart[0] - offset[0]
        x = featurestart[1] - offset[1]
        
        #Below, we check if the feature fits on the map

        if (x < 1 or 
            y < 1 or 
            x + size[1] > self.size[1] - 2 or 
            y + size[0]> self.size[0] - 2):

            return False

        test_y = y

        #Below, we check if the feature collides with anything else
        
        for row in featuregrid:
            test_x = x
            for sign in row:
                if sign != ".":
                    for y in [-1, 0, 1]:
                        for x in [-1, 0, 1]:
                            #A door (D or S) may be placed on walls (#)
                            #Anything else may only be placed on empty tiles (.) 
                            if (self.grid[test_y + y][test_x + x] != "." and 
                                (self.grid[test_y + y][test_x + x] != "#" and 
                                 sign not in "DS")):
                                return False
                test_x += 1
            test_y += 1

        #If we get here, the feature fits.

        for row in featuregrid:
            x = featurestart[1] - offset[1]
            for sign in row:
                if sign != ".":
                    self.grid[y][x] = sign
                    
                    if sign == "#":
                        #All added walls are added to the set
                        self.walls.add((y, x))
                    else:
                        self.wallcount -= 1
                        if self.grid[y][x] == "#":
                            #If a door is placed on a wall, remove it from the set
                            self.walls.discard((y, x))
                x += 1
            y += 1

        return True

    def output(self, filename):
        output = open(filename, "w")

        for y in self.grid:
            for x in y:
                output.write(x)
            output.write("\n")

        output.close()

    def display(self):
        for y in self.grid:
            row = ""
            for x in y:
                row += x
            print(row)


class MapFeature:
    
    def __init__(self, x, y, begin = "start", identity = "random"):
        self.size = (y, x)

        self.startpoint = [0, 0]
        self.grid = []

        for col in range(self.size[0]):
            self.grid.append([])
            for row in range(self.size[1]):
                self.grid[col].append(".")
        
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

        if begin == "west":
            beginning[1] = 0
        elif begin == "north":
            beginning[0] = 0
        elif begin == "east":
            beginning[1] = self.size[1] - 1
        elif begin == "south":
            beginning[0] = self.size[0] - 1


        for i, v in enumerate(beginning):
            if v != -1:
                self.startpoint[i] = v
            else:
                self.startpoint[i] = randrange(1, self.size[i] - 1)


        if begin != "start":
            self.add_door(self.startpoint[0], self.startpoint[1])

        
        if identity == "room":
            rectstart = self.startpoint
            if begin == "west":
                rectstart[1] = 1
            elif begin == "north":
                rectstart[0] = 1
            elif begin == "east":
                rectstart[1] = self.size[1] - 2
            elif begin == "south":
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
                    (westspan + eastspan >= 2 and
                     northspan + southspan >= 2)):
                    self.floorrect(rectstart, westspan, northspan, eastspan, southspan)
                    firstrun = False
                
                rectstart = [randrange(1, self.size[0] - 1), randrange(1, self.size[1] - 1)]
                
        elif identity == "corridor":
            x = 0

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
        southwall = start[0] + south
        westwall = start[1] - west - 1
        eastwall = start[1] + east
        
        print("\n1\n")
        self.display()

        #Place corner walls.
        self.add_wall(northwall, westwall)
        print("\n2\n")
        self.display()
        self.add_wall(northwall, eastwall)
        print("\n3\n")
        self.display()
        self.add_wall(southwall, westwall)
        print("\n4\n")
        self.display()
        self.add_wall(southwall, eastwall)
        print("\n5\n")
        self.display()
        firstrun = True
        for y in range(start[0] - north, start[0] + south):
            self.add_wall(y, westwall)
            self.add_wall(y, eastwall)
            for x in range(start[1] - west, start[1] + east):
                
                if firstrun:
                    self.add_wall(northwall, x)
                    self.add_wall(southwall, x)

                if self.grid[y][x] in ".#":
                    self.add_floor(y, x)

                print("\ncol" + str(x) + "\n")
                self.display()
            
            firstrun = False
            print("\nrow" + str(y) + "\n")
            self.display()
    
    def add_wall(self, y, x, force = False):
        if self.grid[y][x] == "." or force:
            self.grid[y][x] = "#"

    def add_floor(self, y, x):
        self.grid[y][x] = " "
    
    def add_door(self, y, x):
        self.grid[y][x] = "D"
