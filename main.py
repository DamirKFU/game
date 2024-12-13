import pygame
import sys
from menu import show_splash_screen, show_menu, draw_buttons_with_hover
from constants import (
    FONT_SIZE,
    IMAGE_PATHS,
    BUTTON_IMAGES_PATHS,
    BUTTON_SCALE,
)
import db
from settings_menu import handle_settings_menu


from game import game_loop
from utils import load_image


pygame.init()
font = pygame.font.Font(None, FONT_SIZE)
db_manager = db.SQLiteManager("data.db")
screen_type = db_manager.get_value("screen_type")
if screen_type == 1:
    screen = pygame.display.set_mode((1050, 650))
else:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
background_image = load_image(IMAGE_PATHS["background"])
BUTTON_IMAGES = {
    key: load_image(value) for key, value in BUTTON_IMAGES_PATHS.items()
}
pygame.display.set_caption("Заставка")

show_splash_screen(screen, font)
volume = db_manager.get_value("music_volume")
pygame.mixer.music.load("data/music/background.mp3")
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)
while True:
    pygame.display.set_caption("МЕНЮ")
    button_rects, button_positions = show_menu(
        screen, background_image, BUTTON_IMAGES
    )
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if button_rects["start"].collidepoint(mouse_pos):
                game_loop(
                    screen,
                    db_manager,
                )
            elif button_rects["online"].collidepoint(mouse_pos):
                handle_settings_menu(screen, db_manager)
            elif button_rects["exit"].collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()
    mouse_pos = pygame.mouse.get_pos()

    screen.blit(background_image, (0, 0))

    draw_buttons_with_hover(
        screen,
        BUTTON_IMAGES,
        button_positions,
        button_rects,
        mouse_pos,
        BUTTON_SCALE,
    )

    pygame.display.flip()
