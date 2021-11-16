from typing import List, Tuple

from space_invaders.models.pattern import Pattern
from space_invaders.models.radar import Radar

HASH_TOLERANCE = 8
SIMILARITY_THRESHOLD = 0.8


def match(pattern: Pattern, radar: Radar) -> List[Tuple[int, Pattern, int]]:
    results = []
    for sample, hash in radar.generate_samples(pattern.width, pattern.height):
        sliced_pattern = pattern.slice(sample.mask)
        if (
            sliced_pattern.hash() - HASH_TOLERANCE
            <= hash
            <= sliced_pattern.hash() + HASH_TOLERANCE
        ):
            similarity = sliced_pattern.similarity(sample, SIMILARITY_THRESHOLD)
            if similarity:
                results.append((similarity, sample, hash))
    return results
