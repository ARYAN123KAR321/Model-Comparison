import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
SNAKE_SPEED = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Snake")
clock = pygame.time.Clock()

# Load images (using simple shapes for now, can be replaced with actual sprites)
def load_images():
    images = {
        'mario_head': pygame.Surface((GRID_SIZE, GRID_SIZE)),
        'snake_body': pygame.Surface((GRID_SIZE, GRID_SIZE)),
        'coin': pygame.Surface((GRID_SIZE, GRID_SIZE)),
        'brick': pygame.Surface((GRID_SIZE, GRID_SIZE)),
        'enemy': pygame.Surface((GRID_SIZE, GRID_SIZE)),
        'mushroom': pygame.Surface((GRID_SIZE, GRID_SIZE))
    }
    
    # Color the surfaces
    images['mario_head'].fill(RED)
    images['snake_body'].fill(GREEN)
    images['coin'].fill(YELLOW)
    images['brick'].fill(BROWN)
    images['enemy'].fill(BLACK)
    images['mushroom'].fill(RED)
    
    return images

class MarioSnake:
    def __init__(self):
        self.reset()
        self.images = load_images()
    
    def reset(self):
        # Snake properties
        self.length = 3
        self.positions = [(WIDTH // 2, HEIGHT - 2 * GRID_SIZE)]
        self.direction = (GRID_SIZE, 0)
        self.score = 0
        
        # Mario-like properties
        self.jumping = False
        self.jump_count = 0
        self.gravity = 1
        self.on_ground = True
        self.jump_height = 10
        
        # Game elements
        self.coins = []
        self.bricks = []
        self.enemies = []
        self.mushrooms = []
        
        # Generate initial level
        self.generate_level()
    
    def generate_level(self):
        # Create floor
        for x in range(0, WIDTH, GRID_SIZE):
            self.bricks.append((x, HEIGHT - GRID_SIZE))
        
        # Create some platforms
        platforms = [
            (100, HEIGHT - 6 * GRID_SIZE, 7),
            (300, HEIGHT - 8 * GRID_SIZE, 5),
            (500, HEIGHT - 4 * GRID_SIZE, 6)
        ]
        
        for platform in platforms:
            x, y, length = platform
            for i in range(length):
                self.bricks.append((x + i * GRID_SIZE, y))
        
        # Add some random coins
        for _ in range(10):
            x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
            y = random.randint(0, (HEIGHT // GRID_SIZE) - 3) * GRID_SIZE
            if (x, y) not in self.bricks and (x, y) not in self.coins:
                self.coins.append((x, y))
        
        # Add some enemies
        for _ in range(3):
            x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
            y = HEIGHT - 2 * GRID_SIZE
            if (x, y) not in self.positions and (x, y) not in self.enemies:
                self.enemies.append([x, y, 1])  # x, y, direction
        
        # Add some mushrooms (power-ups)
        for _ in range(2):
            x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
            y = random.randint(0, (HEIGHT // GRID_SIZE) - 3) * GRID_SIZE
            if (x, y) not in self.bricks and (x, y) not in self.coins and (x, y) not in self.mushrooms:
                self.mushrooms.append((x, y))
    
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.on_ground:
                    self.jumping = True
                    self.on_ground = False
                    self.jump_count = self.jump_height
                elif event.key == pygame.K_LEFT:
                    self.direction = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT:
                    self.direction = (GRID_SIZE, 0)
    
    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        
        # Handle jumping
        if self.jumping:
            head_y -= self.jump_count
            self.jump_count -= self.gravity
            if self.jump_count < -self.jump_height:
                self.jumping = False
        else:
            # Apply gravity if not on ground
            if not self.on_ground:
                head_y += self.gravity * 2
        
        # Move horizontally
        new_x = head_x + dir_x
        
        # Wrap around screen horizontally
        if new_x < 0:
            new_x = WIDTH - GRID_SIZE
        elif new_x >= WIDTH:
            new_x = 0
        
        new_position = (new_x, head_y)
        
        # Check collision with ground and platforms
        self.on_ground = False
        for brick in self.bricks:
            brick_x, brick_y = brick
            # Check if snake head is directly above a brick and not jumping up
            if new_x == brick_x and head_y + GRID_SIZE <= brick_y and head_y + GRID_SIZE + self.gravity * 2 >= brick_y:
                new_position = (new_x, brick_y - GRID_SIZE)
                self.on_ground = True
                break
        
        # Update positions list with new head position
        self.positions.insert(0, new_position)
        
        # Remove tail if we didn't eat anything
        if len(self.positions) > self.length:
            self.positions.pop()
    
    def check_collisions(self):
        head = self.positions[0]
        
        # Check for collision with coins
        for coin in self.coins[:]:
            if head == coin:
                self.coins.remove(coin)
                self.score += 10
                self.length += 1
                
                # Add new coin
                while True:
                    x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
                    y = random.randint(0, (HEIGHT // GRID_SIZE) - 3) * GRID_SIZE
                    if (x, y) not in self.bricks and (x, y) not in self.coins:
                        self.coins.append((x, y))
                        break
        
        # Check for collision with mushrooms
        for mushroom in self.mushrooms[:]:
            if head == mushroom:
                self.mushrooms.remove(mushroom)
                self.score += 50
                self.length += 3
                
                # Add new mushroom
                while True:
                    x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
                    y = random.randint(0, (HEIGHT // GRID_SIZE) - 3) * GRID_SIZE
                    if (x, y) not in self.bricks and (x, y) not in self.coins and (x, y) not in self.mushrooms:
                        self.mushrooms.append((x, y))
                        break
        
        # Check for collision with enemies
        for enemy in self.enemies[:]:
            if head == (enemy[0], enemy[1]):
                # Check if falling onto enemy (mario-like stomp)
                if self.direction[1] > 0 and not self.on_ground:
                    self.enemies.remove(enemy)
                    self.score += 30
                    # Add new enemy
                    x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
                    y = HEIGHT - 2 * GRID_SIZE
                    self.enemies.append([x, y, 1])
                else:
                    # Game over
                    self.reset()
                    return True
        
        # Check for collision with own body (excluding head)
        if head in self.positions[1:]:
            self.reset()
            return True
        
        # Check for collision with bricks
        for brick in self.bricks:
            if head == brick:
                self.reset()
                return True
        
        return False
    
    def update_enemies(self):
        for enemy in self.enemies:
            # Move enemy horizontally
            enemy[0] += enemy[2] * GRID_SIZE
            
            # Check if enemy is on ground
            on_ground = False
            for brick in self.bricks:
                if (enemy[0], enemy[1] + GRID_SIZE) == brick:
                    on_ground = True
                    break
            
            # Apply gravity if needed
            if not on_ground:
                enemy[1] += GRID_SIZE
            
            # Check for collisions with bricks on sides and change direction
            for brick in self.bricks:
                if (enemy[0] + enemy[2] * GRID_SIZE, enemy[1]) == brick:
                    enemy[2] *= -1
                    break
            
            # Check if enemy is at screen edge
            if enemy[0] <= 0 or enemy[0] >= WIDTH - GRID_SIZE:
                enemy[2] *= -1
    
    def draw(self, screen):
        # Draw background
        screen.fill(SKY_BLUE)
        
        # Draw bricks
        for brick in self.bricks:
            screen.blit(self.images['brick'], brick)
        
        # Draw coins
        for coin in self.coins:
            screen.blit(self.images['coin'], coin)
        
        # Draw enemies
        for enemy in self.enemies:
            screen.blit(self.images['enemy'], (enemy[0], enemy[1]))
        
        # Draw mushrooms
        for mushroom in self.mushrooms:
            screen.blit(self.images['mushroom'], mushroom)
        
        # Draw snake body
        for position in self.positions[1:]:
            screen.blit(self.images['snake_body'], position)
        
        # Draw snake head (mario)
        screen.blit(self.images['mario_head'], self.positions[0])
        
        # Draw score
        font = pygame.font.SysFont('Arial', 20)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))

def main():
    game = MarioSnake()
    
    # Game loop
    while True:
        game.handle_keys()
        game.move()
        game.check_collisions()
        game.update_enemies()
        game.draw(screen)
        
        pygame.display.update()
        clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    main()
