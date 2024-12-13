import pygame
import sys
from constants import (
    FONT_SIZE,
    IMAGE_PATHS,
    BUTTON_SETTING_IMAGES_PATHS,
    BUTTON_SCALE,
    WHITE,
    BLACK,
)
from menu import show_menu
from utils import load_image

pygame.init()

font = pygame.font.Font(None, FONT_SIZE)


def handle_settings_menu(screen, db_manager):
    screen_width, screen_height = screen.get_size()
    background_image = load_image(IMAGE_PATHS["background"])
    BUTTON_IMAGES = {
        key: load_image(value)
        for key, value in BUTTON_SETTING_IMAGES_PATHS.items()
    }
    button_rects, button_positions = show_menu(
        screen, background_image, BUTTON_IMAGES
    )
    while True:
        pygame.display.set_caption("ОПЦИИ")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_rects["menu"].collidepoint(mouse_pos):
                    return
                elif button_rects["plus_volume"].collidepoint(mouse_pos):
                    current_volume = db_manager.get_value("music_volume")
                    db_manager.insert_or_update(
                        "music_volume", min(current_volume + 0.1, 1.0)
                    )
                elif button_rects["minus_volume"].collidepoint(mouse_pos):
                    current_volume = db_manager.get_value("music_volume")
                    db_manager.insert_or_update(
                        "music_volume", max(current_volume - 0.1, 0.0)
                    )
                elif button_rects["resolution"].collidepoint(mouse_pos):
                    current_screen_type = db_manager.get_value("screen_type")
                    if current_screen_type == 1:
                        db_manager.insert_or_update("screen_type", 2)
                    else:
                        db_manager.insert_or_update("screen_type", 1)

        mouse_pos = pygame.mouse.get_pos()

        screen.blit(background_image, (0, 0))

        for key, button_image in BUTTON_IMAGES.items():
            button_pos = button_positions[key]
            if button_rects[key].collidepoint(mouse_pos):
                scaled_button = pygame.transform.scale(
                    button_image,
                    (
                        int(button_image.get_width() * BUTTON_SCALE),
                        int(button_image.get_height() * BUTTON_SCALE),
                    ),
                )
                scaled_button_rect = scaled_button.get_rect(center=button_pos)
                screen.blit(scaled_button, scaled_button_rect.topleft)
            else:
                button_rect = button_image.get_rect(center=button_pos)
                screen.blit(button_image, button_rect.topleft)

        volume_text = font.render(
            f"Громкость: {round(db_manager.get_value('music_volume'), 2)}",
            True,
            WHITE,
        )
        screen_type = (
            "window"
            if db_manager.get_value("screen_type") == 1
            else "full screan"
        )
        text = font.render(
            "Настройки будут применены после захода в игру",
            False,
            BLACK,
        )
        resolution_text = font.render(f"Рзрешение: {screen_type}", True, WHITE)
        screen.blit(text, (0, 0))
        screen.blit(volume_text, (0, 30))
        screen.blit(resolution_text, (0, 60))

        pygame.display.flip()
