import pygame
import math
import sys
import random
import os
import numpy as np
from pygame.locals import *

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.DOUBLEBUF | pygame.HWACCEL)
pygame.display.set_caption("Minecraft FPS")
clock = pygame.time.Clock()

# Map: 1 = dirt, 2 = stone, 3 = target, 4 = wood, 5 = leaves, 6 = monster, 0 = empty space
# Initialize a base small map (will be expanded to 256x256)
base_map = [
    [1,4,4,1,1,4,4,1],
    [1,0,0,0,0,0,0,1],
    [2,0,3,0,0,3,0,2],
    [2,0,0,5,5,0,0,2],
    [1,0,3,0,0,3,0,1],
    [1,2,2,1,1,2,2,1]
]

# Create a 256x256 world map
MAP_WIDTH, MAP_HEIGHT = 256, 256
world_map = [[0 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
height_map = [[0 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

# Optimization variables
RENDER_DISTANCE = 20 * TILE_SIZE  # Only render objects within this distance
VIEW_ANGLE_CHECK = math.pi / 4    # Only render objects in view cone
USE_OCTREE = False                # Set to True for larger worlds
CHUNK_SIZE = 16                   # Process world in chunks

# Optimized ray casting function
def cast_rays(height_offset=0):
    start_angle = player_angle - HALF_FOV
    
    # Pre-calculate sin/cos values for performance
    sin_angles = [math.sin(start_angle + ray * DELTA_ANGLE) for ray in range(NUM_RAYS)]
    cos_angles = [math.cos(start_angle + ray * DELTA_ANGLE) for ray in range(NUM_RAYS)]
    
    # Only process visible chunks (optimization)
    player_chunk_x, player_chunk_y = int(player_x // (CHUNK_SIZE * TILE_SIZE)), int(player_y // (CHUNK_SIZE * TILE_SIZE))
    visible_chunks = []
    
    for cy in range(player_chunk_y - 2, player_chunk_y + 3):
        for cx in range(player_chunk_x - 2, player_chunk_x + 3):
            if 0 <= cx < MAP_WIDTH // CHUNK_SIZE and 0 <= cy < MAP_HEIGHT // CHUNK_SIZE:
                chunk_center_x = (cx * CHUNK_SIZE + CHUNK_SIZE // 2) * TILE_SIZE
                chunk_center_y = (cy * CHUNK_SIZE + CHUNK_SIZE // 2) * TILE_SIZE
                
                # Check if chunk is within render distance
                dx = chunk_center_x - player_x
                dy = chunk_center_y - player_y
                dist = math.sqrt(dx*dx + dy*dy)
                
                if dist < RENDER_DISTANCE * 1.5:  # Add some margin
                    visible_chunks.append((cx, cy))
    
    # Process each ray
    for ray in range(NUM_RAYS):
        sin_a = sin_angles[ray]
        cos_a = cos_angles[ray]
        
        # Use fast DDA algorithm for ray casting
        ray_dir_x = cos_a
        ray_dir_y = sin_a
        
        # Calculate ray position and direction
        map_x, map_y = int(player_x // TILE_SIZE), int(player_y // TILE_SIZE)
        
        # Length of ray from current position to next x or y-side
        delta_dist_x = abs(1 / ray_dir_x) if ray_dir_x != 0 else float('inf')
        delta_dist_y = abs(1 / ray_dir_y) if ray_dir_y != 0 else float('inf')
        
        # Direction to step in x or y direction (either +1 or -1)
        step_x = 1 if ray_dir_x >= 0 else -1
        step_y = 1 if ray_dir_y >= 0 else -1
        
        # Length of ray from one x or y-side to next x or y-side
        side_dist_x = (((map_x + 1) * TILE_SIZE - player_x) / TILE_SIZE) * delta_dist_x if ray_dir_x > 0 else ((player_x - map_x * TILE_SIZE) / TILE_SIZE) * delta_dist_x
        side_dist_y = (((map_y + 1) * TILE_SIZE - player_y) / TILE_SIZE) * delta_dist_y if ray_dir_y > 0 else ((player_y - map_y * TILE_SIZE) / TILE_SIZE) * delta_dist_y
        
        hit = False
        side = 0  # 0 for x-side, 1 for y-side
        max_depth = int(RENDER_DISTANCE / TILE_SIZE)
        
        # Perform DDA
        for depth in range(max_depth):
            # Jump to next map square in x or y direction
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1
            
            # Check if ray hit a wall
            if 0 <= map_x < MAP_WIDTH and 0 <= map_y < MAP_HEIGHT:
                block_type = world_map[map_y][map_x]
                if block_type > 0:
                    if block_type == 3:  # Target
                        # Rest of target check code
                        # ...existing code...
                        pass
                    
                    # Calculate distance perpendicular to camera plane
                    # (to avoid fisheye effect)
                    if side == 0:
                        perp_wall_dist = (map_x * TILE_SIZE - player_x + (1 - step_x) * TILE_SIZE / 2) / ray_dir_x
                        texture_offset = (player_y + perp_wall_dist * ray_dir_y) % TILE_SIZE
                    else:
                        perp_wall_dist = (map_y * TILE_SIZE - player_y + (1 - step_y) * TILE_SIZE / 2) / ray_dir_y
                        texture_offset = (player_x + perp_wall_dist * ray_dir_x) % TILE_SIZE
                    
                    # Get texture for this block type
                    texture = textures.get(block_type, textures[1])
                    
                    # Calculate wall height
                    proj_height = min(HEIGHT * 1.5, PROJ_COEFF / (perp_wall_dist + 0.0001))
                    
                    # Draw wall slice with texture mapping
                    # ...existing code...
                    
                    hit = True
                    break
        
        # Only render monsters if we haven't hit a wall yet
        if not hit:
            for monster in [m for m in monsters if m.alive]:
                # Check if monster is reasonably close to the player
                dx = monster.x - player_x
                dy = monster.y - player_y
                dist_to_monster = dx*dx + dy*dy  # Faster than sqrt for comparison
                
                if dist_to_monster < RENDER_DISTANCE * RENDER_DISTANCE:
                    # Rest of monster rendering code
                    # ...existing code...
                    pass

# More efficient world generation
def generate_world():
    # Generate world in chunks for better performance
    for chunk_y in range(MAP_HEIGHT // CHUNK_SIZE):
        for chunk_x in range(MAP_WIDTH // CHUNK_SIZE):
            generate_chunk(chunk_x, chunk_y)

def generate_chunk(chunk_x, chunk_y):
    start_x = chunk_x * CHUNK_SIZE
    start_y = chunk_y * CHUNK_SIZE
    end_x = min(MAP_WIDTH, start_x + CHUNK_SIZE)
    end_y = min(MAP_HEIGHT, start_y + CHUNK_SIZE)
    
    # Copy the base map to the center if this is the center chunk
    base_height = len(base_map)
    base_width = len(base_map[0])
    center_y = MAP_HEIGHT // 2 - base_height // 2
    center_x = MAP_WIDTH // 2 - base_width // 2
    
    # Check if this chunk contains any of the base map
    base_overlap = (
        start_x <= center_x + base_width and end_x > center_x and
        start_y <= center_y + base_height and end_y > center_y
    )
    
    if base_overlap:
        # Place base map pieces that fall within this chunk
        for y in range(max(0, center_y - start_y), min(CHUNK_SIZE, center_y + base_height - start_y)):
            for x in range(max(0, center_x - start_x), min(CHUNK_SIZE, center_x + base_width - start_x)):
                base_y = y + start_y - center_y
                base_x = x + start_x - center_x
                
                if 0 <= base_y < base_height and 0 <= base_x < base_width:
                    world_map[start_y + y][start_x + x] = base_map[base_y][base_x]
    
    # Generate terrain for the rest of the chunk
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            # Skip cells already set from the base map
            if base_overlap and center_y <= y < center_y + base_height and center_x <= x < center_x + base_width:
                if y - center_y < base_height and x - center_x < base_width:
                    continue
            
            # Border walls
            if x == 0 or y == 0 or x == MAP_WIDTH - 1 or y == MAP_HEIGHT - 1:
                world_map[y][x] = 2  # Stone walls at the borders
                continue
            
            # Use a faster noise function - simpler math for better performance
            noise = ((x * 73) ^ (y * 127)) % 100 / 10.0
            
            if noise > 7:  # Mountains
                world_map[y][x] = 2
                height_map[y][x] = int(noise) % 5
            elif noise > 4:  # Hills
                world_map[y][x] = 1
                height_map[y][x] = int(noise) % 3
            elif noise > 2:  # Forests
                if ((x * 31) ^ (y * 17)) % 10 < 3:  # 30% chance
                    world_map[y][x] = 4 if ((x + y) % 10) < 7 else 5
                    height_map[y][x] = 1
                else:
                    world_map[y][x] = 0
            else:  # Plains
                world_map[y][x] = 0
            
            # Randomly place targets and monsters - but fewer of them
            if world_map[y][x] == 0:
                rand_val = ((x * 263) ^ (y * 371)) % 1000
                if rand_val < 5:  # 0.5% chance for a target
                    world_map[y][x] = 3
                elif rand_val < 8:  # 0.3% chance for a monster
                    world_map[y][x] = 6

# Fill the world map procedurally
def generate_world():
    # Copy the base map to the center as a starting point
    base_height = len(base_map)
    base_width = len(base_map[0])
    center_y = MAP_HEIGHT // 2 - base_height // 2
    center_x = MAP_WIDTH // 2 - base_width // 2
    
    # Place the base map in the center
    for y in range(base_height):
        for x in range(base_width):
            world_map[center_y + y][center_x + x] = base_map[y][x]
    
    # Generate terrain procedurally around the base map
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            # Skip the base map area
            if (center_y <= y < center_y + base_height and 
                center_x <= x < center_x + base_width):
                continue
            
            # Border walls
            if x == 0 or y == 0 or x == MAP_WIDTH - 1 or y == MAP_HEIGHT - 1:
                world_map[y][x] = 2  # Stone walls at the borders
                continue
            
            # Generate random terrain
            noise = (math.sin(x * 0.1) + math.cos(y * 0.1)) * 10
            if noise > 5:  # Mountains
                world_map[y][x] = 2  # Stone
                height_map[y][x] = int(abs(noise)) % 5  # Varying heights
            elif noise > 0:  # Hills
                world_map[y][x] = 1  # Dirt
                height_map[y][x] = int(abs(noise)) % 3
            elif noise > -5:  # Forests
                if random.random() < 0.3:
                    world_map[y][x] = 4 if random.random() < 0.7 else 5  # Woods and leaves
                    height_map[y][x] = 1
                else:
                    world_map[y][x] = 0  # Empty space
            else:  # Plains
                world_map[y][x] = 0  # Empty space
            
            # Randomly place targets and monsters
            if world_map[y][x] == 0:
                if random.random() < 0.01:  # 1% chance for a target
                    world_map[y][x] = 3
                elif random.random() < 0.005:  # 0.5% chance for a monster
                    world_map[y][x] = 6

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DIRT_COLOR = (133, 87, 35)
STONE_COLOR = (128, 128, 128)
GRASS_COLOR = (86, 125, 70)
SKY_COLOR = (158, 201, 226)
WOOD_COLOR = (161, 120, 41)
LEAVES_COLOR = (62, 143, 64)

TILE_SIZE = 64

# Player settings
player_x = 100
player_y = 100
player_height = 32
player_angle = 0
player_z = 0  # Height above ground
player_velocity_z = 0  # Vertical velocity for jumping
gravity = 0.5
jump_strength = 10
is_jumping = False
is_falling = False
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 240  # Higher resolution
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE_SIZE
SCALE = WIDTH // NUM_RAYS

# Movement bobbing
bobbing_offset = 0
bobbing_phase = 0
bobbing_amplitude = 5

# Shooting and scoring
score = 0
ammo = 10
health = 100
shooting = False
gun_cooldown = 0
GUN_COOLDOWN_MAX = 20
targets = []
particles = []
block_hit_marks = []

# Load textures
def load_texture(file_name, size=(TILE_SIZE, TILE_SIZE)):
    # For demonstration, create procedural textures
    texture = pygame.Surface(size)
    
    if file_name == "dirt":
        base_color = DIRT_COLOR
        noise_level = 20
        for x in range(size[0]):
            for y in range(size[1]):
                noise = random.randint(-noise_level, noise_level)
                color = (
                    max(0, min(255, base_color[0] + noise)),
                    max(0, min(255, base_color[1] + noise)),
                    max(0, min(255, base_color[2] + noise))
                )
                texture.set_at((x, y), color)
                
    elif file_name == "stone":
        base_color = STONE_COLOR
        noise_level = 30
        for x in range(size[0]):
            for y in range(size[1]):
                noise = random.randint(-noise_level, noise_level)
                color = (
                    max(0, min(255, base_color[0] + noise)),
                    max(0, min(255, base_color[1] + noise)),
                    max(0, min(255, base_color[2] + noise))
                )
                texture.set_at((x, y), color)
                
    elif file_name == "target":
        texture.fill((100, 30, 30))
        pygame.draw.circle(texture, RED, (size[0]//2, size[1]//2), size[0]//3)
        pygame.draw.circle(texture, WHITE, (size[0]//2, size[1]//2), size[0]//5)
        
    elif file_name == "wood":
        base_color = WOOD_COLOR
        for x in range(size[0]):
            for y in range(size[1]):
                # Add vertical grain
                grain = math.sin(y * 0.2) * 10
                noise = random.randint(-10, 10)
                color = (
                    max(0, min(255, base_color[0] + grain + noise)),
                    max(0, min(255, base_color[1] + grain//2 + noise)),
                    max(0, min(255, base_color[2] + grain//3 + noise))
                )
                texture.set_at((x, y), color)
                
    elif file_name == "leaves":
        base_color = LEAVES_COLOR
        for x in range(size[0]):
            for y in range(size[1]):
                noise = random.randint(-20, 20)
                # Make some pixels transparent for a leafy look
                if random.random() < 0.1:
                    noise = -base_color[1]  # Make darker spots
                color = (
                    max(0, min(255, base_color[0] + noise//2)),
                    max(0, min(255, base_color[1] + noise)),
                    max(0, min(255, base_color[2] + noise//2))
                )
                texture.set_at((x, y), color)
    
    elif file_name == "monster":
        base_color = (139, 0, 0)  # Dark red
        texture.fill(base_color)
        # Draw scary face
        eye_size = size[0] // 5
        pygame.draw.circle(texture, (255, 255, 0), (size[0]//3, size[1]//3), eye_size)
        pygame.draw.circle(texture, (255, 255, 0), (size[0]*2//3, size[1]//3), eye_size)
        pygame.draw.circle(texture, (0, 0, 0), (size[0]//3, size[1]//3), eye_size//2)
        pygame.draw.circle(texture, (0, 0, 0), (size[0]*2//3, size[1]//3), eye_size//2)
        
        # Mouth
        pygame.draw.arc(texture, (0, 0, 0), (size[0]//4, size[1]//2, size[0]//2, size[1]//3), 0, math.pi, 3)
    
    return texture

# Create textures
textures = {
    1: load_texture("dirt"),
    2: load_texture("stone"),
    3: load_texture("target"),
    4: load_texture("wood"),
    5: load_texture("leaves"),
    6: load_texture("monster")
}

# Sound effects
try:
    pygame.mixer.init()
    shoot_sound = pygame.mixer.Sound(os.path.join("shoot.wav"))
    hit_sound = pygame.mixer.Sound(os.path.join("hit.wav"))
    reload_sound = pygame.mixer.Sound(os.path.join("reload.wav"))
except:
    # If sound files aren't available, create dummy functions
    class DummySound:
        def play(self): pass
    shoot_sound = hit_sound = reload_sound = DummySound()

# Particle class for effects
class Particle:
    def __init__(self, x, y, color, velocity_x, velocity_y, lifetime=30, size=3):
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
    
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += 0.1  # Gravity
        self.lifetime -= 1
        return self.lifetime > 0
    
    def draw(self):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color = (*self.color, alpha)
        s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (self.size, self.size), self.size)
        screen.blit(s, (self.x - self.size, self.y - self.size))

# Block hit marker class
class BlockHitMark:
    def __init__(self, x, y, angle, lifetime=20):
        self.x = x
        self.y = y
        self.angle = angle
        self.lifetime = lifetime
    
    def update(self):
        self.lifetime -= 1
        return self.lifetime > 0
    
    def draw(self):
        i, j = int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)
        if 0 <= i < MAP_WIDTH and 0 <= j < MAP_HEIGHT and world_map[j][i] > 0:
            # Draw a crack texture at the hit location
            hit_size = 5 + (20 - self.lifetime)
            color = (255, 255, 255, 128 * (self.lifetime / 20))
            s = pygame.Surface((hit_size*2, hit_size*2), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (hit_size, hit_size), hit_size, 2)
            
            # Get screen coords
            depth = math.sqrt((player_x - self.x)**2 + (player_y - self.y)**2)
            depth *= math.cos(player_angle - self.angle)
            proj_height = min(HEIGHT, PROJ_COEFF / (depth + 0.0001))
            
            ray_num = int((self.angle - (player_angle - HALF_FOV)) / DELTA_ANGLE)
            if 0 <= ray_num < NUM_RAYS:
                screen_x = ray_num * SCALE
                screen_y = HEIGHT // 2 - proj_height // 2
                screen.blit(s, (screen_x, screen_y))

# Monster class for enemies that track the player
class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.speed = 0.5
        self.size = TILE_SIZE // 2
        self.alive = True
        self.hit_time = 0
        self.update_interval = 0
        self.attack_range = TILE_SIZE * 1.5
        self.attack_cooldown = 0
        self.attack_damage = 10
    
    def update(self):
        if not self.alive:
            return
        
        # Update hit flash timer
        if self.hit_time > 0:
            self.hit_time -= 1
        
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Only update movement every few frames for performance
        self.update_interval += 1
        if self.update_interval < 5:
            return
        
        self.update_interval = 0
        
        # Calculate direction to player
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # If player is in attack range
        if distance < self.attack_range and self.attack_cooldown == 0:
            # Attack player
            global health
            health -= self.attack_damage
            self.attack_cooldown = 60  # 1 second cooldown at 60 FPS
            return
        
        # Move toward player if not too close
        if distance > self.size:
            # Normalize direction
            dx /= distance
            dy /= distance
            
            # Calculate new position
            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed
            
            # Convert to map coordinates
            map_x, map_y = int(new_x // TILE_SIZE), int(new_y // TILE_SIZE)
            
            # Check if new position is valid (no collisions)
            if (0 <= map_x < MAP_WIDTH and 0 <= map_y < MAP_HEIGHT and
                (world_map[map_y][map_x] == 0 or world_map[map_y][map_x] == 3)):
                self.x, self.y = new_x, new_y

    def take_damage(self, damage):
        if not self.alive:
            return False
        
        self.health -= damage
        self.hit_time = 10  # Flash red when hit
        
        if self.health <= 0:
            self.alive = False
            global score
            score += 200  # More points than regular targets
            return True
        
        return False

# Initialize targets from the map
def init_targets():
    global targets
    targets = []
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if world_map[y][x] == 3:
                targets.append({
                    'x': x * TILE_SIZE + TILE_SIZE // 2, 
                    'y': y * TILE_SIZE + TILE_SIZE // 2, 
                    'alive': True,
                    'health': 100,
                    'hit_time': 0
                })

# Draw a Minecraft-style crosshair in the center of the screen
def draw_crosshair():
    # Crosshair
    cx, cy = WIDTH // 2, HEIGHT // 2
    pygame.draw.line(screen, WHITE, (cx - 8, cy), (cx - 3, cy), 2)
    pygame.draw.line(screen, WHITE, (cx + 3, cy), (cx + 8, cy), 2)
    pygame.draw.line(screen, WHITE, (cx, cy - 8), (cx, cy - 3), 2)
    pygame.draw.line(screen, WHITE, (cx, cy + 3), (cx, cy + 8), 2)

# Draw the gun at the bottom of the screen with attack animation
def draw_gun():
    gun_height = 200
    gun_width = 240
    gun_x = WIDTH // 2 - gun_width // 2
    gun_y = HEIGHT - gun_height
    
    # Gun movement based on walking and shooting
    gun_offset_y = bobbing_offset
    gun_offset_x = math.sin(bobbing_phase * 0.5) * 3
    
    if shooting:
        # Recoil animation
        recoil = max(0, gun_cooldown - 10) * 2
        gun_offset_y -= recoil
        
    # Draw gun with pickaxe-like design (Minecraft style)
    handle_color = (139, 69, 19)  # Brown
    axe_color = (192, 192, 192)  # Silver
    
    # The handle
    pygame.draw.rect(screen, handle_color, (
        gun_x + 110 + gun_offset_x, 
        gun_y + 50 + gun_offset_y, 
        20, 150))
    
    # The pickaxe head
    if shooting and gun_cooldown > GUN_COOLDOWN_MAX - 5:
        # Attack animation - show the pickaxe swinging
        points = [
            (gun_x + 100 + gun_offset_x, gun_y + 40 + gun_offset_y),
            (gun_x + 140 + gun_offset_x, gun_y + 30 + gun_offset_y),
            (gun_x + 180 + gun_offset_x, gun_y + 50 + gun_offset_y),
            (gun_x + 140 + gun_offset_x, gun_y + 70 + gun_offset_y),
        ]
        pygame.draw.polygon(screen, axe_color, points)
    else:
        # Normal position
        points = [
            (gun_x + 100 + gun_offset_x, gun_y + 60 + gun_offset_y),
            (gun_x + 120 + gun_offset_x, gun_y + 40 + gun_offset_y),
            (gun_x + 160 + gun_offset_x, gun_y + 60 + gun_offset_y),
            (gun_x + 140 + gun_offset_x, gun_y + 80 + gun_offset_y),
        ]
        pygame.draw.polygon(screen, axe_color, points)
    
    # Muzzle flash when shooting
    if shooting and gun_cooldown > GUN_COOLDOWN_MAX - 3:
        pygame.draw.circle(
            screen, 
            YELLOW, 
            (gun_x + 120 + gun_offset_x, gun_y + 50 + gun_offset_y), 
            15)

# Check if the ray hits any target or block
def check_target_hit(ray_angle):
    global score, targets, particles, block_hit_marks, monsters
    
    sin_a = math.sin(ray_angle)
    cos_a = math.cos(ray_angle)
    
    for depth in range(MAX_DEPTH):
        target_x = player_x + depth * cos_a
        target_y = player_y + depth * sin_a
        
        i, j = int(target_x // TILE_SIZE), int(target_y // TILE_SIZE)
        
        # Check if ray hit a wall
        if 0 <= i < MAP_WIDTH and 0 <= j < MAP_HEIGHT and world_map[j][i] > 0:
            if world_map[j][i] != 3:  # Not a target but a wall
                # Create hit effect
                for _ in range(10):
                    particles.append(Particle(
                        target_x, 
                        target_y,
                        (200, 200, 200),
                        random.uniform(-1, 1),
                        random.uniform(-2, -1),
                        random.randint(10, 20),
                        random.randint(1, 3)
                    ))
                block_hit_marks.append(BlockHitMark(target_x, target_y, ray_angle))
                return False
        
        # Check if ray hit a target
        for target in targets:
            if target['alive']:
                dist_to_target = math.sqrt((target_x - target['x'])**2 + (target_y - target['y'])**2)
                if dist_to_target < TILE_SIZE // 2:
                    # Damage target
                    target['health'] -= 50
                    target['hit_time'] = 10  # Flash red when hit
                    
                    # Create blood particles
                    for _ in range(20):
                        particles.append(Particle(
                            target_x, 
                            target_y,
                            (200, 0, 0),
                            random.uniform(-1, 1),
                            random.uniform(-2, 0),
                            random.randint(20, 40),
                            random.randint(2, 4)
                        ))
                    
                    if target['health'] <= 0:
                        target['alive'] = False
                        score += 100
                        hit_sound.play()
                        # Respawn target after a while
                        pygame.time.set_timer(pygame.USEREVENT, 3000, loops=1)
                    return True
    
    # Check if ray hit a monster
    for monster in monsters:
        if monster.alive:
            # Calculate position of monster in ray's path
            dist_to_monster = math.sqrt((player_x - monster.x)**2 + (player_y - monster.y)**2)
            angle_to_monster = math.atan2(monster.y - player_y, monster.x - player_x)
            
            # Check if ray is pointing at monster (with some margin)
            angle_diff = abs((angle_to_monster - ray_angle + math.pi) % (2 * math.pi) - math.pi)
            if angle_diff < 0.1:  # Small angle margin
                # Raycast to monster position
                for depth in range(int(dist_to_monster)):
                    target_x = player_x + depth * math.cos(ray_angle)
                    target_y = player_y + depth * math.sin(ray_angle)
                    
                    # Check for wall in the way
                    i, j = int(target_x // TILE_SIZE), int(target_y // TILE_SIZE)
                    if 0 <= i < MAP_WIDTH and 0 <= j < MAP_HEIGHT and world_map[j][i] > 0 and world_map[j][i] != 3 and world_map[j][i] != 6:
                        break  # Hit a wall instead
                    
                    # Check distance to monster
                    monster_dist = math.sqrt((target_x - monster.x)**2 + (target_y - monster.y)**2)
                    if monster_dist < monster.size:
                        # Monster hit!
                        if monster.take_damage(50):
                            # Create death particles
                            for _ in range(30):
                                particles.append(Particle(
                                    monster.x, monster.y,
                                    (200, 0, 0),
                                    random.uniform(-2, 2),
                                    random.uniform(-3, 0),
                                    random.randint(30, 60),
                                    random.randint(2, 5)
                                ))
                        else:
                            # Create hit particles
                            for _ in range(15):
                                particles.append(Particle(
                                    monster.x, monster.y,
                                    (200, 0, 0),
                                    random.uniform(-1, 1),
                                    random.uniform(-2, 0),
                                    random.randint(20, 40),
                                    random.randint(2, 4)
                                ))
                        
                        hit_sound.play()
                        return True
    
    return False

# Draw the sky gradient and ground
def draw_background():
    # Sky gradient
    sky = pygame.Surface((WIDTH, HEIGHT // 2))
    for y in range(HEIGHT // 2):
        factor = 1 - y / (HEIGHT // 2)
        r = int(SKY_COLOR[0] * factor + 100 * (1 - factor))
        g = int(SKY_COLOR[1] * factor + 150 * (1 - factor))
        b = int(SKY_COLOR[2] * factor + 255 * (1 - factor))
        pygame.draw.line(sky, (r, g, b), (0, y), (WIDTH, y))
    screen.blit(sky, (0, 0))
    
    # Ground (grass)
    ground = pygame.Surface((WIDTH, HEIGHT // 2))
    for y in range(HEIGHT // 2):
        factor = y / (HEIGHT // 2)
        r = int(GRASS_COLOR[0] * (1 - factor * 0.5))
        g = int(GRASS_COLOR[1] * (1 - factor * 0.5))
        b = int(GRASS_COLOR[2] * (1 - factor * 0.5))
        pygame.draw.line(ground, (r, g, b), (0, y), (WIDTH, y))
    screen.blit(ground, (0, HEIGHT // 2))

# Drawing a single ray using DDA (Digital Differential Analyzer) with texture mapping
def cast_rays(height_offset=0):
    start_angle = player_angle - HALF_FOV
    for ray in range(NUM_RAYS):
        angle = start_angle + ray * DELTA_ANGLE
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        
        # Vertical and horizontal lines calculation for texture mapping
        x_vert, y_vert = 0, 0
        x_hor, y_hor = 0, 0
        texture_offset = 0
        
        # Find wall intersections
        for depth in range(MAX_DEPTH):
            target_x = player_x + depth * cos_a
            target_y = player_y + depth * sin_a
            
            # Map coordinates
            i, j = int(target_x // TILE_SIZE), int(target_y // TILE_SIZE)
            
            if 0 <= i < MAP_WIDTH and 0 <= j < MAP_HEIGHT:
                # If we hit a wall
                block_type = world_map[j][i]
                if block_type > 0:
                    if block_type == 3:  # Target
                        # Check if the target at this location is still alive
                        is_alive = False
                        for target in targets:
                            if (target['alive'] and 
                                abs(target['x'] - (i * TILE_SIZE + TILE_SIZE // 2)) < TILE_SIZE // 2 and
                                abs(target['y'] - (j * TILE_SIZE + TILE_SIZE // 2)) < TILE_SIZE // 2):
                                is_alive = True
                                hit_color = RED if target['hit_time'] > 0 else None
                                break
                        
                        if not is_alive:
                            continue  # Skip if target is not alive
                    
                    # Which edge of the block did we hit? (for texture mapping)
                    dx, dy = target_x % TILE_SIZE, target_y % TILE_SIZE
                    texture_offset = dx if abs(dy - 0) < 0.01 or abs(dy - TILE_SIZE) < 0.01 else dy
                    
                    # Get texture for this block type
                    texture = textures.get(block_type, textures[1])  # Default to dirt if missing
                    
                    depth *= math.cos(player_angle - angle)  # Remove fish-eye effect
                    proj_height = min(HEIGHT * 1.5, PROJ_COEFF / (depth + 0.0001))
                    
                    # Scale texture height to match projection height
                    if proj_height > 0:
                        wall_column = texture.subsurface(
                            int(texture_offset / TILE_SIZE * texture.get_width()), 
                            0,
                            1,
                            texture.get_height()
                        )
                        
                        # Apply shading based on distance
                        shade_factor = min(1.0, 600 / (depth + 1))
                        
                        # Scale the texture to match the projection height
                        scaled_column = pygame.transform.scale(
                            wall_column, 
                            (SCALE, int(proj_height))
                        )
                        
                        # Apply shading
                        shade = pygame.Surface(scaled_column.get_size())
                        shade.fill((0, 0, 0))
                        shade.set_alpha(int(255 * (1 - shade_factor)))
                        
                        # For targets, make them flash red when hit
                        if block_type == 3 and hit_color:
                            red_flash = pygame.Surface(scaled_column.get_size())
                            red_flash.fill(hit_color)
                            red_flash.set_alpha(128)
                            scaled_column.blit(red_flash, (0, 0))
                        
                        # Draw the column
                        screen.blit(
                            scaled_column, 
                            (ray * SCALE, HEIGHT // 2 - proj_height // 2 + height_offset)
                        )
                        screen.blit(
                            shade, 
                            (ray * SCALE, HEIGHT // 2 - proj_height // 2 + height_offset)
                        )
                    
                    break
        
        # Add code to render monsters when detected
        for monster in monsters:
            if monster.alive:
                # Calculate angle and distance to monster
                angle_to_monster = math.atan2(monster.y - player_y, monster.x - player_x)
                angle_diff = abs((angle_to_monster - angle + math.pi) % (2 * math.pi) - math.pi)
                dist_to_monster = math.sqrt((player_x - monster.x)**2 + (player_y - monster.y)**2)
                
                # If monster is in this ray's path (with small margin)
                if angle_diff < 0.02 and dist_to_monster < MAX_DEPTH:
                    # Check if there's a wall between player and monster
                    blocked = False
                    for depth in range(int(dist_to_monster)):
                        check_x = player_x + depth * math.cos(angle)
                        check_y = player_y + depth * math.sin(angle)
                        check_i, check_j = int(check_x // TILE_SIZE), int(check_y // TILE_SIZE)
                        if (0 <= check_i < MAP_WIDTH and 0 <= check_j < MAP_HEIGHT and 
                            world_map[check_j][check_i] > 0 and world_map[check_j][check_i] != 3 and 
                            world_map[check_j][check_i] != 6):
                            blocked = True
                            break
                    
                    if not blocked:
                        # Render monster
                        depth = dist_to_monster
                        depth *= math.cos(player_angle - angle)  # Remove fish-eye effect
                        proj_height = min(HEIGHT * 1.5, PROJ_COEFF / (depth + 0.0001))
                        
                        # Get monster texture
                        texture = textures[6]
                        
                        # Make monster flash red when hit
                        hit_red = monster.hit_time > 0
                        
                        # ... similar code to wall rendering, with:
                        # - Use monster texture
                        # - Apply red flash if monster.hit_time > 0
                        # - Render at proper height with player_z offset

# Draw HUD with score, ammo, and health bar in Minecraft style
def draw_hud():
    # Health bar
    health_bar_width = 200
    health_bar_height = 20
    health_pct = max(0, min(1, health / 100))
    
    # Draw health bar outline
    pygame.draw.rect(screen, (0, 0, 0), (10, HEIGHT - 40, health_bar_width + 4, health_bar_height + 4), 2)
    
    # Draw health bar
    health_color = (
        int(255 * (1 - health_pct)),
        int(255 * health_pct),
        0
    )
    pygame.draw.rect(screen, health_color, (12, HEIGHT - 38, int(health_bar_width * health_pct), health_bar_height))
    
    # Draw hearts (Minecraft style)
    for i in range(10):
        if health >= (i+1) * 10:
            # Full heart
            heart_color = (255, 0, 0)
        elif health > i * 10:
            # Half heart
            heart_color = (200, 50, 50) 
        else:
            # Empty heart
            heart_color = (100, 100, 100)
            
        pygame.draw.polygon(screen, heart_color, [
            (30 + i * 20, HEIGHT - 60),
            (40 + i * 20, HEIGHT - 70),
            (50 + i * 20, HEIGHT - 60),
            (40 + i * 20, HEIGHT - 50)
        ])
    
    # Score and ammo
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    ammo_text = font.render(f"Ammo: {ammo}", True, WHITE)
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, WHITE)
    
    screen.blit(score_text, (10, 10))
    screen.blit(ammo_text, (10, 40))
    screen.blit(fps_text, (WIDTH - 100, 10))

# Optimized game update function
def update_game_state():
    global player_velocity_z
    
    # Update physics with fixed timestep
    player_velocity_z += gravity
    player_z += player_velocity_z
    
    # Get floor height at player position with bounds checking
    map_x, map_y = int(player_x // TILE_SIZE), int(player_y // TILE_SIZE)
    floor_height = 0
    
    if 0 <= map_x < MAP_WIDTH and 0 <= map_y < MAP_HEIGHT:
        floor_height = height_map[map_y][map_x] * TILE_SIZE / 3
    
    # Check for collision with floor
    if player_z >= floor_height:
        player_z = floor_height
        player_velocity_z = 0
        is_jumping = False
        is_falling = False
    elif player_velocity_z > 0:
        is_jumping = False
        is_falling = True
    
    # Only update nearby monsters (optimization)
    for monster in monsters:
        if monster.alive:
            dx = monster.x - player_x
            dy = monster.y - player_y
            dist_squared = dx*dx + dy*dy
            
            if dist_squared < RENDER_DISTANCE * RENDER_DISTANCE:
                monster.update()

# Game loop
def game_loop():
    global player_x, player_y, player_z, player_velocity_z, player_angle, shooting, gun_cooldown, ammo, score
    global bobbing_offset, bobbing_phase, particles, block_hit_marks, health, is_jumping, is_falling

    # Initialize game world and entities
    initialize_game()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            # Shooting
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if ammo > 0 and gun_cooldown == 0:
                    shooting = True
                    gun_cooldown = GUN_COOLDOWN_MAX
                    ammo -= 1
                    shoot_sound.play()
                    
                    # Check if shot hit a target
                    if check_target_hit(player_angle):
                        print(f"Hit! Score: {score}")
            
            # Reload ammo
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if ammo < 10:
                    reload_sound.play()
                    ammo = 10
            
            # Respawn targets
            if event.type == pygame.USEREVENT:
                init_targets()
            
            # Jump
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not is_jumping and not is_falling:
                is_jumping = True
                player_velocity_z = -jump_strength
                bobbing_offset -= 10  # Quick up-movement for visual feedback
        
        # Movement
        keys = pygame.key.get_pressed()
        
        # Rotation
        mouse_rel = pygame.mouse.get_rel()
        player_angle += mouse_rel[0] * 0.002
        bobbing_offset += mouse_rel[1] * 0.05
        bobbing_offset = max(-50, min(50, bobbing_offset))
        
        # Keep angle within 0-2π range
        player_angle %= 2 * math.pi
        
        dx = dy = 0
        speed = 2
        moving = False
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dx += speed * math.cos(player_angle)
            dy += speed * math.sin(player_angle)
            moving = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dx -= speed * math.cos(player_angle)
            dy -= speed * math.sin(player_angle)
            moving = True
        if keys[pygame.K_a] and not keys[pygame.K_LEFT]:  # Strafe left
            dx += speed * math.cos(player_angle - math.pi/2)
            dy += speed * math.sin(player_angle - math.pi/2)
            moving = True
        if keys[pygame.K_d] and not keys[pygame.K_RIGHT]:  # Strafe right
            dx += speed * math.cos(player_angle + math.pi/2)
            dy += speed * math.sin(player_angle + math.pi/2)
            moving = True

        # Improved collision check
        new_x, new_y = player_x + dx, player_y + dy
        map_x, map_y = int(new_x // TILE_SIZE), int(new_y // TILE_SIZE)
        
        # Check if the new position is within map bounds
        if 0 <= map_x < MAP_WIDTH and 0 <= map_y < MAP_HEIGHT:
            # Move if there's no wall
            if world_map[map_y][map_x] == 0 or world_map[map_y][map_x] == 3:
                player_x, player_y = new_x, new_y
        
        # Handle bobbing effect
        if moving:
            bobbing_phase += 0.1
            bobbing_offset = math.sin(bobbing_phase) * bobbing_amplitude
        else:
            bobbing_offset *= 0.8  # Dampen the bobbing when not moving
        
        # Return from jump smoothly
        if bobbing_offset < 0:
            bobbing_offset *= 0.9
        
        # Handle jumping and falling physics
        player_velocity_z += gravity
        player_z += player_velocity_z
        
        # Get floor height at player position
        map_x, map_y = int(player_x // TILE_SIZE), int(player_y // TILE_SIZE)
        if 0 <= map_x < MAP_WIDTH and 0 <= map_y < MAP_HEIGHT:
            floor_height = height_map[map_y][map_x] * TILE_SIZE / 3
        else:
            floor_height = 0
        
        # Check for collision with floor
        if player_z >= floor_height:
            player_z = floor_height
            player_velocity_z = 0
            is_jumping = False
            is_falling = False
        elif player_velocity_z > 0:
            is_jumping = False
            is_falling = True
        
        # Update monsters
        for monster in monsters:
            monster.update()
            
            # Check if monster is attacking player
            if monster.alive:
                dist_to_player = math.sqrt((player_x - monster.x)**2 + (player_y - monster.y)**2)
                if dist_to_player < monster.size and monster.attack_cooldown == 0:
                    health -= monster.attack_damage
                    monster.attack_cooldown = 60
        
        # Draw background and 3D view with height offset for jumping/falling
        bobbing_with_jump = bobbing_offset - player_z
        draw_background()
        cast_rays(bobbing_with_jump)
        
        # Update and draw particles
        particles = [p for p in particles if p.update()]
        for particle in particles:
            particle.draw()
        
        # Update block hit marks
        block_hit_marks = [m for m in block_hit_marks if m.update()]
        for mark in block_hit_marks:
            mark.draw()
        
        # Update target hit flashing
        for target in targets:
            if target['hit_time'] > 0:
                target['hit_time'] -= 1
        
        # Handle shooting cooldown
        if gun_cooldown > 0:
            gun_cooldown -= 1
            if gun_cooldown == 0:
                shooting = False
        
        # Draw gun and HUD
        draw_gun()
        draw_crosshair()
        draw_hud()
        
        pygame.display.flip()
        clock.tick(60)

# Lock the mouse to the center for mouse-look controls
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# Reset and reinitialize variables for world generation
def initialize_game():
    global player_x, player_y, player_z, player_angle, monsters, targets

    # Generate the world
    generate_world()
    
    # Place player near the center
    player_x = MAP_WIDTH * TILE_SIZE // 2
    player_y = MAP_HEIGHT * TILE_SIZE // 2
    player_z = 0
    player_angle = 0
    
    # Initialize targets
    init_targets()
    
    # Initialize monsters
    monsters = []
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if world_map[y][x] == 6:  # Monster
                monsters.append(Monster(
                    x * TILE_SIZE + TILE_SIZE // 2,
                    y * TILE_SIZE + TILE_SIZE // 2
                ))

game_loop()