import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 10
FPS = 10

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)

# Snake Class
class Snake:
    def __init__(self):
        self.body = [(300, 200), (290, 200), (280, 200)]
        self.direction = (CELL_SIZE, 0)
    
    def move(self):
        head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        head = (head[0] % WIDTH, head[1] % HEIGHT)  # Wrap around screen
        self.body.insert(0, head)
        self.body.pop()
    
    def change_direction(self, key):
        if key == pygame.K_UP and self.direction != (0, CELL_SIZE):
            self.direction = (0, -CELL_SIZE)
        elif key == pygame.K_DOWN and self.direction != (0, -CELL_SIZE):
            self.direction = (0, CELL_SIZE)
        elif key == pygame.K_LEFT and self.direction != (CELL_SIZE, 0):
            self.direction = (-CELL_SIZE, 0)
        elif key == pygame.K_RIGHT and self.direction != (-CELL_SIZE, 0):
            self.direction = (CELL_SIZE, 0)
    
    def grow(self):
        self.body.append(self.body[-1])
    
    def check_collision(self, obj):
        if isinstance(obj, Fruit):
            return self.body[0] == obj.position
        elif isinstance(obj, Obstacles):
            return any(segment in obj.positions for segment in self.body)
        return False
    
    def check_self_collision(self):
        return self.body[0] in self.body[1:]
    
    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, BLUE, (*segment, CELL_SIZE, CELL_SIZE))

# Fruit Class
class Fruit:
    def __init__(self):
        self.position = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE, random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
    
    def reposition(self):
        self.position = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE, random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
    
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (*self.position, CELL_SIZE, CELL_SIZE))

# Obstacles Class
class Obstacles:
    def __init__(self):
        self.positions = []
        self.directions = []
        self.max_obstacles = 3  # Initial number of obstacle groups
        self.spawn_obstacles()
    
    def spawn_obstacles(self):
        self.positions = []
        self.directions = []
        for _ in range(self.max_obstacles):
            base_x = random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE
            base_y = random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE
            direction = random.choice([(CELL_SIZE, 0), (0, CELL_SIZE)])
            for i in range(3):
                self.positions.append((base_x + i * direction[0], base_y + i * direction[1]))
                self.directions.append(random.choice([(CELL_SIZE, 0), (-CELL_SIZE, 0), (0, CELL_SIZE), (0, -CELL_SIZE)]))
    
    def increase_obstacles(self):
        """Increases the number of obstacles to make the game progressively harder."""
        self.max_obstacles += 1
        self.spawn_obstacles()
    
    def move(self):
        for i in range(len(self.positions)):
            x, y = self.positions[i]
            dx, dy = self.directions[i]
            new_x = (x + dx) % WIDTH
            new_y = (y + dy) % HEIGHT
            self.positions[i] = (new_x, new_y)
    
    def draw(self, screen):
        for pos in self.positions:
            pygame.draw.rect(screen, GRAY, (*pos, CELL_SIZE, CELL_SIZE))

# Game Class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.score = 0
        self.dirt_trail = []  # Store all dirt trail positions with fade timers
        self.score_animation_timer = 0
    
    def start_menu(self):
        clouds = self.generate_clouds(10)
        while True:
            self.screen.fill(SKY_BLUE)
            # Draw clouds
            for cloud in clouds:
                pygame.draw.ellipse(self.screen, WHITE, cloud)
            
            # Render large pixelated "START GAME" text
            font = pygame.font.Font(None, 72)
            text = font.render("START GAME", True, BLACK)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return
    
    def generate_clouds(self, num_clouds):
        clouds = []
        for _ in range(num_clouds):
            x = random.randint(0, WIDTH - 100)
            y = random.randint(0, HEIGHT // 2)
            cloud_width = random.randint(50, 100)
            cloud_height = random.randint(20, 50)
            clouds.append(pygame.Rect(x, y, cloud_width, cloud_height))
        return clouds
    
    def run(self):
        self.start_menu()
        self.snake = Snake()
        self.fruit = Fruit()
        self.obstacles = Obstacles()
        while self.running:
            self.handle_events()
            if not self.paused:
                self.update()
            self.draw()
            self.clock.tick(FPS)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                else:
                    self.snake.change_direction(event.key)
    
    def update(self):
        self.snake.move()
        self.obstacles.move()
        if self.snake.check_collision(self.fruit):
            self.snake.grow()
            self.fruit.reposition()
            self.score += 1  # Increase score when snake eats a fruit
            self.score_animation_timer = 10  # Start score animation timer
            # Increase obstacles every 3 points
            if self.score % 3 == 0:
                self.obstacles.increase_obstacles()
        if self.snake.check_collision(self.obstacles) or self.snake.check_self_collision():
            self.running = False  # End game if snake hits an obstacle or itself
        # Add the snake's current position to the dirt trail
        self.dirt_trail.append((self.snake.body[-1], 255))  # Leave dirt trail at full opacity
    
    def draw(self):
        # Fill the screen with green (grass)
        self.screen.fill(GREEN)
        
        # Draw the dirt trail
        new_trail = []
        for pos, alpha in self.dirt_trail:
            surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
            surface.set_alpha(alpha)
            surface.fill(BROWN)
            self.screen.blit(surface, pos)
            # Decrease opacity and keep only those still visible
            if alpha > 10:
                new_trail.append((pos, alpha - 10))
        self.dirt_trail = new_trail
        
        # Draw the snake, fruit, and obstacles
        self.snake.draw(self.screen)
        self.fruit.draw(self.screen)
        self.obstacles.draw(self.screen)
        
        # Draw the score with animation effect
        font_size = 24 + (5 if self.score_animation_timer > 0 else 0)  # Increase font size during animation
        font = pygame.font.Font(None, font_size)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Decrease the animation timer
        if self.score_animation_timer > 0:
            self.score_animation_timer -= 1
        
        # If paused, display the "PAUSED" text and dim the background
        if self.paused:
            # Dim the screen with a translucent black overlay
            dim_overlay = pygame.Surface((WIDTH, HEIGHT))
            dim_overlay.set_alpha(128)  # Set transparency level
            dim_overlay.fill(BLACK)
            self.screen.blit(dim_overlay, (0, 0))
            
            # Display "PAUSED" text
            font = pygame.font.Font(None, 72)
            paused_text = font.render("PAUSED", True, WHITE)
            self.screen.blit(paused_text, (WIDTH // 2 - paused_text.get_width() // 2, HEIGHT // 2))
        
        pygame.display.flip()

# Main Function
if __name__ == "__main__":
    game = Game()
    game.run()

pygame.quit()
