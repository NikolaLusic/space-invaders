from space_invaders.models.pattern import Pattern
from space_invaders.models.radar import Radar


def load_file(file_path: str):
    with open(file_path) as f:
        return f.read()


def load_radar(file_path: str = None):
    return Radar(load_file(file_path))


def load_pattern(file_path: str = None):
    return Pattern(load_file(file_path))
