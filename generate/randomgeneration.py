from random import *

class GameMap:
    
    def __init__(self, y, x):
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
            if self.fit_feature(room, roomstart, "start"):
                break
            
        print("INITIAL ROOM PLACED")
        self.display()

        iterations = 0

        while (self.wallcount > (self.size[0] * self.size[1]) / 4 and
               iterations < 200 and
               len(self.walls) > 0):
            testcoord = sample(self.walls, 1)[0]
            orientation = self.checkwall(testcoord)
            
            print("TESTING COORDINATE:")
            print(testcoord)
            
            if self.grid[testcoord[0]][testcoord[1]] != "#":
                print("COORDINATE DOES NOT CORRESPOND TO A WALL!")

            if orientation != None:
                maxsize = self.compute_feature_size(orientation, testcoord)
                print("MAXSIZE IS:")
                print(maxsize)
                if maxsize[0] >= 4 and maxsize[1] >= 4:
                    room = MapFeature(randint(4, maxsize[0]), 
                                      randint(4, maxsize[1]), 
                                      orientation)
                    print ("ROOM HAS BEEN GENERATED")
                    print("IT LOOKS LIKE THIS:")
                    if self.fit_feature(room, testcoord, orientation):
                        print()
                        print()
                        print()
                        print("THE ROOM FITS")
                        print()
                        print()
                        print()
                        iterations = 0
                else:
                    print("MAXSIZE IS TOO LOW FOR ANYTHING TO FIT HERE")
                    self.walls.discard(testcoord)
                    print("COORDINATE HAS BEEN REMOVED FROM THE WALL SET")
            else:
                #In this case, features cannot be placed from this wall.
                #Hence, it is removed from the wall set.
                print("ORIENTATION IS NONE")
                self.walls.discard(testcoord)
                print("COORDINATE HAS BEEN REMOVED FROM THE WALL SET")
                print("CURRENT WALL SET LENGTH:")
                print(len(self.walls))

            iterations += 1

        #Below here, no generation happens!
        #This is because the coordinates fuck up!

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

        for row in self.grid:
            for index in emptycols:
                del row[index]

        for index in emptycols:
            self.size[1] -= 1

    def compute_feature_size(self, orientation, coord):
        x = 0
        y = 0
        
        if orientation in "EW":
            ynorth = 0
            ysouth = 0
            y = 1

            if orientation == "E":
                for test in range(coord[1], self.size[1]):
                    if self.grid[coord[0]][test] in "#.":
                        x += 1
                    else:
                        break
            elif orientation == "W":
                for test in range(coord[1], -1, -1):
                    if self.grid[coord[0]][test] in "#.":
                        x += 1
                    else:
                        break

            for test in range(coord[0] - 1, -1, -1):
                if self.grid[test][coord[1]] in "#.":
                    ynorth += 1
                else:
                    break

            for test in range(coord[0] + 1, self.size[0]):
                  if self.grid[test][coord[1]] in "#.":
                      ysouth += 1
                  else:
                      break
            
            y += ynorth + ysouth
        
        elif orientation in "SN":
            xwest = 0
            xeast = 0
            x = 1

            if orientation == "S":
                for test in range(coord[0], self.size[0]):
                    if self.grid[test][coord[1]] in "#.":
                        y += 1
                    else:
                        break
            elif orientation == "N":
                for test in range(coord[0], -1, -1):
                    if self.grid[test][coord[1]] in "#.":
                        y += 1
                    else:
                        break

            for test in range(coord[1] - 1, -1, -1):
                if self.grid[coord[0]][test] in "#.":
                    xwest += 1
                else:
                    break

            for test in range(coord[1] + 1, self.size[1]):
                  if self.grid[coord[0]][test] in "#.":
                      xeast += 1
                  else:
                      break
            
            x += xwest + xeast
        
        return (min(y, self.size[0] // 4), min(x, self.size[1] // 4))
        

    def checkwall(self, coord):
        valid = []
        if self.grid[coord[0] - 1][coord[1]] == " ":
            valid.append("S")
        if self.grid[coord[0] + 1][coord[1]] == " ":
            valid.append("N")
        if self.grid[coord[0]][coord[1] - 1] == " ":
            valid.append("E")
        if self.grid[coord[0]][coord[1] + 1] == " ":
            valid.append("W")

        if len(valid) == 1:
            return valid[0]
        else:
            if ((("S" in valid and "N" in valid) or
                 ("W" in valid and "E" in valid)) and
                len(valid) == 2):
                if randint(1, 100) < 10:
                    self.grid[coord[0]][coord[1]] = "D"
            return None

    def fit_feature(self, feature, featurestart, orientation):
        x = None
        y = None
        direction = None
        featuregrid = feature.get_grid()
        size = feature.get_size()
        highfound = False
        lowfound = False

        print("ACTUAL FEATURE SIZE IS:")
        print(size)
        if size[0] < 4 or size[1] < 4:
            print("THIS ROOM IS TOO SMALL")
            return False

        if orientation in "EW":
            if orientation == "W":
                x = featurestart[1] - (size[1] - 1)
                direction = -1
            else:
                x = featurestart[1]
                direction = 1
                
            high_y = None
            low_y = None
            for offset in range(1, size[0] - 1):
                upper = featurestart[0] - offset
                lower = featurestart[0] - offset + size[0] - 1
                print(lower)
                print(upper)
                print(featurestart[1])
                print(featurestart[1] + direction*(size[1] - 1))
                
                if upper < 0:
                    break
                
                if lower < self.size[0]:

                    print(self.grid[lower][featurestart[1]])
                    print(self.grid[lower][featurestart[1]] in "#.")
                    print(self.grid[upper][featurestart[1]])
                    print(self.grid[upper][featurestart[1]] in "#.")
                    print(self.grid[lower][featurestart[1] + direction*(size[1] - 1)])
                    print(self.grid[lower][featurestart[1] + direction*(size[1] - 1)] in "#.")
                    print(self.grid[upper][featurestart[1] + direction*(size[1] - 1)])
                    print(self.grid[upper][featurestart[1] + direction*(size[1] - 1)] in "#.")
                    
                    if (self.grid[lower][featurestart[1]] in "#." and
                        self.grid[lower][featurestart[1] + direction*(size[1] - 1)] in "#." and
                        self.grid[upper][featurestart[1]] in "#." and
                        self.grid[upper][featurestart[1] + direction*(size[1] - 1)] in "#."):
                        if not highfound:
                            high_y = upper
                            highfound = True
                        if offset == size[0] - 2:
                            low_y = upper
                            lowfound = True
                    elif highfound:
                        low_y = upper + 1
                        lowfound = True

            if not (lowfound and highfound):
                print("THERE IS NO WAY TO PLACE THIS FEATURE HERE")
                return False
            else:
                print("A POSSIBLE RANGE HAS BEEN FOUND")
                y = randint(low_y, high_y)

        elif orientation in ("NS"):
            if orientation == "N":
                y = featurestart[0] - (size[0] - 1)
                direction = -1
            else:
                y = featurestart[0]
                direction = 1

            high_x = None
            low_x = None
            for offset in range(1, size[1] - 1):
                left = featurestart[1] - offset
                right = featurestart[1] - offset + size[1] - 1
                print(left)
                print(right)
                print(featurestart[0])
                print(featurestart[0] + direction*(size[0] - 1))
                if left < 0:
                    break
                if right < self.size[1]:

                    print(self.grid[featurestart[0]][left])
                    print(self.grid[featurestart[0]][left] in "#.")
                    print(self.grid[featurestart[0]][right])
                    print(self.grid[featurestart[0]][right] in "#.")
                    print(self.grid[featurestart[0] + direction*(size[0] - 1)][left])
                    print(self.grid[featurestart[0] + direction*(size[0] - 1)][left] in "#.")
                    print(self.grid[featurestart[0] + direction*(size[0] - 1)][right])
                    print(self.grid[featurestart[0] + direction*(size[0] - 1)][right] in "#.")

                    
                    if (self.grid[featurestart[0]][left] in "#." and
                        self.grid[featurestart[0] + direction*(size[0] - 1)][left] in "#." and
                        self.grid[featurestart[0]][right] in "#." and
                        self.grid[featurestart[0] + direction*(size[0] - 1)][right] in "#."):
                        if not highfound:
                            high_x = left
                            highfound = True
                            print("A HIGH X HAS BEEN FOUND")
                        if offset == size[1] - 2:
                            low_x = left
                            lowfound = True
                            print("A LOW X HAS BEEN FOUND")
                    elif highfound:
                        low_x = left + 1
                        lowfound = True
                        print("A LOW X HAS BEEN FOUND")

            if not (lowfound and highfound):
                print("THERE IS NO WAY TO PLACE THIS FEATURE HERE")
                return False
            else:
                print("A POSSIBLE RANGE HAS BEEN FOUND")
                x = randint(low_x, high_x)

        else:
            y = featurestart[0]
            x = featurestart[1]

        print("FEATURE STARTS AT Y:")
        print(y)
        print("FEATURE STARTS AT X:")
        print(x)
        
        print("THE FEATURE HAS THE FOLLOWING CORNERS:")
        print((y, x))
        print((y, x + size[1] - 1))
        print((y + size[0] - 1, x))
        print((y + size[0] - 1, x + size[1] - 1))
        
        print("THE MAP HAS THE FOLLOWING CORNERS:")
        print((0,0))
        print((0, self.size[1] - 1))
        print((self.size[0] - 1, 0))
        print((self.size[0] - 1, self.size[1] - 1))
            
        #Below, we check if the feature fits on the map

        if (x < 0 or 
            y < 0 or 
            x + size[1] > self.size[1] - 1 or 
            y + size[0]> self.size[0] - 1):
            
            print("THE FEATURE HAS BEEN DETERMINED TO BE OUT OF BOUNDS")
            return False

        test_y = y

        #Below, we check if the feature collides with anything else
        
        for row in featuregrid:
            test_x = x
            for sign in row:
                if sign != ".":
                    if (self.grid[test_y][test_x] != "." and 
                        (self.grid[test_y][test_x] != "#" and 
                         sign != "#")):

                        print("A CONFLICT HAS BEEN FOUND")
                        print("SIGN IS: " + sign)
                        print("SPACE OCCUPIED BY: " + self.grid[test_y][test_x])
                        print("AT COORDINATES: " + str(test_y) + "x" + str(test_x))
                        return False
                test_x += 1
            test_y += 1

        #If we get here, the feature fits.

        for row in featuregrid:
            xcurr = x
            for sign in row:
                if sign != ".":
                    self.grid[y][xcurr] = sign
                    
                    if sign == "#":
                        #All added walls are added to the set
                        self.walls.add((y, xcurr))
                    else:
                        self.wallcount -= 1
                        if self.grid[y][xcurr] == "#":
                            #If a door is placed on a wall, remove it from the set
                            self.walls.discard((y, xcurr))
                xcurr += 1
            y += 1

        #Doors are generated below

        if orientation != "start":

            self.grid[featurestart[0]][featurestart[1]] = "D"

            direction = None
            if orientation in "SE":
                direction = 1
            else:
                direction = -1

            if orientation in "NS":
                check = featurestart[0] + direction
                while self.grid[check][featurestart[1]] != " ":
                    for i in [1, -1]:
                        if self.grid[check][featurestart[1] + i] != " ":
                            self.grid[check][featurestart[1] + i] = "#"
                    self.grid[check][featurestart[1]] = " "
                    check += direction
            else:
                check = featurestart[1] + direction
                while self.grid[featurestart[0]][check] != " ":
                    for i in [1, -1]:
                        if self.grid[featurestart[0] + i][check] != " ":
                            self.grid[featurestart[0] + i][check] = "#"
                    self.grid[featurestart[0]][check] = " "
                    check += direction
            
        

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
        
        print("ORIENTATION IS: " + begin)


        for i, v in enumerate(beginning):
            if v != -1:
                self.startpoint[i] = v
            else:
                self.startpoint[i] = randrange(1, self.size[i] - 2)

        print("STARTPOINT IS:")
        print(self.startpoint)
        
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

    def add_wall(self, y, x, force = False):
        if self.grid[y][x] == "." or force:
            self.grid[y][x] = "#"

    def add_floor(self, y, x):
        self.grid[y][x] = " "
    
    def add_door(self, y, x):
        self.grid[y][x] = "D"
