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


fps = 15

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
play1_button = pygame.Rect(frame[0]//2 - 95, 90, 200, 50)
play2_button = pygame.Rect(frame[0]//2 - 95, 160, 200, 50)
help_button = pygame.Rect(frame[0]//2 - 95, 230, 200, 50)
settings_button = pygame.Rect(frame[0]//2 - 95, 300, 200, 50)
quit_button = pygame.Rect(frame[0]//2 - 95, 370, 200, 50)

background_image = pygame.image.load('./snake/snake_game/background.jpg')  # Replace with your image path
background_image = pygame.transform.scale(background_image, (frame[0], frame[1])) 

def draw_button(text, rect, color, hover_color, mouse_pos):
    score_font = pygame.font.SysFont('consolas', 40)
    if rect.collidepoint(mouse_pos):  
        pygame.draw.rect(main_window, hover_color, rect, border_radius=0)
    else:
        pygame.draw.rect(main_window, color, rect, border_radius=0) 

    text_surface = score_font.render(text, True, black)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def load_highest_score():
    try:
        with open("./snake/highest_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0
    
highest_score = load_highest_score() 


def load_max_obstacles():
    try:
        with open("./snake/max_obstacles.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 5
    
max_obstacles = load_max_obstacles() 

# Function to save highest score to a file
def save_max_obstacles(obs):
    with open("./snake/max_obstacles.txt", "w") as file:
        file.write(str(obs))


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
    hand_cursor = pygame.SYSTEM_CURSOR_HAND
    arrow_cursor = pygame.SYSTEM_CURSOR_ARROW
    while True:
        

        screen.blit(background_image, (0, 0))
        score_font = pygame.font.SysFont("consolas", 20)
        score_surface = score_font.render('Highest Score : ' + str(highest_score), True, black)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (frame[0]/10 + 50, 15)
        main_window.blit(score_surface, score_rect)

        mouse_pos = pygame.mouse.get_pos()
        hovering = False  # Track if mouse is over a button

        if play1_button.collidepoint(mouse_pos) or play2_button.collidepoint(mouse_pos) or quit_button.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(hand_cursor)
            hovering = True
        if not hovering:  # Reset cursor if not hovering over any button
            pygame.mouse.set_cursor(arrow_cursor)

        draw_button("1 Player", play1_button, green, (0, 200, 0), mouse_pos)
        draw_button("2 Players", play2_button, green, (0, 200, 0), mouse_pos)
        draw_button("Help", help_button, green, (0, 200, 0), mouse_pos)
        draw_button("Settings", settings_button, green, (0, 200, 0), mouse_pos)
        draw_button("Quit", quit_button, (255, 209, 102), (255, 186, 26), mouse_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse click
                if play1_button.collidepoint(event.pos):
                    subprocess.run(["python", "./snake/snake_game/1playersnake.py"])
                if play2_button.collidepoint(event.pos):
                    subprocess.run(["python", "./snake/snake_game/2playersnake.py"])
                if help_button.collidepoint(event.pos):
                    show_rules()
                if settings_button.collidepoint(event.pos):
                    settings_menu()
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def settings_menu():
    global max_obstacles
    font = pygame.font.SysFont('times new roman', 40)
    input_box = pygame.Rect(frame[0]//2 + 70, 200, 100, 50)
    color_inactive = white
    color_active = (200, 200, 200)
    color = color_inactive
    active = False
    user_text = str(max_obstacles)
    running = True
    while running:
        screen.fill((50, 50, 50))  # Dark background
        mouse_pos = pygame.mouse.get_pos()

        title = font.render("Settings", True, white)
        screen.blit(title, (frame[0]//2 - title.get_width()//2, 50))

        prompt = font.render("Max Obstacles:  ", True, white)
        screen.blit(prompt, (frame[0]//2 - 200, 200))

        pygame.draw.rect(screen, color, input_box, border_radius=5)
        text_surface = font.render(user_text, True, black)
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 5))

        save_button = pygame.Rect(frame[0]//2 - 70, 300, 140, 50)
        draw_button("Save", save_button, green, (0, 200, 0), mouse_pos)

        back_button = pygame.Rect(frame[0]//2 - 70, 370, 140, 50)
        draw_button("Back", back_button, (255, 209, 102), (255, 186, 26), mouse_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False

                if save_button.collidepoint(event.pos):
                    try:
                        max_obstacles = int(user_text)
                        save_max_obstacles(max_obstacles)
                        running = False
                    except ValueError:
                        pass  # Ignore invalid input

                if back_button.collidepoint(event.pos):
                    running = False

            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]  # Remove last character
                elif event.unicode.isdigit():
                    user_text += event.unicode  # Add typed number

        color = color_active if active else color_inactive

def show_rules():
    rules_running = True
    while rules_running:
        screen.fill(white)  # Set background color
        font = pygame.font.SysFont("consolas", 20)
        
        rules_text = [
            "Game Rules:",
            "1. Use arrows or w, a, s, d to move the snake.",
            "2. Eat whte food to get 1 point and grow longer.",
            "3. Eat red food to get 5 points.",
            "4. Red food will disappear after 5 seconds.",
            "5. The game ends when you hit gray obstacle, wall or yourself.",
            "",
            "Multiplayer Mode:",
            "1. You lose if you collide with other snake's body.",
            "2. Tie if head-on collision.",
            "Press ESC to return to the menu."
        ]
        
        y_offset = 30
        for line in rules_text:
            text_surface = font.render(line, True, black)
            text_rect = text_surface.get_rect(center=(frame[0]//2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 40  # Space between lines
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to go back
                    rules_running = False

main_window = Init(frame)

game_menu()
