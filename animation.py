import pygame
import ezpygame
import os

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

def load_images(directory):
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
        self.images = images[:-1]
        self.index = 0
        self.image = images[self.index]  # 'image' is the current image of the sprite.
        print(len(self.images))

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

    def add(self, sprite, level, unique_id=False):
        id = str(hex(self.counter))
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

class Test(ezpygame.Scene):
    def __init__(self):
        super().__init__()
        self.animation_queue = SpriteQueue()
        self.animation_queue.add(Sprite((50, 50), images=load_images("data/anim/300"), time=100, one_time=False, start_frame=7), 1)
        self.animation_queue.add(Sprite((200, 50), images=load_images("data/anim/300"), time=100, one_time=False, start_frame=3), 1)
        self.animation_queue.add(Sprite((0, 0), images=load_images("data/anim/300"), time=100, one_time=False), 1)
        #self.animation = Sprite((50, 50), images=load_images("data/anim/300"), time=100, one_time=True)
        print(self.animation_queue.level1.keys())

    def update(self, dt):
        self.animation_queue.update(dt)
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.animation_queue.draw(screen)
        #screen.blit(self.animation.image, self.animation.rect)
        pass

app = ezpygame.Application(
    title="Test",
    resolution=(250, 250),
    update_rate=60
)

app.run(Test())