import pygame
import random
import os
import sys

# --- Pygame Initialization ---
pygame.init()
pygame.mixer.init()

# --- Screen Dimensions ---
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixel Hunter: Forest Pursuit")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (100, 150, 50) # Forest ground color
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
LIGHT_BROWN = (160, 82, 45) # For lighter fur/tails
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200) # For rabbit/squirrel
LIGHT_BLUE = (173, 216, 230) # For songbird

# --- Game Clock ---
CLOCK = pygame.time.Clock()
FPS = 60

# --- Fonts ---
FONT_XL = pygame.font.Font(None, 74)
FONT_LG = pygame.font.Font(None, 48)
FONT_MD = pygame.font.Font(None, 36)
FONT_SM = pygame.font.Font(None, 24)

# --- Asset Generation (Draw shapes instead of loading images) ---
def generate_drawn_image(name, size, scale=1):
    # Create a surface with per-pixel alpha for drawing
    image = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
    
    if "crosshair" in name:
        # Custom crosshair
        half_w, half_h = size[0] // 2, size[1] // 2
        pygame.draw.circle(image, WHITE, (half_w, half_h), 10, 1) # Outer ring
        pygame.draw.line(image, WHITE, (half_w - 15, half_h), (half_w + 15, half_h), 2) # Horizontal line
        pygame.draw.line(image, WHITE, (half_w, half_h - 15), (half_w, half_h + 15), 2) # Vertical line
    elif "background" in name:
        # Forest background: sky, ground, trees, bushes
        image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)) # No SRCALPHA for background
        image.fill(LIGHT_BLUE) # Sky
        
        # Ground
        ground_height = 200
        pygame.draw.rect(image, LIGHT_GREEN, (0, SCREEN_HEIGHT - ground_height, SCREEN_WIDTH, ground_height))
        
        # Simple trees
        for _ in range(20):
            x = random.randint(-50, SCREEN_WIDTH + 50)
            y_base = random.randint(SCREEN_HEIGHT - ground_height - 100, SCREEN_HEIGHT - 50)
            trunk_width = random.randint(15, 40)
            trunk_height = random.randint(80, 200)
            leaf_size = random.randint(70, 150)
            
            # Trunk
            pygame.draw.rect(image, BROWN, (x, y_base - trunk_height, trunk_width, trunk_height))
            # Leaves (simple triangle or circle cluster)
            leaf_color = (0, random.randint(80, 150), 0)
            if random.random() < 0.5: # Conifer style
                pygame.draw.polygon(image, leaf_color, [
                    (x - leaf_size // 3, y_base - trunk_height * 0.7),
                    (x + trunk_width + leaf_size // 3, y_base - trunk_height * 0.7),
                    (x + trunk_width // 2, y_base - trunk_height - leaf_size * 0.5)
                ])
            else: # Deciduous style
                pygame.draw.circle(image, leaf_color, (x + trunk_width // 2, y_base - trunk_height - leaf_size // 4), leaf_size // 2)

        # Bushes
        for _ in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(SCREEN_HEIGHT - ground_height - 50, SCREEN_HEIGHT - 70)
            pygame.draw.circle(image, DARK_GREEN, (x, y), random.randint(20, 40))

    elif "deer" in name:
        # Main body
        pygame.draw.ellipse(image, BROWN, (5, 10, 40, 30))
        # Head
        pygame.draw.circle(image, BROWN, (15, 15), 8)
        # Snout
        pygame.draw.rect(image, LIGHT_BROWN, (12, 18, 5, 5))
        # Tail
        pygame.draw.rect(image, WHITE, (40, 25, 8, 8))
        # Simple antlers
        pygame.draw.line(image, BROWN, (15, 10), (10, 5), 2)
        pygame.draw.line(image, BROWN, (15, 10), (20, 5), 2)
    elif "rabbit" in name:
        # Body
        pygame.draw.ellipse(image, LIGHT_GRAY, (5, 15, 40, 25))
        # Head
        pygame.draw.ellipse(image, LIGHT_GRAY, (10, 5, 15, 10))
        # Ears
        pygame.draw.rect(image, LIGHT_GRAY, (12, 0, 4, 8))
        pygame.draw.rect(image, LIGHT_GRAY, (18, 0, 4, 8))
        # Tail
        pygame.draw.circle(image, WHITE, (40, 25), 5)
    elif "fox" in name:
        # Body
        pygame.draw.ellipse(image, ORANGE, (5, 10, 40, 30))
        # Head
        pygame.draw.polygon(image, ORANGE, [(10,15), (20,10), (20,20)])
        # Snout
        pygame.draw.circle(image, BLACK, (10, 17), 3)
        # Tail
        pygame.draw.polygon(image, ORANGE, [(40,15), (48,25), (40,35)])
        pygame.draw.circle(image, WHITE, (45, 25), 5) # Tail tip
    elif "bird" in name: # Bonus Bird (Pheasant like)
        # Body
        pygame.draw.ellipse(image, YELLOW, (10, 15, 30, 20))
        # Head
        pygame.draw.circle(image, YELLOW, (15, 15), 7)
        # Beak
        pygame.draw.polygon(image, ORANGE, [(20,15), (30,17), (20,19)])
        # Eye
        pygame.draw.circle(image, BLACK, (13, 13), 2)
        # Tail
        pygame.draw.polygon(image, YELLOW, [(35,20), (45,22), (35,25)])
    elif "squirrel" in name: # Protected
        # Body
        pygame.draw.ellipse(image, BROWN, (10, 10, 30, 30))
        # Head
        pygame.draw.circle(image, BROWN, (15, 15), 7)
        # Eye
        pygame.draw.circle(image, BLACK, (13, 13), 2)
        # Tail (bushy)
        pygame.draw.polygon(image, LIGHT_BROWN, [(35,5), (45,15), (35,25), (30,15)])
    elif "songbird" in name: # Protected
        # Body
        pygame.draw.ellipse(image, LIGHT_BLUE, (15, 15, 20, 15))
        # Head
        pygame.draw.circle(image, LIGHT_BLUE, (18, 15), 6)
        # Beak
        pygame.draw.polygon(image, ORANGE, [(23,15), (30,17), (23,19)])
        # Eye
        pygame.draw.circle(image, BLACK, (16, 14), 1)
    else:
        # Default placeholder (shouldn't be reached if all types are handled)
        image.fill(RED)
    
    # Scale image (skip for background as it's already screen size)
    if scale != 1 and "background" not in name:
        image = pygame.transform.scale(image, (int(size[0] * scale), int(size[1] * scale)))
    
    return image

# Define default sizes for sprites for the generator
SPRITE_BASE_SIZE = {
    "crosshair": (30, 30),
    "forest_background": (SCREEN_WIDTH, SCREEN_HEIGHT),
    "deer": (50, 50),
    "rabbit": (50, 50),
    "fox": (50, 50),
    "bonus_bird": (50, 50),
    "squirrel": (50, 50),
    "songbird": (50, 50),
}

# Generate all game assets
BACKGROUND = generate_drawn_image("forest_background", SPRITE_BASE_SIZE["forest_background"])
CROSSHAIR_SPRITE = generate_drawn_image("crosshair", SPRITE_BASE_SIZE["crosshair"])

DEER_SPRITE = generate_drawn_image("deer", SPRITE_BASE_SIZE["deer"], scale=2.0)
RABBIT_SPRITE = generate_drawn_image("rabbit", SPRITE_BASE_SIZE["rabbit"], scale=1.2)
FOX_SPRITE = generate_drawn_image("fox", SPRITE_BASE_SIZE["fox"], scale=1.5)
BONUS_BIRD_SPRITE = generate_drawn_image("bonus_bird", SPRITE_BASE_SIZE["bonus_bird"], scale=0.8)
SQUIRREL_SPRITE = generate_drawn_image("squirrel", SPRITE_BASE_SIZE["squirrel"], scale=0.7)
SONGBIRD_SPRITE = generate_drawn_image("songbird", SPRITE_BASE_SIZE["songbird"], scale=0.6)

# Sound Effects - will attempt to load actual files, or use dummy objects if loading fails
# Note: Since the core requirement is to run without external assets, the sound files are expected to be missing.
# The DummySound class ensures no crashes.
class DummySound:
    def play(self): pass
    def set_volume(self, vol): pass

try:
    SHOT_SOUND = pygame.mixer.Sound(os.path.join("assets", "shot.wav"))
    HIT_SOUND = pygame.mixer.Sound(os.path.join("assets", "hit.wav"))
    MISS_SOUND = pygame.mixer.Sound(os.path.join("assets", "miss.wav"))
    PENALTY_SOUND = pygame.mixer.Sound(os.path.join("assets", "penalty.wav"))
    ROUND_END_SOUND = pygame.mixer.Sound(os.path.join("assets", "round_end.wav"))
    GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join("assets", "game_over.wav"))
    
    # Adjust volumes for better balance
    SHOT_SOUND.set_volume(0.4)
    HIT_SOUND.set_volume(0.6)
    MISS_SOUND.set_volume(0.2)
    PENALTY_SOUND.set_volume(0.8)
    ROUND_END_SOUND.set_volume(0.7)
    GAME_OVER_SOUND.set_volume(0.7)
except pygame.error:
    print("Could not load some sound files. Using dummy sound objects.")
    SHOT_SOUND = HIT_SOUND = MISS_SOUND = PENALTY_SOUND = ROUND_END_SOUND = GAME_OVER_SOUND = DummySound()

# --- Game Configuration ---
GAME_STATES = ["MENU", "PLAYING", "ROUND_OVER", "GAME_OVER"]
current_game_state = "MENU"

ROUND_DURATION = 60 # seconds per round
SHOT_COOLDOWN = 300 # milliseconds (0.3 seconds)
PENALTY_LOCKOUT_DURATION = 1000 # milliseconds (1 second)

# --- Animal Data ---
# "spawn_chance" is a relative weight, not a direct probability.
ANIMAL_TYPES = {
    "deer": {"sprite": DEER_SPRITE, "points": 100, "speed": 1.5, "protected": False, "hitbox_scale": 0.7, "spawn_chance": 0.3},
    "rabbit": {"sprite": RABBIT_SPRITE, "points": 50, "speed": 2.5, "protected": False, "hitbox_scale": 0.8, "spawn_chance": 0.4},
    "fox": {"sprite": FOX_SPRITE, "points": 150, "speed": 2.0, "protected": False, "hitbox_scale": 0.75, "spawn_chance": 0.2},
    "bonus_bird": {"sprite": BONUS_BIRD_SPRITE, "points": 300, "speed": 4.0, "protected": False, "hitbox_scale": 0.0, "spawn_chance": 0.1}, # Birds get full hitbox due to small size
    "squirrel": {"sprite": SQUIRREL_SPRITE, "points": -50, "speed": 2.0, "protected": True, "hitbox_scale": 0.8, "spawn_chance": 0.25},
    "songbird": {"sprite": SONGBIRD_SPRITE, "points": -50, "speed": 3.0, "protected": True, "hitbox_scale": 0.0, "spawn_chance": 0.25}, # Birds get full hitbox due to small size
}

# Round difficulty settings (target score, max animals on screen, spawn interval (min_ms, max_ms), animal mix)
ROUND_SETTINGS = {
    1: {"target_score": 500, "max_animals": 3, "spawn_interval": (2000, 3000), "animal_mix": ["deer", "rabbit"]},
    2: {"target_score": 1200, "max_animals": 4, "spawn_interval": (1500, 2500), "animal_mix": ["deer", "rabbit", "fox", "squirrel", "songbird"]},
    3: {"target_score": 2500, "max_animals": 5, "spawn_interval": (1200, 2000), "animal_mix": ["deer", "rabbit", "fox", "bonus_bird", "squirrel", "songbird"]},
    4: {"target_score": 4000, "max_animals": 6, "spawn_interval": (1000, 1800), "animal_mix": ["deer", "rabbit", "fox", "bonus_bird", "squirrel", "songbird"]},
    5: {"target_score": 6000, "max_animals": 7, "spawn_interval": (800, 1500), "animal_mix": ["deer", "rabbit", "fox", "bonus_bird", "squirrel", "songbird"]},
    # Additional rounds can be added for more challenge
}

# --- Game Variables (global for easy access within game functions) ---
current_score = 0
current_round = 1
time_remaining = ROUND_DURATION
game_timer = 0 # Tracks time elapsed within the current round (milliseconds)
last_shot_time = 0 # Last time a shot was fired (milliseconds)
last_spawn_time = 0 # Last time an animal was spawned (milliseconds)
next_spawn_delay = 0 # Delay until next animal spawn (milliseconds)
animals = [] # List to hold active Animal objects
score_popups = [] # List to manage ScorePopup objects
penalty_lockout_active = False # True when player is in penalty lockout
penalty_lockout_start_time = 0 # Time when penalty lockout started (milliseconds)
high_scores = [] # List of tuples: [(score, round_completed), ...]

# --- Helper Functions ---
def save_high_scores():
    # Saves top high scores to a text file
    with open("highscores.txt", "w") as f:
        for score, round_num in high_scores:
            f.write(f"{score},{round_num}\n")

def load_high_scores():
    # Loads high scores from a text file
    global high_scores
    high_scores = []
    if os.path.exists("highscores.txt"):
        with open("highscores.txt", "r") as f:
            for line in f:
                try:
                    score, round_num = map(int, line.strip().split(','))
                    high_scores.append((score, round_num))
                except ValueError:
                    continue # Skip malformed lines
    # Sort by score, descending, and keep only the top 10
    high_scores.sort(key=lambda x: x[0], reverse=True)
    high_scores[:] = high_scores[:10]

def reset_game():
    # Resets all game-related variables to initial state for a new game
    global current_score, current_round, time_remaining, game_timer, \
           last_shot_time, last_spawn_time, next_spawn_delay, animals, \
           score_popups, penalty_lockout_active, penalty_lockout_start_time
    
    current_score = 0
    current_round = 1
    time_remaining = ROUND_DURATION
    game_timer = 0
    last_shot_time = 0
    last_spawn_time = pygame.time.get_ticks() # Initialize for first spawn calculation
    next_spawn_delay = random.randint(*ROUND_SETTINGS[current_round]["spawn_interval"])
    animals.clear()
    score_popups.clear()
    penalty_lockout_active = False
    penalty_lockout_start_time = 0
    pygame.mouse.set_visible(False) # Hide system cursor when in game

# --- Classes ---
class Animal(pygame.sprite.Sprite):
    def __init__(self, animal_type_name, spawn_side):
        super().__init__()
        data = ANIMAL_TYPES[animal_type_name]
        self.image = data["sprite"].copy()
        self.original_image = self.image # Store original for potential flipping
        self.points = data["points"]
        self.speed = data["speed"]
        self.protected = data["protected"]
        self.hitbox_scale = data["hitbox_scale"]
        self.animal_type_name = animal_type_name

        self.spawn_side = spawn_side # "left" or "right"
        
        # Calculate starting position and direction
        if self.spawn_side == "left":
            self.x = -self.image.get_width() # Start off-screen to the left
            self.direction = 1 # Move right
            # Flip image if default faces left and needs to face right
            # Our drawn sprites generally face right, so flip if moving left.
            # Birds are symmetrical enough not to matter much, or small.
            if self.animal_type_name not in ["bonus_bird", "songbird"]:
                 self.image = pygame.transform.flip(self.original_image, True, False) 
        else: # spawn_side == "right"
            self.x = SCREEN_WIDTH # Start off-screen to the right
            self.direction = -1 # Move left
            # Our drawn sprites generally face right, so no flip for moving left.
            # If default faced left, we would flip for right.
            # But the generated images generally face right.
            
        # Random Y position within a reasonable range (simulating ground level/flying)
        ground_level_min = SCREEN_HEIGHT * 0.5
        ground_level_max = SCREEN_HEIGHT * 0.8
        
        # Birds can appear higher
        if "bird" in animal_type_name:
            self.y = random.uniform(SCREEN_HEIGHT * 0.2, SCREEN_HEIGHT * 0.6) - self.image.get_height() / 2
        else:
            self.y = random.uniform(ground_level_min, ground_level_max) - self.image.get_height() / 2
        
        self.rect = self.image.get_rect(topleft=(int(self.x), int(self.y)))
        
        # Create a more accurate hitbox, smaller than the sprite image
        # If hitbox_scale is 0, use full rect to avoid zero-size error
        if self.hitbox_scale > 0:
            self.hitbox = self.rect.inflate(-self.rect.width * (1 - self.hitbox_scale), -self.rect.height * (1 - self.hitbox_scale))
        else:
            self.hitbox = self.rect.copy() # Use full sprite rect if scale is 0 (or very small)
        self.hitbox.center = self.rect.center

    def update(self):
        # Update position
        self.x += self.speed * self.direction
        self.rect.x = int(self.x)
        self.hitbox.center = self.rect.center # Keep hitbox centered with the sprite

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        # For debugging hitboxes (uncomment to visualize):
        # pygame.draw.rect(surface, RED, self.hitbox, 1)

    def is_offscreen(self):
        # Check if the animal has moved completely off the screen
        return (self.direction == 1 and self.rect.left > SCREEN_WIDTH) or \
               (self.direction == -1 and self.rect.right < 0)

    def get_hitbox_rect(self):
        return self.hitbox

class ScorePopup:
    def __init__(self, text, pos, color=WHITE):
        self.text = text
        self.pos = list(pos)
        self.base_color = color # Store original RGB color
        self.font = FONT_MD
        self.start_time = pygame.time.get_ticks()
        self.duration = 1500 # milliseconds for the popup to last
        self.fade_start_time = self.duration * 0.7 # Start fading at 70% duration

    def update(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        self.pos[1] -= 0.5 # Move upwards slowly
        
        return elapsed_time > self.duration # Return True if popup should be removed

    def draw(self, surface):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        alpha = 255
        if elapsed_time > self.fade_start_time:
            # Calculate alpha value for fading out
            alpha = max(0, 255 - int(255 * (elapsed_time - self.fade_start_time) / (self.duration - self.fade_start_time)))
        
        # Render text with base_color and apply alpha to the rendered surface
        text_surface = self.font.render(self.text, True, self.base_color)
        text_surface.set_alpha(alpha)
        surface.blit(text_surface, text_surface.get_rect(center=self.pos))


# --- Game Loop Functions ---

def draw_ui():
    # Display current score
    score_text = FONT_LG.render(f"Score: {current_score}", True, WHITE)
    SCREEN.blit(score_text, (20, 20))

    # Display current round number
    round_text = FONT_LG.render(f"Round: {current_round}", True, WHITE)
    SCREEN.blit(round_text, (SCREEN_WIDTH // 2 - round_text.get_width() // 2, 20))

    # Display time remaining
    time_text = FONT_LG.render(f"Time: {int(time_remaining)}s", True, WHITE)
    SCREEN.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 20, 20))

    # Display target score for the current round
    if current_round <= len(ROUND_SETTINGS) and current_game_state == "PLAYING":
        target_score = ROUND_SETTINGS[current_round]["target_score"]
        target_text = FONT_MD.render(f"Target: {target_score}", True, YELLOW)
        SCREEN.blit(target_text, (SCREEN_WIDTH // 2 - target_text.get_width() // 2, 70))

    # Penalty lockout indicator
    if penalty_lockout_active:
        lockout_text = FONT_XL.render("PENALTY! LOCKED!", True, RED)
        text_rect = lockout_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(lockout_text, text_rect)

def spawn_animal():
    global animals, last_spawn_time, next_spawn_delay

    # Only spawn if below the maximum allowed animals for the current round
    if len(animals) >= ROUND_SETTINGS[current_round]["max_animals"]:
        return

    current_time = pygame.time.get_ticks()
    # Check if enough time has passed since the last spawn
    if current_time - last_spawn_time > next_spawn_delay:
        
        # Get the allowed animal types for the current round
        round_animal_mix = ROUND_SETTINGS[current_round]["animal_mix"]
        
        # Filter ANIMAL_TYPES to only include those in the current round's mix
        available_animals_for_round = {k: v for k, v in ANIMAL_TYPES.items() if k in round_animal_mix}
        
        # Calculate total chance for normalization (to make weighted random selection)
        total_chance = sum(v["spawn_chance"] for v in available_animals_for_round.values())
        
        # Choose animal based on weighted chance
        rand_val = random.uniform(0, total_chance)
        
        chosen_animal_type = None
        cumulative_chance = 0
        for animal_name, data in available_animals_for_round.items():
            cumulative_chance += data["spawn_chance"]
            if rand_val <= cumulative_chance:
                chosen_animal_type = animal_name
                break
        
        if chosen_animal_type:
            spawn_side = random.choice(["left", "right"])
            animals.append(Animal(chosen_animal_type, spawn_side))
            last_spawn_time = current_time
            # Determine next spawn delay within the round's interval
            next_spawn_delay = random.randint(*ROUND_SETTINGS[current_round]["spawn_interval"])


def handle_shooting(pos):
    global current_score, last_shot_time, penalty_lockout_active, penalty_lockout_start_time

    current_time = pygame.time.get_ticks()

    # If penalty lockout is active, prevent shooting
    if penalty_lockout_active:
        PENALTY_SOUND.play() # Replay sound to reinforce lockout
        return
        
    # Apply fire rate cooldown
    if current_time - last_shot_time < SHOT_COOLDOWN:
        return

    SHOT_SOUND.play()
    last_shot_time = current_time

    hit = False
    # Iterate through animals in reverse to safely remove them if hit
    for animal in reversed(animals):
        if animal.get_hitbox_rect().collidepoint(pos):
            hit = True
            
            if animal.protected:
                current_score += animal.points # Points will be negative here
                score_popups.append(ScorePopup(f"{animal.points}", animal.rect.center, RED))
                PENALTY_SOUND.play()
                penalty_lockout_active = True
                penalty_lockout_start_time = current_time
            else:
                current_score += animal.points
                score_popups.append(ScorePopup(f"+{animal.points}", animal.rect.center, WHITE))
                HIT_SOUND.play()

            animals.remove(animal)
            break # Only hit one animal per shot

    if not hit:
        MISS_SOUND.play()

def update_game_state(dt):
    global time_remaining, game_timer, current_round, current_game_state, current_score, \
           penalty_lockout_active, penalty_lockout_start_time, next_spawn_delay, last_spawn_time

    if current_game_state == "PLAYING":
        game_timer += dt # Accumulate delta time
        time_remaining = ROUND_DURATION - (game_timer / 1000) # Convert game_timer to seconds

        # Update penalty lockout status
        if penalty_lockout_active and pygame.time.get_ticks() - penalty_lockout_start_time > PENALTY_LOCKOUT_DURATION:
            penalty_lockout_active = False

        # Spawn new animals
        spawn_animal()
        
        # Update all active animals
        for animal in animals[:]: # Iterate over a copy to allow safe removal
            animal.update()
            if animal.is_offscreen():
                animals.remove(animal) # Remove animals that move off-screen

        # Update and remove expired score pop-ups
        for popup in score_popups[:]:
            if popup.update():
                score_popups.remove(popup)

        # Check round end condition
        if time_remaining <= 0:
            time_remaining = 0 # Ensure time doesn't go negative on display
            round_data = ROUND_SETTINGS[current_round]
            if current_score >= round_data["target_score"]:
                ROUND_END_SOUND.play()
                current_round += 1
                if current_round > len(ROUND_SETTINGS):
                    # All rounds completed - game victory/final score
                    current_game_state = "GAME_OVER"
                    add_high_score(current_score, current_round - 1) # Record score for successfully completed game
                else:
                    # Advance to next round
                    current_game_state = "ROUND_OVER"
                    # Set a timer to automatically transition to the next round after a brief pause
                    pygame.time.set_timer(pygame.USEREVENT + 1, 3000, 1) # Fires USEREVENT + 1 once after 3 seconds
            else:
                # Failed to meet target score - game over
                GAME_OVER_SOUND.play()
                current_game_state = "GAME_OVER"
                add_high_score(current_score, current_round) # Record score for the round failed on

def add_high_score(score, round_num):
    # Adds a new score to the high scores list, sorts, and saves
    high_scores.append((score, round_num))
    high_scores.sort(key=lambda x: x[0], reverse=True)
    high_scores[:] = high_scores[:10] # Keep only the top 10 scores
    save_high_scores()


def draw_menu_screen():
    SCREEN.fill(DARK_GREEN) # Darker green for menu background
    title_text = FONT_XL.render("Pixel Hunter: Forest Pursuit", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    SCREEN.blit(title_text, title_rect)

    start_text = FONT_LG.render("Click to Start", True, YELLOW)
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    SCREEN.blit(start_text, start_rect)

    high_score_title = FONT_MD.render("High Scores:", True, WHITE)
    SCREEN.blit(high_score_title, (SCREEN_WIDTH // 2 - high_score_title.get_width() // 2, SCREEN_HEIGHT * 0.6))
    
    # Display top 5 high scores
    y_offset = SCREEN_HEIGHT * 0.6 + 40
    for i, (score, round_num) in enumerate(high_scores[:5]):
        score_entry_text = FONT_SM.render(f"{i+1}. {score} points (Round {round_num})", True, WHITE)
        score_entry_rect = score_entry_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 30))
        SCREEN.blit(score_entry_text, score_entry_rect)

    pygame.mouse.set_visible(True) # Show the system cursor on menu

def draw_round_over_screen():
    SCREEN.fill(DARK_GREEN)
    round_over_text = FONT_XL.render(f"Round {current_round - 1} Complete!", True, WHITE)
    round_over_rect = round_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    SCREEN.blit(round_over_text, round_over_rect)

    score_text = FONT_LG.render(f"Your Score: {current_score}", True, YELLOW)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    SCREEN.blit(score_text, score_rect)
    
    next_round_text = FONT_MD.render("Moving to next round...", True, WHITE)
    next_round_rect = next_round_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.7))
    SCREEN.blit(next_round_text, next_round_rect)

    pygame.mouse.set_visible(False) # Hide system cursor, crosshair will be shown in next round

def draw_game_over_screen():
    SCREEN.fill(RED)
    game_over_text = FONT_XL.render("GAME OVER!", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    SCREEN.blit(game_over_text, game_over_rect)

    final_score_text = FONT_LG.render(f"Final Score: {current_score}", True, YELLOW)
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    SCREEN.blit(final_score_text, final_score_rect)
    
    restart_text = FONT_MD.render("Click to return to Menu", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.7))
    SCREEN.blit(restart_text, restart_rect)

    pygame.mouse.set_visible(True) # Show system cursor for menu interaction


# --- Main Game Loop ---
def main():
    global current_game_state, current_round, current_score, time_remaining, game_timer, \
           last_shot_time, last_spawn_time, next_spawn_delay, penalty_lockout_active, \
           penalty_lockout_start_time

    load_high_scores() # Load high scores at the start of the game
    
    running = True
    while running:
        dt = CLOCK.tick(FPS) # Delta time in milliseconds, capped at FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    if current_game_state == "PLAYING":
                        handle_shooting(event.pos)
                    elif current_game_state == "MENU":
                        reset_game() # Prepare for a new game
                        current_game_state = "PLAYING"
                    elif current_game_state == "GAME_OVER":
                        current_game_state = "MENU" # Go back to menu
                        load_high_scores() # Reload high scores after a game
            
            if event.type == pygame.USEREVENT + 1: # Custom event for round over auto-advance
                if current_game_state == "ROUND_OVER":
                    current_game_state = "PLAYING"
                    # Reset round-specific elements for the new round
                    animals.clear()
                    score_popups.clear()
                    game_timer = 0
                    time_remaining = ROUND_DURATION
                    last_spawn_time = pygame.time.get_ticks() # Reset spawn timer for the new round
                    if current_round <= len(ROUND_SETTINGS): # Ensure round exists in settings
                        next_spawn_delay = random.randint(*ROUND_SETTINGS[current_round]["spawn_interval"])


        # --- Update Game State ---
        update_game_state(dt)

        # --- Drawing ---
        SCREEN.blit(BACKGROUND, (0, 0)) # Draw background first

        if current_game_state == "MENU":
            draw_menu_screen()
        elif current_game_state == "PLAYING":
            # Draw animals
            for animal in animals:
                animal.draw(SCREEN)
            # Draw score pop-ups
            for popup in score_popups:
                popup.draw(SCREEN)
            # Draw main UI elements
            draw_ui()
            
            # Draw crosshair last to be on top of everything
            mouse_pos = pygame.mouse.get_pos()
            crosshair_rect = CROSSHAIR_SPRITE.get_rect(center=mouse_pos)
            if not penalty_lockout_active:
                SCREEN.blit(CROSSHAIR_SPRITE, crosshair_rect)
            else:
                # Draw a 'locked' crosshair during penalty
                locked_crosshair_color = RED
                # Draw an 'X' or similar to indicate locked state
                pygame.draw.line(SCREEN, locked_crosshair_color, (mouse_pos[0] - 15, mouse_pos[1] - 15), (mouse_pos[0] + 15, mouse_pos[1] + 15), 3)
                pygame.draw.line(SCREEN, locked_crosshair_color, (mouse_pos[0] + 15, mouse_pos[1] - 15), (mouse_pos[0] - 15, mouse_pos[1] + 15), 3)
                pygame.draw.circle(SCREEN, locked_crosshair_color, mouse_pos, 20, 2) # Larger circle

        elif current_game_state == "ROUND_OVER":
            draw_round_over_screen()
        elif current_game_state == "GAME_OVER":
            draw_game_over_screen()
        
        pygame.display.flip() # Update the full display Surface to the screen

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()