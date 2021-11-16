from functools import lru_cache
from typing import Iterable, Optional, Tuple

import numpy as np
from space_invaders.models.coordinate import Point
from space_invaders.models.matrix import Matrix

ALPHABET = {"-": 0, "o": 1}


class Pattern(Matrix):
    """Data structure representing a pattern in the radar or in the query."""

    __slots__ = ("top_left", "bottom_right", "mask", "vector_hash")

    def __init__(
        self,
        input,
        top_left: Point = None,
        bottom_right: Point = None,
        mask: "Mask" = None,
    ) -> None:
        super(Pattern, self).__init__(input)
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.mask = mask

    def similarity(
        self,
        candidate: "Pattern",
        threshold: float = 0,
    ) -> Optional[float]:
        """Calculate similarity percentage between current object and a
        candidate."""
        score = 1
        diff = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.matrix[i][j] != candidate.matrix[i][j]:
                    diff += 1
                    score = 1 - diff / (candidate.width * candidate.height)
                    if score < threshold:
                        return None
        return score

    @staticmethod
    def _get_char_value(char: str) -> int:
        return 1 if char == "o" else 0

    def _sum_chars(self, input: Tuple[str]) -> int:
        return sum(ALPHABET.get(char) for char in input)

    @classmethod
    def column_hash(cls, column: Iterable[str]) -> int:
        return sum(ALPHABET.get(char) for char in column)

    def slice(self, mask: "Mask") -> "Pattern":
        if mask is None:
            return self

        if mask.top_left and mask.bottom_right:
            return Pattern(
                self.matrix[
                    mask.top_left.row : mask.bottom_right.row + 1,
                    mask.top_left.col : mask.bottom_right.col + 1,
                ]
            )
        if mask.top_left:
            return Pattern(self.matrix[mask.top_left.row :, mask.top_left.col :])
        if mask.bottom_right:
            return Pattern(
                self.matrix[: mask.bottom_right.row + 1, : mask.bottom_right.col + 1]
            )

    @lru_cache()
    def hash(self, mask: "Mask" = None) -> int:
        column_hashes = np.array(
            [self._sum_chars(x) for x in zip(*self.slice(mask).matrix)]
        )
        return sum(column_hashes)

    def _vector_hash(self):
        top = self._sum_chars(self.matrix[0, :])
        bottom = self._sum_chars(self.matrix[-1, :])
        left = self._sum_chars(self.matrix[:, 0])
        right = self._sum_chars(self.matrix[:, -1])
        return top, bottom, left, right


class Mask:
    """Data structure used to mask part of the query pattern."""

    __slots__ = ("top_left", "bottom_right")

    def __init__(self, top_left: Point, bottom_right: Point):
        self.top_left = top_left
        self.bottom_right = bottom_right
