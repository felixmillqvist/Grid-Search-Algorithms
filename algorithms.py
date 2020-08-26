import math
from queue import PriorityQueue
from queue import Queue
from collections import deque
import pygame

DISTANCE = 1

def manhattan_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw, start = None):
    while current in came_from and not current is start:
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
        
        for neighbor in current.get_neighbors():
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

        for neighbor in current.get_neighbors():
            alt_dist = dist[current] + DISTANCE
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

def breadth_first_search(draw, start, end):
    q = Queue()
    current = start
    q.put((current, {}))
    while not q.empty():
        current, path = q.get()

        if not current == start:
            current.make_closed()

        if current == end:
            reconstruct_path(path, end, draw, start)
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.get_neighbors():
            if not (neighbor.is_closed() or neighbor.is_open()):
                neighbor.make_open()
                path[neighbor] = current
                q.put((neighbor, path))

        draw()
    return False



def depth_first_search(draw, start, end):
    q = deque()
    current = start
    q.append((current, {}))
    while q:
        current, path = q.pop()

        if not current == start:
            current.make_closed()

        if current == end:
            reconstruct_path(path, end, draw, start)
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.get_neighbors():
            if not (neighbor.is_closed() or neighbor.is_open()):
                neighbor.make_open()
                path[neighbor] = current
                q.append((neighbor, path))

        draw()
    return False

def kruskals(draw, grid):
    pass

def prims(draw, grid):
    pass
