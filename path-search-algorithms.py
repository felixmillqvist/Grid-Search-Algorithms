import pygame
import pickle
import os
from algorithms import *
from antSystem import AntSystem
WIDTH = 800

DISTANCE = 1
ROWS = 20

RED = (255, 117, 109)
GREEN = (133, 222, 119)
BLUE = (161, 201, 241)
YELLOW =  (255, 244, 156)
WHITE = (249, 255, 203)
BLACK = (112, 69, 35)
PURPLE = (149, 125, 173)
ORANGE = (255, 180, 71)
GREY = (135, 92, 54)
TURQUOISE = (130, 179, 255)

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Grid Path Finding Algorithms")



class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = BLACK
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def get_neighbors(self):
        return self.neighbors

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == WHITE

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def is_clear(self):
        return self.color == BLACK

    def reset(self):
        self.color = BLACK

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid, diagonal):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        if diagonal:
            if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_barrier(): # Lower Left
                self.neighbors.append(grid[self.row + 1][self.col - 1])

            if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_barrier(): # Upper Left
                self.neighbors.append(grid[self.row - 1][self.col - 1])

            if self.col < self.total_rows - 1 and self.row < self.total_rows - 1 and not grid[self.row + 1][self.col + 1].is_barrier(): # Lower Right
                self.neighbors.append(grid[self.row + 1][self.col + 1])

            if self.col < self.total_rows - 1 and self.row > 0 and not grid[self.row - 1][self.col + 1].is_barrier(): # Upper Right
                self.neighbors.append(grid[self.row - 1][self.col + 1])

    def reset_neighbors(self):
        self.neighbor = []

    def __lt__(self, other):
        return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

def reset_searched_nodes(grid):
    for row in grid:
        for node in row:
            if  not (node.is_start() or node.is_end() or node.is_barrier()):
                node.reset()
                node.reset_neighbors()


def draw_grid(win, rows, width):
    gap  = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width, tree=False, path=[], locs=[]):
    win.fill(BLACK)

    for row in grid:
        for node in row:
            node.draw(win)
            if tree and node.is_barrier():
                pygame.draw.circle(WIN, (0,0,0), (node.x+node.width//2, node.y+node.width//2), 10)
    if tree and len(path) > 0 and len(locs) > 0:
        draw_path(win, grid, path, locs)


    draw_grid(win, rows, width)
    pygame.display.update()

def draw_path(win, grid, path, locs):
    n_locs = len(locs)
    locs_ext = []
    for edge in path:
        locs_ext.append(locs[edge])
    locs_ext.append(locs[path[0]])

    for i in range(n_locs):
        node1 = grid[locs_ext[i][0]][locs_ext[i][1]]
        node2 = grid[locs_ext[i+1][0]][locs_ext[i+1][1]]
        pos1 = (node1.x+node1.width//2, node1.y+node1.width//2)
        pos2 = (node2.x+node2.width//2, node2.y+node2.width//2)

        pygame.draw.line(win, (0,0,0), pos1, pos2, 3)


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def update_all_neighbors(grid, diagonal):
    for row in grid:
        for node in row:
            node.update_neighbors(grid, diagonal)

def make_tree(grid):
    for row in grid:
        for node in row:
            if node.is_clear():
                node.make_barrier()
            elif node.is_barrier():
                node.reset()

def get_locations(grid):
    locations = []
    for row in grid:
        for node in row:
            if node.is_barrier():
                locations.append((node.row, node.col))
    return locations

def save_grid(grid):
    reset_searched_nodes(grid)

    file_index = 1
    file_name = F"example_grid_{file_index}.pkl"
    while os.path.isfile(file_name):
        file_name = F"example_grid_{file_index}.pkl"
        file_index += 1
    with open(file_name, 'wb') as pickle_file:
        pickle.dump(grid, pickle_file)

def switch_grid(grid_index):
    grid_index += 1
    start = None
    end = None
    file_name = F"example_grid_{grid_index}.pkl"
    if  not os.path.isfile(file_name):
        grid_index = 1
    file_name = F"example_grid_{grid_index}.pkl"
    if  os.path.isfile(file_name):
        with open(file_name, 'rb') as pickle_file:
            grid = pickle.load(pickle_file)
            for row in grid:
                for node in row:
                    if node.is_start():
                        start = node
                    elif node.is_end():
                        end = node
    return (grid, start, end, grid_index)

def main():
    grid = make_grid(ROWS, WIDTH)

    start = None
    end = None
    run = True
    diagonal = False
    tree = False
    grid_index = 0
    path = []
    locs = []

    while run:
        draw(WIN, grid, ROWS,  WIDTH, tree, path, locs)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                node = grid[row][col]

                if not start and node != end and not tree:
                    start = node
                    start.make_start()

                if not end and node != start and not tree:
                    end = node
                    end.make_end()

                if (node != end and node != start) or tree:
                    node.make_barrier()

            if pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                node = grid[row][col]
                node.reset()

                if node == start:
                    start = None
                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    reset_searched_nodes(grid)
                    update_all_neighbors(grid, diagonal)
                    a_star(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)

                if event.key == pygame.K_d and start and end:
                    reset_searched_nodes(grid)
                    update_all_neighbors(grid, diagonal)
                    dijkstra(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)

                if event.key == pygame.K_b and start and end:
                    reset_searched_nodes(grid)
                    update_all_neighbors(grid, diagonal)
                    breadth_first_search(lambda: draw(WIN, grid, ROWS, WIDTH), start, end)

                if event.key == pygame.K_j and start and end:
                    reset_searched_nodes(grid)
                    update_all_neighbors(grid, diagonal)
                    depth_first_search(lambda: draw(WIN, grid, ROWS, WIDTH), start, end)

                if event.key == pygame.K_n:
                    diagonal = not diagonal

                if event.key == pygame.K_t:
                    tree = not tree

                if event.key == pygame.K_m:
                    make_tree(grid)

                if event.key == pygame.K_c:
                    locs = get_locations(grid)
                    from antSystem import GetNNPath
                    path, path_length = GetNNPath(locs)

                    for (iteration, ant, path_length, path) in AntSystem(locs):
                        print(f'Iteration: {iteration} Ant: {ant} Length: {path_length}')
                        draw(WIN, grid, ROWS,  WIDTH, tree, path, locs)


                if event.key == pygame.K_r:
                    reset_searched_nodes(grid)

                if event.key == pygame.K_q:
                    run = False

                if event.key == pygame.K_s:
                    save_grid(grid)

                if event.key == pygame.K_g:
                    grid, start, end, grid_index = switch_grid(grid_index)





    pygame.quit()

main()
