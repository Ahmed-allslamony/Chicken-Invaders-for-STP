import pygame
import sys
import random
import math
import os

pygame.init()
pygame.mixer.init() # تهيئة نظام الصوت المدمج

# -------------------------
# إعدادات الشاشة والبيانات
# -------------------------
WIDTH, HEIGHT = 1500, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invaders - Wave Motion Edition 🌌🌊")

clock = pygame.time.Clock()
FPS = 60

# -------------------------
# نظام حفظ وقراءة أعلى نتيجة
# -------------------------
HIGH_SCORE_FILE = "highscore.txt"
try:
    with open(HIGH_SCORE_FILE, "r") as file:
        high_score = int(file.read())
except:
    high_score = 0

# -------------------------
# تحميل الصور والأصوات
# -------------------------
try:
    BACK_IMG = pygame.image.load("background.png").convert()
    BACK_IMG = pygame.transform.scale(BACK_IMG, (WIDTH, HEIGHT))
    ENEMY_IMG = pygame.transform.scale(pygame.image.load("chicken.png").convert_alpha(), (80, 70))
    EGG_IMG = pygame.transform.scale(pygame.image.load("egg.png").convert_alpha(), (20, 25))
except:
    BACK_IMG = pygame.Surface((WIDTH, HEIGHT)); BACK_IMG.fill((0, 0, 30))
    ENEMY_IMG = pygame.Surface((80, 70)); ENEMY_IMG.fill((255, 0, 0))
    EGG_IMG = pygame.Surface((20, 25)); EGG_IMG.fill((255, 255, 0))

# تحميل صوت الإصابة
try:
    hit_sound_path =os.path.join("assets", "sounds", "chickDie3.mp3")
    HIT_SOUND = pygame.mixer.Sound(hit_sound_path)
except:
    HIT_SOUND = None

# تحميل صوت الانفجار
# try:
#     # لاحظ أن هذا المسار لا يزال المسار الافتراضي، قم بتعديله إذا كان لديك ملف لانفجار المربعات
#     explosion_sound_path = r"C:\مسار\الملف\الخاص\بك\explosion.mp3"
#     EXPLOSION_SOUND = pygame.mixer.Sound(explosion_sound_path)
# except:
#     EXPLOSION_SOUND = None

# تحميل صوت إطلاق النار
try:
    shoot_sound_path =os.path.join("assets", "sounds", "(beep).mp3")
    SHOOT_SOUND = pygame.mixer.Sound(shoot_sound_path)
    SHOOT_SOUND.set_volume(0.2) 
except:
    SHOOT_SOUND = None

# تحميل موسيقى الخلفية (القائمة)
try:
    bg_music_path = os.path.join("assets", "sounds", "CI4MinorWin.mp3")
    pygame.mixer.music.load(bg_music_path)
    pygame.mixer.music.set_volume(0.3)
except:
    pass 
 
# تحميل صوت الخسارة
try:
    gameover_sound_path = os.path.join("assets", "sounds", "CI4GameOver.mp3")
    GAMEOVER_SOUND = pygame.mixer.Sound(gameover_sound_path)
except:
    GAMEOVER_SOUND = None

font_small = pygame.font.SysFont("Segoe UI Symbol", 30, bold=True)
font_large = pygame.font.SysFont("Arial", 100, bold=True)

# -------------------------
# الكلاسات والوظائف
# -------------------------
class Collectible:
    def __init__(self, x, y, coll_type):
        self.rect = pygame.Rect(x, y, 25, 25) 
        self.type = coll_type                 
        self.speed = 4                        
        
    def update(self):
        self.rect.y += self.speed
        
    def draw(self, surface):
        if self.type == 'health':
            pygame.draw.rect(surface, (0, 255, 0), self.rect)
            pygame.draw.line(surface, (255, 255, 255), (self.rect.centerx, self.rect.top + 5), (self.rect.centerx, self.rect.bottom - 5), 3)
            pygame.draw.line(surface, (255, 255, 255), (self.rect.left + 5, self.rect.centery), (self.rect.right - 5, self.rect.centery), 3)
        elif self.type == 'score':
            pygame.draw.circle(surface, (255, 215, 0), self.rect.center, 12)
            pygame.draw.circle(surface, (255, 255, 255), self.rect.center, 12, 2)
        elif self.type == 'weapon':
            pygame.draw.rect(surface, (0, 100, 255), self.rect) 
            points = [(self.rect.centerx, self.rect.top + 5), (self.rect.left + 5, self.rect.bottom - 5), (self.rect.right - 5, self.rect.bottom - 5)]
            pygame.draw.polygon(surface, (255, 255, 255), points)

def create_enemy():
    return {
        "x": random.randint(100, WIDTH - 200),
        "base_y": random.randint(50, 150),
        "speed": random.choice([-4, 4]),
        "angle": random.uniform(0, math.pi * 2),
        "amplitude": random.randint(30, 60),
        "wave_speed": random.uniform(0.05, 0.1)
    }

def draw_player_triangle(x, y, size):
    points = [(x + size // 2, y), (x, y + size), (x + size, y + size)]
    pygame.draw.polygon(screen, (0, 200, 255), points)
    pygame.draw.polygon(screen, (255, 255, 255), points, 2)

# -------------------------
# الشاشات (Menu & Game Over)
# -------------------------
def main_menu():
    try:
        pygame.mixer.music.play(-1)
    except:
        pass

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
            if i == selected_option: 
                pygame.draw.rect(screen, (0, 200, 255), rect.inflate(20, 10), 2)
            screen.blit(text, rect)
            
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: selected_option = 0
                if event.key == pygame.K_DOWN: selected_option = 1
                if event.key == pygame.K_RETURN:
                    if selected_option == 0: return
                    else: pygame.quit(); sys.exit()

def game_over_screen(score, level):
    global high_score
    
    pygame.mixer.music.stop()
    
    try:
        if GAMEOVER_SOUND: GAMEOVER_SOUND.play()
    except:
        pass
        
    if score > high_score: 
        high_score = score
        try:
            with open(HIGH_SCORE_FILE, "w") as file:
                file.write(str(high_score))
        except:
            pass

    over_running = True
    while over_running:
        screen.blit(BACK_IMG, (0,0))
        title = font_large.render("MISSION FAILED", True, (255, 50, 50))
        stats = f"SCORE: {score}  |  BEST: {high_score}  |  LEVEL: {level}"
        stats_txt = font_small.render(stats, True, (255, 255, 255))
        
        # --- التعديل هنا: تم تغيير الكلمة إلى ENTER ---
        retry_txt = font_small.render("Press ENTER to Restart", True, (0, 255, 0))
        menu_txt = font_small.render("Press ESC to Main Menu", True, (200, 200, 200))
        
        screen.blit(title, title.get_rect(center=(WIDTH//2, 250)))
        screen.blit(stats_txt, stats_txt.get_rect(center=(WIDTH//2, 400)))
        screen.blit(retry_txt, retry_txt.get_rect(center=(WIDTH//2, 530)))
        screen.blit(menu_txt, menu_txt.get_rect(center=(WIDTH//2, 600)))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                # --- التعديل هنا: تم تغيير الزر إلى K_RETURN ---
                if event.key == pygame.K_RETURN: 
                    return "restart" 
                if event.key == pygame.K_ESCAPE: 
                    return "menu"

# -------------------------
# الحلقة الأساسية (Game Loop)
# -------------------------
next_action = "menu" 

while True:
    if next_action == "menu":
        main_menu()
        
    # إيقاف أي أصوات وموسيقى عند بدء اللعب
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    
    # إعادة ضبط بيانات اللعبة
    game = {
        "player_x": WIDTH // 2, "player_y": HEIGHT - 100,
        "bullets": [], "eggs": [], "enemies": [create_enemy()],
        "collectibles": [], 
        "score": 0, "health": 3, "level": 1, "player_size": 35,
        "weapon_level": 1 
    }
    
    game_active = True
    while game_active:
        clock.tick(FPS)
        screen.blit(BACK_IMG, (0,0))

        # تحديث الليفل والأعداء
        new_level = 1 + (game["score"] // 100)
        if new_level > game["level"]:
            game["level"] = new_level
            if len(game["enemies"]) < 5: 
                game["enemies"].append(create_enemy())

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit(); sys.exit()
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # تشغيل صوت إطلاق النار
                try:
                    if SHOOT_SOUND: SHOOT_SOUND.play()
                except: pass
                
                # تحديد عدد ومكان الرصاصات بناءً على الترقية
                px, py, ps = game["player_x"], game["player_y"], game["player_size"]
                
                if game["weapon_level"] == 1:
                    game["bullets"].append([px + ps // 2, py])
                elif game["weapon_level"] == 2:
                    game["bullets"].append([px, py + 10])
                    game["bullets"].append([px + ps, py + 10])
                else:
                    game["bullets"].append([px - 5, py + 15])
                    game["bullets"].append([px + ps // 2, py])
                    game["bullets"].append([px + ps + 5, py + 15])

        # حركة اللاعب
        keys = pygame.key.get_pressed()
        p_speed = 10
        if keys[pygame.K_LEFT] and game["player_x"] > 0: game["player_x"] -= p_speed
        if keys[pygame.K_RIGHT] and game["player_x"] < WIDTH - game["player_size"]: game["player_x"] += p_speed
        if keys[pygame.K_UP] and game["player_y"] > 0: game["player_y"] -= p_speed
        if keys[pygame.K_DOWN] and game["player_y"] < HEIGHT - game["player_size"]: game["player_y"] += p_speed

        player_rect = pygame.Rect(game["player_x"], game["player_y"], game["player_size"], game["player_size"])

        # تحديث الأعداء
        for enemy in game["enemies"]:
            enemy["x"] += enemy["speed"] + (0.5 * game["level"] * (1 if enemy["speed"] > 0 else -1))
            if enemy["x"] <= 0 or enemy["x"] >= WIDTH - 80: 
                enemy["speed"] *= -1
            
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

        # الرصاص واختبار التصادمات
        for b in game["bullets"][:]:
            b[1] -= 15
            pygame.draw.circle(screen, (255, 255, 0), (int(b[0]), int(b[1])), 5)
            for enemy in game["enemies"]:
                ey = enemy["base_y"] + math.sin(enemy["angle"]) * enemy["amplitude"]
                enemy_rect = pygame.Rect(enemy["x"], ey, 80, 70)
                bullet_rect = pygame.Rect(b[0]-5, b[1]-5, 10, 10)
                
                if bullet_rect.colliderect(enemy_rect):
                    # تشغيل صوت الإصابة والانفجار
                    try:
                        if HIT_SOUND: HIT_SOUND.play()
                        if EXPLOSION_SOUND: EXPLOSION_SOUND.play()
                    except: pass
                        
                    # فرصة 20% لظهور جائزة
                    if random.random() < 0.20:
                        c_type = random.choice(['health', 'score', 'weapon'])
                        game["collectibles"].append(Collectible(enemy["x"] + 25, ey + 20, c_type))

                    game["score"] += 20
                    enemy["x"] = random.randint(100, WIDTH-200)
                    if b in game["bullets"]: 
                        game["bullets"].remove(b)
                    break
                    
            if b in game["bullets"] and b[1] < 0: 
                game["bullets"].remove(b)

        # حركة البيض وتصادمه مع اللاعب
        egg_speed = min(12, 5 + (game["level"] * 0.5))
        for egg in game["eggs"][:]:
            egg[1] += egg_speed
            screen.blit(EGG_IMG, (egg[0], egg[1]))
            egg_rect = pygame.Rect(egg[0], egg[1], 20, 25)
            
            if player_rect.colliderect(egg_rect):
                game["health"] -= 1
                game["eggs"].remove(egg)
            elif egg[1] > HEIGHT: 
                game["eggs"].remove(egg)

        # تحديث ورسم الجوائز (Collectibles)
        for coll in game["collectibles"][:]:
            coll.update()
            coll.draw(screen)
            
            # التحقق من اصطدام اللاعب بالجائزة
            if player_rect.colliderect(coll.rect):
                if coll.type == 'health':
                    if game["health"] < 5: 
                        game["health"] += 1     
                elif coll.type == 'score':
                    game["score"] += 100 
                elif coll.type == 'weapon':
                    if game["weapon_level"] < 3: 
                        game["weapon_level"] += 1
                    
                game["collectibles"].remove(coll)
                
            elif coll.rect.y > HEIGHT:
                game["collectibles"].remove(coll)

        # واجهة المستخدم ورسم اللاعب
        draw_player_triangle(game["player_x"], game["player_y"], game["player_size"])
        hearts = "❤️" * game["health"]
        hud = f"Score: {game['score']}   Health: {hearts}   Chickens: {len(game['enemies'])}   Level: {game['level']}   Weapon: Lv {game['weapon_level']}"
        screen.blit(font_small.render(hud, True, (255, 255, 255)), (20, 20))
        
        pygame.display.flip()

        # نهاية اللعبة
        if game["health"] <= 0:
            game_active = False
            next_action = game_over_screen(game["score"], game["level"])
