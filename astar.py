import pygame
import math
from queue import PriorityQueue

WIDTH = 800

DISTANCE = 1
ROWS = 5

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
        self.neighbours = []
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

def manhattan_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = manhattan_distance(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + DISTANCE
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + manhattan_distance(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()
    return False
    
def dijkstra(draw, grid, start, end):
    count = 0
    pq = PriorityQueue()
    pq.put((0, count, start))
    prev = {}
    dist = {node: float("inf") for row in grid for node in row}
    dist[start] = 0

    pq_hash = {start}

    while not pq.empty():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = pq.get()[2]
        pq_hash.remove(current)

        if current == end:
            reconstruct_path(prev, end, draw)
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            alt_dist = dist[current] + DISTANCE;
            if alt_dist < dist[neighbor]:
                dist[neighbor] = alt_dist
                prev[neighbor] = current
                if neighbor not in pq_hash:
                    count += 1
                    pq.put((dist[neighbor], count, neighbor))
                    pq_hash.add(neighbor)
                    neighbor.make_open()
                
        draw()

        if current != start:
           current.make_closed()

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
        
def draw(win, grid, rows, width):
    win.fill(BLACK)

    for row in grid:
        for node in row:
            node.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()

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

def main():
    grid = make_grid(ROWS, WIDTH)

    start = None
    end = None
    run = True
    diagonal = False

    while run:
        draw(WIN, grid, ROWS,  WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    start.make_start()

                if not end and node != start:
                    end = node
                    end.make_end()

                if node != end and node != start:
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
                    update_all_neighbors(grid, diagonal)
                    a_star(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)

                if event.key == pygame.K_d and start and end:
                    update_all_neighbors(grid, diagonal)
                    dijkstra(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)

                if event.key == pygame.K_n:
                    diagonal = not diagonal

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, WIDTH)  

                if event.key == pygame.K_r:
                    reset_searched_nodes(grid)
                    
                

    pygame.quit()

main()


    

