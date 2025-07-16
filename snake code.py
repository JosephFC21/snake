import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
DARK_RED = (100, 0, 0)  # Add this color near your other color definitions if you want
DARK_GREEN = (0, 60, 0)  # Add near other color definitions

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Font for score
font = pygame.font.SysFont('Arial', 24)

# Clock for controlling frame rate
clock = pygame.time.Clock()

def draw_snake(snake):
    # Draw body
    for segment in snake[1:]:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
    # Draw head with eyes and tongue
    head = snake[0]
    pygame.draw.rect(screen, DARK_GREEN, (*head, CELL_SIZE, CELL_SIZE))
    # Eyes
    eye_radius = 3
    offset = 4
    if len(snake) > 1:
        dx = head[0] - snake[1][0]
        dy = head[1] - snake[1][1]
    else:
        dx, dy = 0, -CELL_SIZE  # Default facing up
    # Eye positions based on direction
    if dx > 0:  # Right
        eye1 = (head[0] + CELL_SIZE - offset, head[1] + offset)
        eye2 = (head[0] + CELL_SIZE - offset, head[1] + CELL_SIZE - offset)
        tongue = [(head[0] + CELL_SIZE, head[1] + CELL_SIZE // 2)]
    elif dx < 0:  # Left
        eye1 = (head[0] + offset, head[1] + offset)
        eye2 = (head[0] + offset, head[1] + CELL_SIZE - offset)
        tongue = [(head[0], head[1] + CELL_SIZE // 2)]
    elif dy > 0:  # Down
        eye1 = (head[0] + offset, head[1] + CELL_SIZE - offset)
        eye2 = (head[0] + CELL_SIZE - offset, head[1] + CELL_SIZE - offset)
        tongue = [(head[0] + CELL_SIZE // 2, head[1] + CELL_SIZE)]
    else:  # Up
        eye1 = (head[0] + offset, head[1] + offset)
        eye2 = (head[0] + CELL_SIZE - offset, head[1] + offset)
        tongue = [(head[0] + CELL_SIZE // 2, head[1])]
    pygame.draw.circle(screen, WHITE, eye1, eye_radius)
    pygame.draw.circle(screen, WHITE, eye2, eye_radius)
    # Tongue (red line)
    for t in tongue:
        if dx != 0:
            pygame.draw.line(screen, RED, (head[0] + CELL_SIZE // 2, head[1] + CELL_SIZE // 2), t, 2)
        elif dy != 0:
            pygame.draw.line(screen, RED, (head[0] + CELL_SIZE // 2, head[1] + CELL_SIZE // 2), t, 2)

def draw_food(food_pos):
    pygame.draw.rect(screen, RED, (*food_pos, CELL_SIZE, CELL_SIZE))

def random_food_position(snake, wall_shrink=0, apples=None):
    # Ensure apples stay within the walls (pixel precision)
    min_x = wall_shrink
    max_x = WIDTH - CELL_SIZE - wall_shrink
    min_y = wall_shrink
    max_y = HEIGHT - CELL_SIZE - wall_shrink
    while True:
        x = random.randint(min_x // CELL_SIZE, max_x // CELL_SIZE) * CELL_SIZE
        y = random.randint(min_y // CELL_SIZE, max_y // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake and (apples is None or (x, y) not in apples) and min_x <= x <= max_x and min_y <= y <= max_y:
            return (x, y)

def show_controls():
    controls = [
        "Controls:",
        "Arrow Keys - Move",
        "Esc - Quit"
    ]
    for i, text in enumerate(controls):
        ctrl_text = font.render(text, True, WHITE)
        screen.blit(ctrl_text, (10, 40 + i * 24))

def show_controls_menu():
    showing = True
    while showing:
        screen.fill(BLACK)
        title_text = font.render("Controls", True, WHITE)
        move_text = font.render("Arrow Keys - Move", True, WHITE)
        esc_text = font.render("Esc - Quit", True, WHITE)
        back_text = font.render("Press any key to return", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - 50, HEIGHT // 2 - 80))
        screen.blit(move_text, (WIDTH // 2 - 90, HEIGHT // 2 - 40))
        screen.blit(esc_text, (WIDTH // 2 - 90, HEIGHT // 2))
        screen.blit(back_text, (WIDTH // 2 - 120, HEIGHT // 2 + 40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                showing = False

def draw_stars():
    # Draw random stars on the background
    for _ in range(80):
        star_x = random.randint(0, WIDTH)
        star_y = random.randint(0, HEIGHT)
        pygame.draw.circle(screen, WHITE, (star_x, star_y), 1)

def main(mode="regular"):
    # 2 Player mode setup
    if mode == "2player":
        speed = 5
        snake1 = [(WIDTH // 4, HEIGHT // 2)]
        dir1 = (CELL_SIZE, 0)  # Start moving right
        snake2 = [(3 * WIDTH // 4, HEIGHT // 2)]
        dir2 = (-CELL_SIZE, 0)  # Start moving left
        score1 = 0
        score2 = 0
        apples = []
        num_apples = 3
        for _ in range(num_apples):
            apples.append(random_food_position(snake1 + snake2, 0, apples))
        running = True
        while running:
            clock.tick(speed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Snake 1 (Arrow keys)
                    if event.key == pygame.K_UP and dir1 != (0, CELL_SIZE):
                        dir1 = (0, -CELL_SIZE)
                    elif event.key == pygame.K_DOWN and dir1 != (0, -CELL_SIZE):
                        dir1 = (0, CELL_SIZE)
                    elif event.key == pygame.K_LEFT and dir1 != (CELL_SIZE, 0):
                        dir1 = (-CELL_SIZE, 0)
                    elif event.key == pygame.K_RIGHT and dir1 != (-CELL_SIZE, 0):
                        dir1 = (CELL_SIZE, 0)
                    # Snake 2 (WASD)
                    elif event.key == pygame.K_w and dir2 != (0, CELL_SIZE):
                        dir2 = (0, -CELL_SIZE)
                    elif event.key == pygame.K_s and dir2 != (0, -CELL_SIZE):
                        dir2 = (0, CELL_SIZE)
                    elif event.key == pygame.K_a and dir2 != (CELL_SIZE, 0):
                        dir2 = (-CELL_SIZE, 0)
                    elif event.key == pygame.K_d and dir2 != (-CELL_SIZE, 0):
                        dir2 = (CELL_SIZE, 0)
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            # Move snakes
            new_head1 = (snake1[0][0] + dir1[0], snake1[0][1] + dir1[1])
            new_head2 = (snake2[0][0] + dir2[0], snake2[0][1] + dir2[1])

            # Check collisions for snake1
            if (new_head1[0] < 0 or new_head1[0] > WIDTH - CELL_SIZE or
                new_head1[1] < 0 or new_head1[1] > HEIGHT - CELL_SIZE or
                new_head1 in snake1 or new_head1 in snake2):
                running = False
            # Check collisions for snake2
            if (new_head2[0] < 0 or new_head2[0] > WIDTH - CELL_SIZE or
                new_head2[1] < 0 or new_head2[1] > HEIGHT - CELL_SIZE or
                new_head2 in snake2 or new_head2 in snake1):
                running = False

            snake1.insert(0, new_head1)
            snake2.insert(0, new_head2)

            # Check apples for both snakes
            ate1 = False
            ate2 = False
            for i, apple in enumerate(apples):
                if new_head1 == apple:
                    score1 += 1
                    apples[i] = random_food_position(snake1 + snake2, 0, apples)
                    ate1 = True
                if new_head2 == apple:
                    score2 += 1
                    apples[i] = random_food_position(snake1 + snake2, 0, apples)
                    ate2 = True
            if not ate1:
                snake1.pop()
            if not ate2:
                snake2.pop()

            # Draw everything
            screen.fill(BLACK)
            # Draw snake 1 (GREEN)
            for segment in snake1[1:]:
                pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
            head1 = snake1[0]
            pygame.draw.rect(screen, DARK_GREEN, (*head1, CELL_SIZE, CELL_SIZE))
            # Eyes and tongue for snake 1
            eye_radius = 3
            offset = 4
            if len(snake1) > 1:
                dx1 = head1[0] - snake1[1][0]
                dy1 = head1[1] - snake1[1][1]
            else:
                dx1, dy1 = CELL_SIZE, 0
            if dx1 > 0:  # Right
                eye1a = (head1[0] + CELL_SIZE - offset, head1[1] + offset)
                eye1b = (head1[0] + CELL_SIZE - offset, head1[1] + CELL_SIZE - offset)
                tongue1 = [(head1[0] + CELL_SIZE, head1[1] + CELL_SIZE // 2)]
            elif dx1 < 0:  # Left
                eye1a = (head1[0] + offset, head1[1] + offset)
                eye1b = (head1[0] + offset, head1[1] + CELL_SIZE - offset)
                tongue1 = [(head1[0], head1[1] + CELL_SIZE // 2)]
            elif dy1 > 0:  # Down
                eye1a = (head1[0] + offset, head1[1] + CELL_SIZE - offset)
                eye1b = (head1[0] + CELL_SIZE - offset, head1[1] + CELL_SIZE - offset)
                tongue1 = [(head1[0] + CELL_SIZE // 2, head1[1] + CELL_SIZE)]
            else:  # Up
                eye1a = (head1[0] + offset, head1[1] + offset)
                eye1b = (head1[0] + CELL_SIZE - offset, head1[1] + offset)
                tongue1 = [(head1[0] + CELL_SIZE // 2, head1[1])]
            pygame.draw.circle(screen, WHITE, eye1a, eye_radius)
            pygame.draw.circle(screen, WHITE, eye1b, eye_radius)
            for t in tongue1:
                pygame.draw.line(screen, RED, (head1[0] + CELL_SIZE // 2, head1[1] + CELL_SIZE // 2), t, 2)

            # Draw snake 2 (BLUE)
            for segment in snake2[1:]:
                pygame.draw.rect(screen, (0, 0, 200), (*segment, CELL_SIZE, CELL_SIZE))
            head2 = snake2[0]
            pygame.draw.rect(screen, (0, 0, 100), (*head2, CELL_SIZE, CELL_SIZE))
            # Eyes and tongue for snake 2
            if len(snake2) > 1:
                dx2 = head2[0] - snake2[1][0]
                dy2 = head2[1] - snake2[1][1]
            else:
                dx2, dy2 = -CELL_SIZE, 0
            if dx2 > 0:  # Right
                eye2a = (head2[0] + CELL_SIZE - offset, head2[1] + offset)
                eye2b = (head2[0] + CELL_SIZE - offset, head2[1] + CELL_SIZE - offset)
                tongue2 = [(head2[0] + CELL_SIZE, head2[1] + CELL_SIZE // 2)]
            elif dx2 < 0:  # Left
                eye2a = (head2[0] + offset, head2[1] + offset)
                eye2b = (head2[0] + offset, head2[1] + CELL_SIZE - offset)
                tongue2 = [(head2[0], head2[1] + CELL_SIZE // 2)]
            elif dy2 > 0:  # Down
                eye2a = (head2[0] + offset, head2[1] + CELL_SIZE - offset)
                eye2b = (head2[0] + CELL_SIZE - offset, head2[1] + CELL_SIZE - offset)
                tongue2 = [(head2[0] + CELL_SIZE // 2, head2[1] + CELL_SIZE)]
            else:  # Up
                eye2a = (head2[0] + offset, head2[1] + offset)
                eye2b = (head2[0] + CELL_SIZE - offset, head2[1] + offset)
                tongue2 = [(head2[0] + CELL_SIZE // 2, head2[1])]
            pygame.draw.circle(screen, WHITE, eye2a, eye_radius)
            pygame.draw.circle(screen, WHITE, eye2b, eye_radius)
            for t in tongue2:
                pygame.draw.line(screen, RED, (head2[0] + CELL_SIZE // 2, head2[1] + CELL_SIZE // 2), t, 2)

            # Draw apples
            for apple in apples:
                draw_food(apple)
            score_text1 = font.render(f"P1 Score: {score1}", True, WHITE)
            score_text2 = font.render(f"P2 Score: {score2}", True, WHITE)
            screen.blit(score_text1, (10, 10))
            screen.blit(score_text2, (WIDTH - 150, 10))
            pygame.display.flip()

        # Game over message and return to home screen
        screen.fill(DARK_RED)
        game_over_text = font.render("Game Over! Press any key to return.", True, WHITE)
        score_text1 = font.render(f"P1 Score: {score1}", True, WHITE)
        score_text2 = font.render(f"P2 Score: {score2}", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 30))
        screen.blit(score_text1, (WIDTH // 2 - 70, HEIGHT // 2 + 10))
        screen.blit(score_text2, (WIDTH // 2 - 70, HEIGHT // 2 + 40))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    waiting = False
        return

    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = (0, -CELL_SIZE)
    score = 0
    wall_shrink = 0

    # Relax mode settings
    if mode == "relax":
        speed = 5  # Steady pace for relax mode
        apples = []
        num_apples = 5
        for _ in range(num_apples):
            apples.append(random_food_position(snake, wall_shrink, apples))
    else:
        speed = 5  # Steady pace for all modes
        food_pos = random_food_position(snake, wall_shrink)

    running = True
    while running:
        clock.tick(speed)

        # Set wall boundaries
        if mode == "impossible":
            wall_margin = wall_shrink
            min_x = wall_margin
            max_x = WIDTH - CELL_SIZE - wall_margin
            min_y = wall_margin
            max_y = HEIGHT - CELL_SIZE - wall_margin
        else:
            min_x = 0
            max_x = WIDTH - CELL_SIZE
            min_y = 0
            max_y = HEIGHT - CELL_SIZE

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if (new_head[0] < min_x or new_head[0] > max_x or
            new_head[1] < min_y or new_head[1] > max_y):
            running = False

        if new_head in snake:
            running = False

        snake.insert(0, new_head)

        if mode == "relax":
            ate_apple = False
            for i, apple in enumerate(apples):
                if new_head == apple:
                    score += 1
                    apples[i] = random_food_position(snake, wall_shrink, apples)
                    ate_apple = True
            if not ate_apple:
                snake.pop()
        else:
            if new_head == food_pos:
                score += 1
                if mode == "regular":
                    speed += 0.2
                    food_pos = random_food_position(snake, wall_shrink)
                elif mode == "impossible":
                    speed += 0.7
                    wall_shrink += 1  # Shrink wall only when apple is eaten
                    food_pos = random_food_position(snake, wall_shrink)
            else:
                snake.pop()

        # Draw everything
        if mode == "relax":
            screen.fill(DARK_GREEN)
        else:
            screen.fill(BLACK)
        if mode == "impossible" and wall_shrink > 0:
            pygame.draw.rect(screen, DARK_RED, (wall_shrink, wall_shrink,
                                                WIDTH - 2 * wall_shrink,
                                                HEIGHT - 2 * wall_shrink), 4)
        draw_snake(snake)
        if mode == "relax":
            for apple in apples:
                draw_food(apple)
        else:
            draw_food(food_pos)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

    # Game over message and return to home screen
    screen.fill(DARK_RED)
    game_over_text = font.render("Game Over! Press any key to return.", True, WHITE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 30))
    screen.blit(score_text, (WIDTH // 2 - 70, HEIGHT // 2 + 10))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                waiting = False

def home_screen():
    while True:
        screen.fill(BLACK)
        draw_stars()
        title_text = font.render("Snake Game", True, WHITE)

        # Mode options and positions
        modes = [
            ("Press 1 for Regular Mode", WIDTH // 2 - 120, HEIGHT // 2 - 80),
            ("Press 2 for Impossible Mode", WIDTH // 2 - 120, HEIGHT // 2 - 40),
            ("Press 3 for Relax Mode", WIDTH // 2 - 120, HEIGHT // 2),
            ("Press 4 for 2 Player Mode", WIDTH // 2 - 120, HEIGHT // 2 + 40),
            ("Press C for Controls", WIDTH // 2 - 120, HEIGHT // 2 + 80),
            ("Press Esc to Quit", WIDTH // 2 - 120, HEIGHT // 2 + 120)
        ]

        # Draw title
        screen.blit(title_text, (WIDTH // 2 - 70, HEIGHT // 2 - 140))

        # Draw mode boxes (all same size)
        box_width = 340
        box_height = 36
        box_margin = 10
        for text, x, y in modes:
            pygame.draw.rect(screen, RED, (x - box_margin, y - box_margin, box_width, box_height), 0)
            mode_text = font.render(text, True, WHITE)
            screen.blit(mode_text, (x, y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main(mode="regular")
                elif event.key == pygame.K_2:
                    main(mode="impossible")
                elif event.key == pygame.K_3:
                    main(mode="relax")
                elif event.key == pygame.K_4:
                    main(mode="2player")
                elif event.key == pygame.K_c:
                    show_controls_menu()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    while True:
        home_screen()