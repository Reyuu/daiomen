import pygame
import collections
import ezpygame

Point = collections.namedtuple("Point", ["x", "y"])

class Selection:
    def __init__(self):
        """
        Selection class for handling game input.
        """
        """
        self.state = { "set1",
                       "ready",
                       "processing",
                       "idle" }
        """
        self.state = "idle"
        self.pos1 = (-1, -1)
        self.pos2 = (-1, -1)

    def add_pos(self, pos):
        if self.state == "idle":
            self.pos1 = pos
            self.state = "set1"
            return None
        if self.state == "set1":
            self.pos2 = pos
            self.state = "ready"
            return None

    def check_ready(self):
        if self.state == "ready":
            self.state = "processing"
            return True
        return False

    def after_process(self):
        if self.state == "processing":
            self.state = "idle"
            self.pos1 = (-1, -1)
            self.pos2 = (-1, -1)

class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.text = "Example"
        self.connected_to = []
        self.pos = Point(x=x, y=y)
        self.width = 100
        self.height = 100

    def get_rect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

def isPointInsideRect(x, y, rect):
    """
    Checks if point is inside some rectangle (Rect object)
    :param x: horizontal
    :param y: vertical
    :param rect: rect to check inside
    :return: bool
    """
    if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
        return True
    else:
        return False

def doRectsOverlap(rect1, rect2):
    """
    Checks if rectangles (Rect objects) overlap
    :param rect1: first Rect object
    :param rect2: second Rect object
    :return: bool
    """
    for a, b in [(rect1, rect2), (rect2, rect1)]:
        # Check if a's corners are inside b
        if((isPointInsideRect(a.left, a.top, b)) or
               (isPointInsideRect(a.left, a.bottom, b)) or
               (isPointInsideRect(a.right, a.top, b)) or
               (isPointInsideRect(a.right, a.bottom, b))):
            return True
    return False





class Editor(ezpygame.Scene):
    def __init__(self):
        super().__init__()
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 16)
        self.counter = 0
        self.node_collection = []

    def check_collisions(self, x, y):
        for i in range(len(self.node_collection)):
            if isPointInsideRect(x, y, self.node_collection[i].get_rect()):
                return i
        return False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pos = Point(x=pos[0], y=pos[1])
            if event.button == 1:
                col = self.check_collisions(pos.x, pos.y)
                if type(col) == int:
                    self.node_collection[col].pos = pos
                else:
                    self.node_collection += [Node("Node%s" % self.counter, pos.x, pos.y)]
                    self.counter += 1

    def draw(self, screen):
        screen.fill((255, 255, 255))
        for item in self.node_collection:
            pygame.draw.rect(screen, (225, 225, 225), pygame.Rect(item.pos.x, item.pos.y, item.width, item.height))
            pygame.draw.rect(screen, (235, 235, 235), pygame.Rect(item.pos.x, item.pos.y, item.width, 20))
            name = self.font.render(item.name, True, (210, 210, 210))
            text = self.font.render(item.text, True, (210, 210, 210))
            screen.blit(name, item.pos)
            screen.blit(text, (item.pos.x, item.pos.y+20))



app = ezpygame.Application(
    title="Daoimen",
    resolution=(1280, 720),
    update_rate=60
)

app.run(Editor())