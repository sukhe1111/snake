import pygame
import random

# Initialize pygame
pygame.init()

# Set up the display
width = 600
height = 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game - Food Section")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake and food block size
block_size = 20

# Food class
class Food:
    def __init__(self):
        self.x = random.randrange(0, width - block_size, block_size)
        self.y = random.randrange(0, height - block_size, block_size)

    def spawn_food(self):
        """Randomly place food on the screen."""
        self.x = random.randrange(0, width - block_size, block_size)
        self.y = random.randrange(0, height - block_size, block_size)

    def draw_food(self):
        """Draw the food on the screen."""
        pygame.draw.rect(win, RED, (self.x, self.y, block_size, block_size))

# Main game loop (for testing purposes)
def game_loop():
    clock = pygame.time.Clock()
    food = Food()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.fill(BLACK)  # Fill screen with black
        food.draw_food()  # Draw food on screen
        pygame.display.update()  # Update display

        clock.tick(15)  # Control the game speed

    pygame.quit()

# Run the game loop
game_loop()
