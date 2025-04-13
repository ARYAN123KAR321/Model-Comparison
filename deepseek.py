import pygame
import random

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
GRAVITY = 0.5
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario Snake")

class Player:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = 50
        self.y = SCREEN_HEIGHT - TILE_SIZE - 50
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.velocity_y = 0
        self.on_ground = True
        self.direction = 1
        self.speed = 5
        self.jump_power = -12
        self.tail_positions = []
        self.tail_length = 0

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

    def update(self, platforms):
        # Horizontal movement
        self.x += self.direction * self.speed

        # Vertical movement
        self.y += self.velocity_y
        self.velocity_y += GRAVITY

        # Platform collisions
        self.on_ground = False
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.y = platform.rect.top - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.y = platform.rect.bottom
                    self.velocity_y = 0

        # Update tail
        self.tail_positions.append((self.x, self.y))
        if len(self.tail_positions) > self.tail_length:
            self.tail_positions.pop(0)

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

class Collectible:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.active = True

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.direction = 1
        self.speed = 3

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - TILE_SIZE:
            self.direction *= -1

# Game initialization
player = Player()
platforms = [
    Platform(0, SCREEN_HEIGHT - TILE_SIZE, SCREEN_WIDTH * 10, TILE_SIZE),
    Platform(300, SCREEN_HEIGHT - TILE_SIZE*3, 200, TILE_SIZE),
    Platform(600, SCREEN_HEIGHT - TILE_SIZE*5, 200, TILE_SIZE),
]
collectibles = [Collectible(400, SCREEN_HEIGHT - TILE_SIZE*4)]
enemies = [Enemy(200, SCREEN_HEIGHT - TILE_SIZE*2)]

camera_offset = 0
clock = pygame.time.Clock()
running = True

# Main game loop
while running:
    screen.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.jump()
            elif event.key == pygame.K_LEFT:
                player.direction = -1
            elif event.key == pygame.K_RIGHT:
                player.direction = 1

    # Update game state
    player.update(platforms)
    
    # Update enemies
    for enemy in enemies:
        enemy.update()

    # Collectible collision
    for collectible in collectibles[:]:
        if collectible.active and pygame.Rect(player.x, player.y, 
           player.width, player.height).colliderect(collectible.rect):
            player.tail_length += 5
            collectible.active = False
            collectibles.remove(collectible)
            collectibles.append(Collectible(
                random.randint(camera_offset + SCREEN_WIDTH, camera_offset + SCREEN_WIDTH * 2),
                random.randint(TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE*2)
            ))

    # Collision checks
    for enemy in enemies:
        if pygame.Rect(player.x, player.y, player.width, player.height).colliderect(enemy.rect):
            running = False

    for pos in player.tail_positions[:-10]:
        if pygame.Rect(pos[0], pos[1], player.width, player.height).colliderect(
            player.x, player.y, player.width, player.height):
            running = False

    # Camera scrolling
    if player.x - camera_offset > SCREEN_WIDTH * 0.6:
        camera_offset = player.x - SCREEN_WIDTH * 0.6

    # Drawing
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, 
                        (platform.rect.x - camera_offset, platform.rect.y, 
                         platform.rect.width, platform.rect.height))

    for collectible in collectibles:
        if collectible.active:
            pygame.draw.rect(screen, YELLOW, 
                           (collectible.rect.x - camera_offset, collectible.rect.y, 
                            TILE_SIZE, TILE_SIZE))

    for enemy in enemies:
        pygame.draw.rect(screen, RED, 
                        (enemy.rect.x - camera_offset, enemy.rect.y, 
                         TILE_SIZE, TILE_SIZE))

    pygame.draw.rect(screen, BLUE, 
                    (player.x - camera_offset, player.y, 
                     player.width, player.height))

    for pos in player.tail_positions:
        pygame.draw.rect(screen, WHITE, 
                        (pos[0] - camera_offset, pos[1], 
                         player.width, player.height))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
