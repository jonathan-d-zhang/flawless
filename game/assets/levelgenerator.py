import itertools
import copy
import random

width = 5
height = 5

#(N,E,S,W)
characters = {
    (1, 0, 0, 0): '╵',
    (0, 1, 0, 0): '╶',
    (0, 0, 1, 0): '╷',
    (0, 0, 0, 1): '╴',

    (1, 1, 0, 0): '└',
    (0, 1, 1, 0): '┌',
    (0, 0, 1, 1): '┐',
    (1, 0, 0, 1): '┘',

    (1, 0, 1, 0): '│',
    (0, 1, 0, 1): '─',
    (1, 1, 1, 1): '┼',
    (0, 0, 0, 0): ' ',
}

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.horizontal_paths_left = True
        self.vertical_paths_left = True
        self.board = []
        for y in range(height + 2):
            row = []
            for x in range(width + 2):
                row.append((0, 0, 0, 0))
            self.board.append(row)
    
    def print_board(self):
        for row in self.board:
            print("".join(characters[cell] for cell in row))

    def get_paths(self):
        groups = Groups()
        for y, row in list(enumerate(self.board))[1:-1]:
            for x, cell in list(enumerate(row))[1:-1]:
                if cell == (0, 0, 0, 0):
                    continue
                elif cell == (1, 1, 1, 1):
                    groups.add((x, y, 'v'))
                    groups.merge((x, y, 'v'), (x, y-1, 'v')) # Connect North
                    groups.add((x, y, 'h'))
                    groups.merge((x, y, 'h'), (x-1, y, 'h')) # Connect West
                else:
                    groups.add((x, y))
                    if cell[0]: # Connect North
                        groups.merge((x, y), (x, y-1, 'v'))
                    if cell[3]: # Connect West
                        groups.merge((x, y), (x-1, y, 'h'))
        self.paths = groups.grouplist()
        return self.paths

    def place_cops(self):
        self.cops = [random.choice(x) + (random.choice((True, False)),) for x in self.paths]
        return self.cops

    def add_random_row_cop(self):
        if not self.horizontal_paths_left:
            return False
        boardbackup = copy.deepcopy(self.board)
        full_list = []
        for y, row in list(enumerate(self.board))[1:-1]:
            potential_ends = []
            for x, cell in list(enumerate(row))[1:-1]:
                if cell == (0, 0, 0, 0):
                    potential_ends.append((x,y))
                elif cell == (1, 0, 1, 0):
                    continue
                else:
                    if len(potential_ends) >= 2:
                        full_list.extend(itertools.combinations(potential_ends,2))
                    potential_ends = []
            if len(potential_ends) >= 2:
                full_list.extend(itertools.combinations(potential_ends,2))
        if len(full_list) == 0:
            self.horizontal_paths_left = False
            return False
        end1, end2 = random.choice(full_list)
        self.board[end1[1]][end1[0]] = (0, 1, 0, 0)
        self.board[end2[1]][end2[0]] = (0, 0, 0, 1)
        for x in range(end1[0]+1, end2[0]):
            if self.board[end1[1]][x] == (1, 0, 1, 0):
                self.board[end1[1]][x] = (1, 1, 1, 1)
            elif self.board[end1[1]][x] == (0, 0, 0, 0):
                self.board[end1[1]][x] = (0, 1, 0, 1)
            else:
                raise ValueError("Obstical to row add")
        winable = self.run_board()
        if winable:
            return True
        else:
            # print("Failed to win this one")
            self.board = boardbackup
            return False

    def add_random_column_cop(self):
        if not self.vertical_paths_left:
            return False
        boardbackup = copy.deepcopy(self.board)
        full_list = []
        for x in range(1, self.width+1):
            potential_ends = []
            for y in range(1, self.height+1):
                cell = self.board[y][x]
                if cell == (0, 0, 0, 0):
                    potential_ends.append((x,y))
                elif cell == (0, 1, 0, 1):
                    continue
                else:
                    if len(potential_ends) >= 2:
                        full_list.extend(itertools.combinations(potential_ends,2))
                    potential_ends = []
            if len(potential_ends) >= 2:
                full_list.extend(itertools.combinations(potential_ends,2))
        if len(full_list) == 0:
            self.vertical_paths_left = False
            return False
        end1, end2 = random.choice(full_list)
        self.board[end1[1]][end1[0]] = (0, 0, 1, 0)
        self.board[end2[1]][end2[0]] = (1, 0, 0, 0)
        for y in range(end1[1]+1, end2[1]):
            if self.board[y][end1[0]] == (0, 1, 0, 1):
                self.board[y][end1[0]] = (1, 1, 1, 1)
            elif self.board[y][end1[0]] == (0, 0, 0, 0):
                self.board[y][end1[0]] = (1, 0, 1, 0)
            else:
                raise ValueError("Obstical to column add")
        winable = self.run_board()
        if winable:
            return True
        else:
            # print("Failed to win this one")
            self.board = boardbackup
            return False

    def print_gameboard(self):
        for row in self.gameboard:
            print("".join(characters.get(cell, cell) for cell in row))

    def run_board(self):
        self.get_paths()
        self.place_cops()
        self.entrance = 5
        self.exit = 1
        self.gameboard = []
        self.gameboard.append(['W']*(self.width+12))
        for row in self.board[1:-1]:
            self.gameboard.append(['W']*6 + row[1:-1] + ['W']*6)
        self.gameboard.append(['W']*(self.width+12))
        
        self.player = (1, self.entrance)
        for removewall in range(5):
            self.gameboard[self.entrance][removewall+1] = (0, 0, 0, 0)
            self.gameboard[self.exit][-removewall-2] = (0, 0, 0, 0)
        self.exit = (self.width+12-2, self.exit)

        self.gameboard[self.player[1]][self.player[0]] = 'P'
        self.gameboard[self.exit[1]][self.exit[0]] = 'E'
        for cop in self.cops:
            self.gameboard[cop[1]][cop[0]+5] = 'C'
        self.print_gameboard()

        newpaths = []
        cop_indexes = []
        for cop, path in zip(self.cops, self.paths):
            newpath = path + path[1:-1][::-1]
            cop_x, cop_y, copface = cop
            if (cop_x, cop_y) == path[0]:
                cop_idx = 0
            elif (cop_x, cop_y) == path[-1]:
                cop_idx = len(path)-1
            elif copface:
                cop_idx = path.index((cop_x, cop_y))
            else:                
                cop_idx = len(path) + path[1:-1][::-1].index((cop_x, cop_y))
            assert newpath[cop_idx] == (cop_x, cop_y)
            newpaths.append(newpath)
            cop_indexes.append(cop_idx)

        states = [(self.player, tuple(cop_indexes))]
        seen = set()
        winable = False
        while states:
            player, cop_indexes = states.pop()
            if (player, cop_indexes) in seen:
                continue
            seen.add((player, cop_indexes))
            if player == self.exit:
                winable = True
                continue
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                newplayer = (player[0] + dx, player[1] + dy)
                if self.gameboard[newplayer[1]][newplayer[0]] == 'W':
                    continue
                new_cop_indexes = []
                spotted = False
                for idx, p in zip(cop_indexes, newpaths):
                    newcop = Cop(idx, p)
                    for death_spot in newcop.get_death_spots():
                        if newplayer == death_spot:
                            spotted = True
                            break
                    new_cop_indexes.append(newcop.idx)
                    if spotted:
                        break
                if spotted:
                    continue
                states.append((newplayer, tuple(new_cop_indexes)))
        # print(seen)
        return winable
                

class Cop:
    def __init__(self, idx, path):
        self.idx = idx
        self.path = path
        self.updateface()

    def position(self):
        return self.path[self.idx]

    def move(self):
        self.idx = (self.idx + 1) % len(self.path)

    def updateface(self):
        curposition = self.position()
        nextposition = self.path[(self.idx + 1) % len(self.path)]
        self.face = (nextposition[0] - curposition[0], nextposition[1] - curposition[1])
    
    def vision(self):
        curposition = self.position()
        for x in range(1, 3+1):
            yield (curposition[0] + self.face[0]*x, curposition[1] + self.face[1]*x)

    def get_death_spots(self):
        yield from self.vision()
        self.move()
        yield from self.vision()
        self.updateface()
        yield from self.vision()
        self.move()
        yield from self.vision()
        self.updateface()
        yield from self.vision()

def generate_all_unique_boards(height, width):
    queue = [empty_board(height, width)]
    for y in range(1, height + 1):
        for x in range(1, width + 1):
            new_queue = []
            for board in queue:
                boardnew = copy.deepcopy(board)
                for cell in characters:
                    if boardnew[y-1][x][2] != cell[0]:
                        continue
                    if boardnew[y][x-1][1] != cell[3]:
                        continue
                    if boardnew[y+1][x] is not None and boardnew[y+1][x][0] != cell[2]:
                        continue
                    if boardnew[y][x+1] is not None and boardnew[y][x+1][3] != cell[1]:
                        continue
                    boardnew[y][x] = cell
                    new_queue.append(boardnew)
            queue = new_queue
    return queue

class Groups:
    def __init__(self):
        self.groups = {}
        self.grouplookup = {}

    def add(self, point):
        if point in self.groups:
            raise ValueError("Point's group already created?")
        groupname = point
        self.groups[groupname] = [point]
        self.grouplookup[point] = groupname

    def get_point_group(self, point):
        if point in self.grouplookup:
            return self.grouplookup[point]
        elif len(point) == 3 and point[:2] in self.grouplookup:
            return self.grouplookup[point[:2]]
        else:
            raise ValueError("Point not found")

    def merge(self, point1, point2):
        g1 = self.get_point_group(point1)
        g2 = self.get_point_group(point2)
        if g1 == g2:
            return
        for element in self.groups[g2]:
            self.grouplookup[element] = g1
        self.groups[g1].extend(self.groups[g2])
        del self.groups[g2]

    def grouplist(self):
        returnlist = []
        for group in self.groups.values():
            returnlist.append(tuple(position[:2] for position in group))
        return returnlist


b = Board(width, height)
for x in range(10):
    random.choice((b.add_random_row_cop, b.add_random_column_cop))()
    b.print_board()

# for x in range(5):
#     b.add_random_column_cop()
#     b.print_board()

print(b.get_paths())
print(b.place_cops())
print(b.run_board())