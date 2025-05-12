import pygame
import random
import os

# Initialize Pygame (Module: external library for graphics)
pygame.init()

# Set up the game window (Variables: store dimensions)
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors (Data Types: tuples for RGB values)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Load images with error handling (File I/O and try-except)
BASE_PATH = os.path.dirname(__file__)  # File path of the script
try:
    BIRD_IMG = pygame.image.load(os.path.join(BASE_PATH, "assets", "bird.png")).convert_alpha()
    BIRD_IMG = pygame.transform.scale(BIRD_IMG, (20, 20))  # Scale image
    SKY_IMG = pygame.image.load(os.path.join(BASE_PATH, "assets", "sky.png")).convert()
    SKY_IMG = pygame.transform.scale(SKY_IMG, (WIDTH, HEIGHT))
    GROUND_IMG = pygame.image.load(os.path.join(BASE_PATH, "assets", "ground.png")).convert()
    GROUND_HEIGHT = 100
    GROUND_IMG = pygame.transform.scale(GROUND_IMG, (WIDTH, GROUND_HEIGHT))
    GAME_OVER_IMG = pygame.image.load(os.path.join(BASE_PATH, "assets", "game_over.png")).convert_alpha()
    GAME_OVER_IMG = pygame.transform.scale(GAME_OVER_IMG, (300, 100))
    PIPE_TOP_IMG = pygame.image.load(os.path.join(BASE_PATH, "assets", "pipe_top.png")).convert_alpha()
    PIPE_BOTTOM_IMG = pygame.image.load(os.path.join(BASE_PATH, "assets", "pipe_bottom.png")).convert_alpha()
except pygame.error as e:
    print(f"Image loading error: {e}. Using rectangles for pipes.")
    PIPE_TOP_IMG = None
    PIPE_BOTTOM_IMG = None

# Load high score with file I/O (File I/O)
HIGH_SCORE_FILE = os.path.join(BASE_PATH, "high_score.txt")
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0  # Default to 0 if file doesn't exist or is invalid

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

# Bird class (Object-Oriented Programming)
class Bird:
    def __init__(self, x, y, size):
        self.x = x  # Variable: x-position
        self.y = y  # Variable: y-position
        self.velocity = 0  # Variable: movement speed
        self.size = size  # Variable: collision box size
        self.GRAVITY = 0.5  # Constant: gravity effect
        self.FLAP = -10  # Constant: upward force on flap

    def update(self):
        self.velocity += self.GRAVITY  # Update velocity with gravity
        self.y += self.velocity  # Update position

    def flap(self):
        self.velocity = self.FLAP  # Apply flap force

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

# Pipe management (DSA: List as dynamic array)
MAX_PIPES = 5  # DSA: Limit pipes like a queue
pipes = []  # List: stores pipe dictionaries
pipe_speed = 3  # Constant: speed at which pipes move (Fix for undefined variable)

# Ground properties
ground_x = 0
ground_speed = pipe_speed  # Match ground speed to pipe speed

# Game variables
score = 0
high_score = load_high_score()
game_state = "MENU"  # Control Flow: state machine
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
FPS = 60
bird = Bird(100, HEIGHT // 2, 20)  # Instantiate Bird object

def draw_bird():
    """Function: Draw the bird image (encapsulates drawing logic)"""
    screen.blit(BIRD_IMG, (bird.x, bird.y))

def draw_background():
    """Function: Draw the sky background"""
    screen.blit(SKY_IMG, (0, 0))

def draw_ground():
    """Function: Draw and scroll the ground"""
    global ground_x
    screen.blit(GROUND_IMG, (ground_x, HEIGHT - GROUND_HEIGHT))
    screen.blit(GROUND_IMG, (ground_x + WIDTH, HEIGHT - GROUND_HEIGHT))
    if game_state == "PLAYING":
        ground_x -= ground_speed
        if ground_x <= -WIDTH:
            ground_x += WIDTH  # Loop ground

def draw_pipes():
    """Function: Draw pipes using images or rectangles"""
    for pipe in pipes:
        if PIPE_TOP_IMG and PIPE_BOTTOM_IMG:
            top_scaled = pygame.transform.scale(PIPE_TOP_IMG, (50, pipe['top']))
            bottom_scaled = pygame.transform.scale(PIPE_BOTTOM_IMG, (50, HEIGHT - pipe['bottom']))
            screen.blit(top_scaled, (pipe['x'], pipe['top'] - top_scaled.get_height()))
            screen.blit(bottom_scaled, (pipe['x'], pipe['bottom']))
        else:
            pygame.draw.rect(screen, GREEN, (pipe['x'], 0, 50, pipe['top']))
            pygame.draw.rect(screen, GREEN, (pipe['x'], pipe['bottom'], 50, HEIGHT - pipe['bottom']))

def check_collision():
    """Function: Algorithm for collision detection"""
    bird_rect = bird.get_rect()
    for pipe in pipes:
        top_pipe = pygame.Rect(pipe['x'], 0, 50, pipe['top'])
        bottom_pipe = pygame.Rect(pipe['x'], pipe['bottom'], 50, HEIGHT - pipe['bottom'])
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
            return True
    if bird.y <= 0 or bird.y + bird.size >= HEIGHT - GROUND_HEIGHT:
        return True
    return False

def reset_game(full_reset=True):
    """Function: Reset game state with conditional logic"""
    global score, pipes, ground_x
    bird.y = HEIGHT // 2
    bird.velocity = 0
    pipes = []
    if full_reset:
        score = 0
    ground_x = 0

# Main game loop (Control Flow: while loop)
running = True
last_pipe_time = pygame.time.get_ticks()
while running:
    # Event handling (Control Flow: for loop)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == "MENU":
                if event.key == pygame.K_n:  # New Game
                    reset_game(full_reset=True)
                    game_state = "PLAYING"
                elif event.key == pygame.K_c:  # Continue
                    reset_game(full_reset=False)
                    game_state = "PLAYING"
            elif game_state == "PLAYING" and event.key == pygame.K_SPACE:
                bird.flap()
            elif game_state == "GAME_OVER" and event.key == pygame.K_SPACE:
                game_state = "MENU"

    if game_state == "PLAYING":
        # Update bird (Object method)
        bird.update()

        # Generate pipes (DSA: queue-like behavior with limit)
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe_time > 1500 and len(pipes) < MAX_PIPES:
            gap_y = random.randint(150, HEIGHT - 150 - GROUND_HEIGHT)  # Random: generate gap
            pipes.append({'x': WIDTH, 'top': gap_y - 75, 'bottom': gap_y + 75, 'scored': False})
            last_pipe_time = current_time

        # Update pipes (List manipulation)
        for pipe in pipes[:]:  # Copy to avoid modifying during iteration
            pipe['x'] -= pipe_speed
            if pipe['x'] + 50 < bird.x and not pipe['scored']:
                score += 1
                pipe['scored'] = True
        pipes[:] = [pipe for pipe in pipes if pipe['x'] > -50]  # List comprehension

        # Check collisions (Algorithm)
        if check_collision():
            game_state = "GAME_OVER"
            if score > high_score:
                high_score = score
                save_high_score(high_score)

    # Draw everything (Functions)
    draw_background()
    draw_pipes()
    draw_ground()
    draw_bird()
    if game_state == "MENU":
        menu_text1 = font.render("New Game (N)", True, BLACK)
        menu_text2 = font.render("Continue (C)", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(menu_text1, (WIDTH // 2 - 70, HEIGHT // 2 - 50))
        screen.blit(menu_text2, (WIDTH // 2 - 70, HEIGHT // 2))
        screen.blit(high_score_text, (WIDTH // 2 - 70, HEIGHT // 2 + 50))
    elif game_state == "PLAYING":
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
    elif game_state == "GAME_OVER":
        screen.blit(GAME_OVER_IMG, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        score_text = font.render(f"Score: {score}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(score_text, (WIDTH // 2 - 50, HEIGHT // 2 + 70))
        screen.blit(high_score_text, (WIDTH // 2 - 70, HEIGHT // 2 + 100))

    # Update display (Control Flow)
    pygame.display.flip()
    clock.tick(FPS)

# Save high score and exit (File I/O)
if score > high_score:
    save_high_score(score)
pygame.quit()