import pygame
import random

# Game settings
WIDTH, HEIGHT = 800, 600
FPS = 60
TILE_SIZE = 32

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario-Snake Hybrid")
clock = pygame.time.Clock()

# Load assets
mario_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
mario_img.fill((0, 0, 255))  # placeholder blue square

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = mario_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - TILE_SIZE * 2
        self.vel_y = 0
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5
        self.rect.x += dx

        # Gravity
        self.vel_y += 0.5
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.y += self.vel_y

        # Check collisions
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.vel_y > 0:
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -10

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

class Snake:
    def __init__(self):
        self.body = [(WIDTH//4, HEIGHT//2)]
        self.direction = (TILE_SIZE, 0)

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, RED, (*segment, TILE_SIZE, TILE_SIZE))

# Create game objects
player = Player()
platforms = pygame.sprite.Group()
# Ground platform
platforms.add(Platform(0, HEIGHT - TILE_SIZE, WIDTH, TILE_SIZE))
# Floating platforms
platforms.add(Platform(200, 400, TILE_SIZE * 3, TILE_SIZE))
platforms.add(Platform(500, 300, TILE_SIZE * 2, TILE_SIZE))

snake = Snake()

# Items to collect
items = []
for _ in range(5):
    x = random.randrange(0, WIDTH // TILE_SIZE) * TILE_SIZE
    y = random.randrange(0, HEIGHT // TILE_SIZE) * TILE_SIZE
    items.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

# Game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    player.update(platforms)
    snake.move()

    # Check item collection
    head_rect = pygame.Rect(*snake.body[0], TILE_SIZE, TILE_SIZE)
    for item in items[:]:
        if head_rect.colliderect(item):
            items.remove(item)
            snake.grow()
            # spawn new item
            x = random.randrange(0, WIDTH // TILE_SIZE) * TILE_SIZE
            y = random.randrange(0, HEIGHT // TILE_SIZE) * TILE_SIZE
            items.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

    # Draw
    screen.fill(WHITE)
    for plat in platforms:
        screen.blit(plat.image, plat.rect)
    for item in items:
        pygame.draw.rect(screen, (255, 165, 0), item)  # orange items
    player_group = pygame.sprite.Group(player)
    player_group.draw(screen)
    snake.draw(screen)

    pygame.display.flip()

pygame.quit()
