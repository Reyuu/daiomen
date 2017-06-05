import pygame
import collections
import ezpygame
import re
import os
Point = collections.namedtuple("Point", ["x", "y"])

def load_png(name):
    """
    Load image and return image object
    :param directory: 
    :param name: 
    """
    fullname = os.path.join(name)
    #fullname = name
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image: %s' % fullname)
        raise SystemExit(message)

    return image, image.get_rect()

class Speaker:
    def __init__(self):
        self.image = ""
        self.current_image = pygame.Surface((1, 1))
        self.name = ""
        self.visibility = True
        self.side = "left"

    def process(self):
        #print(self.image)
        self.current_image = load_png(self.image)[0]
        if self.side == "left":
            self.current_image = pygame.transform.flip(self.current_image, True, False)

    def handle_set(self, n, m):
        #print(n, m)
        n = n.strip("\"")
        m = m.strip("\"")
        if n == "image":
            self.image = m
            self.process()
        if n == "name":
            self.name = m
        if n == "side":
            print(n, m)
            self.side = m.lower()
            print(self.side)
        if n == "visibility":
            bl = {"false": False, "true": True}
            self.visibility = bool(bl[m.lower()])


class Scripting:
    def __init__(self):
        self.keywords = {}
        self.constants = {"Speaker": Speaker}
        self.variables = {"current_speaker": None, "current_line": "",
                          "name1": Speaker(), "name2": Speaker()}
        self.paused = False

    def parse_instruction(self, instruction):
        #print(instruction)
        words = instruction.split(" ")
        if words[0] == "create":
            self.variables.update({words[2]: self.constants[words[1]]()})
        if words[0] == "set":
            try:
                var = words[1].split(".")[0]
                #print(var)
                if isinstance(self.variables[var], self.constants["Speaker"]):
                    self.variables[var].handle_set(words[1].split(".")[1], words[2])
            except IndexError:
                pass

    def parse_line(self, line):
        if not(self.paused):
            if line[0] == "#":
                return "##comment"
            if line[:2] == "<<":
                self.parse_instruction(line[2:-3])
                return "##instruction"
            if line[0] == "[":
                self.variables.update({"current_speaker": line[1:-2]})
                return "##speaker_set"
            if line == "\n":
                self.paused = True
                return "##paused"
            else:
                self.variables["current_line"] = line[:-1]
                return line[:-1]
        else:
            return "##paused"


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

"""
a = Scripting()
with open("data/script/dialogue/001_RinaConsta_TEST.dia") as f:
   content = f.readlines()
#content = [x.strip() for x in content]
content = collections.deque(content)
initial = True
item = ""
while 1:
    if initial:
        item = content.popleft()
        initial = False
    if not(a.parse_line(item) == "##paused"):
        item = content.popleft()
    else:
        pass
"""

class Game(ezpygame.Scene):
    def __init__(self):
        super().__init__()
        pygame.font.init()
        self.font = pygame.font.Font("data/foo.ttf", 32)
        self.scripting = Scripting()
        self.dialogue = collections.deque()
        with open("data/script/dialogue/001_RinaConsta_TEST.dia") as f:
            self.dialogue = collections.deque(f.readlines())
        self.script_line = self.dialogue.popleft()
        self.test_bg = load_png("data/menu_bg02.png")[0].convert_alpha()

    def darken(self, surf):
        surface = pygame.Surface((surf.get_width(), surf.get_height()), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 150))
        surface.blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return surface

    def draw(self, screen):
        #TODO port to DialoueBox class with transparency, update() handling and animations
        screen.fill((0, 0, 0))
        screen.blit(self.test_bg, (0, 0))
        if self.scripting.paused:
            cur_speaker = self.scripting.variables["current_speaker"]
            cur_speaker_rendered = self.font.render(self.scripting.variables[cur_speaker].name, True, (255, 255, 255))
            line = self.font.render(self.scripting.variables["current_line"], True, (255, 255, 255))
            dialogue_box = pygame.Surface((self.application.resolution[0], self.application.resolution[1]-250))
            dialogue_box.fill((0, 0, 0))
            name1_img = self.scripting.variables["name1"].current_image
            name2_img = self.scripting.variables["name2"].current_image
            if cur_speaker == "name1":
                name2_img = self.darken(name2_img)
            if cur_speaker == "name2":
                name1_img = self.darken(name1_img)
            if self.scripting.variables["name1"].visibility:
                if self.scripting.variables["name1"].side == "left":
                    screen.blit(name1_img, (50,200))
                if self.scripting.variables["name1"].side == "right":
                    screen.blit(name1_img, (self.application.resolution[0]-300, 200))
                #add middle
            if self.scripting.variables["name2"].visibility:
                if self.scripting.variables["name2"].side == "left":
                    screen.blit(name2_img, (50,200))
                if self.scripting.variables["name2"].side == "right":
                    screen.blit(name2_img, (self.application.resolution[0]-300, 200))
                #add middle
            screen.blit(dialogue_box, (0, self.application.resolution[1] - 250))
            screen.blit(cur_speaker_rendered, (50, self.application.resolution[1]-250))
            screen.blit(line, (50, self.application.resolution[1]-(250-64)))
        pass

    def update(self, dt):
        result = self.scripting.parse_line(self.script_line)
        if result == "##paused":
            pass
        else:
            self.script_line = self.dialogue.popleft()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Trying to upause")
                self.scripting.paused = False
                self.script_line = self.dialogue.popleft()
        pass

    def on_enter(self, previous_scene=None):
        pass

    def on_exit(self, next_scene=None):
        pass




app = ezpygame.Application(
    title="Daoimen",
    resolution=(1280, 720),
    update_rate=60
)

app.run(Game())
