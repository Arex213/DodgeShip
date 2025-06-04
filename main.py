import pygame
import random 
import sys

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("DodgeShip")
clock = pygame.time.Clock()

# Load assets
ship_image_raw=pygame.image.load("sprites/ship.png").convert_alpha()
ship_image = pygame.transform.scale(ship_image_raw, (ship_image_raw.get_width() * 2, ship_image_raw.get_height() * 2))
ship_rect = ship_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
obstacle_image_raw = pygame.image.load("sprites/obstacle.png").convert_alpha()
obstacle_image = pygame.transform.scale(obstacle_image_raw, (obstacle_image_raw.get_width() * 2, obstacle_image_raw.get_height() * 2))
obstacle_rect = obstacle_image.get_rect(center=(random.randint(0, SCREEN_WIDTH), 0))
background=pygame.image.load("sprites/bg1.png").convert_alpha()
background=pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))

# Game variables
score = 0
game_over = False
x=0; y=0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw everything
    screen.fill(BLACK)
    screen.blit(background,(x,y))
    screen.blit(background,(x,y-SCREEN_HEIGHT))
    screen.blit(ship_image, ship_rect)
    screen.blit(obstacle_image, obstacle_rect)

    if not game_over:
        # Move the obstacle
        obstacle_rect.y += 10 
        if obstacle_rect.y > SCREEN_HEIGHT:
            obstacle_rect.y = 0
            obstacle_rect.x = random.randint(0, SCREEN_WIDTH)
            score += 1

        # Check for collisions
        if ship_rect.colliderect(obstacle_rect):
            game_over = True
        
        # Moving background
        y +=1
        if y==SCREEN_HEIGHT:
            y=0

        if score >=15:
             obstacle_rect.y +=3
             y +=3

        # Handle ship movement
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and ship_rect.top > 0:
            ship_rect.y -= 7
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and ship_rect.bottom < SCREEN_HEIGHT:
            ship_rect.y += 7
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and ship_rect.left > 0:
            ship_rect.x -= 7
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and ship_rect.right < SCREEN_WIDTH:
            ship_rect.x += 7

        # Keep the ship within the screen bounds
        ship_rect.clamp_ip(screen.get_rect())

        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))


    if game_over:
        game_over_text = font.render("Game Over", True, RED)
        score_text = font.render(f"Score: {score}", True, YELLOW)
        restart_button = pygame.key.get_pressed()
        if restart_button[pygame.K_r]:
            game_over = False
            score = 0
            y=0 # Reset background position
            ship_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
            obstacle_rect.center = (random.randint(0, SCREEN_WIDTH), 0)
        restart_text = font.render("Press R to Restart", True, GREEN)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + -20))

    pygame.display.flip()
    clock.tick(FPS)


