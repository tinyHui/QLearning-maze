from PIL import Image
from matplotlib.pyplot import imshow
from io import BytesIO
import IPython.display
import numpy as np
from random import randint, choice
from collections import defaultdict

BLOCK_SIZE = 10
PASSAGE = (255,255,255)
WALL = (0,0,0)
START = (0,255,0)
END = (255,0,0)
VISITED = (255,255,0)

class Maze:

    def __init__(self, size=(49,49), verbose=False):
        self.h, self.w = size
        self.size = size
        self.maze = None
        self.visited = []
        self.start = None
        self.end = None
        self.visited_count = defaultdict(int)
        self.verbose = verbose
        
    def generate(self):
        self.maze = [[Cell(pos=(h, w)) for w in range(self.w)] for h in range(self.h)]

        frontier_list = []
        cell = self.__get__(1, 1)
        cell.set_as_passage()
        self.start = cell.get_pos()
        frontier_list += self.__neighbor_frontiers(cell)

        while len(frontier_list) > 0:
            if len(frontier_list) == 1:
                self.end = frontier_list[0].get_pos()

            cell = choice(frontier_list)

            neighbor = choice(self.__neighbot_passenges(cell))
            self.__connect(cell, neighbor)

            for frontier in self.__neighbor_frontiers(cell):
                if not frontier in frontier_list:
                    frontier_list.append(frontier)

            frontier_list.remove(cell)
            
            if self.verbose:
                self.draw()

    def draw(self):
        img = []
        # convert 2-d array to image
        for h in range(self.h):
            line = []
            for w in range(self.w):
                if self.__get__(h, w).is_passage():
                    line.append(PASSAGE)
                else:
                    line.append(WALL)

            img.append(line)
        
        # mark visited points
        for cell in self.visited:
            h, w = cell.get_pos()
            img[h][w] = VISITED
            
        if self.start is not None and self.end is not None:
            h, w = self.start
            img[h][w] = START
            h, w = self.end
            img[h][w] = END

        img = self.__scale(img, BLOCK_SIZE)
        self.__showarray(img)

    def get(self, hp, wp):
        try:
            cell = self.maze[hp][wp]
            if not cell.is_passage():
                raise IndexError
            return cell
        except IndexError:
            raise IndexError('Hit border')
    
    def get_size(self):
        return self.size

    def mark_history(self, cell): 
        self.visited.append(cell)
        self.visited_count[cell] += 1
        
    def empty_history(self):
        del self.visited[:]
        # del self.visited_count[:]
        
    def get_all_passages(self):
        all_passages = []
        for row in self.maze:
            all_passages += filter(lambda x: x.is_passage(), row)
        return all_passages
    
    def is_end(self, pos):
        return pos == self.end
        
    def __get__(self, hp, wp):
        return self.maze[hp][wp]

    def __neighbors(self, cell, dist=1):
        neighbors = []
        hp, wp = cell.get_pos()
        if hp - dist > 0:          neighbors.append(self.__get__(hp - dist, wp))
        if hp + dist < self.h - 1: neighbors.append(self.__get__(hp + dist, wp))
        if wp - dist > 0:          neighbors.append(self.__get__(hp, wp - dist))
        if wp + dist < self.w - 1: neighbors.append(self.__get__(hp, wp + dist))
        return neighbors

    def __neighbor_frontiers(self, cell):
        frontiers = []
        for neighbor in self.__neighbors(cell, dist=2):
            if not neighbor.is_passage():
                frontiers.append(neighbor)
        return frontiers

    def __neighbot_passenges(self, cell):
        passenges = []
        for neighbor in self.__neighbors(cell, dist=2):
            if neighbor.is_passage():
                passenges.append(neighbor)
        return passenges

    def __connect(self, c1, c2):
        c1.set_as_passage()
        c1_h_pos, c1_w_pos = c1.get_pos()
        c2_h_pos, c2_w_pos = c2.get_pos()
        if   c1_h_pos == c2_h_pos and c1_w_pos - 2 == c2_w_pos:   self.__get__(c1_h_pos, c1_w_pos - 1).set_as_passage()
        elif c1_h_pos == c2_h_pos and c1_w_pos + 2 == c2_w_pos:   self.__get__(c1_h_pos, c1_w_pos + 1).set_as_passage()
        elif c1_h_pos - 2 == c2_h_pos and c1_w_pos == c2_w_pos:   self.__get__(c1_h_pos - 1, c1_w_pos).set_as_passage()
        elif c1_h_pos + 2 == c2_h_pos and c1_w_pos == c2_w_pos:   self.__get__(c1_h_pos + 1, c1_w_pos).set_as_passage()
        c2.set_as_passage()

    def __scale(self, img, s):
        img_new = []
        for line in img:
            line_new = []
            for cell in line:
                line_new += [cell] * s

            for _ in range(s):
                img_new.append(line_new)

        return img_new

    def __showarray(self, a, fmt='png'):
        a = np.uint8(a)
        f = BytesIO()
        Image.fromarray(a).save(f, fmt)
        IPython.display.display(IPython.display.Image(data=f.getvalue()))
        IPython.display.clear_output(wait=True)

        
class Cell:

    def __init__(self, value=False, pos=(0, 0)):
        self.v = value
        self.pos = pos

    def set_as_wall(self):
        self.v = False

    def set_as_passage(self):
        self.v = True

    def is_passage(self):
        return self.v

    def get_pos(self):
        return self.pos

    def __eq__(self, o):
        return self.pos == o.pos

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "(h=%d, w=%d, v=%s)" % (*self.pos, self.v)
    
    def __hash__(self):
        return hash(self.pos)
