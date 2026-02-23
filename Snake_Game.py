import pygame
import random

# Initialize pygame
pygame.init()

# ---------------- COLORS ----------------
color_white = (255, 255, 255)
color_yellow = (255, 255, 102)
color_black = (0, 0, 0)
color_brown = (213, 200, 80)
color_green = (0, 255, 0)
color_grey = (128,128,128)

# ---------------- SCREEN ----------------
box_len = 900                     # Width of game window
box_height = 600                  # Height of game window
screen = pygame.display.set_mode((box_len, box_height))   # Create game window
pygame.display.set_caption("Snake Game")

# ---------------- CLOCK ----------------
clock = pygame.time.Clock()        # Controls game speed (FPS)

# ---------------- SNAKE SETTINGS ----------------
snake_block = 10                  # Size of snake block
snake_speed = 10                  # Speed of snake

# ---------------- FONTS ----------------
font_style = pygame.font.SysFont("arial", 30, True)
score_font = pygame.font.SysFont("arial", 30, True)

# ---------------- SCORE FUNCTION ----------------
def show_score(score):
    """Display the player's score on the screen"""
    value = score_font.render("Score: " + str(score), True, color_yellow)
    screen.blit(value, [10, 10])

# ---------------- DRAW SNAKE ----------------
def draw_snake(block_size, snake_list):
    """Draw the snake on the screen"""
    for block in snake_list:
        pygame.draw.rect(screen, color_black,
                         [block[0], block[1], block_size, block_size])

# ---------------- DISPLAY MESSAGE ----------------
def display_message(msg, color):
    """Display message at the center of the screen"""
    message = font_style.render(msg, True, color)
    screen.blit(message, [box_len // 6, box_height // 3])

# ---------------- MAIN GAME FUNCTION ----------------
def game_loop():
    game_over = False          # Ends the game
    game_close = False         # Triggers game over screen

    # Snake starting position (center of screen)
    x = box_len // 2
    y = box_height // 2

    # Movement variables
    x_change = 0
    y_change = 0

    snake_list = []            # Stores snake body blocks
    snake_length = 1           # Initial snake length

    # Random food position
    food_x = round(random.randrange(0, box_len - snake_block) / 10.0) * 10
    food_y = round(random.randrange(0, box_height - snake_block) / 10.0) * 10

    # ---------------- GAME LOOP ----------------
    while not game_over:

        # ----- GAME OVER SCREEN -----
        while game_close:
            screen.fill(color_grey)
            display_message("You Lost! Press C to Play Again or Q to Quit",
                            color_brown)
            show_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        return game_loop()   # Restart game

        # ----- EVENT HANDLING -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = snake_block
                    x_change = 0

        # ----- WALL COLLISION -----
        if x >= box_len or x < 0 or y >= box_height or y < 0:
            game_close = True

        # ----- MOVE SNAKE -----
        x += x_change
        y += y_change
        screen.fill(color_grey)

        # ----- DRAW FOOD -----
        pygame.draw.rect(screen, color_green,
                         [food_x, food_y, snake_block, snake_block])

        # ----- UPDATE SNAKE BODY -----
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # ----- SELF COLLISION -----
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        # ----- DRAW SNAKE & SCORE -----
        draw_snake(snake_block, snake_list)
        show_score(snake_length - 1)

        pygame.display.update()

        # ----- FOOD EATEN -----
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, box_len - snake_block) / 10.0) * 10
            food_y = round(random.randrange(0, box_height - snake_block) / 10.0) * 10
            snake_length += 1

        # Control game speed
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# ---------------- START GAME ----------------
game_loop()