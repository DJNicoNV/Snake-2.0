import pygame
import time
import random
import os
import sys

# Constants
WINDOW_X = 720
WINDOW_Y = 480
SNAKE_SPEED = 15

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)

UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

# Initializing pygame
pygame.init()

# Initialize game window
pygame.display.set_caption("Snake")
game_window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))

# FPS controller
fps = pygame.time.Clock()


def load_high_score():
    if os.path.exists('high_score.txt'):
        with open('high_score.txt', 'r') as file:
            return int(file.read())
    else:
        return 0


def save_high_score(score):
    with open('high_score.txt', 'w') as file:
        file.write(str(score))


# Initializing game variables
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
fruit_position = [random.randrange(1, (WINDOW_X // 10)) * 10, random.randrange(1, (WINDOW_Y // 10)) * 10]
fruit_spawn = True
direction = RIGHT
change_to = direction
score = 0
high_score = load_high_score()  # Load high score at the beginning


def game_over():
    global score, high_score

    if score > high_score:
        high_score = score
        save_high_score(high_score)

    # Display game over message
    font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = font.render('Your Score is : ' + str(score), True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (WINDOW_X / 2, WINDOW_Y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(1, WHITE, 'times new roman', 20)

    # Display high score
    high_score_surface = font.render('High Score : ' + str(high_score), True, WHITE)
    high_score_rect = high_score_surface.get_rect()
    high_score_rect.midtop = (WINDOW_X / 2, WINDOW_Y / 2)
    game_window.blit(high_score_surface, high_score_rect)

    # Display choice message
    choice_surface = font.render('Play again? (Y/N)', True, WHITE)
    choice_rect = choice_surface.get_rect()
    choice_rect.midtop = (WINDOW_X / 2, WINDOW_Y * 3 / 4)
    game_window.blit(choice_surface, choice_rect)
    pygame.display.flip()

    # Wait for a while
    time.sleep(2)

    # Ask if the player wants to play again
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # 'y' for yes
                    reset_game()
                    return
                elif event.key == pygame.K_n:  # 'n' for no
                    pygame.quit()
                    sys.exit()


def reset_game():
    global snake_position, snake_body, fruit_position, fruit_spawn, direction, change_to, score
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    fruit_position = [random.randrange(1, (WINDOW_X // 10)) * 10, random.randrange(1, (WINDOW_Y // 10)) * 10]
    fruit_spawn = True
    direction = RIGHT
    change_to = direction
    score = 0


def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)


# Main function
while True:
    high_score = load_high_score()  # Update high score at the beginning of each game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != DOWN:
                change_to = UP
            if event.key == pygame.K_DOWN and direction != UP:
                change_to = DOWN
            if event.key == pygame.K_LEFT and direction != RIGHT:
                change_to = LEFT
            if event.key == pygame.K_RIGHT and direction != LEFT:
                change_to = RIGHT

    if change_to == UP and direction != DOWN:
        direction = UP
    if change_to == DOWN and direction != UP:
        direction = DOWN
    if change_to == LEFT and direction != RIGHT:
        direction = LEFT
    if change_to == RIGHT and direction != LEFT:
        direction = RIGHT

    if direction == UP:
        snake_position[1] -= 10
    if direction == DOWN:
        snake_position[1] += 10
    if direction == LEFT:
        snake_position[0] -= 10
    if direction == RIGHT:
        snake_position[0] += 10

    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (WINDOW_X // 10)) * 10, random.randrange(1, (WINDOW_Y // 10)) * 10]

    fruit_spawn = True
    game_window.fill(BLACK)

    for pos in snake_body:
        pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, WHITE, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > WINDOW_X - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > WINDOW_Y - 10:
        game_over()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # Displaying score continuously
    show_score(1, WHITE, 'times new roman', 20)

    # Refresh game screen
    pygame.display.flip()

    # Frame Per Second /Refresh Rate
    fps.tick(SNAKE_SPEED)
