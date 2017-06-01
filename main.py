import os
import pygame
import ezpygame
import random
import math
from pprint import pprint



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

def load_png(directory, name):
    """
    Load image and return image object
    :param directory: 
    :param name: 
    """
    fullname = os.path.join(directory, name)
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

def blurSurf(surface, amt):
    """
    Blur the given surface by the given 'amount'.  Only values 1 and greater
    are valid.  Value 1 = no blur.
    """
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt)
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf



class Sprite:

    def __init__(self, pos, images, one_time=False, time=0.1, start_frame=0):
        """
        Animated sprite object.

        Args:
            pos: Position of the screen where Sprite should be placed at.
            images: Images to change between.
        """
        self.size = (images[0].get_width(), images[0].get_height())
        self.rect = pygame.Rect(pos, self.size)
        self.images = images
        self.index = 0
        self.image = images[self.index]  # 'image' is the current image of the sprite.
        #print(len(self.images))

        self.animation_time = 0
        self.time_between_frames = time
        self.current_time = start_frame

        #self.animation_frames = 6
        self.current_frame = 0

        self.one_time = one_time

    def get_frame(self):
        return self.images[self.current_frame]

    def update(self, dt):
        """
        Updates the image of Sprite

        Args:
            dt: Time since last call to update.

        Returns:
            None
        """
        if (self.one_time == True) and (len(self.images)-1 == self.index):
            return False
        try:
            self.current_time += dt/self.time_between_frames
        except ZeroDivisionError:
            self.current_time += dt/100
        self.index = int(self.current_time) % len(self.images)
        self.image = self.images[self.index]
        #print(int(self.current_time))
        #Finally fucking works

    def move(self, pos):
        self.rect = pygame.Rect(pos, self.size)


class SpriteQueue:
    def __init__(self):
        self.counter = 0
        self.level1 = {}
        self.level2 = {}
        self.level3 = {}

    def to_hex(self, i):
        return str(hex(int(i))[2:].zfill(8).upper())

    def add(self, sprite, level, unique_id=False):
        id = self.to_hex(self.counter)
        if type(unique_id) == str:
            id = unique_id
        if level == 1:
            self.level1.update({id: sprite})
        if level == 2:
            self.level2.update({id: sprite})
        if level == 3:
            self.level3.update({id: sprite})
        self.counter += 1
        return id

    def update(self, dt):
        """ 
        pop_em = []
        for key in self.level1.keys():
            print(key)
            if not(self.level1[key].update(dt)):
                pop_em += self.to_hex(key)
        for key in pop_em:
            try:
                self.level1.pop(self.to_hex(key))
            except KeyError:
                pass
        pop_em = []
        for key in self.level2.keys():
            if not(self.level2[key].update(dt)):
                pop_em += self.to_hex(key)
        for key in pop_em:
            try:
                self.level2.pop(self.to_hex(key))
            except KeyError:
                pass
        pop_em = []
        for key in self.level3.keys():
            if not(self.level3[key].update(dt)):
                pop_em += self.to_hex(key)
        for key in pop_em:
            try:
                self.level3.pop(self.to_hex(key))
            except KeyError:
                pass
        """
        for key in self.level1.keys():
            self.level1[key].update(dt)
        for key in self.level2.keys():
            self.level2[key].update(dt)
        for key in self.level3.keys():
            self.level3[key].update(dt)

    def draw(self, screen):
        for key in self.level1.keys():
            screen.blit(self.level1[key].image, self.level1[key].rect)
        for key in self.level2.keys():
            screen.blit(self.level2[key].image, self.level2[key].rect)
        for key in self.level3.keys():
            screen.blit(self.level3[key].image, self.level3[key].rect)


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


class FirstTimeRun:
    def __init__(self):
        self.timed = 500
        self.result = True
        self.hold_on = 0

    def update(self, dt):
        if float(self.hold_on) < self.timed:
            self.hold_on += dt
        if float(self.hold_on) >= self.timed:
            #print(self.hold_on, self.timed)
            self.result = False
        return self.result


class Game(ezpygame.Scene):

    def __init__(self):
        super().__init__()
        pygame.display.set_icon(load_png("data", "icon.png")[0])
        pygame.font.init()
        pygame.mixer.init()
        pygame.mixer.music.load("data/music/dj4real-clv-ovation-2-98.wav")
        pygame.mixer.music.play(-1)
        self.score = 0
        self.counter = 0
        self.rev_count = False
        self.grid_size = 8
        print("Initialized the game with "
              "\n\tCounter = %s"
              "\n\tReverse counter = %s"
              "\n\tGrid_size = %s" % (self.counter, self.rev_count, self.grid_size))
        self.resources = tuple(self.load_images("data/faces"))
        print("Resources loaded: len(%s)" % len(self.resources))
        self.mapp = []
        for i in range(8):
            line = 8 * [-1]
            self.mapp.append(line)
        self.generate_board()
        print("Generated board with")
        pprint(self.mapp)
        self.selection = Selection()
        self.font = pygame.font.Font("data/foo.ttf", 64)
        self.frame_image = load_png("data", "frame.png")[0]
        self.frame_image_selected = load_png("data", "frame_selected.png")[0]
        self.back_hovering = False
        self.back_rect = pygame.Rect(0, 0, 0, 0)
        self.first_run = FirstTimeRun()
        self.animation_queue = SpriteQueue()
        self.effect_300 = self.load_images("data/anim/300")
        #self.effect_300 = self.effect_300 + reversed(self.effect_300)

    def generate_board(self):
        """
        Walks mapp grid and rolls value from 0 to 3 for EVERY block.
        :return: 
        """
        self.score -= 1000
        for y in range(0, self.grid_size):
            for x in range(0, self.grid_size):
                self.mapp[y][x] = random.randint(0, len(self.resources)-2)

    def load_images(self, directory):
        """
        Loads images from the directory and returns unsorted(!) list of surfaces with Surface((1, 1)) at the end.
        :param directory: 
        :return: unsorted(!) list of surfaces with Surface((1, 1)) at the end
        """
        names = os.listdir(directory)
        #names = [f for f in os.listdir(directory) if os.path.isfile(f)]
        print("Loading images with"
              "\n\t%s" % names)
        d = []
        for name in names:
            d.append(load_png(directory, name)[0])
        d.append(pygame.Surface((1, 1)))
        return d

    def on_enter(self, previous_scene=None):
        self.previous_scene = previous_scene

    def fall_the_blocks(self):
        """
        Moves blocks from top to bottom until there's no possible walk down tree
        :return: 
        """
        fallen = True
        while True:
            for y in range(0, self.grid_size):
                for x in range(0, self.grid_size):
                    try:
                        if self.mapp[y][x] >= 0:
                            if self.mapp[y+1][x] == -1: # xd
                                temp = self.mapp[y][x]
                                self.mapp[y][x] = -1
                                self.mapp[y+1][x] = int(temp)  # prevent referencing
                                fallen = True
                            fallen = False
                    except IndexError:
                        pass
            if not fallen:
                break

    def swap(self, pos1, pos2):
        """
        Swaps two blocks
        DEBUG PURPOSES ONLY
        :param pos1: 
        :param pos2: 
        :return: 
        """
        block1 = int(self.mapp[pos1[1]][pos1[0]])
        block2 = int(self.mapp[pos2[1]][pos2[0]])
        self.mapp[pos1[1]][pos1[0]] = block2
        self.mapp[pos2[1]][pos2[0]] = block1

    def check_move(self, pos1, pos2):
        """
        Checks if move is valid and executes it.
        :param pos1: 
        :param pos2: 
        :return: 
        """
        print(pos1, pos2)
        print(abs(pos1[0] - pos2[0]))
        if (pos1[0] > 7) or (pos1[1] > 7) or (pos1[0] < 0) or (pos1[1] < 0):
            print("Outside grid [0]")
            return False
        if (pos2[0] > 7) or (pos2[1] > 7) or (pos2[0] < 0) or (pos2[1] < 0):
            print("Outside grid [1]")
            return False
        if abs(pos1[0] - pos2[0]) > 1:
            return False
        if abs(pos1[1] - pos2[1]) > 1:
            return False
        print("Tried to match")
        try:
            block1 = int(self.mapp[pos1[1]][pos1[0]])
            block2 = int(self.mapp[pos2[1]][pos2[0]])
        except IndexError:
            return False
        self.mapp[pos1[1]][pos1[0]] = block2
        self.mapp[pos2[1]][pos2[0]] = block1
        if not(self.check_matched()):
            self.mapp[pos1[1]][pos1[0]] = block1
            self.mapp[pos2[1]][pos2[0]] = block2
            print(False)
            return False
        print(True)
        return True

    def check_matched(self):
        """
        Checks if any blocks are matched and puts -1 (empty) values in their stead
        :return: 
            bool matched
        """
        """
        Possible states:
        a) x x x [x+](?)
        b) x
           x
           x
           [x+](?)
        """
        matched = False
        for y in range(0, self.grid_size):
            for x in range(0, self.grid_size):
                # vertical
                try:
                    if self.mapp[y][x] == -1:
                        continue
                    if (self.mapp[y][x] == self.mapp[y][x+1]) and (self.mapp[y][x] == self.mapp[y][x+2]):
                        self.animation_queue.add(Sprite(self.transform_to_pixels((x, y)), images=self.effect_300, time=50, one_time=True), 1)
                        type_ = int(self.mapp[y][x])
                        for i in range(0, 3):
                            self.mapp[y][x+i] = -1
                        matched = True
                        # found_more_matches = False
                        matches = []
                        i = 2
                        self.score += 300
                        while True:
                            i += 1
                            if type_ == self.mapp[y][x+i]:
                                # found_more_matches = True
                                matches += [(x+i, y)]
                            else:
                                # found_more_matches = False
                                break
                        if not(matches == []):
                            for pos in matches:
                                self.mapp[pos[1]][pos[0]] = -1
                            self.score += 300*len(matches)
                except IndexError:
                    pass
                # horizontal
                try:
                    if (self.mapp[y][x] == self.mapp[y+1][x]) and (self.mapp[y][x] == self.mapp[y+2][x]):
                        #print((x-1)*self.grid_size)
                        self.animation_queue.add(Sprite(self.transform_to_pixels((x, y)), images=self.effect_300, time=50, one_time=True), 1)
                        type_ = int(self.mapp[y][x])
                        for i in range(0, 3):
                            self.mapp[y+i][x] = -1
                        matched = True
                        # found_more_matches = False
                        matches = []
                        i = 2
                        self.score += 300
                        while True:
                            i += 1
                            if type_ == self.mapp[y+i][x]:
                                # found_more_matches = True
                                matches += [(x, y+i)]
                            else:
                                # found_more_matches = False
                                break
                        if not(matches == []):
                            for pos in matches:
                                self.mapp[pos[1]][pos[0]] = -1
                                self.score += 300 * len(matches)
                except IndexError:
                    pass
        return matched

    def generate_missing(self):
        """
        Walks down mapp grid and rolls value from 0 to 3 if block is equal to -1 (empty).
        :return: 
        """
        for y in range(0, self.grid_size):
            for x in range(0, self.grid_size):
                if self.mapp[y][x] == -1:
                    self.mapp[y][x] = random.randint(0, len(self.resources)-2)
                    self.mapp[y][x] = random.randint(0, len(self.resources)-2)

    def check_possible_states(self):
        """
        Walks down mapp grid and checks if there are possible moves
        :return: 
            number of possible moves
        """
        """
        Possible states:
        a) vertical
            - . x 
              x . 
              . x 

            - . x 
              x . 
              x . 

            - x .
              . x
              . x 

            - x . 
              . x
              x . 

            - x . 
              x . 
              . x

            - . x 
              . x
              x . 

        b) horizontal
            - x . x x

            - x x . x
        """
        possible_moves = 0
        possbible_moves_pos = []
        for y in range(0, self.grid_size):
            for x in range(0, self.grid_size):
                # check hor first since less
                try:
                    if self.mapp[y][x] == -1:
                        continue
                    if (self.mapp[y][x] == self.mapp[y][x+2]) and (self.mapp[y][x] == self.mapp[y][x+3]):
                        possible_moves += 1
                        possbible_moves_pos += [(x, y, 1)]
                    if (self.mapp[y][x] == self.mapp[y][x+1]) and (self.mapp[y][x] == self.mapp[y][x+3]):
                        possible_moves += 1
                        possbible_moves_pos += [(x, y, 2)]
                except IndexError:
                    pass
                try:
                    if (self.mapp[y][x] == self.mapp[y+1][x+1]) and (self.mapp[y][x] == self.mapp[y+2][x+1]):
                        if self.mapp[y][x] == -1:
                            continue
                        possible_moves += 1
                        possbible_moves_pos += [(x, y, 3)]
                    if (self.mapp[y][x] == self.mapp[y+1][x+1]) and (self.mapp[y][x] == self.mapp[y][x+2]):
                        if self.mapp[y][x] == -1:
                            continue
                        possible_moves += 1
                        possbible_moves_pos += [(x, y, 4)]
                    if (self.mapp[y][x] == self.mapp[y+1][x]) and (self.mapp[y][x] == self.mapp[y+2][x+1]):
                        if self.mapp[y][x] == -1:
                            continue
                        possible_moves += 1
                        possbible_moves_pos += [(x, y, 5)]
                    if (self.mapp[y][x+1] == self.mapp[y+1][x]) and (self.mapp[y][x+1] == self.mapp[y+2][x+1]):
                        if self.mapp[y][x+1] == -1:
                            continue
                        possible_moves += 1
                        possbible_moves_pos += [(x, y, 6)]
                    if (self.mapp[y][x+1] == self.mapp[y+1][x]) and (self.mapp[y][x+1] == self.mapp[y+2][x]):
                        if self.mapp[y][x+1] == -1:
                            continue
                        possible_moves += 1
                        possbible_moves_pos += [(x, y, 7)]
                    if (self.mapp[y][x+1] == self.mapp[y+1][x+1]) and (self.mapp[y][x+1] == self.mapp[y+2][x]):
                        if self.mapp[y][x+1] == -1:
                            continue
                        possible_moves += 1
                        possbible_moves_pos += [(x, y, 8)]
                except IndexError:
                    pass
        return possible_moves
        # print(possible_moves)
        # pprint(possbible_moves_pos)

    @staticmethod
    def transform_to_grid(pos, grid_size=64):
        """
        Transforms reverse cartesian coordinates to grid coordinates.
        :param pos: 
        :param grid_size: 
        :return: 
        """
        x = pos[0]
        y = pos[1]
        # print(math.ceil((x-100)/64)-1, math.ceil((y-100)/64)-1)
        return math.ceil((x - 100) / grid_size - 1), math.ceil((y - 100) / grid_size - 1)

    @staticmethod
    def transform_to_pixels(pos, grid_size=64):
        """
        Transforms grid coordinates to reverse cartesian coordinates.
        :param pos:
        :param grid_size:
        :return:
        """
        x = pos[0]
        y = pos[1]
        return math.ceil(x*(grid_size+1))+100, math.ceil(y*(grid_size+1))+100

    def on_exit(self, next_scene=None):
        pygame.mixer.fadeout(250)

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if isPointInsideRect(mouse_pos[0], mouse_pos[1], self.back_rect):
            self.back_hovering = True
        else:
            self.back_hovering = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.animation_queue.add(
                    Sprite(mouse_pos, images=self.load_images("data/anim/300"), time=50, one_time=False), 1)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = self.transform_to_grid(mouse_pos)
            if isPointInsideRect(mouse_pos[0], mouse_pos[1], self.back_rect):
                self.application.change_scene(self.previous_scene)
            if (pos[0] > 7) or (pos[1] > 7) or (pos[0] < 0) or (pos[1] < 0):
                print("Outside grid [3]")
                return False
            else:
                self.selection.add_pos(pos)
            # print(pygame.mouse.get_pos())
            if self.selection.check_ready():
                # self.swap(self.transform_to_grid(self.selection.pos1),
                #          self.transform_to_grid(self.selection.pos2))
                self.check_move(self.selection.pos1,
                                self.selection.pos2)
                self.selection.after_process()

    def update(self, dt):
        states = self.check_possible_states()
        if states < 1:
            self.generate_board()
        self.check_matched()
        # for i in range(7):
        self.fall_the_blocks()
        self.generate_missing()
        if self.first_run.update(dt):
            self.score = 0
        self.animation_queue.update(dt)

    def draw(self, screen):
        if not self.rev_count:
            self.counter += 0.5
        if self.rev_count:
            self.counter -= 0.5
        if self.counter == 54:
            self.rev_count = True
        if self.counter == 0:
            self.rev_count = False
        color_r = self.counter % 55
        color_g = self.counter % 55 - 10
        color_b = self.counter % 55 - 10
        screen.fill((200+color_r, 150+color_g, 150+color_b))
        start_pos = (100, 100)
        grid_size = 64
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                screen.blit(pygame.transform.scale(self.resources[self.mapp[y][x]],
                                                   (grid_size, grid_size)),
                            (start_pos[0]+x*grid_size, start_pos[1]+y*grid_size))
                screen.blit(self.frame_image, ((start_pos[0]-4)+x*grid_size, (start_pos[1]-4)+y*grid_size))
        if not((self.selection.pos1[0] == -1) and (self.selection.pos1[1] == -1)):
            screen.blit(self.frame_image_selected, ((start_pos[0]-4)+self.selection.pos1[0]*grid_size, (start_pos[1]-4)+self.selection.pos1[1]*grid_size))
        bg_score = pygame.Surface((len(str(self.score))*(52), 96), flags=pygame.HWSURFACE)
        bg_score.fill((255, 255, 255))
        bg_score = pygame.transform.rotozoom(bg_score.convert_alpha(), 5 - (self.counter % 55)/4, 1.0 - (self.counter % 55)/500)
        screen.blit(blurSurf(bg_score, 1.01), (start_pos[0]+(8*64)+100-(len(str(self.score))*(32))/4, 90))
        score = self.font.render("%s" % self.score, True, (0, 0, 0))
        score = pygame.transform.rotozoom(score, 5 - (self.counter % 55)/4, 1.0 - (self.counter % 55)/500)
        screen.blit(score, (start_pos[0]+(8*64)+100, 100))

        bg_back = pygame.Surface((len("BACK")*52, 80), flags=pygame.HWSURFACE)
        self.back_rect = pygame.Rect(start_pos[0]+(8*64)+100-(len(str("BACK"))*(52))/4, 720-90, len("BACK")*52, 80)
        bg_back.fill((255, 255, 255))
        back = self.font.render("BACK", True, (0, 0, 0))
        if self.back_hovering:
            bg_back = pygame.transform.rotozoom(bg_back.convert_alpha(), (int(55/2) - (self.counter % 55))/4, 1.0 - (self.counter % 55) / 500)
            back = pygame.transform.rotozoom(back.convert_alpha(), (int(55/2) - (self.counter % 55))/4, 1.0 - (self.counter % 55) / 500)
        else:
            pass
        screen.blit(bg_back, (start_pos[0]+(8*64)+100-(len(str("BACK"))*(52))/4, 720-90))
        screen.blit(back, (start_pos[0]+(8*64)+100-(len(str("BACK"))*(52)/8), 720-90))
        self.animation_queue.draw(screen)


class Menu(ezpygame.Scene):

    def __init__(self):
        super().__init__()
        pygame.display.set_icon(load_png("data", "icon.png")[0])
        pygame.font.init()
        pygame.mixer.init()
        self.font = pygame.font.Font("data/foo.ttf", 64)
        self.menu_bg = load_png("data", "menu_bg02.png")[0]
        self.title = load_png("data", "title.png")[0]
        self.start_rect = pygame.Rect(0, 0, 0, 0)
        self.hovering_start = False
        self.exit_rect = pygame.Rect(0, 0, 0, 0)
        self.hovering_exit = False
        self.counter = 0
        self.rev_count = False
        self.debug = False

    def update(self, dt):
        if not self.rev_count:
            self.counter += 0.5
        if self.rev_count:
            self.counter -= 0.5
        if self.counter == 54:
            self.rev_count = True
        if self.counter == 0:
            self.rev_count = False

    def on_enter(self, previous_scene=None):
        pygame.mixer.music.load("data/music/eendee-eendeestrings-free3.wav")
        pygame.mixer.music.play(-1)

    def on_exit(self, next_scene=None):
        pygame.mixer.fadeout(250)

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if isPointInsideRect(mouse_pos[0], mouse_pos[1], self.start_rect):
            self.hovering_start = True
        else:
            self.hovering_start = False
        if isPointInsideRect(mouse_pos[0], mouse_pos[1], self.exit_rect):
            self.hovering_exit = True
        else:
            self.hovering_exit = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if isPointInsideRect(mouse_pos[0], mouse_pos[1], self.start_rect):
                self.application.change_scene(Game())
            if isPointInsideRect(mouse_pos[0], mouse_pos[1], self.exit_rect):
                os._exit(-1)
        pass

    def draw(self, screen):
        #screen.blit(pygame.transform.smoothscale(self.menu_bg, (1280, 720)), (0,0))
        screen.blit(self.menu_bg, (0, 0))
        """
        start = self.font.render("START", True, (0, 0, 0))
        start_rect = start.get_rect(center=(1280/2, 500))
        exit = self.font.render("EXIT", True, (0, 0, 0))
        exit_rect = start.get_rect(center=(1280/2 + 48/2+3, 500+8+64))
        if self.hovering_start:
            screen.blit(pygame.transform.rotozoom(blurSurf(start, 5), (int(55/2) - (self.counter%55))/4, 1.0 - (self.counter % 55)/500), start_rect)
        else:
            screen.blit(blurSurf(start, 5), start_rect)
        if self.hovering_exit:
            screen.blit(pygame.transform.rotozoom(blurSurf(exit, 5), (int(55/2) - (self.counter % 55))/4, 1.0 - (self.counter % 55) / 500), exit_rect)
        else:
            screen.blit(blurSurf(exit, 5), exit_rect)
        """
        start = self.font.render("START", True, (255, 255, 255))
        start_rect = start.get_rect(center=(1280 / 2, 500))
        exit = self.font.render("EXIT", True, (255, 255, 255))
        exit_rect = start.get_rect(center=(1280 / 2 + 48/2+3, 500 + 8 + 64))
        if self.hovering_start:
            screen.blit(pygame.transform.rotozoom(start, (int(55/2) - (self.counter % 55))/4, 1.0 - (self.counter % 55) / 500),
                start_rect)
        else:
            screen.blit(start, start_rect)
        if self.hovering_exit:
            screen.blit(pygame.transform.rotozoom(exit, (int(55/2) - (self.counter % 55))/4, 1.0 - (self.counter % 55) / 500),
                        exit_rect)
        else:
            screen.blit(exit, exit_rect)

        title_rect = self.title.get_rect(center=(1280/2, 150))
        screen.blit(self.title, title_rect)

        self.start_rect = start_rect
        self.exit_rect = exit_rect

        if self.debug:
            pygame.draw.rect(screen, (255, 0, 0), start_rect, 1)
            pygame.draw.rect(screen, (255, 0, 0), exit_rect, 1)
        pass



app = ezpygame.Application(
    title="Daoimen",
    resolution=(1280, 720),
    update_rate=60
)

app.run(Menu())
