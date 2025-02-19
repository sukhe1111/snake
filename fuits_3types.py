import pygame
import random
import time  # Import time to handle the timer

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)  # Color for the speed-up food
YELLOW = (255, 255, 0)  # Color for the regular food
ORANGE = (255, 165, 0)  # Color for the slow-down food
BLUE = (50, 153, 213)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Clock for controlling game speed
clock = pygame.time.Clock()

# Snake and food class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = (0, -BLOCK_SIZE)
        self.color = BLACK
        self.base_speed = 15  # Initial speed
        self.speed = self.base_speed  # Default speed
        self.score = 0
        self.boost_end_time = 0  # To track when the speed boost ends
        self.slow_end_time = 0  # To track when the slow effect ends

    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        self.positions.insert(0, new_head)
        self.positions.pop()

    def grow(self):
        self.length += 1
        self.score += 1

    def accelerate(self):
        self.speed = self.base_speed + 5  # Increase speed by 5
        self.boost_end_time = time.time() + 3  # Speed boost lasts for 3 seconds

    def slow_down(self):
        self.speed = self.base_speed - 5  # Decrease speed by 5
        self.slow_end_time = time.time() + 3  # Slow down effect lasts for 3 seconds

    def update_speed(self):
        # Reset speed if boost has expired
        if time.time() > self.boost_end_time:
            self.speed = self.base_speed

        # Reset speed if slow effect has expired
        if time.time() > self.slow_end_time:
            self.speed = self.base_speed

    def draw(self):
        for pos in self.positions:
            pygame.draw.rect(screen, self.color, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

# Food class
class Food:
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.position = (random.randrange(1, (SCREEN_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                         random.randrange(1, (SCREEN_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE)

    def randomize_position(self):
        self.position = (random.randrange(1, (SCREEN_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                         random.randrange(1, (SCREEN_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE)

    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# Main game function
def game_loop():
    game_over = False
    snake = Snake()
    food_regular = Food(YELLOW, 1)  # Regular food (yellow) that adds 1 point
    food_boost = Food(GREEN, 3)  # Green food that accelerates the snake and gives 3 points
    food_slow = Food(ORANGE, 2)  # Orange food that slows down the snake and gives 2 points

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.direction = (-BLOCK_SIZE, 0)
                elif event.key == pygame.K_RIGHT:
                    snake.direction = (BLOCK_SIZE, 0)
                elif event.key == pygame.K_UP:
                    snake.direction = (0, -BLOCK_SIZE)
                elif event.key == pygame.K_DOWN:
                    snake.direction = (0, BLOCK_SIZE)

        # Move the snake
        snake.move()

        # Check for collision with regular food
        if snake.positions[0] ==
