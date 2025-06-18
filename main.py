import pygame, sys
from pygame.locals import *

WORLD_WIDTH = 380
WORLD_HEIGHT = 216
PLAY_AREA_X_MIN = 4     # límite izquierdo de la zona de juego
PLAY_AREA_X_MAX = 295   # límite derecho de la zona de juego
PLAY_AREA_Y_MIN = 5     # límite superior de la zona de juego

def mi_error(mensaje):
    print(f"ERROR: {mensaje}")
    pygame.quit()
    sys.exit()


def get_new_scale_factor(display_x_resolution, display_y_resolution):
    max_x_scale_factor = int(display_x_resolution / WORLD_WIDTH)
    max_y_scale_factor = int(display_y_resolution / WORLD_HEIGHT)
    new_scale_factor = min(max_x_scale_factor, max_y_scale_factor)
    new_scale_factor = max(1, new_scale_factor) # el factor de escala mínimo es 1
    return new_scale_factor


def init_game():
    global hero
    hero.rect.x = (PLAY_AREA_X_MAX - PLAY_AREA_X_MIN - hero.rect.width) // 2  # definimos la posición inicial del sprite
    hero.rect.y = 200  # definimos la posición inicial del sprite
    hero.moving_left = False
    hero.moving_right = False

    ball.rect.x = 30
    ball.rect.y = 30
    ball.vel_y = 2


def screen_menu():
    global screen, scale_factor
    # lectura cola de eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == VIDEORESIZE:
            new_x_resolution, new_y_resolution = event.dict['size']
            scale_factor = get_new_scale_factor(new_x_resolution, new_y_resolution)
        elif event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                init_game()
                screen = "game"

    # dibujamos el frame del menú
    draw_surface.fill((0, 0, 0))
    draw_surface.blit(img_menu_title, ((WORLD_WIDTH - img_menu_title.get_width()) / 2, 50))
    draw_surface.blit(img_menu_subtitle, ((WORLD_WIDTH - img_menu_subtitle.get_width()) / 2, 80))


def screen_game():
    global scale_factor, screen

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == VIDEORESIZE:
            new_x_resolution, new_y_resolution = event.dict['size']
            scale_factor = get_new_scale_factor(new_x_resolution, new_y_resolution)
        elif event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                hero.moving_left = True
            elif event.key == K_RIGHT:
                hero.moving_right = True
        elif event.type == pygame.KEYUP:
            if event.key == K_LEFT:
                hero.moving_left = False
            elif event.key == K_RIGHT:
                hero.moving_right = False

    if hero.moving_left:
        hero.rect.x -= 3
        if hero.rect.x < PLAY_AREA_X_MIN:
            hero.rect.x = PLAY_AREA_X_MIN
    if hero.moving_right:
        hero.rect.x += 3
        if hero.rect.x > PLAY_AREA_X_MAX - hero.rect.width:
            hero.rect.x = PLAY_AREA_X_MAX - hero.rect.width

    ball.rect.y -= ball.vel_y
    if ball.rect.y < PLAY_AREA_Y_MIN:
        ball.vel_y *= -1

    if pygame.sprite.collide_rect(ball, hero):
        ball.vel_y *= -1

    # dibujamos el frame de la partida
    draw_surface.fill((0, 0, 0))
    draw_surface.blit(ball.image, (ball.rect.x, ball.rect.y))
    draw_surface.blit(hero.image, (hero.rect.x, hero.rect.y))
    draw_surface.blit(img_hud, (0, 0))

pygame.init()

# Definimos el factor inicial de escalado. Se usa para definir el tamaño inicial de la ventana
# del juego y para multiplicar la superficie draw_surface al mostrarla en display_surface
scale_factor = get_new_scale_factor(int(pygame.display.Info().current_w * 0.7), int(pygame.display.Info().current_h))

display_surface = pygame.display.set_mode((WORLD_WIDTH * scale_factor, WORLD_HEIGHT * scale_factor),  HWSURFACE | DOUBLEBUF | RESIZABLE)
draw_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT),  HWSURFACE | DOUBLEBUF)

pygame.display.set_caption('pypong')

font_title = pygame.font.Font("assets/8-bit_wonder.ttf", 24) # 8 bit wonder font: https://www.dafont.com/es/8bit-wonder.font
font_paragraph = pygame.font.Font("assets/8-bit_wonder.ttf", 7)

img_menu_title = font_title.render("pypong", False, (0, 255, 0))
img_menu_subtitle = font_paragraph.render("press space to start", False, (0, 255, 0))
img_hud = pygame.image.load('assets/hud.png')

# Creamos un objeto de la clase pygame.sprite
hero = pygame.sprite.Sprite()
hero.image = pygame.image.load('assets/hero.png')
hero.rect = hero.image.get_rect()  # definimos el hitbox del sprite

ball = pygame.sprite.Sprite()
ball.image = pygame.image.load('assets/ball.png')
ball.rect = ball.image.get_rect()  # definimos el hitbox del sprite

screen = "menu"
clock = pygame.time.Clock()
while True:  # main game loop
    if screen == "menu":
        screen_menu()
    elif screen == "game":
        screen_game()
    else:
        mi_error("Pantalla no válida")

    scaled_draw_surface = pygame.transform.scale(draw_surface, (WORLD_WIDTH * scale_factor, WORLD_HEIGHT * scale_factor))
    display_surface.fill((0, 0, 0))
    display_surface.blit(scaled_draw_surface, ((display_surface.get_width() - scaled_draw_surface.get_width()) / 2, (display_surface.get_height() - scaled_draw_surface.get_height()) / 2))
    pygame.display.update()
    clock.tick(30)
