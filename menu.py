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


#%%
# Game 관련 변수들


screen = pygame.display.set_mode((frame[0], frame[1]))

# Buttons (x, y, width, height)
play1_button = pygame.Rect(frame[0]//2 - 95, 150, 200, 50)
play2_button = pygame.Rect(frame[0]//2 - 95, 220, 200, 50)
quit_button = pygame.Rect(frame[0]//2 - 95, 300, 200, 50)

background_image = pygame.image.load('D:/Code/snake/snake/background.jpg')  # Replace with your image path
background_image = pygame.transform.scale(background_image, (frame[0], frame[1])) 

def draw_button(text, rect, color, hover_color, mouse_pos):
    score_font = pygame.font.SysFont('times new roman', 50)
    if rect.collidepoint(mouse_pos):  
        pygame.draw.rect(main_window, hover_color, rect, border_radius=0)  # Hover color
    else:
        pygame.draw.rect(main_window, color, rect, border_radius=0)  # Normal color

    text_surface = score_font.render(text, True, black)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)



# %%
def Init(size):
    # 초기화 후 error가 일어났는지 알아봅니다.
    # Checks for errors encountered
    check_errors = pygame.init()

    if check_errors[1] > 0:
        print(
            f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
        sys.exit(-1)
    else:
        print('[+] Game successfully initialised')

    # pygame.display를 통해 제목, window size를 설정하고 초기화합니다.
    # Initialise game window using pygame.display
    pygame.display.set_caption('Hungry Snake Game')
    game_window = pygame.display.set_mode(size)
    return game_window

menu_color = pygame.Color(153, 204, 255)
def game_menu():
    while True:
        screen.blit(background_image, (0, 0))

        mouse_pos = pygame.mouse.get_pos()  # Get current mouse position

        draw_button("1 Player", play1_button, green, (0, 200, 0), mouse_pos)
        draw_button("2 Players", play2_button, green, (0, 200, 0), mouse_pos)
        draw_button("Quit", quit_button, (255, 209, 102), (255, 186, 26), mouse_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse click
                if play1_button.collidepoint(event.pos):
                    subprocess.run(["python", "D:/Code/snake/snake/1playersnake.py"])
                if play2_button.collidepoint(event.pos):
                    subprocess.run(["python", "D:/Code/snake/snake/2playersnake.py"])
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


main_window = Init(frame)

game_menu()
