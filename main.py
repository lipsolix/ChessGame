import copy
import threading
import queue

def inv_team(team):
    if team == "white":
        return "black"
    return "white"

class Figure:

    def __init__(self):
        self.turns = 0


class King(Figure):

    def __init__(self, color):
        super().__init__()
        self.possible_turns = []
        self.color = color
        self.cost = 100


    def get_possible_turns(self,chessboard, x, y):
        self.possible_turns = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if (x+i != x) or (y+j != y):
                    if (x + i > -1) and (x + i < 8) and (y + j > -1) and (y + j < 8):
                        if chessboard[y+j][x+i] is None:
                            self.possible_turns.append((x+i, y+j))
                        elif chessboard[y+j][x+i].color != self.color:
                            self.possible_turns.append((x+i, y+j))

        return self.possible_turns


class Queen(Figure):

    def __init__(self, color):
        super().__init__()
        self.possible_turns = []
        self.color = color
        self.cost = 9

    def get_possible_turns(self, chessboard, x, y):
        self.possible_turns = []
        for i in range(1, 8):
            if (x + i < 8) and (x + i > -1) and (i != 0):
                if chessboard[y][x+i] is None:
                    self.possible_turns.append((x+i, y))
                elif chessboard[y][x+i].color == self.color:
                    break
                else:
                    self.possible_turns.append((x+i, y))
                    break

        for i in range(1, 8):
            if (x - i < 8) and (x - i > -1) and (i != 0):
                if chessboard[y][x-i] is None:
                    self.possible_turns.append((x-i, y))
                elif chessboard[y][x-i].color == self.color:
                    break
                else:
                    self.possible_turns.append((x-i, y))
                    break

        for i in range(1, 8):
            if (y + i < 8) and (y + i > -1) and (i != 0):
                if chessboard[y+i][x] is None:
                    self.possible_turns.append((x, y+i))
                elif chessboard[y+i][x].color == self.color:
                    break
                else:
                    self.possible_turns.append((x, y+i))
                    break
        for i in range(1, 8):
            if (y - i < 8) and (y - i > -1) and (i != 0):
                if chessboard[y-i][x] is None:
                    self.possible_turns.append((x, y-i))
                elif chessboard[y-i][x].color == self.color:
                    break
                else:
                    self.possible_turns.append((x, y-i))
                    break

        for i in (-1, 1):
            for j in (-1, 1):
                for k in range(1, 8):
                    if (x+k*i > -1) and (y+k*j < 8) and (x+k*i < 8) and (y+k*j > -1):
                        if chessboard[y+k*j][x+k*i] is None:
                            self.possible_turns.append((x+k*i, y+k*j))
                        elif chessboard[y+k*j][x+k*i].color == self.color:
                            break
                        else:
                            self.possible_turns.append((x+k*i, y+k*j))
                            break

        return self.possible_turns


class Knight(Figure):

    def __init__(self, color):
        super().__init__()
        self.possible_turns = []
        self.color = color
        self.cost = 3

    def get_possible_turns(self,chessboard, x, y):
        self.possible_turns = []
        for i, j in ((2, 1), (1, 2), (-1, 2), (2, -1), (1, -2), (-2, 1), (-1, -2), (-2, -1)):
            if (x + i > -1) and (x + i < 8) and (y +j > -1) and (y + j < 8):
                if chessboard[y+j][x+i] is None:
                    self.possible_turns.append((x+i, y+j))
                elif chessboard[y+j][x+i].color != self.color:
                    self.possible_turns.append((x+i, y+j))
        return self.possible_turns


class Rook(Figure):

    def __init__(self, color):
        super().__init__()
        self.color = color
        self.cost = 5
        self.possible_turns = []

    def get_possible_turns(self,chessboard, x, y):
        self.possible_turns = []

        for i in range(1, 8):
            if (x + i < 8) and (x + i > -1) and (i != 0):
                if chessboard[y][x+i] is None:
                    self.possible_turns.append((x+i, y))
                elif chessboard[y][x+i].color == self.color:
                    break
                else:
                    self.possible_turns.append((x+i, y))
                    break

        for i in range(1, 8):
            if (x - i < 8) and (x - i > -1) and (i != 0):
                if chessboard[y][x-i] is None:
                    self.possible_turns.append((x-i, y))
                elif chessboard[y][x-i].color == self.color:
                    break
                else:
                    self.possible_turns.append((x-i, y))
                    break

        for i in range(1, 8):
            if (y + i < 8) and (y + i > -1) and (i != 0):
                if chessboard[y+i][x] is None:
                    self.possible_turns.append((x, y+i))
                elif chessboard[y+i][x].color == self.color:
                    break
                else:
                    self.possible_turns.append((x, y+i))
                    break
        for i in range(1, 8):
            if (y - i < 8) and (y - i > -1) and (i != 0):
                if chessboard[y-i][x] is None:
                    self.possible_turns.append((x, y-i))
                elif chessboard[y-i][x].color == self.color:
                    break
                else:
                    self.possible_turns.append((x, y-i))
                    break

        return self.possible_turns


class Bishop(Figure):

    def __init__(self, color):
        super().__init__()
        self.possible_turns = []
        self.color = color
        self.cost = 3

    def get_possible_turns(self, chessboard, x, y):
        self.possible_turns = []
        for i in (-1, 1):
            for j in (-1, 1):
                for k in range(1, 8):
                    if (x+k*i > -1) and (y+k*j < 8) and (x+k*i < 8) and (y+k*j > -1):
                        if chessboard[y+k*j][x+k*i] is None:
                            self.possible_turns.append((x+k*i, y+k*j))
                        elif chessboard[y+k*j][x+k*i].color == self.color:
                            break
                        else:
                            self.possible_turns.append((x+k*i, y+k*j))
                            break

        return self.possible_turns


class Pawn(Figure):

    def __init__(self, color):
        super().__init__()
        self.possible_turns = []
        self.color = color
        self.cost = 1
        if self.color == 'white':
            self.direction = -1
        else:
            self.direction = 1

    def get_possible_turns(self, chessboard, x, y):
        self.possible_turns = []
        for i in (-1, 1):
            if (x + i > -1) and (x + i < 8) and (y + self.direction > 0) and (y + self.direction < 8):
                if (chessboard[y+self.direction][x+i] is None):
                    continue
                elif (chessboard[y+self.direction][x+i].color == self.color):
                    continue
                else:
                    self.possible_turns.append((x+i, y + self.direction))
        if (y + self.direction > 0) and (y + self.direction < 8) and (chessboard[y+self.direction][x] is None):
            self.possible_turns.append((x, y + self.direction))
            if (self.turns == 0) and (chessboard[y+2*self.direction][x] is None):
                self.possible_turns.append((x, y + 2*self.direction))
        return self.possible_turns


class Table:
    def __init__(self):
        self.table = []

    def get(self):
        return self.table

    def init(self):
        self.table = [[None for i in range(8)] for i in range(8)]

        ###Kings ������
        k = King(color='white')
        self.table[7][4] = k
        k = King(color="black")
        self.table[0][4] = k

        ###Queens �����
        q = Queen(color="white")
        self.table[7][3] = q
        q = Queen(color="black")
        self.table[0][3] = q

        ###Knights ����
        n = Knight(color="white")
        self.table[7][1] = n
        n = Knight(color="black")
        self.table[0][1] = n
        n = Knight(color="white")
        self.table[7][6] = n
        n = Knight(color="black")
        self.table[0][6] = n


        ###Rooks �����
        r = Rook(color="white")
        self.table[7][0] = r
        r = Rook(color="black")
        self.table[0][0] = r
        r = Rook(color="white")
        self.table[7][7] = r
        r = Rook(color="black")
        self.table[0][7] = r

        ###Bishops �����
        b = Bishop(color="white")
        self.table[7][2] = b
        b = Bishop(color="white")
        self.table[7][5] = b
        b = Bishop(color="black")
        self.table[0][2] = b
        b = Bishop(color="black")
        self.table[0][5] = b


        ###Pawns �����
        for i in range(8):
            p = Pawn(color="black")
            self.table[1][i] = p
        for i in range(8):
            p = Pawn(color="white")
            self.table[6][i] = p

def king_position(chessboard, team):
    for y in range(8):
        for x in range(8):
            if isinstance(chessboard[y][x], King) and (chessboard[y][x].color == team):
                return x, y

def show_table(x):
    for i in range(8):
        for j in range(8):
            y = x[i][j]
            if y is not None:
                print(y.color[0], end=' ')
            else:
                print(0, end=' ')
        print(end='\n')


def run_simulation(chessboard, buffer, team, depth, fx, fy, tx, ty):
    
    if (depth == 0):
        buffer.put((0, fx, fy, tx, ty))
        return
    new_chessboard = copy.deepcopy(chessboard)
    
    if new_chessboard[ty][tx] is None:
        turn_cost = 0
    else:
        turn_cost = new_chessboard[ty][tx].cost
    if fx != -1:
        new_chessboard[ty][tx] = new_chessboard[fy][fx]
        new_chessboard[fy][fx] = None
        new_chessboard[ty][tx].cost += 1
    kx, ky = king_position(new_chessboard, inv_team(team))
    p_turns = []
    for y in range(8):
        for x in range(8):
            figure = new_chessboard[y][x]
            if figure is None:
                continue
            if figure.color != team:
                continue
            turns = figure.get_possible_turns(new_chessboard, x, y)
            for turn in turns:
                tx, ty = turn
                p_turns.append((x, y, tx, ty))
                if (kx == tx) and (ky == ty):
                    buffer.put(None)
                    return
    new_buffer = queue.Queue(0)
    for turn in p_turns:
        threading.Thread(target=run_simulation, args=(new_chessboard, new_buffer, inv_team(team), depth - 1, *turn)).start()
    max_impact = -100000000
    max_impact_turn = None
    for i in range(len(p_turns)):
        data = new_buffer.get()
        if data is not None:
            points, *turn = data
            if max_impact < (turn_cost - points):
                max_impact = turn_cost - points
                max_impact_turn = turn
    buffer.put((max_impact, *max_impact_turn))
    return max_impact_turn

def predict(chessboard, team, depth):
    q = queue.Queue(0)
    return run_simulation(chessboard, q, team, depth, -1, -1, -1,-1)

table = Table()
table.init()
chessboard = table.get()

show_table(chessboard)
x = predict(chessboard, "white", 3)

print(x)

