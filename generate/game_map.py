from random import *
from generate.map_feature import *
from generate.abstract_room import *


class GameMap:
    
    def __init__(self, y, x):
        self.size = [y, x]
        self.grid = []
        self.walls = set()
        self.rooms = {}

        # Fill the entire map with rock.

        for row in range(self.size[0]):
            self.grid.append([])
            for sign in range(self.size[1]):
                self.grid[row].append(".")

        # Generate the map.

        self.generate()

    def generate(self):
        # This function generates the grid.

        # Initialize the room count, used as keys to certain rooms in the
        # abstract map.
        room_key = 0

        # Generate the first room in a random spot.
        while True:
            roomstart = (randrange(1, self.size[0] - 2), 
                         randrange(1, self.size[1] - 2))
            room = MapFeature(randrange(5, 21), randrange(5, 21))
            if self.fit_feature(room, roomstart, "start", room_key):
                # Once a room has been succesfully generated, break loop.
                room_key += 1
                break

        # Make a counter. It's supposed to count failed iterations.
        iterations = 0

        # Make new rooms until we have reached 200 failed iterations.
        # The second part of the if statement should not be able to happen.
        # It is, however, there to prevent errors in case it does.
        while (iterations < 200 and len(self.walls) > 0):
            
            # Pick a random wall tile and check it's orientation.
            testcoord = sample(self.walls, 1)[0]
            orientation = self.checkwall(testcoord)

            if orientation is not None:
                # Compute how big the feature is allowed to be.
                maxsize = self.compute_feature_size(orientation, testcoord)

                if maxsize[0] >= 4 and maxsize[1] >= 4:
                    # If the feature is big enough, generate it and try to fit it.
                    room = MapFeature(randint(4, maxsize[0]), 
                                      randint(4, maxsize[1]), 
                                      orientation)

                    if self.fit_feature(room, testcoord, orientation, room_key):
                        # If the feature fits, this is a succesful iteration.
                        # As such, we reset the counter.
                        room_key += 1
                        iterations = 0

                else:
                    # If no feature can fit here, never try this wall again.
                    self.walls.discard(testcoord)
            else:
                # If no orientation is possible, this wall can't be used.
                # Hence, we won't try it again.
                self.walls.discard(testcoord)

            iterations += 1

        # The code below computes abstract paths between the rooms of the map.
        for key, room in self.rooms.items():
            # Store the keys to all other rooms.
            keys = [k for k in self.rooms]
            for k in keys:
                path = self.compute_abstract_path(key, k)
                if path is None:
                    print("No paths are possible between these rooms!")
                    break
                room.add_path(k, AbstractPath(path, len(path) - 1))
                
                

    def compute_abstract_path(self, src, dst, visited = []):
        visited.append(src)
        
        if src == dst:
            return visited
        else:
            possible = [c for c in self.rooms[src].get_connects() if
                        c not in visited]
            if len(possible) > 0:
                for p in possible:
                    paths = []
                    path = self.compute_abstract_path(p, dst, visited)

                    if path is not None:
                        paths.append(path)

                    if len(paths) > 0:
                        return min(paths)
                    else:
                        return None
            else:
                return None

                
                    
                

    def compute_feature_size(self, orientation, coord):
        # This function determines the maximum size of a feature to be 
        # generated.

        x = 0
        y = 0
        
        #How this is done depends on the orientation.
        if orientation in "EW":
            # In this case, the feature's horizontal start point is well
            # defined.

            ynorth = 0
            ysouth = 0
            y = 1

            # We check how much horizontal room we have.
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

            # Then, we check how much vertical room we have.
            # We do this by examining both directions relative to where we are.
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
            # In this case, the feature's vertical start point is well
            # defined.

            xwest = 0
            xeast = 0
            x = 1

            # We check how much vertical room we have.
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

            # Then, we check how much horizontal room we have.
            # We do this by examining both directions relative to where we are.
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
        
        # No matter how much room we get, we do not generate any features that
        # that are larger than a quarter of the map in any direction.
        return (min(y, self.size[0] // 4), min(x, self.size[1] // 4))
        

    def checkwall(self, coord):
        # This function is used to check the orientation of a wall.
        # It also places some doors. Unknown if it will keep doing that.

        # We check all possible scenarios, to see if any are valid.
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
            # If only a single orientation is valid, we return it.
            return valid[0]
        else:
            # If multiple orientations are "valid", it means we are dealing
            # with a corner or a 1 tile wide wall.
            # No features can be placed from these. Hence, we return None.
            if ((("S" in valid and "N" in valid) or
                 ("W" in valid and "E" in valid)) and
                len(valid) == 2):
                # If we are dealing with a 1 tile wide wall, maybe place a door.
                if randint(1, 100) < 10:
                    self.grid[coord[0]][coord[1]] = "D"
            return None

    def fit_feature(self, feature, featurestart, orientation, key):
        # This function attempts to fit a feature in some kind of location.

        x = None
        y = None
        direction = None
        featuregrid = feature.get_grid()
        size = feature.get_size()
        highfound = False
        lowfound = False

        if size[0] < 4 or size[1] < 4:
            # If a generated room is too small for some reason, discard it.
            return False

        # The procedure of fitting a room is dependent on orientation.
        if orientation in "EW":

            # In this case, x coordinates can be easily determined.
            if orientation == "W":
                x = featurestart[1] - (size[1] - 1)
                direction = -1
            else:
                x = featurestart[1]
                direction = 1
                
            # Y coordinates have to be determined through testing.
            # We test a number of offsets to find a viable range.
            # We do this to minimize conflicts.
            high_y = None
            low_y = None
            for offset in range(1, size[0] - 1):
                upper = featurestart[0] - offset
                lower = featurestart[0] - offset + size[0] - 1
                
                if upper < 0:
                    # If we go out of bounds, we break.
                    break
                
                # Likewise, there is no need to check coordinates that are out
                # of bounds in the other direction.
                if lower < self.size[0]:
                    
                    # Here, we minimize conflicts by attempting to define the
                    # range of coordinates so that obvious ones do not occur.
                    if (self.grid[lower][featurestart[1]] in "#." and
                        self.grid[lower][featurestart[1] + 
                                         direction*(size[1] - 1)] in "#." and
                        self.grid[upper][featurestart[1]] in "#." and
                        self.grid[upper][featurestart[1] + 
                                         direction*(size[1] - 1)] in "#."):

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
                # If high and low points have not both been found, there is no
                # range ehwre the feature can be placed without obvious
                # conflicts.
                return False
            else:
                # If there is a range, we fit the feature inside it.
                y = randint(low_y, high_y)

        elif orientation in ("NS"):
            # This case works the same way as above, only with x and y
            # coordinates flipped.

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

                if left < 0:
                    break
                if right < self.size[1]:
                    
                    if (self.grid[featurestart[0]][left] in "#." and
                        self.grid[featurestart[0] + 
                                  direction*(size[0] - 1)][left] in "#." and
                        self.grid[featurestart[0]][right] in "#." and
                        self.grid[featurestart[0] + 
                                  direction*(size[0] - 1)][right] in "#."):

                        if not highfound:
                            high_x = left
                            highfound = True

                        if offset == size[1] - 2:
                            low_x = left
                            lowfound = True

                    elif highfound:
                        low_x = left + 1
                        lowfound = True

            if not (lowfound and highfound):
                return False
            else:
                x = randint(low_x, high_x)

        else:
            # If we are generating the first room, we need not care about
            # fitting it.
            y = featurestart[0]
            x = featurestart[1]

        # At this point, we have determined where we want to try placing the 
        # feature.

        # Hopefully, the feature should not be able to go out of bounds.
        # We check for it anyway however.
        if (x < 0 or 
            y < 0 or 
            x + size[1] > self.size[1] - 1 or 
            y + size[0]> self.size[0] - 1):
            
            return False

        # Then, we check to see if it collides with features already on the map.

        test_y = y
        
        for row in featuregrid:
            test_x = x
            for sign in row:
                if sign != ".":
                    if (self.grid[test_y][test_x] != "." and 
                        (self.grid[test_y][test_x] != "#" and 
                         sign != "#")):

                        return False
                test_x += 1
            test_y += 1

        # If we get here, the feature fits.

        # We generate an abstract room.
        self.rooms[key] = AbstractRoom()
            
        for row in featuregrid:
            xcurr = x
            for sign in row:
                if sign != ".":
                    
                    # Every sign on the feature grid that is not rock is placed.
                    self.grid[y][xcurr] = sign
                    
                    if sign == "#":
                        # All new walls are added to the set.
                        self.walls.add((y, xcurr))
                    else:
                        self.rooms[key].add_coord(y, xcurr)
                        

                xcurr += 1
            y += 1

        # Next, we generate doors.
        # This algorithm still causes some anomalies.
        if orientation != "start":

            self.grid[featurestart[0]][featurestart[1]] = "D"

            # When we have placed a door, we make a corridor that connects it
            # to the feature. This is to avoid doors leading to rock tiles.
            # finally, we connect the rooms on the abstract map.
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

                for poskey, room in self.rooms.items():
                    if room.contains(featurestart[0] - direction,
                                     featurestart[1]):
                        room.connect(key)
                        self.rooms[key].connect(poskey)
                        break
            else:
                check = featurestart[1] + direction
                while self.grid[featurestart[0]][check] != " ":
                    for i in [1, -1]:
                        if self.grid[featurestart[0] + i][check] != " ":
                            self.grid[featurestart[0] + i][check] = "#"
                    self.grid[featurestart[0]][check] = " "
                    check += direction

                for poskey, room in self.rooms.items():
                    if room.contains(featurestart[0],
                                     featurestart[1] - direction):
                        room.connect(key)
                        self.rooms[key].connect(poskey)
                        break
            
        # If we get here without errors, we return true.
        return True

    def display_abstract_map(self):
        # This function outputs the abstract map into a terminal.
        for key, room in self.rooms.items():
            print("ROOM KEY: " + str(key))
            print("    CONNECTED TO:")
            for item in room.get_connects():
                print("        " + str(item))

    def output(self, filename):
        # This function outputs the grid to a text file.

        output = open(filename, "w")

        for y in self.grid:
            for x in y:
                output.write(x)
            output.write("\n")

        output.close()

    def display(self):
        # This function outputs the grid to a terminal window.

        for y in self.grid:
            row = ""
            for x in y:
                row += x
            print(row)
