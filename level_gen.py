from obstacle import Obstacle
from platform import Platform
from player import Player


def generate_level(cell_coef, level_str):
    cell_width = cell_coef * Player.PLAYER_HEIGHT
    cell_height = cell_width * 2
    rows = list(filter(lambda s: s != "", map(lambda s: s.strip(), level_str.splitlines())))
    level_size = (len(rows[0]) * cell_width, len(rows) * cell_height)
    level = []
    player_pos = None
    for y, row in enumerate(rows):
        for x, el in enumerate(row):
            if el == '=' or el == 'W':
                if y < len(rows) - 1:
                    level.append(
                        Platform(x * cell_width + cell_width // 2, y * cell_height + cell_height // 10, cell_width,
                                 cell_height // 5, el == 'W'))
                else:
                    level.append(
                        Platform(x * cell_width + cell_width // 2, y * cell_height + cell_height // 2, cell_width,
                                 cell_height, el == 'W'))
            elif el == '#':
                level.append(Obstacle(x * cell_width + cell_width // 2, y * cell_height + cell_height // 2, cell_width,
                                      cell_height))
            elif el == 'P':
                player_pos = (x * cell_width + cell_width // 2, y * cell_height + cell_height // 2)
    if not player_pos:
        raise ValueError("Player position not found")
    return {
        "player_pos": player_pos,
        "size": level_size,
        "level": level
    }
