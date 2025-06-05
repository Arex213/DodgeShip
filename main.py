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

SLOW_MOTION_EVENT = pygame.USEREVENT + 2
SMALLER_OBSTACLE_EVENT = pygame.USEREVENT + 3

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

slow_motion_pu_image_raw = pygame.image.load("sprites/slow_motion.png").convert_alpha()
slow_motion_pu_image = pygame.transform.scale(slow_motion_pu_image_raw, (ship_image_raw.get_width() * 1.5, ship_image_raw.get_height() * 1.5))
slow_motion_pu_rect = slow_motion_pu_image.get_rect(center=(random.randint(100, 700), random.randint(500, 550)))

smaller_obstacle_pu_image_raw = pygame.image.load("sprites/smaller_obstacle.png").convert_alpha()
smaller_obstacle_pu_image = pygame.transform.scale(smaller_obstacle_pu_image_raw, (obstacle_image_raw.get_width() * 1.5, obstacle_image_raw.get_height() * 1.5))
smaller_obstacle_pu_rect = smaller_obstacle_pu_image.get_rect(center=(random.randint(100, 700), random.randint(500, 550)))

# Game variables
score = 0
game_over = False
x=0; y=0
in_main_menu = True
high_score = 0

# Power-up functions
def slow_motion_powerup():
    global FPS
    FPS = 30  # Reduce FPS for slow motion effect
    pygame.time.set_timer(pygame.USEREVENT, 5000)  # Reset FPS after 5 seconds

def smaller_obstacle_powerup():
    global obstacle_image, obstacle_rect
    obstacle_image = pygame.transform.scale(obstacle_image_raw, (obstacle_image_raw.get_width() // 2, obstacle_image_raw.get_height() // 2))
    obstacle_rect = obstacle_image.get_rect(center=obstacle_rect.center) # Update the rect to match the new image size
    pygame.time.set_timer(pygame.USEREVENT + 1, 5000)  # Reset obstacle size after 5 seconds

def spawn_slow_motion_powerup():
    global slow_motion_pu_rect
    slow_motion_pu_rect.x = random.randint(100, 700)
    slow_motion_pu_rect.y = random.randint(500, 550)

def spawn_smaller_obstacle_powerup():
    global smaller_obstacle_pu_rect
    smaller_obstacle_pu_rect.x = random.randint(100, 700)
    smaller_obstacle_pu_rect.y = random.randint(500, 550)

# Set up power-up timers
pygame.time.set_timer(SLOW_MOTION_EVENT, 30000)  # Spawn slow motion every 30 seconds
pygame.time.set_timer(SMALLER_OBSTACLE_EVENT, 40000)  # Spawn smaller obstacle every 40 seconds

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.USEREVENT:
            FPS = 60  # Reset FPS to normal after slow motion
            pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop the timer
        if event.type == pygame.USEREVENT + 1:
            obstacle_image = pygame.transform.scale(obstacle_image_raw, (obstacle_image_raw.get_width() * 2, obstacle_image_raw.get_height() * 2))
            obstacle_rect = obstacle_image.get_rect(center=obstacle_rect.center)
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
        if event.type == SLOW_MOTION_EVENT:
            if slow_motion_pu_rect.x < 0:  # Only spawn if not already active
                spawn_slow_motion_powerup()
        if event.type == SMALLER_OBSTACLE_EVENT:
            if smaller_obstacle_pu_rect.x < 0:  # Only spawn if not already active
                spawn_smaller_obstacle_powerup()

    # Draw everything
    screen.fill(BLACK)
    screen.blit(background,(x,y))
    screen.blit(background,(x,y-SCREEN_HEIGHT))
    screen.blit(ship_image, ship_rect)
    screen.blit(obstacle_image, obstacle_rect)

    if in_main_menu:
        screen.fill(BLACK)
        title_text = font.render("DodgeShip", True, WHITE)
        start_text = font.render("Press Enter to Start", True, GREEN)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            in_main_menu = False
            score = 0
            y=0

    if not game_over and not in_main_menu:
        # Move the obstacle
        obstacle_rect.y += 10 
        if obstacle_rect.y > SCREEN_HEIGHT:
            obstacle_rect.y = 0
            obstacle_rect.x = random.randint(0, SCREEN_WIDTH)
            score += 1
            high_score = max(high_score, score)

        # Check for collisions
        if ship_rect.colliderect(obstacle_rect):
            game_over = True
        
        if ship_rect.colliderect(slow_motion_pu_rect):
            slow_motion_powerup()
            slow_motion_pu_rect.x = -100 # Move off-screen
            slow_motion_pu_rect.y = -100

        if ship_rect.colliderect(smaller_obstacle_pu_rect):
            smaller_obstacle_powerup()
            smaller_obstacle_pu_rect.x = -100 # Move off-screen
            smaller_obstacle_pu_rect.y = -100
        
        # Moving background
        y +=2
        if y==SCREEN_HEIGHT:
            y=0

        if score >=15:
             obstacle_rect.y +=3

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

    if not in_main_menu:
        # Draw power-ups only if they are on the screen
        if slow_motion_pu_rect.x >= 0:
            screen.blit(slow_motion_pu_image, slow_motion_pu_rect)
        if smaller_obstacle_pu_rect.x >= 0:
            screen.blit(smaller_obstacle_pu_image, smaller_obstacle_pu_rect)

    if game_over:
        game_over_text = font.render("Game Over", True, RED)
        score_text = font.render(f"Score: {score}", True, BLUE)
        if score > high_score:
            high_score = score
        high_score_text = font.render(f"High Score: {high_score}", True, YELLOW)
        restart_text = font.render("Press R to Restart", True, GREEN)
        restart_button = pygame.key.get_pressed()
        if restart_button[pygame.K_r]:
            game_over = False
            score = 0
            y=0 # Reset background position
            ship_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
            obstacle_rect.center = (random.randint(0, SCREEN_WIDTH), 0)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + +20))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))

    pygame.display.flip()
    clock.tick(FPS)