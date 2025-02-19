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

# 시간을 흐르게 하기 위한 FPS counter
# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

#%%
# Game 관련 변수들
# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

snake_pos2 = [100, 450]
snake_body2 = [[100, 450], [100-10, 450], [100-(2*10), 450]]

food_pos = [random.randrange(1, (frame[0]//10)) * 10,
            random.randrange(1, (frame[1]//10)) * 10]
food_spawn = True

direction = 'RIGHT'
direction2 = 'RIGHT'


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
    pygame.display.set_caption('Snake 2 player')
    game_window = pygame.display.set_mode(size)
    return game_window

# %% [markdown]
# ##### 1-3. 기본 logic 함수 모음(basic logics of the game)
# 게임을 플레이하기 위해 필요한 함수들의 모음입니다.
# 자세한 부분은 각 주석을 확인해주세요.
#
# This is the set of functions that are required in the game.
# You can see more details in comments on each cell.



# %%
# Game Over
def game_over(window, size, snake):
    # 'Game Over'문구를 띄우기 위한 설정입니다.
    # Settings of the 'Game Over' string to show on the screen
    my_font = pygame.font.SysFont('times new roman', 90)
    if snake == 0:
        game_over_surface = my_font.render('Tie', True, red)
    else:
        game_over_surface = my_font.render('Player '+ str(snake)+ " wins", True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (size[0]/2, size[1]/4)

    # window를 검은색으로 칠하고 설정했던 글자를 window에 복사합니다.
    # Fill window as black and copy 'Game Over' strings to main window.
    window.fill(black)
    window.blit(game_over_surface, game_over_rect)

    # 'show_score' 함수를 부릅니다.
    # Call 'show_score' function.

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
    if direction != 'DOWN' and key == ord('w'):
        return 'UP'
    if direction != 'UP' and  key == ord('s'):
        return 'DOWN'
    if direction != 'RIGHT' and key == ord('a'):
        return 'LEFT'
    if direction != 'LEFT' and key == ord('d'):
        return 'RIGHT'
    # 모두 해당하지 않다면 원래 방향을 돌려줍니다.
    # Return current direction if none of keyboard input occured
    return cur_dir

def get_keyboard2(key, cur_dir):
    # WASD, 방향키를 입력 받으면 해당 방향으로 이동합니다.
    # 방향이 반대방향이면 무시합니다.
    # Chnage direction using WASD or arrow key
    # Ignore keyboard input if input key has opposite direction
    if direction2 != 'DOWN' and key == pygame.K_UP:
        return 'UP'
    if direction2 != 'UP' and key == pygame.K_DOWN:
        return 'DOWN'
    if direction2 != 'RIGHT' and key == pygame.K_LEFT:
        return 'LEFT'
    if direction2 != 'LEFT' and key == pygame.K_RIGHT:
        return 'RIGHT'
    # 모두 해당하지 않다면 원래 방향을 돌려줍니다.
    # Return current direction if none of keyboard input occured
    return cur_dir

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
                direction2 = get_keyboard2(event.key, direction2)

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

    if direction2 == 'UP':
        snake_pos2[1] -= 10
    if direction2 == 'DOWN':
        snake_pos2[1] += 10
    if direction2 == 'LEFT':
        snake_pos2[0] -= 10
    if direction2 == 'RIGHT':
        snake_pos2[0] += 10

    # 우선 증가시키고 음식의 위치가 아니라면 마지막을 뺍니다.
    # Grow snake first, check if food is on sanke head(if not, delete last)
    snake_body.insert(0, list(snake_pos))
    snake_body2.insert(0, list(snake_pos2))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        food_spawn = False
    else:
        snake_body.pop()
    if snake_pos2[0] == food_pos[0] and snake_pos2[1] == food_pos[1]:
        food_spawn = False
    else:
        snake_body2.pop()

    # 음식이 없다면 음식을 랜덤한 위치에 생성합니다.
    # Spawning food on the screen with random position
    if not food_spawn:
        food_pos = [
            random.randrange(1, (frame[0]//10)) * 10,
            random.randrange(1, (frame[1]//10)) * 10
        ]
    food_spawn = True

    # 우선 게임을 검은 색으로 채우고 뱀의 각 위치마다 그림을 그립니다.
    # Fill the screen black and draw each position of snake
    draw_grass_pattern(main_window, frame)
    for pos in snake_body:
        pygame.draw.rect(main_window, blue,
                         pygame.Rect(pos[0], pos[1], 10, 10))
        
    for pos in snake_body2:
        pygame.draw.rect(main_window, red,
                         pygame.Rect(pos[0], pos[1], 10, 10))

    # 음식을 그립니다.
    # Draw snake food
    pygame.draw.circle(main_window, white, (food_pos[0] + 5, food_pos[1] + 5), 5)

    # Game Over 상태를 확인합니다.
    # Check Game Over conditions

    # 바깥 벽 처리를 합니다.
    # Check if the snake hit the wall
    if snake_pos[0] < 0 or snake_pos[0] > frame[0] - 10:
        snake = 2
        game_over(main_window, frame, snake)
    if snake_pos[1] < 0 or snake_pos[1] > frame[1] - 10:
        snake = 2
        game_over(main_window, frame, snake)
    if snake_pos2[0] < 0 or snake_pos2[0] > frame[0] - 10:
        snake = 1
        game_over(main_window, frame, snake)
    if snake_pos2[1] < 0 or snake_pos2[1] > frame[1] - 10:
        snake = 1
        game_over(main_window, frame, snake)

    # 뱀의 몸에 닿았는지 확인합니다.
    # Check if the snake is hit itself
    if snake_pos == snake_pos2:
        snake = 0
        game_over(main_window, frame, snake)
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            snake = 2
            game_over(main_window, frame, snake)
    for block in snake_body2[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            snake = 2
            game_over(main_window, frame, snake)

    for block in snake_body2[1:]:
        if snake_pos2[0] == block[0] and snake_pos2[1] == block[1]:
            snake = 1
            game_over(main_window, frame, snake)
    for block in snake_body[1:]:
        if snake_pos2[0] == block[0] and snake_pos2[1] == block[1]:
            snake = 1
            game_over(main_window, frame, snake)

    # 점수를 띄워줍니다.
    # Show score with defined function

    # 실제 화면에 보이도록 업데이트 해줍니다.
    # Refresh game screen
    pygame.display.update()

    # 해당 FPS만큼 대기합니다.
    # Refresh rate
    fps_controller.tick(fps)