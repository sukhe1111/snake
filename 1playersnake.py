# %% [markdown]
# ### Pygame Example

# %% [markdown]
# #### 0. 예제 설명(Introduction)
# Pygame은 쉽게 Game을 제작할 수 있도록 만들어진 module의 집합입니다.
# Python과 제공되는 간단한 몇가지의 함수만을 사용하여 실제로 구동할 수 있는 수준으로 만들 수 있습니다.
# 자세한 사항은 [Pygame Homepage](https://www.pygame.org/)를 참조해주세요.
#
# Pygame is a set of python module for writing game easliy.
# This allows you to create fully featured games and multimedia programs in the python language.
# You can see more details in [Pygame Homepage](https://www.pygame.org/).

# %% [markdown]
# ##### 0-1. 사전 준비(prerequirements)
# Pygame을 사용하기 위해 `pip`를 통한 pygame library를 설치합니다.
# 이 코드는 시작 후 한번만 실행해도 됩니다.
#
# You should install Pygame library with `pip` module
# This code only needs to be run once after startup.

# %%
# Jupyter 내부에서 shell command 실행을 위해 '%'를 사용하여 'pip'를 실행합니다.
# Insert `%` before running 'pip' command for running shell commands on Jupyter
# %pip install pygame

# %%
# Python으로 실행하고 싶으시다면 위 코드를 삭제하시고 아래의 코드를 실행해주세요.
# Delete the '%pip' code and run this code if you want to run on python
import sys
import subprocess
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame'])

# %% [markdown]
# #### 1. 모듈 임포트(Module import)
# 설치한 pygame library 및 기타 필요한 모듈을 사용하기 위해 import합니다.
#
# Import `pygame library` and other modules to use in this code

# %%
# Pygame module import
import pygame
# 시간 확인, random 부여 등을 위한 module import
# Modules for time checking and randomization
import random
import time

# %% [markdown]
# ##### 1-1. 게임 사전 설정(Settings on the game)
# 게임에 대한 기본적인 설정에 대한 변수 들을 미리 정의합니다.
#
# Define variables that initializes the game

# %%
# Frame 수 조절(초당 그려지는 수)
# Framerate per seconds
fps = 15

# 창의 크기
# Window size
frame = (720, 480)

# 색깔 정의 (Red, Green, Blue)
# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)
gray = pygame.Color(128, 128, 128)

# 시간을 흐르게 하기 위한 FPS counter
# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

#%%
# Game 관련 변수들
# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (frame[0]//10)) * 10,
            random.randrange(1, (frame[1]//10)) * 10]
food_spawn = True
# Obstacles list
obstacles = []

direction = 'RIGHT'

score = 0

special_fruit = None
special_fruit_timer = None

def load_highest_score():
    try:
        with open("highest_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0
    
highest_score = load_highest_score() 

# Function to save highest score to a file
def save_highest_score(score):
    with open("highest_score.txt", "w") as file:
        file.write(str(score))

def spawn_special_fruit():
    global special_fruit, special_fruit_timer
    special_fruit = [random.randrange(1, (frame[0]//10)) * 10,
            random.randrange(1, (frame[1]//10)) * 10]
    special_fruit_timer = time.time()  # Record spawn time

# %% [markdown]
# ##### 1-2. Pygame 초기화(Initialize Pygame)
# Pygame을 사용하기 위해 창 크기, 제목 등을 주어 초기화를 해줍니다.
# 만약 초기화를 실패하였다면 오류를 알려주고 종료하도록 합니다.
# 함수로 만들어서 게임이 동작하기 전에 부를 수 있도록 합니다.
#
# Initialize Pygame with window size, and title.
# When initializing Pygame failed, prints error and exit program.
# Run before executing main logic of the game.


# %%
def Init(size):
    # 초기화 후 error가 일어났는지 알아봅니다.
    # Checks for errors encountered
    check_errors = pygame.init()

    # pygame.init() example output -> (6, 0)
    # 두번째 항목이 error의 수를 알려줍니다.
    # second number in tuple gives number of errors
    if check_errors[1] > 0:
        print(
            f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
        sys.exit(-1)
    else:
        print('[+] Game successfully initialised')

    # pygame.display를 통해 제목, window size를 설정하고 초기화합니다.
    # Initialise game window using pygame.display
    pygame.display.set_caption('Snake Example with PyGame')
    game_window = pygame.display.set_mode(size)
    return game_window

# %% [markdown]
# ##### 1-3. 기본 logic 함수 모음(basic logics of the game)
# 게임을 플레이하기 위해 필요한 함수들의 모음입니다.
# 자세한 부분은 각 주석을 확인해주세요.
#
# This is the set of functions that are required in the game.
# You can see more details in comments on each cell.

# Function to generate new obstacles
def generate_obstacles(score):
    num_obstacles = min(score // 5+1, 6)  # Increase obstacles every 5 points, max 5
    obstacles.clear()  # Clear previous obstacles
    for _ in range(num_obstacles):
        new_obstacle = [random.randrange(1, (frame[0]//10)) * 10,
                        random.randrange(1, (frame[1]//10)) * 10]
        obstacles.append(new_obstacle)
    
# Check if snake collides with any obstacle
def check_collision():
    for obs in obstacles:
        if snake_pos[0] == obs[0] and snake_pos[1] == obs[1]:  # Collision check
            game_over(main_window, frame)
# %%
# Score
def show_score(window, size, choice, color, font, fontsize):
    # Score를 띄우기 위한 설정입니다.
    # Settings for showing score on screen
    score_font = pygame.font.SysFont(font, fontsize)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()

    highest = score_font.render('Highest Score : ' + str(highest_score), True, white)
    score_highest = highest.get_rect()   
    # Game over 상황인지 게임중 상황인지에 따라 다른 위치를 선정합니다.
    # Select different location depending on the situation.
    if choice == 1:
        score_rect.midtop = (size[0]/10, 15)
        score_highest.midtop = (size[0]/10 + 200, 15)
    else:
        score_rect.midtop = (size[0]/2, size[1]/1.25)
        score_highest.midtop = (size[0]/2, size[1]/1.25 + 30)

    # 설정한 글자를 window에 복사합니다.
    # Copy the string to windows
    window.blit(score_surface, score_rect)
    window.blit(highest, score_highest)

# %%
# Game Over
def game_over(window, size):
    # 'Game Over'문구를 띄우기 위한 설정입니다.
    # Settings of the 'Game Over' string to show on the screen
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('Game Over', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (size[0]/2, size[1]/4)

    # window를 검은색으로 칠하고 설정했던 글자를 window에 복사합니다.
    # Fill window as black and copy 'Game Over' strings to main window.
    
    window.fill(black)
    window.blit(game_over_surface, game_over_rect)

    # 'show_score' 함수를 부릅니다.
    # Call 'show_score' function.
    show_score(window, size, 0, green, 'times', 20)

    # 그려진 화면을 실제로 띄워줍니다.
    # Show drawn windows to screen
    pygame.display.flip()

    # 3초 기다린 후 게임을 종료합니다.
    # exit program after 3 seconds.
    time.sleep(3)
    pygame.quit()
    sys.exit()


# %%
# Keyboard input
def get_keyboard(key, cur_dir):
    # WASD, 방향키를 입력 받으면 해당 방향으로 이동합니다.
    # 방향이 반대방향이면 무시합니다.
    # Chnage direction using WASD or arrow key
    # Ignore keyboard input if input key has opposite direction
    if direction != 'DOWN' and key == pygame.K_UP or key == ord('w'):
        return 'UP'
    if direction != 'UP' and key == pygame.K_DOWN or key == ord('s'):
        return 'DOWN'
    if direction != 'RIGHT' and key == pygame.K_LEFT or key == ord('a'):
        return 'LEFT'
    if direction != 'LEFT' and key == pygame.K_RIGHT or key == ord('d'):
        return 'RIGHT'
    # 모두 해당하지 않다면 원래 방향을 돌려줍니다.
    # Return current direction if none of keyboard input occured
    return cur_dir

#Grass tiles
def draw_grass_pattern(window, frame, tile_size=20):
    #coloring
    light_green = pygame.Color(170, 215, 81)
    dark_green = pygame.Color(162, 209, 73)

    rows = frame[1] // tile_size
    cols = frame[0] // tile_size

    for row in range(rows):
        for col in range(cols):
            color = light_green if (row + col) % 2 == 0 else dark_green
            pygame.draw.rect(window, color, (col * tile_size, row * tile_size, tile_size, tile_size))
# %% [markdown]
# #### 2. 메인 프로그램
# Game이 동작하기 위한 메인 코드 입니다.
#
# This is main code of the game.


# %%
# 초기화합니다.
# Initialize
main_window = Init(frame)

while True:
    # 게임에서 event를 받아옵니다.
    # Get event from user
    for event in pygame.event.get():
        # 종료시 실제로 프로그램을 종료합니다.
        # Close program if QUIT event occured
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # esc 키를 눌렀을떄 종료 신호를 보냅니다.
            # Create quit event when 'esc' key pressed
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            else:
                # 입력 키로 방향을 얻어냅니다.
                # Get direction with key
                direction = get_keyboard(event.key, direction)
    
    # 실제로 뱀의 위치를 옮깁니다.
    # Move the actual snake position
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10
    
    # 우선 증가시키고 음식의 위치가 아니라면 마지막을 뺍니다.
    # Grow snake first, check if food is on sanke head(if not, delete last)
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        fps+=0.25
        food_spawn = False
    else:
        snake_body.pop()

    #Check collision with obstacles
    check_collision() 

    # 음식이 없다면 음식을 랜덤한 위치에 생성합니다.
    # Spawning food on the screen with random position
    if not food_spawn:
        food_pos = [
            random.randrange(1, (frame[0]//10)) * 10,
            random.randrange(1, (frame[1]//10)) * 10
        ]
     # Update obstacles
        generate_obstacles(score) 
        food_spawn = True

    if special_fruit is None and random.randrange(1, 100) > 98:
        spawn_special_fruit()

    # Check if snake eats special fruit
    if special_fruit and snake_pos == special_fruit:
        score += 5  # Give 5 points
        special_fruit = None  # Remove special fruit


    if special_fruit and time.time() - special_fruit_timer > 5:
        special_fruit = None

    # 우선 게임을 검은 색으로 채우고 뱀의 각 위치마다 그림을 그립니다.
    # Fill the screen black and draw each position of snake
    #main_window.fill(black)
    # Fill the screen black
    draw_grass_pattern(main_window, frame)
    for pos in snake_body:
        pygame.draw.rect(main_window, blue,
                         pygame.Rect(pos[0], pos[1], 10, 10))

    # 음식을 그립니다.
    # Draw snake food - circle
    pygame.draw.circle(main_window, white, (food_pos[0] + 5, food_pos[1] + 5), 5)

    if special_fruit:
        pygame.draw.circle(main_window, red, (special_fruit[0] + 6, special_fruit[1] + 6), 6)
    # 방해를 그립니다.
    # Draw obstacles 
    for obs in obstacles:
                     pygame.draw.rect(main_window, gray, pygame.Rect(obs[0], obs[1], 10, 10))

    # Game Over 상태를 확인합니다.
    # Check Game Over conditions

    # 바깥 벽 처리를 합니다.
    # Check if the snake hit the wall
    if snake_pos[0] < 0 or snake_pos[0] > frame[0] - 10:
        game_over(main_window, frame)
    if snake_pos[1] < 0 or snake_pos[1] > frame[1] - 10:
        game_over(main_window, frame)

    # 뱀의 몸에 닿았는지 확인합니다.
    # Check if the snake is  hit obstacle
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over(main_window, frame)

    # 점수를 띄워줍니다.
    # Show score with defined function

    if score > highest_score:
        highest_score = score
        save_highest_score(highest_score)

    show_score(main_window, frame, 1, white, 'consolas', 20)

    # 실제 화면에 보이도록 업데이트 해줍니다.
    # Refresh game screen
    pygame.display.update()

    # 해당 FPS만큼 대기합니다.
    # Refresh rate
    fps_controller.tick(fps)