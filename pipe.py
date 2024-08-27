import pygame
import os
import random

# Load and scale the pipe image
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))

class Pipe:
    # Class variables defining the gap size between pipes and their velocity
    GAP = 200  # Vertical space between the top and bottom pipes
    VEL = 5    # Horizontal speed at which the pipes move leftward

    def __init__(self, x):
        """Initializes the pipe with a given x position."""
        self.x = x  # The x-coordinate where the pipe is drawn
        self.height = 0  # Placeholder for pipe height, to be set later

        # Define the top and bottom positions of the pipes (will be calculated)
        self.top = 0
        self.bottom = 0

        # Load and store the pipe images, flipping the top pipe vertically
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)  # Flipped image for the top pipe
        self.PIPE_BOTTOM = PIPE_IMG  # Image for the bottom pipe

        self.passed = False  # Flag to check if the bird has passed this pipe
        self.set_height()  # Set the initial height for the pipes

    def set_height(self):
        """Sets the height of the top and bottom pipes, creating a random gap."""
        self.height = random.randrange(50, 450)  # Randomly determine the height of the gap
        self.top = self.height - self.PIPE_TOP.get_height()  # Calculate the top pipe position
        self.bottom = self.height + self.GAP  # Calculate the bottom pipe position

    def move(self):
        """Moves the pipe to the left by reducing its x-coordinate."""
        self.x -= self.VEL  # Move the pipe left by its velocity

    def draw(self, win):
        """Draws the top and bottom pipes on the game window."""
        # Draw the top pipe at the calculated top position
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # Draw the bottom pipe at the calculated bottom position
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        """
        Checks for a collision between the pipe and the bird.
        Uses pixel-perfect collision detection.
        """
        bird_mask = bird.get_mask()  # Get the collision mask for the bird
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)  # Get the mask for the top pipe
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)  # Get the mask for the bottom pipe

        # Calculate the offsets between the bird and the pipes for collision checking
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # Check for overlap between the bird and the top pipe
        t_point = bird_mask.overlap(top_mask, top_offset)
        # Check for overlap between the bird and the bottom pipe
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)

        # If there is an overlap with either the top or bottom pipe, a collision has occurred
        if t_point or b_point:
            return True  # Collision detected

        return False  # No collision detected
