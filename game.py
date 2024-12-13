import pygame
import pygame.locals
import sys
from menu import show_menu, draw_buttons_with_hover
from constants import (
    TILE_WIDTH,
    TILE_HEIGHT,
    IMAGE_PATHS,
    FPS,
    BLACK,
    MAX_TILES_X,
    MAX_TILES_Y,
    BUTTON_SCALE,
    BUTTON_GAME_IMAGES_PATHS,
)
from utils import load_image

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
destructible_group = pygame.sprite.Group()
indestructible_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
bombs_group = pygame.sprite.Group()
explosions_group = pygame.sprite.Group()
len_fire = 1
speed = 1


def reset_game():
    all_sprites.empty()
    tiles_group.empty()
    player_group.empty()
    walls_group.empty()
    bombs_group.empty()
    destructible_group.empty()
    indestructible_group.empty()
    enemies_group.empty()
    explosions_group.empty()


def show_victory_screen(screen):
    font = pygame.font.Font(None, 74)
    text = font.render("Победа", True, (255, 255, 255))
    screen_width, screen_height = screen.get_size()
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

        screen.fill(BLACK)
        screen.blit(text, text_rect)
        pygame.display.flip()


def handle_pause(
    screen,
    button_images,
    button_scale,
):
    paused = True

    button_rects, button_positions = show_menu(
        screen,
        None,
        button_images,
    )
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_rects["start"].collidepoint(mouse_pos):
                    paused = False
                elif button_rects["menu"].collidepoint(mouse_pos):
                    return "menu"
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        draw_buttons_with_hover(
            screen,
            button_images,
            button_positions,
            button_rects,
            mouse_pos,
            button_scale,
        )

        pygame.display.flip()
    return "game"


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        pos_x,
        pos_y,
        groups,
        player_image,
        bomb_image,
        tiles_image,
        offset_x,
        offset_y,
    ):
        super().__init__(*groups)
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.bomb_image = bomb_image
        self.image = player_image
        self.tiles_image = tiles_image
        self.rect = self.image.get_rect(
            topleft=(
                pos_x * TILE_WIDTH + offset_x,
                pos_y * TILE_HEIGHT + offset_y,
            )
        )

    def run(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.locals.K_LEFT]:
            self.rect = self.rect.move(-speed, 0)
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect = self.rect.move(speed, 0)
        if keys[pygame.locals.K_RIGHT]:
            self.rect = self.rect.move(speed, 0)
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect = self.rect.move(-speed, 0)
        if keys[pygame.locals.K_UP]:
            self.rect = self.rect.move(0, -speed)
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect = self.rect.move(0, speed)
        if keys[pygame.locals.K_DOWN]:
            self.rect = self.rect.move(0, speed)
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect = self.rect.move(0, -speed)

    def update(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pos_x, pos_y = (
                (self.rect.centerx - self.offset_x) // TILE_WIDTH,
                (self.rect.centery - self.offset_y) // TILE_HEIGHT,
            )
            Bomb(
                pos_x,
                pos_y,
                [bombs_group],
                self.bomb_image,
                self.tiles_image,
                self.offset_x,
                self.offset_y,
            )


class Enemy(pygame.sprite.Sprite):
    def __init__(
        self, pos_x, pos_y, groups, enemy_image, offset_x, offset_y, type_move
    ):
        super().__init__(*groups)
        self.image = enemy_image
        self.type_move = type_move
        self.speed = 1
        self.rect = self.image.get_rect(
            topleft=(
                pos_x * TILE_WIDTH + offset_x + 5,
                pos_y * TILE_HEIGHT + offset_y + 5,
            )
        )

    def update(self):
        if self.type_move == "-":
            self.rect = self.rect.move(self.speed, 0)
            if pygame.sprite.spritecollideany(
                self, walls_group
            ) or pygame.sprite.spritecollideany(self, bombs_group):
                self.rect = self.rect.move(-self.speed, 0)
                self.speed = -self.speed
        else:
            self.rect = self.rect.move(0, self.speed)
            if pygame.sprite.spritecollideany(
                self, walls_group
            ) or pygame.sprite.spritecollideany(self, bombs_group):
                self.rect = self.rect.move(0, -self.speed)
                self.speed = -self.speed

        if pygame.sprite.spritecollideany(self, explosions_group):

            self.kill()


class Tile(pygame.sprite.Sprite):
    def __init__(
        self, tile_type, pos_x, pos_y, groups, tile_images, offset_x, offset_y
    ):
        super().__init__(*groups)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect(
            topleft=(
                pos_x * TILE_WIDTH + offset_x,
                pos_y * TILE_HEIGHT + offset_y,
            )
        )


class Bomb(pygame.sprite.Sprite):
    def __init__(
        self, pos_x, pos_y, groups, bomb_image, tiles_image, offset_x, offset_y
    ):
        super().__init__(*groups)
        self.image = bomb_image
        self.tiles_image = tiles_image
        self.rect = self.image.get_rect(
            topleft=(
                pos_x * TILE_WIDTH + offset_x + 12.5,
                pos_y * TILE_HEIGHT + offset_y + 12.5,
            )
        )
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.timer = 3000
        self.start_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.timer:
            self.explode()

    def explode(self):
        pos_x, pos_y = (
            (self.rect.centerx - self.offset_x) // TILE_WIDTH,
            (self.rect.centery - self.offset_y) // TILE_HEIGHT,
        )
        for current_pos_x in range(pos_x, pos_x + len_fire + 1):
            explosion = Explosion(
                current_pos_x,
                pos_y,
                explosions_group,
                self.offset_x,
                self.offset_y,
                "x",
            )
            if pygame.sprite.spritecollideany(explosion, indestructible_group):
                explosion.kill()
                break
            wall = pygame.sprite.spritecollideany(
                explosion, destructible_group
            )

            if wall:
                wall.kill()
                Tile(
                    "empty",
                    current_pos_x,
                    pos_y,
                    [all_sprites, tiles_group],
                    self.tiles_image,
                    self.offset_x,
                    self.offset_y,
                )
                break
        for current_pos_x in range(pos_x - 1, pos_x - len_fire - 1, -1):
            explosion = Explosion(
                current_pos_x,
                pos_y,
                explosions_group,
                self.offset_x,
                self.offset_y,
                "x",
            )
            if pygame.sprite.spritecollideany(explosion, indestructible_group):
                explosion.kill()
                break
            wall = pygame.sprite.spritecollideany(
                explosion, destructible_group
            )

            if wall:
                wall.kill()
                Tile(
                    "empty",
                    current_pos_x,
                    pos_y,
                    [all_sprites, tiles_group],
                    self.tiles_image,
                    self.offset_x,
                    self.offset_y,
                )
                break
        for current_pos_y in range(pos_y, pos_y + len_fire + 1):
            explosion = Explosion(
                pos_x,
                current_pos_y,
                explosions_group,
                self.offset_x,
                self.offset_y,
                "y",
            )
            if pygame.sprite.spritecollideany(explosion, indestructible_group):
                explosion.kill()
                break
            wall = pygame.sprite.spritecollideany(
                explosion, destructible_group
            )

            if wall:
                wall.kill()
                Tile(
                    "empty",
                    pos_x,
                    current_pos_y,
                    [all_sprites, tiles_group],
                    self.tiles_image,
                    self.offset_x,
                    self.offset_y,
                )
                break
        for current_pos_y in range(pos_y - 1, pos_y - len_fire - 1, -1):
            explosion = Explosion(
                pos_x,
                current_pos_y,
                explosions_group,
                self.offset_x,
                self.offset_y,
                "y",
            )
            if pygame.sprite.spritecollideany(explosion, indestructible_group):
                explosion.kill()
                break
            wall = pygame.sprite.spritecollideany(
                explosion, destructible_group
            )

            if wall:
                wall.kill()
                Tile(
                    "empty",
                    pos_x,
                    current_pos_y,
                    [all_sprites, tiles_group],
                    self.tiles_image,
                    self.offset_x,
                    self.offset_y,
                )
                break

        self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, groups, offset_x, offset_y, side):
        super().__init__(groups)
        if side == "x":
            self.image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT // 2))
            self.rect = self.image.get_rect().move(
                TILE_WIDTH * pos_x + offset_x,
                TILE_HEIGHT * pos_y + 12.5 + offset_y,
            )
        else:
            self.image = pygame.Surface((TILE_WIDTH // 2, TILE_HEIGHT))
            self.rect = self.image.get_rect().move(
                TILE_WIDTH * pos_x + 12.5 + offset_x,
                TILE_HEIGHT * pos_y + offset_y,
            )
        self.image.fill((255, 0, 0))
        self.timer = 1000
        self.start_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.timer:
            self.kill()


def load_level(filename):
    filename = "data/levels/" + filename
    with open(filename, "r") as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, "."), level_map))


def generate_level(level, offset_x, offset_y):
    player_image = load_image(IMAGE_PATHS["player"])
    tile_images = {
        "wall": load_image(IMAGE_PATHS["wall"]),
        "empty": load_image(IMAGE_PATHS["empty"]),
        "cobblestone": load_image(IMAGE_PATHS["cobblestone"]),
    }
    bomb_image = load_image(IMAGE_PATHS["bomb"])
    enemy_image = load_image(IMAGE_PATHS["enemy"])
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == ".":
                Tile(
                    "empty",
                    x,
                    y,
                    [all_sprites, tiles_group],
                    tile_images,
                    offset_x,
                    offset_y,
                )
            elif level[y][x] == "#":
                Tile(
                    "cobblestone",
                    x,
                    y,
                    [
                        all_sprites,
                        walls_group,
                        tiles_group,
                        indestructible_group,
                    ],
                    tile_images,
                    offset_x,
                    offset_y,
                )
            elif level[y][x] == "$":
                Tile(
                    "wall",
                    x,
                    y,
                    [
                        all_sprites,
                        walls_group,
                        tiles_group,
                        destructible_group,
                    ],
                    tile_images,
                    offset_x,
                    offset_y,
                )
            elif level[y][x] == "@":
                Tile(
                    "empty",
                    x,
                    y,
                    [all_sprites, tiles_group],
                    tile_images,
                    offset_x,
                    offset_y,
                )
                new_player = Player(
                    x,
                    y,
                    [player_group],
                    player_image,
                    bomb_image,
                    tile_images,
                    offset_x,
                    offset_y,
                )
            elif level[y][x] == "-" or level[y][x] == "|":
                Tile(
                    "empty",
                    x,
                    y,
                    [all_sprites, tiles_group],
                    tile_images,
                    offset_x,
                    offset_y,
                )
                Enemy(
                    x,
                    y,
                    [
                        all_sprites,
                        enemies_group,
                    ],
                    enemy_image,
                    offset_x,
                    offset_y,
                    level[y][x],
                )

    return new_player


def game_loop(screen, db_manager):
    level = db_manager.get_value("level")
    pygame.display.set_caption(f"level: {level}")
    screen_width, screen_height = screen.get_size()
    BUTTON_IMAGES = {
        key: load_image(value)
        for key, value in BUTTON_GAME_IMAGES_PATHS.items()
    }
    level_width = MAX_TILES_X * TILE_WIDTH
    level_height = MAX_TILES_Y * TILE_HEIGHT
    offset_x = (screen_width - level_width) // 2
    offset_y = (screen_height - level_height) // 2
    player = generate_level(load_level(f"{level}.txt"), offset_x, offset_y)
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    next_screen = handle_pause(
                        screen, BUTTON_IMAGES, BUTTON_SCALE
                    )
                    if next_screen == "menu":
                        reset_game()
                        running = False
                        return
                player.update(event)
        bombs_group.update()
        explosions_group.update()
        enemies_group.update()
        if pygame.sprite.spritecollideany(
            player, explosions_group
        ) or pygame.sprite.spritecollideany(player, enemies_group):
            reset_game()
            player = generate_level(
                load_level(f"{level}.txt"), offset_x, offset_y
            )
        if len(enemies_group) == 0:
            reset_game()
            level = level + 1
            try:
                player = generate_level(
                    load_level(f"{level}.txt"), offset_x, offset_y
                )
                db_manager.insert_or_update("level", level)
            except FileNotFoundError:
                level -= 1
                show_victory_screen(screen)
                running = False
                return
        player.run()
        tiles_group.draw(screen)
        player_group.draw(screen)
        enemies_group.draw(screen)
        bombs_group.draw(screen)
        explosions_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
