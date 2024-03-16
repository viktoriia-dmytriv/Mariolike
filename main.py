from enum import Enum

import globals
import levels
from globals import *
from player import Player

# initialize pygame
pygame.init()

# set up the window
window = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption('Mariolike')


class State(Enum):
    PAUSE = 1
    RECORDING = 2
    PLAYING = 3
    WIN = 4
    LOSE = 5


current_level = 0

all_sprites = None
player = None
current_state = None
frames = None
time_moving = None
screen = None


def start_level(level):
    global all_sprites, player, current_state, frames, time_moving, screen
    globals.WIDTH, globals.HEIGHT = level["size"]
    globals.level = level["level"]
    screen = pygame.Surface((globals.WIDTH, globals.HEIGHT))
    all_sprites = pygame.sprite.Group()
    all_sprites.add(globals.level)
    player = Player(level["player_pos"])
    all_sprites.add(player)
    current_state = State.RECORDING
    frames = []
    time_moving = 1


start_level(levels.levels[current_level])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    clock.tick(60)
    keys = pygame.key.get_pressed()

    need_restart = False

    window.fill((0, 0, 0))
    if frames:
        current_frame = frames[0].copy()
    else:
        current_frame = None
    if current_state == State.PLAYING:
        if current_frame:
            pygame.draw.polygon(current_frame, (0, 192, 0), [(10, 10), (40, 25), (10, 40)])
        if len(frames) <= 1:
            if player.win:
                current_state = State.WIN
            elif player.lose:
                current_state = State.LOSE
            else:
                current_state = State.PAUSE
        else:
            frames.pop(0)
    elif current_state == State.PAUSE:
        if current_frame:
            pygame.draw.rect(current_frame, (0, 0, 192), (10, 10, 10, 30))
            pygame.draw.rect(current_frame, (0, 0, 192), (30, 10, 10, 30))
        if keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP]:
            time_moving = 1
            current_state = State.RECORDING
    elif current_state == State.RECORDING:
        if current_frame:
            pygame.draw.circle(current_frame, (255, 0, 0), (25, 25), 15)

        if keys[pygame.K_UP]:
            player.jump()

        if keys[pygame.K_LEFT]:
            player.move_left()
        elif keys[pygame.K_RIGHT]:
            player.move_right()
        else:
            player.stop()

        all_sprites.update()

        if player.win or player.lose:
            current_state = State.PLAYING

        # drawing the scene
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)

        frames.append(screen.copy())

        time_moving -= clock.get_time() / 1000
        if time_moving <= 0:
            current_state = State.PLAYING
    elif current_state == State.WIN:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('You win!', True, (0, 0, 0))
        if current_frame:
            current_frame.blit(text, (0, 0))
        if keys[pygame.K_DOWN]:
            if current_level + 1 < len(levels.levels):
                current_level += 1
            need_restart = True
    elif current_state == State.LOSE:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('You lose!', True, (0, 0, 0))
        if current_frame:
            current_frame.blit(text, (0, 0))
        if keys[pygame.K_DOWN]:
            need_restart = True

    if current_frame:
        width = min(globals.WIDTH / globals.HEIGHT * window.get_height(), window.get_width())
        height = min(globals.HEIGHT / globals.WIDTH * window.get_width(), window.get_height())
        window.blit(
            pygame.transform.scale(current_frame, (width, height)),
            ((window.get_width() - width) / 2, (window.get_height() - height) / 2))
    pygame.display.flip()
    if need_restart:
        start_level(levels.levels[current_level])
