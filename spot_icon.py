import pygame
import random
import os
import sys

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spot the Icon [Singapore Edition]")
FPS = 60
FONT = pygame.font.Font('assets/PlaywriteHU-VariableFont_wght.ttf', 28)

# --- Load Images ---
ASSET_FOLDER = 'assets'
ICON_NAMES = [
    "chilli_crab.png",
    "marina_bay_sands.png",
    "changi_airport.png",
    "art_sci_museum.png",
    "singapore_flyer.jpg",
    "merlion.png",
    "eiffel_tower.png",
    "great_wall.png",
    "big_ben.png",
    "pyramid.jpg",
    "statue_of_liberty.jpg",
    "leaning_tower_of_pisa.png"
]

# Helper to load and scale images
def load_icon(name):
    path = os.path.join(ASSET_FOLDER, name)
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (100, 100))

ICONS = {name: load_icon(name) for name in ICON_NAMES}

# --- Collision Prevention Helpers ---
MIN_DISTANCE = 120  # Minimum distance between icon centers

def is_far_enough(new_rect, existing_rects, min_dist):
    for rect in existing_rects:
        dx = new_rect.centerx - rect.centerx
        dy = new_rect.centery - rect.centery
        distance = (dx**2 + dy**2) ** 0.5
        if distance < min_dist:
            return False
    return True

# --- Game Object ---
class GameIcon:
    def __init__(self, name, existing_rects):
        self.name = name
        self.image = ICONS[name]
        self.rect = self.image.get_rect()

        # Try positions until a non-overlapping one is found
        while True:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(100, HEIGHT - self.rect.height)
            if is_far_enough(self.rect, existing_rects, MIN_DISTANCE):
                break

        # Random floating velocity
        self.dx = random.choice([-1, 1]) * random.uniform(0.5, 1.0)
        self.dy = random.choice([-1, 1]) * random.uniform(0.5, 1.0)

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce off edges
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.dx *= -1
        if self.rect.top < 100 or self.rect.bottom > HEIGHT:
            self.dy *= -1

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# --- UI Screens ---
def draw_start_screen():
    SCREEN.fill((255, 255, 255))  # white background

    # Title Text
    title = FONT.render("Welcome to Spot the Icon [Singapore Edition]", True, (255, 0, 0))
    prompt = FONT.render("Click anywhere to start", True, (255, 0, 0))
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
    SCREEN.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 300))
    pygame.display.flip()

def draw_game_screen(target_name, icons):
    SCREEN.fill((240, 248, 255))  # Background
    target_text = FONT.render(f"Find: {target_name.split('.')[0].replace('_', ' ').title()}", True, (0, 0, 0))
    SCREEN.blit(target_text, (WIDTH // 2 - target_text.get_width() // 2, 20))

    for icon in icons:
        icon.move()
        icon.draw(SCREEN)

    pygame.display.flip()

def draw_end_screen(correct):
    SCREEN.fill((240, 248, 255))
    msg = "Good job!" if correct else "Oops, try again!"
    feedback = FONT.render(msg, True, (0, 200, 0) if correct else (200, 0, 0))
    prompt = FONT.render("Click to play again", True, (100, 100, 100))
    SCREEN.blit(feedback, (WIDTH // 2 - feedback.get_width() // 2, 250))
    SCREEN.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 320))
    pygame.display.flip()

# --- Main Game ---
def main():
    clock = pygame.time.Clock()
    game_state = "start"
    target_icon = None
    icons = []
    correct_selection = False

    while True:
        clock.tick(FPS)

        # State control
        if game_state == "start":
            draw_start_screen()
        elif game_state == "play":
            draw_game_screen(target_icon.name, icons)
        elif game_state == "end":
            draw_end_screen(correct_selection)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "start":
                    # Generate icons with spacing
                    chosen_icons = random.sample(ICON_NAMES, 5)
                    target_name = random.choice(chosen_icons)
                    icons = []
                    used_rects = []

                    for name in chosen_icons:
                        icon = GameIcon(name, used_rects)
                        used_rects.append(icon.rect)
                        icons.append(icon)

                    target_icon = [icon for icon in icons if icon.name == target_name][0]
                    game_state = "play"

                elif game_state == "play":
                    pos = pygame.mouse.get_pos()
                    for icon in icons:
                        if icon.rect.collidepoint(pos):
                            correct_selection = (icon.name == target_icon.name)
                            game_state = "end"
                            break

                elif game_state == "end":
                    game_state = "start"

if __name__ == "__main__":
    main()
