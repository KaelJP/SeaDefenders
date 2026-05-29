import pygame
import sys
import random
import os
from pygame.locals import *
from button import Button

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        if os.path.exists(os.path.join(parent_dir, relative_path)):
            base_path = parent_dir
        else:
            base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# COLORS
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
pink = (255, 182, 193)
yellow = (255, 255, 0)
orange = (255, 165, 0)
cyan = (0, 255, 255)
green4 = (0, 139, 0, 255)
gold = (255, 215, 0, 255)
yellow3 = (205, 205, 0, 255)

# SCREEN AND FONT SETTINGS
pygame.init()
screen = pygame.display.set_mode((1000, 700))  # Full-screen size for layout
pygame.display.set_caption('Sea Defenders')
clock = pygame.time.Clock()

def get_font(size):  # Font loader
    return pygame.font.Font(resource_path("fonts/Pixelify Sans.ttf"), size)

def text_font(size):  # Font loader
    return pygame.font.Font(resource_path("fonts/SpicyRice.ttf"), size)

def health_font(size):  # Font loader
    return pygame.font.Font(resource_path("fonts/ConcertOne.ttf"), size)

#sounds
menu_sound = pygame.mixer.Sound(resource_path("audio/menu.mp3"))
battle_sound = pygame.mixer.Sound(resource_path("audio/battle.mp3"))
button_sound = pygame.mixer.Sound(resource_path("audio/button.mp3"))
back_sound = pygame.mixer.Sound(resource_path("audio/back.mp3"))
winner_sound = pygame.mixer.Sound(resource_path("audio/winner.mp3"))


# LOAD IMAGES
try:
    battle_background = pygame.image.load(resource_path("background/battle.jpg")).convert()
    battle_background = pygame.transform.scale(battle_background, (1000, 700))  # Resize background

    # Load sprites
    player1_sprite = pygame.image.load(resource_path("aquatics/aqua.png")).convert_alpha()  # Aqua (Player 1 sprite)
    player2_sprite = pygame.image.load(resource_path("wastes/waste.png")).convert_alpha()  # Waste (Player 2 sprite)
    player1_sprite = pygame.transform.scale(player1_sprite, (200, 200))  # Scale Aqua
    player2_sprite = pygame.transform.flip(pygame.transform.scale(player2_sprite, (200, 200)), True, False)  # Scale and flip Waste to face Aqua

    player1_icon = pygame.image.load(resource_path("players/p1.png")).convert_alpha()
    player1_icon = pygame.transform.scale(player1_icon, (50, 50))  # Load and scale Player 1 icon
    player2_icon = pygame.image.load(resource_path("players/p2.png")).convert_alpha()
    player2_icon = pygame.transform.scale(player2_icon, (50, 50))  # Load and scale Player 2 icon

    # Load platforms
    pf1_sprite = pygame.image.load(resource_path("platform/pf1.png")).convert_alpha()
    pf2_sprite = pygame.image.load(resource_path("platform/pf2.png")).convert_alpha()
    pf1_sprite = pygame.transform.scale(pf1_sprite, (320, 130))  # Enlarge and scale platform 1
    pf2_sprite = pygame.transform.scale(pf2_sprite, (350, 120))  # Enlarge and scale platform 2

    print("Assets loaded successfully.")
except pygame.error as e:
    print(f"Error loading assets: {e}")
    sys.exit()

def draw_health_bar(x, y, name, health, max_health, icon):
    """Draw health bar with a name and icon."""
    pygame.draw.rect(screen, black, (x - 5, y - 5, 220, 40), border_radius=5)
    pygame.draw.rect(screen, white, (x, y, 210, 30), border_radius=5)
    pygame.draw.rect(screen, red, (x + 5, y + 5, 200, 20))  # Full bar background
    pygame.draw.rect(screen, green, (x + 5, y + 5, 200 * (health / max_health), 20))  # Current health proportion
    font = health_font(18)
    name_text = font.render(name, True, white)
    health_text = font.render(f"{health} / {max_health}", True, black)
    screen.blit(name_text, (x + 5, y - 20))
    screen.blit(health_text, (x + 120, y + 5))
    screen.blit(icon, (x - 50, y - 16))  # Display icon beside health bar

def draw_turn_indicator(turn):
    """Draw an indicator at the top to show whose turn it is."""
    pygame.draw.rect(screen, black, (400, 10, 200, 50), border_radius=10)  # Centered and wide
    pygame.draw.rect(screen, white, (405, 15, 190, 40), border_radius=10)

    font = text_font(20)
    if turn == "Player 1":
        text = "Player 1's Turn"
        text_color = black
    else:
        text = "Player 2's Turn"
        text_color = blue

    turn_text = font.render(text, True, text_color)
    turn_rect = turn_text.get_rect(center=(500, 35))  # Perfectly centered
    screen.blit(turn_text, turn_rect)

def draw_dialog_box(message="What will you do?"):
    """Draw the dialog box."""
    pygame.draw.rect(screen, black, (50, 550, 900, 100), border_radius=10)
    pygame.draw.rect(screen, white, (55, 555, 890, 90), border_radius=10)

    font = get_font(25)
    dialog_text = font.render(message, True, black)
    text_rect = dialog_text.get_rect(topleft=(70, 570))  # Align text to the side
    screen.blit(dialog_text, text_rect)

def display_winner(winner):
    winner_sound.play()
    battle_sound.stop()
    """Display the winner screen with fade-in effect."""
    alpha_surface = pygame.Surface((1000, 700))
    alpha_surface.fill(black)
    for alpha in range(0, 256, 10):
        alpha_surface.set_alpha(alpha)
        screen.blit(alpha_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)

    while True:
        screen.fill(black)
        # Center the Winner text
        font = get_font(50)
        text = f"{winner} WINS!"
        winner_text = font.render(text, True, white)
        winner_rect = winner_text.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(winner_text, winner_rect)

        # Center the buttons
        PLAY_AGAIN_BUTTON = Button(image=None, pos=(screen.get_width() // 2, 350), text_input="PLAY AGAIN", font=get_font(30),
                                   base_color="White", hovering_color="Green")
        MAIN_MENU_BUTTON = Button(image=None, pos=(screen.get_width() // 2, 450), text_input="MAIN MENU", font=get_font(30),
                                  base_color="White", hovering_color="Yellow")
        QUIT_BUTTON = Button(image=None, pos=(screen.get_width() // 2, 550), text_input="QUIT", font=get_font(30),
                             base_color="White", hovering_color="Red")

        for button in [PLAY_AGAIN_BUTTON, MAIN_MENU_BUTTON, QUIT_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                button_sound.play()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_AGAIN_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    button_sound.play()
                    play()
                if MAIN_MENU_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    button_sound.play()
                    main_menu()
                if QUIT_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    button_sound.play()
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

        clock.tick(60)

def transition_screen():
    """Screen transition effect."""
    for alpha in range(0, 256, 20):
        transition_surface = pygame.Surface((1000, 700))
        transition_surface.fill(black)
        transition_surface.set_alpha(alpha)
        screen.blit(transition_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)

def death_animation(sprite, x, y):
    """Character death fade-out animation."""
    for alpha in range(255, -1, -15):
        fade_surface = sprite.copy()
        fade_surface.set_alpha(alpha)
        screen.blit(battle_background, (0, 0))
        screen.blit(fade_surface, (x, y))
        pygame.display.update()
        clock.tick(60)

def draw_skill_text(skill_text, pos, mouse_pos, base_color, glow_color):
    """Draw skill text with glow effect when hovered."""
    font = get_font(20)
    if pos[0] < mouse_pos[0] < pos[0] + 150 and pos[1] < mouse_pos[1] < pos[1] + 20:
        skill_text_surface = font.render(skill_text, True, glow_color)
    else:
        skill_text_surface = font.render(skill_text, True, base_color)
    screen.blit(skill_text_surface, pos)

def handle_multiple_characters(player_healths, player_max_healths, player_sprites, x, y):
    """Handle the current character's health and sprite visibility."""
    for i in range(len(player_healths)):
        if player_healths[i] > 0:  # Current character is alive
            return player_sprites[i], player_healths[i], player_max_healths[i]

    return None, 0, 0  # All characters are dead

def handle_multiple_characters(player_healths, player_max_healths, player_sprites, x, y):
    """Handle the current character's health and sprite visibility."""
    for i in range(len(player_healths)):
        if player_healths[i] > 0:  # Current character is alive
            return player_sprites[i], player_healths[i], player_max_healths[i]

    return None, 0, 0  # All characters are dead

def play():
    battle_sound.play()
    # Define three Aqua characters and their health values
    aqua_sprites = [
        pygame.transform.scale(pygame.image.load(resource_path("aquatics/aqua.png")).convert_alpha(), (200, 200)),
        pygame.transform.scale(pygame.image.load(resource_path("aquatics/AQUA2.png")).convert_alpha(), (200, 200)),
        pygame.transform.scale(pygame.image.load(resource_path("aquatics/AQUA3.png")).convert_alpha(), (200, 200))
    ]
    aqua_healths = [100, 100, 100]
    aqua_max_healths = [100, 100, 100]
    aqua_defeated_names = ["Bluphi", "Gyarokku", "Crobster"]

    # Define three Waste characters and their health values
    waste_sprites = [
        pygame.transform.flip(pygame.transform.scale(pygame.image.load(resource_path("wastes/waste.png")).convert_alpha(), (200, 200)), True, False),
        pygame.transform.flip(pygame.transform.scale(pygame.image.load(resource_path("wastes/WASTE2.png")).convert_alpha(), (200, 200)), True, False),
        pygame.transform.flip(pygame.transform.scale(pygame.image.load(resource_path("wastes/WASTE3.png")).convert_alpha(), (200, 200)), True, False)
    ]
    waste_healths = [100, 100, 100]
    waste_max_healths = [100, 100, 100]
    
    player1_heals = 2
    player2_heals = 2
    player1_stunned = False
    player2_stunned = False
    turn = "Player 1"  # Start with Player 1's turn
    dialog_message = "What will you do?"
    
    transition_screen()

    while True:
        # Get the index of the current character for each player
        current_aqua_index = next((i for i, health in enumerate(aqua_healths) if health > 0), None)
        current_waste_index = next((i for i, health in enumerate(waste_healths) if health > 0), None)

        # Get the sprites and health of the current active characters
        current_aqua_sprite = aqua_sprites[current_aqua_index] if current_aqua_index is not None else None
        player1_health = aqua_healths[current_aqua_index] if current_aqua_index is not None else 0
        player1_max_health = aqua_max_healths[current_aqua_index] if current_aqua_index is not None else 0

        current_waste_sprite = waste_sprites[current_waste_index] if current_waste_index is not None else None
        player2_health = waste_healths[current_waste_index] if current_waste_index is not None else 0
        player2_max_health = waste_max_healths[current_waste_index] if current_waste_index is not None else 0

        # Draw background and platforms
        screen.blit(battle_background, (0, 0))
        screen.blit(pf1_sprite, (20, 460))  # Platform for Aqua
        screen.blit(pf2_sprite, (615, 260))  # Platform for Waste

        # Draw current characters if they are alive
        if current_aqua_sprite:
            screen.blit(current_aqua_sprite, (100, 350))
        if current_waste_sprite:
            screen.blit(current_waste_sprite, (700, 165))

        draw_health_bar(100, 250, "MIKE", player1_health, player1_max_health, player1_icon)
        draw_health_bar(700, 50, "RIPTAR", player2_health, player2_max_health, player2_icon)

        # Draw turn indicator
        draw_turn_indicator(turn)

        # Draw dialog box
        draw_dialog_box(dialog_message)

        # Menu buttons (skills)
        GAME_MOUSE_POS = pygame.mouse.get_pos()

        if turn == "Player 1":
            draw_skill_text("AQUA SPLASH", (200, 600), GAME_MOUSE_POS, blue, cyan)
            
            draw_skill_text("WATER SHIELD", (400, 600), GAME_MOUSE_POS, pink, red)
            draw_skill_text("TIDAL CRIT", (600, 600), GAME_MOUSE_POS, yellow3, red)
            draw_skill_text("HEAL", (800, 600), GAME_MOUSE_POS, green4, green)
        else:
            draw_skill_text("POISON SLASH", (200, 600), GAME_MOUSE_POS, red, blue )
            draw_skill_text("TOXIC FOG", (400, 600), GAME_MOUSE_POS, blue, yellow)
            draw_skill_text("STUN", (600, 600), GAME_MOUSE_POS, orange, yellow)
            draw_skill_text("HEAL", (800, 600), GAME_MOUSE_POS, green, yellow)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == "Player 1" and current_aqua_index is not None:
                    if not player1_stunned:
                        if 200 < GAME_MOUSE_POS[0] < 350 and 600 < GAME_MOUSE_POS[1] < 620:
                            crit = random.random() < 0.2
                            damage = 18 if crit else 10
                            dialog_message = f"Player 1 uses Aqua Splash! {'Critical Hit!' if crit else ''} Deals {damage} damage!"
                            waste_healths[current_waste_index] -= damage
                            turn = "Player 2"
                        elif 400 < GAME_MOUSE_POS[0] < 550 and 600 < GAME_MOUSE_POS[1] < 620:
                            dialog_message = "Player 1 uses Water Shield! Reduces next damage by 50%!"
                            player1_stunned = False
                            turn = "Player 2"
                        elif 600 < GAME_MOUSE_POS[0] < 750 and 600 < GAME_MOUSE_POS[1] < 620:
                            damage = 25 if random.random() < 0.3 else 0
                            dialog_message = f"Player 1 uses Tidal Crit! {'Lands a massive hit!' if damage > 0 else 'Missed!'}"
                            waste_healths[current_waste_index] -= damage
                            turn = "Player 2"
                        elif 800 < GAME_MOUSE_POS[0] < 950 and 600 < GAME_MOUSE_POS[1] < 620:
                            if player1_heals > 0:
                                dialog_message = "Player 1 uses Heal! Restores 15 HP!"
                                aqua_healths[current_aqua_index] += 15
                                if aqua_healths[current_aqua_index] > aqua_max_healths[current_aqua_index]:
                                    aqua_healths[current_aqua_index] = aqua_max_healths[current_aqua_index]
                                player1_heals -= 1
                            else:
                                dialog_message = "Player 1 is out of heals!"
                            turn = "Player 2"
                    else:
                        dialog_message = "Player 1 is stunned and misses their turn!"
                        player1_stunned = False
                        turn = "Player 2"

                elif turn == "Player 2" and current_waste_index is not None:
                    if not player2_stunned:
                        if 200 < GAME_MOUSE_POS[0] < 350 and 600 < GAME_MOUSE_POS[1] < 620:
                            crit = random.random() < 0.2
                            damage = 20 if crit else 12
                            dialog_message = f"Player 2 uses Poison Slash! {'Critical Hit!' if crit else ''} Deals {damage} damage!"
                            aqua_healths[current_aqua_index] -= damage
                            turn = "Player 1"
                        elif 400 < GAME_MOUSE_POS[0] < 550 and 600 < GAME_MOUSE_POS[1] < 620:
                            dialog_message = "Player 2 uses Toxic Fog! Player 1 takes damage over time."
                            aqua_healths[current_aqua_index] -= 5  # Damage over time
                            turn = "Player 1"
                        elif 600 < GAME_MOUSE_POS[0] < 750 and 600 < GAME_MOUSE_POS[1] < 620:
                            dialog_message = "Player 2 uses Stun! Player 1 is stunned for 1 turn."
                            player1_stunned = True
                            turn = "Player 1"
                        elif 800 < GAME_MOUSE_POS[0] < 950 and 600 < GAME_MOUSE_POS[1] < 620:
                            if player2_heals > 0:
                                dialog_message = "Player 2 uses Heal! Restores 15 HP!"
                                waste_healths[current_waste_index] += 15
                                if waste_healths[current_waste_index] > waste_max_healths[current_waste_index]:
                                    waste_healths[current_waste_index] = waste_max_healths[current_waste_index]
                                player2_heals -= 1
                            else:
                                dialog_message = "Player 2 is out of heals!"
                            turn = "Player 1"
                    else:
                        dialog_message = "Player 2 is stunned and misses their turn!"
                        player2_stunned = False
                        turn = "Player 1"

        # Handle character death
        if current_aqua_index is not None and aqua_healths[current_aqua_index] <= 0:
            death_animation(aqua_sprites[current_aqua_index], 100, 350)
            aqua_healths[current_aqua_index] = 0
            pygame.time.wait(500)

        if current_waste_index is not None and waste_healths[current_waste_index] <= 0:
            death_animation(waste_sprites[current_waste_index], 700, 165)
            waste_healths[current_waste_index] = 0
            pygame.time.wait(500)
            
        if sum(aqua_healths) <= 0:
            display_winner("MIKE")

        if sum(waste_healths) <= 0:
            display_winner("RIPTAR")
        
        pygame.display.update()

def about():
    """Display the about screen."""
    transition_screen()

    while True:
        ABOUT_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill(white)
        
        ABOUT_TEXT = get_font(55).render("ABOUT", True, black)
        ABOUT_RECT = ABOUT_TEXT.get_rect(center=(500, 90))
        screen.blit(ABOUT_TEXT, ABOUT_RECT)

        description_lines  = [
            "Sea Defenders is a strategic 2-player game that",
            "draws inspiration from Pokémon. Players engage in",
            "battles using aquatic creatures to protect marine life.",
            "Instead of catching creatures, you automatically",
            "receive them when the battle begins.",
            "",
            "With no leveling system, the game focuses purely",
            "on strategy and luck. Make your moves wisely and",
            "enjoy a fun, competitive experience!",""
            ,"Members:", "Pelayo, Karl Jhon P." , "Palencia David Jr. M.", "Casue, Stephen A."
        ]
        ABOUT_BACK = Button(image=None, pos=(500, 660),
                            text_input="BACK", font=get_font(55), base_color="Black", hovering_color="Green")
        ABOUT_BACK.changeColor(ABOUT_MOUSE_POS)
        ABOUT_BACK.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                back_sound.play()
                if ABOUT_BACK.checkForInput(ABOUT_MOUSE_POS):
                    main_menu()

        description_font = get_font(35)
        y_offset = 160  
        for line in description_lines:
            text_surface = description_font.render(line, True, black)
            text_rect = text_surface.get_rect(center=(500, y_offset))  
            screen.blit(text_surface, text_rect)
            y_offset += 35  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        
def main_menu():
    menu_sound.play()
    """Display the main menu."""
    BG = pygame.image.load(resource_path("background/menu.jpg")).convert()
    BG = pygame.transform.scale(BG, (1000, 700))

    # Load button images
    play_button_image = pygame.image.load(resource_path("assets/play_button.png")).convert_alpha()
    about_button_image = pygame.image.load(resource_path("assets/about_button.png")).convert_alpha()
    quit_button_image = pygame.image.load(resource_path("assets/quit_button.png")).convert_alpha()
    
    
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = text_font(100).render("SEA DEFENDERS", True, "Blue")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 100))

        PLAY_BUTTON = Button(image=play_button_image, pos=(500, 300), text_input="START", 
                             font=get_font(35), base_color="White", hovering_color="Green")
        ABOUT_BUTTON = Button(image=about_button_image, pos=(500, 400), text_input="ABOUT", 
                              font=get_font(35), base_color="White", hovering_color="Green")
        QUIT_BUTTON = Button(image=quit_button_image, pos=(500, 500), text_input="QUIT", 
                             font=get_font(35), base_color="White", hovering_color="Red")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, ABOUT_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    button_sound.play()
                    menu_sound.stop()  
                    play()
                if ABOUT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    button_sound.play()
                    menu_sound.stop()  
                    about()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()