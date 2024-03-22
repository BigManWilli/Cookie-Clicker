import pygame
import sys
import json

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COOKIE_COLOR = (255, 215, 0)
CLICK_COLOR = (255, 255, 255)
UPGRADE_COLOR = (0, 255, 0)
FPS = 60
SAVE_FILE = "save.json"
CLICK_FLASH_DURATION = 0.1
UPGRADE_FLASH_DURATION = 0.5

# Game variables
cookie_count = 0
click_value = 1
auto_click_value = 0
upgrade_multiplier = 1.2  # Multiplier for increasing upgrade costs
upgrades = {
    "Grandma's Recipe": {"quantity": 0, "base_cost": 10, "click_value": 2, "auto_click_value": 0},
    "Cookie Factory": {"quantity": 0, "base_cost": 50, "click_value": 5, "auto_click_value": 0},
    "Chocolate Chips": {"quantity": 0, "base_cost": 100, "click_value": 0, "auto_click_value": 1},
    "Cookie Truck": {"quantity": 0, "base_cost": 200, "click_value": 10, "auto_click_value": 0},
    "Cookie Castle": {"quantity": 0, "base_cost": 500, "click_value": 0, "auto_click_value": 5},
    "Cookie Continent": {"quantity": 0, "base_cost": 1000, "click_value": 20, "auto_click_value": 10},
    "Cookie Planet": {"quantity": 0, "base_cost": 2000, "click_value": 0, "auto_click_value": 20},
    "Cookie Universe": {"quantity": 0, "base_cost": 5000, "click_value": 50, "auto_click_value": 50},
    "Galactic Bakery": {"quantity": 0, "base_cost": 10000, "click_value": 100, "auto_click_value": 100},
    "Cookie Nebula": {"quantity": 0, "base_cost": 20000, "click_value": 0, "auto_click_value": 200},
    "Cookie Dimension": {"quantity": 0, "base_cost": 50000, "click_value": 200, "auto_click_value": 500},
    "Golden Oven": {"quantity": 0, "base_cost": 100000, "click_value": 500, "auto_click_value": 1000},
    "Rainbow Sprinkles": {"quantity": 0, "base_cost": 200000, "click_value": 0, "auto_click_value": 5000},
}

# Load save data
try:
    with open(SAVE_FILE, "r") as file:
        save_data = json.load(file)
        cookie_count = save_data.get("cookie_count", 0)
        click_value = save_data.get("click_value", 1)
        auto_click_value = save_data.get("auto_click_value", 0)
        for upgrade in upgrades:
            upgrades[upgrade]["quantity"] = save_data.get(upgrade, 0)
except FileNotFoundError:
    pass

# Set up the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cookie Clicker")
clock = pygame.time.Clock()

# Load images
cookie_img = pygame.image.load("cookie.jpg")
cookie_img = pygame.transform.scale(cookie_img, (150, 150))  # Make the cookie smaller
cookie_rect = cookie_img.get_rect(center=(WIDTH // 4, HEIGHT // 2))  # Move the cookie to the left

# Fonts
font = pygame.font.SysFont("Arial", 32)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def save_progress():
    data_to_save = {
        "cookie_count": cookie_count,
        "click_value": click_value,
        "auto_click_value": auto_click_value
    }
    for upgrade in upgrades:
        data_to_save[upgrade] = upgrades[upgrade]["quantity"]
    with open(SAVE_FILE, "w") as file:
        json.dump(data_to_save, file)

def draw_click_effect():
    pygame.draw.circle(screen, CLICK_COLOR, (cookie_rect.centerx, cookie_rect.centery), 60, width=10)

def draw_upgrade_effect():
    pygame.draw.rect(screen, UPGRADE_COLOR, cookie_rect)

# Main game loop
running = True
click_flash_timer = 0
upgrade_flash_timer = 0
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_progress()
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if cookie_rect.collidepoint(event.pos):
                cookie_count += click_value
                click_flash_timer = CLICK_FLASH_DURATION
            else:
                for i, upgrade in enumerate(upgrades):
                    upgrade_rect = pygame.Rect(WIDTH // 2, 10 + i * 50, 300, 50)
                    if upgrade_rect.collidepoint(event.pos):
                        upgrade_data = upgrades[upgrade]
                        cost = upgrade_data["base_cost"] * (upgrade_multiplier ** upgrade_data["quantity"])
                        if cookie_count >= cost:
                            cookie_count -= cost
                            upgrades[upgrade]["quantity"] += 1
                            click_value += upgrade_data["click_value"]
                            auto_click_value += upgrade_data["auto_click_value"]
                            upgrade_flash_timer = UPGRADE_FLASH_DURATION

    # Update auto-clicker
    cookie_count += auto_click_value / FPS

    # Draw cookie
    screen.blit(cookie_img, cookie_rect)

    # Draw cookie count
    draw_text(f"Cookies: {int(cookie_count)}", font, WHITE, 10, 10)

    # Draw upgrades
    for i, upgrade in enumerate(upgrades):
        upgrade_data = upgrades[upgrade]
        cost = upgrade_data["base_cost"] * (upgrade_multiplier ** upgrade_data["quantity"])
        draw_text(f"{upgrade} ({upgrade_data['quantity']}): {int(cost)} cookies", font, WHITE, WIDTH // 2, 10 + i * 50)

    # Draw passive income
    draw_text(f"Passive income: {auto_click_value} cookies per second", font, WHITE, 10, HEIGHT - 50)

    # Draw click effect
    if click_flash_timer > 0:
        draw_click_effect()
        click_flash_timer -= 1 / FPS

    # Draw upgrade effect
    if upgrade_flash_timer > 0:
        draw_upgrade_effect()
        upgrade_flash_timer -= 1 / FPS

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
