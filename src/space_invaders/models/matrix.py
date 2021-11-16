from typing import Generator, List, Union

import numpy as np


class Matrix:
    """Data structure representing a 2D matrix."""

    __slots__ = "matrix"

    def __init__(self, input: Union[str, List[List[str]], Generator]) -> None:
        if isinstance(input, str):
            self.matrix = self._parse_str(input)
        elif isinstance(input, List):
            self.matrix = np.array(input)
        else:
            self.matrix = input

    @staticmethod
    def _parse_str(string: str) -> List[List[str]]:
        """Parse string into a list of lists."""
        return np.array([[char for char in line] for line in string.splitlines()])

    def to_list_of_strings(self) -> List[str]:
        return ["".join(line) for line in self.matrix]

    def print(self) -> None:
        for row in self.matrix:
            print("".join(row))

    @property
    def width(self) -> int:
        return len(self.matrix[0])

    @property
    def height(self) -> int:
        return len(self.matrix)
