import pygame
from pygame.locals import *
import sys
import random
import time
 
pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional
 
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snowman Platformer")

background = pygame.image.load("background.png")

Butt_font = pygame.font.Font(None, 30)
test_font = pygame.font.Font('font/Pixeltype.ttf', 55)
test_font2 = pygame.font.Font('font/Barbie.otf', 40)
bg_music = pygame.mixer.Sound('audio/snow.mp3')
bg_music.play(loops=-1)

blue = (4, 72, 148)
bluey = (76, 172, 233)
bluey2 = (26,128,229)
bluey3 = (159, 210, 239)
bluey4 = (142, 194, 226)
Dusty_Green = (168, 168, 168)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.image.load("snowman.png")
        self.rect = self.surf.get_rect()
   
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
        self.score = 0 
 
    def move(self):
        self.acc = vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
                 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
             
        self.rect.midbottom = self.pos
 
    def jump(self): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
    def update(self):
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:   
                        hits[0].point = False   
                        self.score += 1          
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load("graphics/coin/coin.png")
        self.rect = self.image.get_rect()

        self.rect.topleft = pos

    def update(self):
        if self.rect.colliderect(P1.rect):
            P1.score += 5
            self.kill()


class Button:
    def __init__(self, text, width, height, pos, elevation):
        # Core attributes
        self.pressed = False
        self.elevatation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        # Creating a top rect
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = bluey2

        # Creating a bottom rect
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_colour = bluey

        # Text
        self.text_surface = Butt_font.render(text, True, blue)
        self.text_rect = self.text_surface.get_rect(center=self.top_rect.center)

    def draw(self):
        # Elevation Logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(displaysurface, self.bottom_colour, self.bottom_rect, border_radius=12)
        # The border_radius code makes the button more rounded.
        pygame.draw.rect(displaysurface, self.top_color, self.top_rect, border_radius=12)
        displaysurface.blit(self.text_surface, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        # It checks whether the mouse is colliding with a single point
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = Dusty_Green
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevatation
                if self.pressed == True:
                    print('click')
                    self.pressed = False

        else:
            self.dynamic_elevation = self.elevatation
            self.top_color = bluey3


class platform(pygame.sprite.Sprite):
    def __init__(self, width = 0, height = 18):
        super().__init__()

        if width == 0:
            width = random.randint(50, 120)

        self.image = pygame.image.load("platform.png")
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),
                                               random.randint(0, HEIGHT-30)))

        self.point = True   
        self.moving = True
        self.speed = random.randint(-1, 1)

        if (self.speed == 0):
            self.moving == False
 
    def move(self):
        hits = self.rect.colliderect(P1.rect)
        if self.moving == True:  
            self.rect.move_ip(self.speed,0)
            if hits:
                P1.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

    def generateCoin(self):
        if (self.speed == 0):
            coins.add(Coin((self.rect.centerx, self.rect.centery - 50)))
 
 
def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False
 
def plat_gen():
    while len(platforms) < 6:
        width = random.randrange(50,100)
        p  = None      
        C = True
         
        while C:
             p = platform()
             p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-50, 0))
             C = check(p, platforms)

        p.generateCoin()
        platforms.add(p)
        all_sprites.add(p)
 

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
coins = pygame.sprite.Group()
        
PT1 = platform(450, 80)
#PT1.surf = pygame.Surface((WIDTH, 20))
#PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
PT1.moving = False
PT1.point = False 
 
P1 = Player()

all_sprites.add(PT1)
all_sprites.add(P1)
platforms.add(PT1)

 
for x in range(random.randint(4,5)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    pl.generateCoin()
    platforms.add(pl)
    all_sprites.add(pl)

start_button = Button('Start Game', 150, 40, (130, 250), 6)
exit_button = Button('Exit', 150, 40, (130, 350), 6)
try_again_button = Button('Try Again', 150, 40, (130, 250), 6)


game_started = False
game_running = True
game_over = False

while game_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    if not game_started:
        displaysurface.fill(blue)
        game_name = test_font.render('Snowman', False, (225, 225, 225))
        game_name2 = test_font.render('Platformer', False, (225, 225, 225))
        
        game_name_rect = game_name.get_rect(center=(WIDTH / 2, 63))
        game_name_rect_two = game_name.get_rect(center=(188, 100))

        displaysurface.blit(game_name, game_name_rect)
        displaysurface.blit(game_name2, game_name_rect_two)
        
        start_button.draw()
        exit_button.draw()

        if start_button.pressed:
            game_started = True

    elif game_over:
        # Game over screen
        displaysurface.fill(blue)
        game_over_text = test_font2.render("Game Over", False, (255, 255, 255))
        game_over_text2 = test_font2.render(f'Your score: {P1.score}', False, (255, 255, 255))
        
        game_over_rect = game_over_text.get_rect(center=(WIDTH / 2, 63))
        game_over_rect2 = game_over_text2.get_rect(center=(198, 100))
        
        displaysurface.blit(game_over_text, game_over_rect)
        displaysurface.blit(game_over_text2, game_over_rect2)

        try_again_button.draw()
        exit_button.draw()

        if try_again_button.pressed:
            # Reset game state
            all_sprites.empty()
            platforms.empty()
            coins.empty()

            PT1 = platform(450, 80)
            PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
            PT1.moving = False
            PT1.point = False

            P1 = Player()

            all_sprites.add(PT1)
            all_sprites.add(P1)
            platforms.add(PT1)

            for x in range(random.randint(4, 5)):
                C = True
                pl = platform()
                while C:
                    pl = platform()
                    C = check(pl, platforms)
                pl.generateCoin()
                platforms.add(pl)
                all_sprites.add(pl)

            game_over = False

        elif exit_button.pressed:
            pygame.quit()
            sys.exit()


    #Game screen
    else:
        # Game screen
        P1.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            P1.jump()
        else:
            P1.cancel_jump()

        if P1.rect.top > HEIGHT:
            game_over = True

        if P1.rect.top <= HEIGHT / 3:
            P1.pos.y += abs(P1.vel.y)
            for plat in platforms:
                plat.rect.y += abs(P1.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()


            for coin in coins:
                coin.rect.y += abs(P1.vel.y)
                if coin.rect.top >= HEIGHT:
                    coin.kill()

        plat_gen()

        displaysurface.blit(background, (0, 0))
        f = pygame.font.SysFont("Verdana", 20)
        g = f.render(str(P1.score), True, (123, 255, 0))
        displaysurface.blit(g, (WIDTH / 2, 10))

        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
            entity.move()

        for coin in coins:
            displaysurface.blit(coin.image, coin.rect)
            coin.update()


    pygame.display.update()
    FramePerSec.tick(FPS)


    if exit_button.pressed:
        pygame.quit()
        sys.exit()

