import pygame
import os

# Load and scale the base image
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))

class Base:
    # Class variables for the base's velocity and width, and the image itself
    VEL = 5  # Speed at which the base moves to the left
    WIDTH = BASE_IMG.get_width()  # Width of the base image
    IMG = BASE_IMG  # The base image that will be drawn

    def __init__(self, y):
        """Initializes the base with a starting vertical position (y-coordinate)."""
        self.y = y  # The y-coordinate where the base is drawn
        self.x1 = 0  # The starting x-coordinate for the first base image
        self.x2 = self.WIDTH  # The starting x-coordinate for the second base image (placed right after the first)

    def move(self):
        """Moves the base images to the left, creating a continuous scrolling effect."""
        self.x1 -= self.VEL  # Move the first base image to the left
        self.x2 -= self.VEL  # Move the second base image to the left

        # Check if the first base image has completely moved off-screen
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH  # Move it to the right, right after the second base image
        
        # Check if the second base image has completely moved off-screen
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH  # Move it to the right, right after the first base image

    def draw(self, win):
        """Draws the base on the game window."""
        # Draw the first base image
        win.blit(self.IMG, (self.x1, self.y))
        # Draw the second base image
        win.blit(self.IMG, (self.x2, self.y))
