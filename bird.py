import pygame
import os

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5


    def __init__(self, x, y): 
        """Initializes the bird object with its starting position and other attributes."""
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]


    def jump(self):
        """Makes the bird jump by setting its initial upward velocity."""
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """Calculates the bird's new position based on its velocity and gravity."""
        self.tick_count += 1

        # Calculate displacement considering gravity
        displacement = self.vel * self.tick_count + 1.5 * self.tick_count**2
        displacement = min(displacement, 16)                # Limit maximum downward movement
        if displacement < 0:                                # Limit upward movement
            displacement -= 2

        self.y = self.y + displacement


        if displacement < 0 or self.y < self.height + 50: # Bird is moving upward - Tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:                                             # Bird is moving downward - Tilt down
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY



    def draw(self, win):
        """Draws the bird on the game window with the appropriate image and rotation."""
        self.img_count += 1

        # Animate bird based on a timer
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # Animate bird without flapping while nosediving
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # Rotate around centet based on tilt angle
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rec = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rec.topleft)

    def get_mask(self):
        """Returns a collision mask for the bird object."""
        return pygame.mask.from_surface(self.img)