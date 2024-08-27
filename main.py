import pygame
import random
import neat
import os

pygame.font.init()

# Import custom classes for the game elements
from bird import Bird
from base import Base
from pipe import Pipe

# Constants for the game window dimensions
WIN_WIDTH = 500
WIN_HEIGHT = 800

GEN = 0  # Global variable to track the number of generations

# Load and scale the background image
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# Initialize the font for displaying the score and generation
STAT_FONT = pygame.font.SysFont("comicsans", 40)

def draw_window(win, birds, pipes, base, score, gen):
    """
    Draws the game window, including the background, pipes, base, birds, and score.
    
    Parameters:
    win (Surface): The game window surface to draw on.
    birds (list): List of Bird objects representing the birds in the game.
    pipes (list): List of Pipe objects representing the pipes in the game.
    base (Base): The Base object representing the moving base at the bottom of the screen.
    score (int): The current score in the game.
    gen (int): The current generation of birds.
    """
    win.blit(BG_IMG, (0, 0))  # Draw the background

    for pipe in pipes:
        pipe.draw(win)  # Draw each pipe

    # Render and display the score
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    # Render and display the generation count
    text = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    base.draw(win)  # Draw the base

    for bird in birds:
        bird.draw(win)  # Draw each bird

    pygame.display.update()  # Update the display

def process_events():
    """
    Processes Pygame events. Handles quitting the game.
    
    Returns:
    bool: True if the game should continue running, False if it should quit.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Handle quitting the game
            pygame.quit()
            quit()
    return True

def evaluate_birds(birds, pipes, nets, ge):
    """
    Evaluates the birds' positions and actions based on their neural network outputs.
    
    Parameters:
    birds (list): List of Bird objects representing the birds in the game.
    pipes (list): List of Pipe objects representing the pipes in the game.
    nets (list): List of neural networks controlling each bird.
    ge (list): List of genome objects associated with each bird.
    
    Returns:
    bool: True if the game should continue running, False if all birds are dead.
    """
    pipe_ind = 0
    if len(birds) > 0:
        if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1  # Use the second pipe if the first one is passed
    else:
        return False  # End the loop if all birds are dead

    for x, bird in enumerate(birds):
        bird.move()  # Move the bird
        ge[x].fitness += 0.1  # Reward the bird for staying alive

        # Activate the neural network for the bird and get the output
        output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

        if output[0] > 0.5:  # If the output suggests a jump, make the bird jump
            bird.jump()

    return True

def handle_pipe_collisions(birds, pipes, nets, ge):
    """
    Handles pipe collisions and updates bird status accordingly.
    
    Parameters:
    birds (list): List of Bird objects representing the birds in the game.
    pipes (list): List of Pipe objects representing the pipes in the game.
    nets (list): List of neural networks controlling each bird.
    ge (list): List of genome objects associated with each bird.
    
    Returns:
    bool: True if a new pipe should be added, False otherwise.
    """
    add_pipe = False
    rem = []  # List to keep track of pipes that need to be removed

    for pipe in pipes:
        for x, bird in enumerate(birds):
            if pipe.collide(bird):  # Check if the bird has collided with a pipe
                ge[x].fitness -= 1  # Penalize the bird's fitness for colliding
                birds.pop(x)  # Remove the bird from the list
                nets.pop(x)  # Remove the bird's neural network
                ge.pop(x)  # Remove the bird's genome

            # Check if the bird has passed the pipe
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True  # Mark the pipe as passed
                add_pipe = True  # Flag to add a new pipe

        # Remove pipes that have moved off-screen
        if pipe.x + pipe.PIPE_TOP.get_width() < 0:
            rem.append(pipe)

        pipe.move()  # Move the pipe to the left

    for r in rem:
        pipes.remove(r)  # Remove off-screen pipes

    return add_pipe

def remove_dead_birds(birds, nets, ge):
    """
    Removes birds that have collided with the ground or flown too high.
    
    Parameters:
    birds (list): List of Bird objects representing the birds in the game.
    nets (list): List of neural networks controlling each bird.
    ge (list): List of genome objects associated with each bird.
    """
    for x, bird in enumerate(birds):
        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            birds.pop(x)  # Remove the bird from the list
            nets.pop(x)  # Remove the bird's neural network
            ge.pop(x)  # Remove the bird's genome

def main(genomes, config):
    """
    The main function where the game loop runs. It handles bird movement, pipe creation,
    collision detection, scoring, and NEAT algorithm integration.
    
    Parameters:
    genomes (list): List of genomes provided by NEAT for evaluation.
    config (Config): NEAT configuration object.
    """
    global GEN
    GEN += 1  # Increment the generation count at the start of each run
    nets = []  # List to hold the neural networks for each bird
    ge = []  # List to hold the genome objects for each bird
    birds = []  # List to hold the Bird objects

    for _, g in genomes:
        # Create a neural network for each genome using the NEAT config
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))  # Start each bird at a fixed position
        g.fitness = 0  # Initialize the fitness score for each genome
        ge.append(g)

    base = Base(730)  # Create the base object at the bottom of the screen
    pipes = [Pipe(600)]  # Create the first pipe with an initial x position
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # Set up the game window
    clock = pygame.time.Clock()  # Create a clock object to control the game speed

    score = 0  # Initialize the game score
    run = True  # Variable to control the main game loop

    while run:
        clock.tick(30)  # Limit the game loop to 30 ticks per second
        run = process_events()  # Process events and check if the game should continue

        # Evaluate the birds' actions and movement
        if not evaluate_birds(birds, pipes, nets, ge):
            break  # End the loop if all birds are dead

        # Handle pipe collisions and determine if a new pipe should be added
        if handle_pipe_collisions(birds, pipes, nets, ge):
            score += 1  # Increment the score
            for g in ge:
                g.fitness += 5  # Reward the birds for successfully passing a pipe
            pipes.append(Pipe(600))  # Add a new pipe

        remove_dead_birds(birds, nets, ge)  # Remove birds that have hit the ground or flown too high

        base.move()  # Move the base to create a scrolling effect
        draw_window(win, birds, pipes, base, score, GEN)  # Draw the game window

def run(config_path):
    """
    Sets up the NEAT algorithm and runs the simulation.
    
    Parameters:
    config_path (str): Path to the NEAT configuration file.
    """
    # Load the NEAT configuration from the provided file path
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, 
                                config_path)
    
    # Create a population based on the configuration
    p = neat.Population(config)

    # Add reporters to show progress in the console
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run the simulation for up to 50 generations
    winner = p.run(main, 50)

if __name__ == "__main__":
    # Get the path to the configuration file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)  # Run the NEAT algorithm
