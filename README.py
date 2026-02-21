import pygame
import sys
import random
import math
import os

pygame.init()

# -------------------------
# إعدادات الشاشة والبيانات
# -------------------------
WIDTH, HEIGHT = 1500, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invaders - Wave Motion Edition 🌌🌊")

clock = pygame.time.Clock()
FPS = 60
high_score = 0 

# تحميل الصور
try:
    BACK_IMG = pygame.image.load("background.png").convert()
    BACK_IMG = pygame.transform.scale(BACK_IMG, (WIDTH, HEIGHT))
    ENEMY_IMG = pygame.transform.scale(pygame.image.load("chicken.png").convert_alpha(), (80, 70))
    EGG_IMG = pygame.transform.scale(pygame.image.load("egg.png").convert_alpha(), (20, 25))
except:
    BACK_IMG = pygame.Surface((WIDTH, HEIGHT)); BACK_IMG.fill((0, 0, 30))
    ENEMY_IMG = pygame.Surface((80, 70)); ENEMY_IMG.fill((255, 0, 0))
    EGG_IMG = pygame.Surface((20, 25)); EGG_IMG.fill((255, 255, 0))

font_small = pygame.font.SysFont("Segoe UI Symbol", 30, bold=True)
font_large = pygame.font.SysFont("Arial", 100, bold=True)

# -------------------------
# وظائف الرسم والمنطق
# -------------------------
def create_enemy():
    return {
        "x": random.randint(100, WIDTH - 200),
        "base_y": random.randint(50, 150), # المركز الذي تتحرك حوله الموجة
        "speed": random.choice([-4, 4]),
        "angle": random.uniform(0, math.pi * 2), # زاوية البداية للموجة
        "amplitude": random.randint(30, 60),    # مدى ارتفاع وانخفاض الموجة
        "wave_speed": random.uniform(0.05, 0.1) # سرعة تذبذب الموجة
    }

def draw_player_triangle(x, y, size):
    points = [(x + size // 2, y), (x, y + size), (x + size, y + size)]
    pygame.draw.polygon(screen, (0, 200, 255), points)
    pygame.draw.polygon(screen, (255, 255, 255), points, 2)

# -------------------------
# الشاشات (Menu & Game Over)
# -------------------------
def main_menu():
    menu_running = True
    selected_option = 0
    options = ["START GAME", "QUIT"]
    while menu_running:
        screen.blit(BACK_IMG, (0,0))
        title = font_large.render("CHICKEN INVADERS", True, (255, 215, 0))
        screen.blit(title, title.get_rect(center=(WIDTH//2, 200)))
        hs_text = font_small.render(f"HIGHEST SCORE: {high_score}", True, (0, 255, 255))
        screen.blit(hs_text, hs_text.get_rect(center=(WIDTH//2, 300)))
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected_option else (100, 100, 100)
            text = font_small.render(option, True, color)
            rect = text.get_rect(center=(WIDTH//2, 450 + i * 80))
            if i == selected_option: pygame.draw.rect(screen, (0, 200, 255), rect.inflate(20, 10), 2)
            screen.blit(text, rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: selected_option = 0
                if event.key == pygame.K_DOWN: selected_option = 1
                if event.key == pygame.K_RETURN:
                    if selected_option == 0: return
                    else: pygame.quit(); sys.exit()

def game_over_screen(score, level):
    global high_score
    if score > high_score: high_score = score
    over_running = True
    while over_running:
        screen.blit(BACK_IMG, (0,0))
        title = font_large.render("MISSION FAILED", True, (255, 50, 50))
        stats = f"SCORE: {score}  |  BEST: {high_score}  |  LEVEL: {level}"
        stats_txt = font_small.render(stats, True, (255, 255, 255))
        retry_txt = font_small.render("Press SPACE to return to Menu", True, (200, 200, 200))
        screen.blit(title, title.get_rect(center=(WIDTH//2, 250)))
        screen.blit(stats_txt, stats_txt.get_rect(center=(WIDTH//2, 400)))
        screen.blit(retry_txt, retry_txt.get_rect(center=(WIDTH//2, 550)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: return

# -------------------------
# الحلقة الأساسية
# -------------------------
while True:
    main_menu()
    game = {
        "player_x": WIDTH // 2, "player_y": HEIGHT - 100,
        "bullets": [], "eggs": [], "enemies": [create_enemy()],
        "score": 0, "health": 3, "level": 1, "player_size": 35
    }
    
    game_active = True
    while game_active:
        clock.tick(FPS)
        screen.blit(BACK_IMG, (0,0))

        # تحديث الليفل والأعداء (بحد أقصى 5)
        new_level = 1 + (game["score"] // 100)
        if new_level > game["level"]:
            game["level"] = new_level
            if len(game["enemies"]) < 5: game["enemies"].append(create_enemy())

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game["bullets"].append([game["player_x"] + game["player_size"] // 2, game["player_y"]])

        # حركة اللاعب (4 اتجاهات)
        keys = pygame.key.get_pressed()
        p_speed = 10
        if keys[pygame.K_LEFT] and game["player_x"] > 0: game["player_x"] -= p_speed
        if keys[pygame.K_RIGHT] and game["player_x"] < WIDTH - game["player_size"]: game["player_x"] += p_speed
        if keys[pygame.K_UP] and game["player_y"] > 0: game["player_y"] -= p_speed
        if keys[pygame.K_DOWN] and game["player_y"] < HEIGHT - game["player_size"]: game["player_y"] += p_speed

        player_rect = pygame.Rect(game["player_x"], game["player_y"], game["player_size"], game["player_size"])

        # تحديث الأعداء (حركة Wave)
        for enemy in game["enemies"]:
            # الحركة الأفقية
            enemy["x"] += enemy["speed"] + (0.5 * game["level"] * (1 if enemy["speed"] > 0 else -1))
            if enemy["x"] <= 0 or enemy["x"] >= WIDTH - 80: enemy["speed"] *= -1
            
            # الحركة الموجية الرأسية
            enemy["angle"] += enemy["wave_speed"]
            current_y = enemy["base_y"] + math.sin(enemy["angle"]) * enemy["amplitude"]
            
            enemy_rect = pygame.Rect(enemy["x"], current_y, 80, 70)
            screen.blit(ENEMY_IMG, (enemy["x"], current_y))

            # تصادم اللاعب مع العدو
            if player_rect.colliderect(enemy_rect):
                game["health"] -= 1
                enemy["x"], enemy["base_y"] = random.randint(100, WIDTH-200), random.randint(50, 150)

            # إطلاق البيض
            fire_chance = 0.008 + (min(game["level"], 10) * 0.002) 
            if random.random() < fire_chance:
                num_eggs = 1 if game["level"] < 5 else 2
                for i in range(num_eggs):
                    game["eggs"].append([enemy["x"] + 40 + (i*20), current_y + 60])

        # الرصاص والبيض (نفس المنطق الثابت)
        for b in game["bullets"][:]:
            b[1] -= 15
            pygame.draw.circle(screen, (255, 255, 0), (int(b[0]), int(b[1])), 5)
            for enemy in game["enemies"]:
                ey = enemy["base_y"] + math.sin(enemy["angle"]) * enemy["amplitude"]
                if pygame.Rect(b[0]-5, b[1]-5, 10, 10).colliderect(pygame.Rect(enemy["x"], ey, 80, 70)):
                    game["score"] += 20
                    enemy["x"] = random.randint(100, WIDTH-200)
                    if b in game["bullets"]: game["bullets"].remove(b)
                    break
            if b in game["bullets"] and b[1] < 0: game["bullets"].remove(b)

        egg_speed = min(12, 5 + (game["level"] * 0.5))
        for egg in game["eggs"][:]:
            egg[1] += egg_speed
            screen.blit(EGG_IMG, (egg[0], egg[1]))
            if player_rect.colliderect(pygame.Rect(egg[0], egg[1], 20, 25)):
                game["health"] -= 1
                game["eggs"].remove(egg)
            elif egg[1] > HEIGHT: game["eggs"].remove(egg)

        if game["health"] <= 0:
            game_active = False
            game_over_screen(game["score"], game["level"])

        draw_player_triangle(game["player_x"], game["player_y"], game["player_size"])
        hearts = "❤️" * game["health"]
        hud = f"Score: {game['score']}   Health: {hearts}   Chickens: {len(game['enemies'])}   Level: {game['level']}"
        screen.blit(font_small.render(hud, True, (255, 255, 255)), (20, 20))
        pygame.display.flip()
