import pygame


def show_splash_screen(screen, font):
    screen_width, screen_height = screen.get_size()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    FADE_DURATION = 3

    screen.fill(BLACK)
    text = font.render("By Damir Sakhbiev", True, WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

    for alpha in range(0, 256, 5):
        text.set_alpha(alpha)
        screen.fill(BLACK)
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(FADE_DURATION * 1000 // 256)

    pygame.time.wait(1000)

    for alpha in range(255, -1, -5):
        text.set_alpha(alpha)
        screen.fill(BLACK)
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(FADE_DURATION * 1000 // 256)


def show_menu(screen, background_image, button_images):
    if background_image:
        screen.blit(background_image, (0, 0))

    button_rects = {}
    button_positions = {}
    screen_width, screen_height = screen.get_size()
    indx = 100 * (len(button_images) // 2)
    for key, button_image in button_images.items():
        button_pos = (screen_width // 2, screen_height // 2 - indx)
        button_positions[key] = button_pos
        button_rect = button_image.get_rect(center=button_pos)
        screen.blit(button_image, button_rect.topleft)
        button_rects[key] = button_rect
        indx -= 100
    return button_rects, button_positions


def draw_buttons_with_hover(
    screen,
    button_images,
    button_positions,
    button_rects,
    mouse_pos,
    button_scale,
):
    for key, button_image in button_images.items():
        button_pos = button_positions[key]
        if button_rects[key].collidepoint(mouse_pos):
            scaled_button = pygame.transform.scale(
                button_image,
                (
                    int(button_image.get_width() * button_scale),
                    int(button_image.get_height() * button_scale),
                ),
            )
            scaled_button_rect = scaled_button.get_rect(center=button_pos)
            screen.blit(scaled_button, scaled_button_rect.topleft)
        else:
            button_rect = button_image.get_rect(center=button_pos)
            screen.blit(button_image, button_rect.topleft)
