import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# --- Window Settings ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20  # Size of each grid cell
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Snake color
RED = (255, 0, 0)    # Food color
BLUE = (0, 0, 255)   # Obstacle color
YELLOW = (255, 255, 0) # Powerup color

# --- Game Settings ---
FPS = 10
SNAKE_SPEED = 1  # Snake moves 1 grid cell per frame, effectively
OBSTACLE_COUNT = 10  # Number of obstacles
POWERUP_DURATION = 50 # Frames the powerup lasts
GROW_AMOUNT = 3 # How much snake grows after eating food

# --- Mario Elements ---
MARIO_COLOR = (200, 50, 50)  # Example Mario color (red cap)
MARIO_SIZE_X = GRID_SIZE
MARIO_SIZE_Y = GRID_SIZE
JUMP_SPEED = -10
GRAVITY = 0.5
FLOOR_LEVEL = SCREEN_HEIGHT - GRID_SIZE # Y-coordinate of the "floor"
BLOCK_SIZE = GRID_SIZE

# --- Fonts ---
BASIC_FONT = pygame.font.Font('freesansbold.ttf', 18) # Use a default font

# --- Functions ---

def draw_grid():
    """Draws the grid lines on the screen."""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

def generate_food(snake_body, obstacles, mario_pos):
    """Generates the food at a random location, avoiding the snake, obstacles, and Mario."""
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        food_pos = (x, y)
        if (
            food_pos not in snake_body
            and food_pos not in obstacles
            and food_pos != (mario_pos[0] // GRID_SIZE, mario_pos[1] // GRID_SIZE) # Avoid spawning on Mario's initial pos
        ):
            break
    return food_pos

def generate_obstacle():
    """Generates a random obstacle location."""
    x = random.randint(0, GRID_WIDTH - 1)
    y = random.randint(0, GRID_HEIGHT - 1)
    return (x, y)

def display_message(text, color, surface, x, y):
    """Displays text on the screen."""
    text_obj = BASIC_FONT.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def draw_mario(position_x, position_y):
    """Draws Mario on the screen."""
    pygame.draw.rect(screen, MARIO_COLOR, (position_x, position_y, MARIO_SIZE_X, MARIO_SIZE_Y))

def generate_powerup(snake_body, food_pos, obstacles, mario_pos):
    """Generates a power-up at a random location, avoiding snake, food and obstacles."""
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        powerup_pos = (x, y)
        if (powerup_pos not in snake_body and powerup_pos != food_pos and powerup_pos not in obstacles and powerup_pos != (mario_pos[0] // GRID_SIZE, mario_pos[1] // GRID_SIZE)):
            break
    return powerup_pos

# --- Main Game Function ---
def main():
    """Main function to run the game."""
    global screen, clock, SNAKE_SPEED

    # Initialize screen and clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Super Mario Snake")
    clock = pygame.time.Clock()

    # --- Game Variables ---
    snake_body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # Initial snake position
    snake_direction = (1, 0)  # Initial direction (right)
    food_pos = generate_food(snake_body, [], (0,0))  # Initial food position.  Correctly initialized now.
    game_over = False
    mario_pos = [50, FLOOR_LEVEL]  # Initial Mario position
    mario_velocity_y = 0
    is_jumping = False
    obstacles = [generate_obstacle() for _ in range(OBSTACLE_COUNT)] # List of obstacle positions
    score = 0
    powerup_pos = None # No powerup initially
    powerup_active = False
    powerup_timer = 0
    ate_food_this_frame = False #track if food was eaten in current frame
    level = 1
    
    # --- Game Loop ---
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, 1):
                    snake_direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    snake_direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    snake_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    snake_direction = (1, 0)
                elif event.key == pygame.K_SPACE and not is_jumping: # Spacebar for jump
                    mario_velocity_y = JUMP_SPEED
                    is_jumping = True

        # --- Mario Movement ---
        mario_velocity_y += GRAVITY
        mario_pos[1] += mario_velocity_y

        # --- Floor Collision ---
        if mario_pos[1] >= FLOOR_LEVEL:
            mario_pos[1] = FLOOR_LEVEL
            mario_velocity_y = 0
            is_jumping = False

        # --- Snake Movement ---
        new_head = (
            (snake_body[0][0] + snake_direction[0]) % GRID_WIDTH,
            (snake_body[0][1] + snake_direction[1]) % GRID_HEIGHT,
        )

        # --- Collision Detection ---
        if new_head in snake_body[1:]:
            game_over = True  # Game over if snake hits itself
            break

        if new_head in obstacles:
            game_over = True # Game over if snake hits obstacle
            break
        
        ate_food_this_frame = False #reset
        if new_head == (food_pos[0], food_pos[1]):
            snake_body.insert(0, new_head)
            food_pos = generate_food(snake_body, obstacles, mario_pos)
            score += 10
            ate_food_this_frame = True #track
            if score % 50 == 0:  # Increase speed every 50 points
                SNAKE_SPEED += 1
                level += 1
                
            if random.randint(0, 19) == 0: # 5% chance of powerup
                powerup_pos = generate_powerup(snake_body, food_pos, obstacles, mario_pos)

        else:
            snake_body.insert(0, new_head)
            snake_body.pop()

        # --- Power-up Effects ---
        if powerup_active:
            powerup_timer -= 1
            if powerup_timer <= 0:
                powerup_active = False
                SNAKE_SPEED = 1 #reset
                print("Powerup Over")

        # --- Power-up Collision ---
        if powerup_pos and new_head == powerup_pos:
            powerup_active = True
            powerup_timer = POWERUP_DURATION
            powerup_pos = None
            SNAKE_SPEED = 2  # Double the speed
            score += 30
            print("Powerup Collected!")
            if ate_food_this_frame:
                for _ in range(GROW_AMOUNT):
                    snake_body.append(snake_body[-1])

        # --- Drawing ---
        screen.fill(BLACK)
        draw_grid()

        # Draw Snake
        for x, y in snake_body:
            pygame.draw.rect(screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        # Draw Food
        pygame.draw.rect(screen, RED, (food_pos[0] * GRID_SIZE, food_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        # Draw Mario
        draw_mario(mario_pos[0], mario_pos[1])

        # Draw Obstacles
        for x, y in obstacles:
            pygame.draw.rect(screen, BLUE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Draw Powerup
        if powerup_pos:
            pygame.draw.rect(screen, YELLOW, (powerup_pos[0] * GRID_SIZE, powerup_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Display Score
        display_message(f"Score: {score}", WHITE, screen, 100, 20)
        display_message(f"Level: {level}", WHITE, screen, 700, 20)

        if game_over:
            display_message("Game Over!", RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
