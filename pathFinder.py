import math
import random
import types
import copy
import pygame
from enum import Enum


# MAZE BLOCK
class CellType(Enum):
    Empty = 1
    Block = 2


class CellMark(Enum):
    No = 0
    Start = 1
    End = 2


class Cell:
    def __init__(self, type=CellType.Empty, position=None):
        self.type = type
        self.count = 0
        self.mark = CellMark.No
        self.path_from = None
        self.position = position


class CellGrid:
    def __init__(self, board):
        self.board = board

    def get_size(self):
        return [len(self.board), len(self.board[0])]

    def at(self, position):
        return self.board[position[0]][position[1]]

    def clone(self):
        return CellGrid(copy.deepcopy(self.board))

    def clear_count(self, count):
        for o in self.board:
            for i in o:
                i.count = count
                i.path_from = None

    def is_valid_point(self, pos):
        sz = self.get_size()
        return pos[0] >= 0 and pos[1] >= 0 and pos[0] < sz[0] and pos[1] < sz[1]


def create_wall_maze(x, y):
    board = [[Cell(type=CellType.Empty, position=[ix, iy]) for iy in range(y)] for ix in range(x)]
    for i in range(0, x):
        board[i][int(y / 2)].type = CellType.Block
    for i in range(0, y):
        board[int(x / 2)][i].type = CellType.Block

    board[random.randint(0, x / 2 - 1)][int(y / 2)].type = CellType.Empty
    board[random.randint(x / 2 + 1, x - 1)][int(y / 2)].type = CellType.Empty
    board[int(x / 2)][random.randint(0, y / 2 - 1)].type = CellType.Empty
    board[int(x / 2)][random.randint(y / 2 + 1, y - 1)].type = CellType.Empty

    return types.SimpleNamespace(board=CellGrid(board),
                                 start=[random.randrange(0, x / 2), random.randrange(y / 2 + 1, y)],
                                 end=[random.randrange(x / 2 + 1, x), random.randrange(0, y / 2)])


def create_maze(num_of_rows, red_snake, purple_snake, snack):
    board = [[Cell(type=CellType.Empty, position=[ix, iy]) for iy in range(num_of_rows)] for ix in range(num_of_rows)]
    head_pos = red_snake.head.cube_position
    purple_head_pos = purple_snake.head.cube_position
    for ith_cube, cube_object in enumerate(red_snake.body):
        cube_object = cube_object.cube_position[:]
        if not head_pos[0] >= num_of_rows or head_pos[0] < 0 or head_pos[1] >= num_of_rows or head_pos[1] < 0:
            board[cube_object[0]][cube_object[1]].type = CellType.Block
    for ith_cube, cube_object in enumerate(purple_snake.body):
        cube_object = cube_object.cube_position[:]
        if not purple_head_pos[0] >= num_of_rows or purple_head_pos[0] < 0 or purple_head_pos[1] >= num_of_rows or \
                purple_head_pos[1] < 0:
            board[cube_object[0]][cube_object[1]].type = CellType.Block

    return types.SimpleNamespace(board=CellGrid(board),
                                 start=purple_snake.body[0].cube_position,
                                 end=snack.cube_position)


def add_point(a, b):
    return [a[0] + b[0], a[1] + b[1]]


# PATH FINDER BLOCK
def fill_shortest_path(board, start, end, max_distance=math.inf):
    """ Creates a duplicate of the board and fills the `Cell.count` field with the distance from the start to that cell. """
    nboard = board.clone()
    nboard.clear_count(math.inf)

    # mark the start and end for the UI
    nboard.at(start).mark = CellMark.Start
    nboard.at(end).mark = CellMark.End

    # we start here, thus a distance of 0
    open_list = [start]
    nboard.at(start).count = 0

    # (x,y) offsets from current cell
    while open_list:

        random_direction = random.randint(1, 5)
        if random_direction == 2:
            neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        else:
            neighbours = [[0, -1], [0, 1], [-1, 0], [1, 0]]

        cur_pos = open_list.pop(0)
        cur_cell = nboard.at(cur_pos)

        for neighbour in neighbours:
            ncell_pos = add_point(cur_pos, neighbour)
            if not nboard.is_valid_point(ncell_pos):
                continue

            cell = nboard.at(ncell_pos)

            if cell.type != CellType.Empty:
                continue

            distance = cur_cell.count + 1
            if distance > max_distance:
                continue

            if cell.count > distance:
                cell.count = distance
                cell.path_from = cur_cell
                open_list.append(ncell_pos)

    return nboard

def backtrack_to_start(board, end):
    """ Returns the path to the end, assuming the board has been filled in via fill_shortest_path """
    cell = board.at(end)
    # print(cell)
    path = []
    lis = []
    while cell != None:
        path.append(cell)
        cell = cell.path_from
        for i in path[-1:]:
            for j in i.position:
                lis.append(j)
    next_move = lis[-4:-2]

    return next_move

def backtrack_to_start_to_draw_purpose(board, end):
    """ Returns the path to the end, assuming the board has been filled in via fill_shortest_path """
    cell = board.at(end)
    # print(cell)
    path = []
    lis = []
    while cell != None:
        path.append(cell)
        cell = cell.path_from
        for i in path[-1:]:
            for j in i.position:
                lis.append(j)

    return path


# DRAW BLOCK
pygame.init()
pygame.display.set_caption("Path Finding Demo")
cell_font = pygame.font.SysFont(pygame.font.get_default_font(), 25)


def trans_rect(r, off):
    return [r[0] + off[0], r[1] + off[1], r[2], r[3]]


def main_loop(ui):
    screen = pygame.display.set_mode((750, 600))

    clock = pygame.time.Clock()
    clock.tick()
    i = 0
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break
            if event.key == pygame.K_RIGHT:
                ui.step(1)
            if event.key == pygame.K_LEFT:
                ui.step(-1)
            if event.key == pygame.K_r:
                ui.reset_snake()

        ui.draw(screen)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


class Finder:
    def __init__(self):
        self.path = None
        self.board = None

    def set_board(self, board):
        self.board = board

    def set_path(self, path):
        self.path = path

    def run(self):
        main_loop(self)

    def draw(self, surface):
        if self.board == None:
            return

        draw_board(surface, surface.get_rect(), self.board)
        if self.path != None:
            draw_path(surface, surface.get_rect(), self.board, self.path)

    def step(self, steps):
        pass

    def reset(self):
        pass


class BoardMetrics:
    def __init__(self, area, board):
        self.area = area
        self.spacing = 3
        self.left = area[0] + self.spacing
        self.top = area[1] + self.spacing
        self.width = area[2] - area[0] - 2 * self.spacing
        self.height = area[3] - area[1] - 2 * self.spacing
        self.num_y = board.get_size()[1]
        self.num_x = board.get_size()[0]
        self.cy = self.height / self.num_y
        self.cx = self.width / self.num_x

    def cell_rect(self, pos):
        return [self.left + pos[0] * self.cx, self.top + pos[1] * self.cy, self.cx - self.spacing,
                self.cy - self.spacing]

    def cell_center(self, pos):
        rct = self.cell_rect(pos)
        return [rct[0] + rct[2] / 2, rct[1] + rct[3] / 2]


def draw_board(surface, area, board):
    pygame.draw.rect(surface, (0, 0, 0), area)
    metrics = BoardMetrics(area, board)

    colors = {
        CellType.Empty: (40, 40, 40),
        CellType.Block: (128, 100, 0),
    }
    marks = {
        CellMark.Start: (110, 110, 0),
        CellMark.End: (0, 110, 0),
    }
    for y in range(0, metrics.num_y):
        for x in range(0, metrics.num_x):
            cell = board.at([x, y])
            clr = colors.get(cell.type, (100, 100, 0))
            cell_rect = metrics.cell_rect([x, y])

            pygame.draw.rect(surface, clr, cell_rect)

            if cell.count != math.inf:
                number = cell_font.render("{}".format(cell.count), True, (255, 255, 255))
                surface.blit(number, trans_rect(number.get_rect(),
                                                [cell_rect[0] + (cell_rect[2] - number.get_rect()[2]) / 2,
                                                 cell_rect[1] + (cell_rect[3] - number.get_rect()[3]) / 2]
                                                ))

            mark = marks.get(cell.mark, None)
            if mark != None:
                pygame.draw.rect(surface, mark, cell_rect, metrics.spacing)


def draw_path(surface, area, board, path):
    metrics = BoardMetrics(area, board)
    for i in range(0, len(path) - 1):
        ctr_a = metrics.cell_center(path[i].position)
        ctr_b = metrics.cell_center(path[i + 1].position)
        pygame.draw.line(surface, (120, 220, 0), ctr_a, ctr_b, metrics.spacing)


# RUN CODE BLOCK
def path_finder(num_of_rows, red_snake, purple_snake, snack):
    maze = create_maze(num_of_rows, red_snake, purple_snake, snack)
    filled = fill_shortest_path(maze.board, maze.start, maze.end)
    next_move = backtrack_to_start(filled, maze.end)

    return next_move

def path_finder_draw_maze(num_of_rows, red_snake, purple_snake, snack):
    maze = create_maze(num_of_rows, red_snake, purple_snake, snack)
    filled = fill_shortest_path(maze.board, maze.start, maze.end)
    path = backtrack_to_start_to_draw_purpose(filled, maze.end)

    finder = Finder()
    finder.set_board(filled)
    finder.set_path(path)
    finder.run()
# The start cell is outlined in yellow and has a zero in it. The numbers increase, in increments of one, away from that spot.
# All cells in the grid are labeled with their Manhatten distance from the starting point.
# We can find a path back to the start from the destination node by scanning the neighbors and picking the one with the lowest number.
