import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors (for pipes and text)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Load images from assets folder
BASE_PATH = os.path.dirname(__file__)
BIRD_IMG = pygame.image.load(os.path.join(BASE_PATH, "assets", "bird.png")).convert_alpha()
BIRD_IMG = pygame.transform.scale(BIRD_IMG, (20, 20))  # Scale to match bird_size
SKY_IMG = pygame.image.load(os.path.join(BASE_PATH, "assets", "sky.png")).convert()
SKY_IMG = pygame.transform.scale(SKY_IMG, (WIDTH, HEIGHT))  # Match screen size
GROUND_IMG = pygame.image.load(os.path.join(BASE_PATH, "assets", "ground.png")).convert()
GROUND_HEIGHT = 100
GROUND_IMG = pygame.transform.scale(GROUND_IMG, (WIDTH, GROUND_HEIGHT))  # Ground strip

# Bird properties
bird_x = 100
bird_y = HEIGHT // 2
bird_velocity = 0
bird_size = 20  # Used for collision detection
GRAVITY = 0.5
FLAP = -10

# Pipe properties
pipe_width = 50
pipe_gap = 150
pipe_speed = 3
pipes = []
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks()

# Ground properties
ground_x = 0
ground_speed = pipe_speed  # Match pipe speed for consistency

# Game variables
score = 0
game_over = False
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
FPS = 60

def draw_bird():
    """Draw the bird image at its position"""
    screen.blit(BIRD_IMG, (bird_x, bird_y))

def draw_background():
    """Draw the sky background"""
    screen.blit(SKY_IMG, (0, 0))

def draw_ground():
    """Draw and scroll the ground"""
    global ground_x
    screen.blit(GROUND_IMG, (ground_x, HEIGHT - GROUND_HEIGHT))
    screen.blit(GROUND_IMG, (ground_x + WIDTH, HEIGHT - GROUND_HEIGHT))  # Second image for looping
    ground_x -= ground_speed
    if ground_x <= -WIDTH:
        ground_x += WIDTH  # Loop ground

def draw_pipes():
    """Draw all pipes as green rectangles"""
    for pipe in pipes:
        # Top pipe
        pygame.draw.rect(screen, GREEN, (pipe['x'], 0, pipe_width, pipe['top']))
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, (pipe['x'], pipe['bottom'], pipe_width, HEIGHT - pipe['bottom']))

def check_collision():
    """Check if the bird collides with pipes or screen boundaries"""
    bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)
    for pipe in pipes:
        top_pipe = pygame.Rect(pipe['x'], 0, pipe_width, pipe['top'])
        bottom_pipe = pygame.Rect(pipe['x'], pipe['bottom'], pipe_width, HEIGHT - pipe['bottom'])
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
            return True
    if bird_y <= 0 or bird_y + bird_size >= HEIGHT - GROUND_HEIGHT:
        return True
    return False

def reset_game():
    """Reset the game state"""
    global bird_y, bird_velocity, pipes, score, game_over, last_pipe, ground_x
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    game_over = False
    last_pipe = pygame.time.get_ticks()
    ground_x = 0

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                else:
                    bird_velocity = FLAP

    if not game_over:
        # Update bird
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        # Generate pipes
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > pipe_frequency:
            gap_y = random.randint(150, HEIGHT - 150 - GROUND_HEIGHT)
            pipes.append({
                'x': WIDTH,
                'top': gap_y - pipe_gap // 2,
                'bottom': gap_y + pipe_gap // 2,
                'scored': False
            })
            last_pipe = current_time

        # Update pipes
        for pipe in pipes:
            pipe['x'] -= pipe_speed
            if pipe['x'] + pipe_width < bird_x and not pipe['scored']:
                score += 1
                pipe['scored'] = True

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe['x'] > -pipe_width]

        # Check collisions
        if check_collision():
            game_over = True

    # Draw everything
    draw_background()  # Draw sky first
    draw_pipes()      # Then pipes
    draw_ground()     # Then ground
    draw_bird()       # Then bird (on top)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    if game_over:
        game_over_text = font.render("Game Over! Press SPACE to restart", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))

    # Update display and control frame rate
    pygame.display.flip()
    clock.tick(FPS)

# Clean up and exit
pygame.quit()