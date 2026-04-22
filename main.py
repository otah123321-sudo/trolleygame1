import pygame
import random
import os

# --- Настройки ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trolleybus Pro 0.0.2")
clock = pygame.time.Clock()

fullscreen = False
BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, 'images')

def get_image(name, size):
    path = os.path.join(IMG_DIR, name)
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except:
        surf = pygame.Surface(size)
        surf.fill((150, 0, 200)) # Те самые фиолетовые квадраты
        pygame.draw.rect(surf, (220, 50, 255), surf.get_rect(), 4)
        return surf

# --- Рекорды ---
def load_record():
    try:
        if os.path.exists("record.txt"):
            with open("record.txt", "r") as f: return int(f.read())
    except: pass
    return 0

def save_record(score):
    try:
        with open("record.txt", "w") as f: f.write(str(score))
    except: pass

# --- Ресурсы ---
# Игрок размера "6"
player_img = get_image('player.png', (120, 150))
item_img = get_image('item.png', (80, 60))

bgs = {
    '1': get_image('bg_tashkent.png', (WIDTH, HEIGHT)),
    '2': get_image('bg_space.png', (WIDTH, HEIGHT)),
    '3': get_image('bg_jupiter.png', (WIDTH, HEIGHT)),
    '4': get_image('bg_univ.png', (WIDTH, HEIGHT)),
    '5': get_image('bg_city.png', (WIDTH, HEIGHT))
}

# --- Классы ---
class Player_Class(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(midbottom=(WIDTH//2, HEIGHT-10))
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: self.rect.x -= 12
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.rect.x += 12
        
        # Мышь (движение персонажа)
        if pygame.mouse.get_rel()[0] != 0:
            self.rect.centerx = pygame.mouse.get_pos()[0]
        
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

class Item_Class(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = item_img
        self.rect = self.image.get_rect()
        self.reset()
    
    def reset(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-400, -50)
        self.speed = random.randint(3, 6) # Медленно

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT: self.reset()

# --- Логика ---
MENU, GAME = 0, 1
state = MENU
score = 0
high_score = load_record()
active_bg = None

all_sprites = pygame.sprite.Group()
items_group = pygame.sprite.Group()
player_obj = None # Игрок с маленькой буквы

font = pygame.font.SysFont("Arial", 40, bold=True)
sm_font = pygame.font.SysFont("Arial", 25)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # Ctrl + A: Полный экран
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and event.key == pygame.K_a:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

            if state == MENU:
                choice = pygame.key.name(event.key)
                if choice in bgs:
                    active_bg = bgs[choice]
                    state = GAME
                    score = 0
                    all_sprites.empty(); items_group.empty()
                    player_obj = Player_Class()
                    all_sprites.add(player_obj)
                    for _ in range(5):
                        it = Item_Class(); all_sprites.add(it); items_group.add(it)
            
            elif event.key == pygame.K_ESCAPE:
                state = MENU

    if state == MENU:
        screen.fill((20, 20, 40))
        screen.blit(font.render("TROLLEYBUS PRO 0.0.2", True, (255, 255, 255)), (180, 80))
        screen.blit(sm_font.render(f"РЕКОРД: {high_score}", True, (255, 215, 0)), (320, 150))
        screen.blit(sm_font.render("CTRL+A: ПОЛНЫЙ ЭКРАН", True, (0, 255, 0)), (300, 190))
        
        y = 250
        maps = ["1: ТАШКЕНТ", "2: КОСМОС", "3: ЮПИТЕР", "4: ВСЕЛЕННАЯ", "5: КРАСИВЫЙ ГОРОД"]
        for m in maps:
            screen.blit(sm_font.render(m, True, (200, 100, 255)), (300, y))
            y += 40
            
    elif state == GAME:
        all_sprites.update()
        
        # Проверка касания без вылетов
        if player_obj is not None:
            hits = pygame.sprite.spritecollide(player_obj, items_group, True)
            for hit in hits:
                score += 1
                if score > high_score:
                    high_score = score
                    save_record(high_score)
                new_it = Item_Class()
                all_sprites.add(new_it); items_group.add(new_it)

        screen.blit(active_bg, (0, 0))
        all_sprites.draw(screen)
        screen.blit(font.render(f"СЧЕТ: {score}", True, (255, 255, 255)), (10, 10))
        screen.blit(sm_font.render(f"РЕКОРД: {high_score}", True, (255, 215, 0)), (10, 60))

    pygame.display.flip()
    clock.tick(144)

pygame.quit()