import pygame
import random
import time
import sys

# Initialize Pygame
def Init(size):
    check_errors = pygame.init()
    if check_errors[1] > 0:
        print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
        sys.exit(-1)
    else:
        print('[+] Game successfully initialised')
    pygame.display.set_caption('Snake Example with PyGame')
    game_window = pygame.display.set_mode(size)
    return game_window

# Display the score on the screen
def show_score(window, size, choice, color, font, fontsize, score):
    score_font = pygame.font.SysFont(font, fontsize)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()

    if choice == 1:
        score_rect.midtop = (size[0]/10, 15)
    else:
        score_rect.midtop = (size[0]/2, size[1]/1.25)

    window.blit(score_surface, score_rect)

# Game Over screen
def game_over(window, size):
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('Game Over', True, pygame.Color(255, 0, 0))
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (size[0]/2, size[1]/4)

    window.fill(pygame.Color(0, 0, 0))
    window.blit(game_over_surface, game_over_rect)
    show_score(window, size, 0, pygame.Color(0, 255, 0), 'times', 20, 0)

    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# Handle keyboard input
def get_keyboard(key, cur_dir, snake_number):
    if snake_number == 1:  # First snake (WASD)
        if cur_dir != 'DOWN' and (key == pygame.K_UP or key == ord('w')):
            return 'UP'
        if cur_dir != 'UP' and (key == pygame.K_DOWN or key == ord('s')):
            return 'DOWN'
        if cur_dir != 'RIGHT' and (key == pygame.K_LEFT or key == ord('a')):
            return 'LEFT'
        if cur_dir != 'LEFT' and (key == pygame.K_RIGHT or key == ord('d')):
            return 'RIGHT'
    elif snake_number == 2:  # Second snake (Arrow keys)
        if cur_dir != 'DOWN' and key == pygame.K_UP:
            return 'UP'
        if cur_dir != 'UP' and key == pygame.K_DOWN:
            return 'DOWN'
        if cur_dir != 'RIGHT' and key == pygame.K_LEFT:
            return 'LEFT'
        if cur_dir != 'LEFT' and key == pygame.K_RIGHT:
            return 'RIGHT'
    return cur_dir

# Main game loop
def game_loop():
    frame = (720, 480)
    fps = 15
    fps_controller = pygame.time.Clock()

    # Initial snake positions and bodies
    snake1_pos = [100, 50]
    snake1_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

    snake2_pos = [200, 50]
    snake2_body = [[200, 50], [200-10, 50], [200-(2*10), 50]]

    food_pos = [random.randrange(1, (frame[0]//10)) * 10, random.randrange(1, (frame[1]//10)) * 10]
    food_spawn = True

    direction1 = 'RIGHT'
    direction2 = 'RIGHT'

    score1 = 0
    score2 = 0

    main_window = Init(frame)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                else:
                    direction1 = get_keyboard(event.key, direction1, 1)
                    direction2 = get_keyboard(event.key, direction2, 2)

        # Update position of snake 1
        if direction1 == 'UP':
            snake1_pos[1] -= 10
        if direction1 == 'DOWN':
            snake1_pos[1] += 10
        if direction1 == 'LEFT':
            snake1_pos[0] -= 10
        if direction1 == 'RIGHT':
            snake1_pos[0] += 10

        # Update position of snake 2
        if direction2 == 'UP':
            snake2_pos[1] -= 10
        if direction2 == 'DOWN':
            snake2_pos[1] += 10
        if direction2 == 'LEFT':
            snake2_pos[0] -= 10
        if direction2 == 'RIGHT':
            snake2_pos[0] += 10

        snake1_body.insert(0, list(snake1_pos))
        snake2_body.insert(0, list(snake2_pos))

        if snake1_pos[0] == food_pos[0] and snake1_pos[1] == food_pos[1]:
            score1 += 1
            food_spawn = False
        else:
            snake1_body.pop()

        if snake2_pos[0] == food_pos[0] and snake2_pos[1] == food_pos[1]:
            score2 += 1
            food_spawn = False
        else:
            snake2_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (frame[0]//10)) * 10, random.randrange(1, (frame[1]//10)) * 10]
        food_spawn = True

        # Fill the game window
        main_window.fill(pygame.Color(0, 0, 0))

        # Draw both snakes
        for pos in snake1_body:
            pygame.draw.rect(main_window, pygame.Color(0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))
        for pos in snake2_body:
            pygame.draw.rect(main_window, pygame.Color(0, 0, 255), pygame.Rect(pos[0], pos[1], 10, 10))

        # Draw the food
        pygame.draw.rect(main_window, pygame.Color(255, 255, 255), pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Game Over checks for both snakes
        if snake1_pos[0] < 0 or snake1_pos[0] > frame[0] - 10 or snake1_pos[1] < 0 or snake1_pos[1] > frame[1] - 10:
            game_over(main_window, frame)
        if snake2_pos[0] < 0 or snake2_pos[0] > frame[0] - 10 or snake2_pos[1] < 0 or snake2_pos[1] > frame[1] - 10:
            game_over(main_window, frame)
        for block in snake1_body[1:]:
            if snake1_pos[0] == block[0] and snake1_pos[1] == block[1]:
                game_over(main_window, frame)
        for block in snake2_body[1:]:
            if snake2_pos[0] == block[0] and snake2_pos[1] == block[1]:
                game_over(main_window, frame)

        # Display the score
        show_score(main_window, frame, 1, pygame.Color(255, 255, 255), 'consolas', 20, score1)
        show_score(main_window, frame, 2, pygame.Color(255, 255, 255), 'consolas', 20, score2)

        # Update the game window
        pygame.display.update()
        fps_controller.tick(fps)