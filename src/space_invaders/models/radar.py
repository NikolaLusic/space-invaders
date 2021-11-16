from math import ceil
from typing import Generator, Optional, Tuple

from space_invaders.models.coordinate import Point
from space_invaders.models.matrix import Matrix
from space_invaders.models.pattern import Mask, Pattern


class Radar(Matrix):
    """Data structure representing the input from a radar scan."""

    def __init__(self, input) -> None:
        super(Radar, self).__init__(input)

    def generate_samples(self, width: int, height: int, overflow: int = None):
        """Generate all possible samples of the provided size, including the
        smaller partial edge cases - down to the provided overflow size."""
        min_row_index = int(height / 2)
        previous_sample = None
        old_hash = None

        for row_index in range(-min_row_index, self.height - int(height / 2) + 1):
            if row_index % 2 == 0:
                generator = (col_index for col_index in range(0, self.width + 1))
            else:
                generator = (col_index for col_index in range(self.width, -1, -1))
            for sample in self._generate_row(row_index, width, height, generator):
                sample_hash = self._rolling_hash(old_hash, sample, previous_sample)
                previous_sample = sample
                old_hash = sample_hash
                yield sample, sample_hash

    def _generate_row(
        self, row_index: int, width: int, height: int, generator: Generator
    ):
        """Generate a single row at the row_index."""
        for col_index in generator:
            top_left, bottom_right = self._get_coordinates(
                width, height, col_index, row_index
            )
            mask = self._create_mask(height, width, top_left, bottom_right)
            sample = Pattern(
                [
                    self.matrix[row][max(top_left.col, 0) : bottom_right.col + 1]
                    for row in range(
                        max(row_index, 0), min(row_index + height, self.height)
                    )
                ],
                top_left=top_left,
                bottom_right=bottom_right,
                mask=mask,
            )
            yield sample

    def _create_mask(
        self, height: int, width: int, top_left: Point, bottom_right: Point
    ) -> Optional[Mask]:
        """Create mask for the query pattern."""
        points = [None, None, None, None]
        if top_left.row <= 0:
            points[0] = height - bottom_right.row - 1
        if top_left.col <= 0:
            points[1] = width - bottom_right.col - 1
        if bottom_right.row == self.height - 1:
            points[2] = bottom_right.row - top_left.row
        if bottom_right.col >= self.width - 1:
            points[3] = bottom_right.col - top_left.col

        if all(point is None for point in points):
            return None

        return Mask(
            Point(points[0] or 0, points[1] or 0),
            Point(points[2] or height - 1, points[3] or width - 1),
        )

    def _get_coordinates(
        self, width: int, height: int, col_index: int, row_index: int
    ) -> Tuple[Point, Point]:
        """Figure out the top left and bottom right coordinates from the
        provided input."""
        start_col = max(col_index - ceil(width / 2), 0)
        start_row = max(row_index, 0)
        top_left = Point(start_row, start_col)

        end_col = min(col_index + int(width / 2) - 1, self.width - 1)
        end_row = min(row_index + height, self.height) - 1
        bottom_right = Point(end_row, end_col)
        return top_left, bottom_right

    @staticmethod
    def _rolling_hash(
        old_hash: Optional[int], sample: Pattern, prev_sample: Pattern
    ) -> int:
        """Calculate hash value of the current sample"""
        if prev_sample is None:
            return sample.hash()
        if old_hash is None:
            return sample.hash()

        remove_vector = None
        add_vector = None

        if sample.top_left.col > prev_sample.top_left.col:
            remove_vector = prev_sample.matrix[:, 0]
        if sample.top_left.col < prev_sample.top_left.col:
            add_vector = sample.matrix[:, 0]
        if sample.bottom_right.col > prev_sample.bottom_right.col:
            add_vector = sample.matrix[:, -1]
        if sample.bottom_right.col < prev_sample.bottom_right.col:
            remove_vector = prev_sample.matrix[:, -1]
        if sample.top_left.row > prev_sample.top_left.row:
            remove_vector = prev_sample.matrix[0, :]
        if sample.bottom_right.row > prev_sample.bottom_right.row:
            add_vector = sample.matrix[-1, :]

        new_hash = (
            old_hash - Pattern.column_hash(tuple(remove_vector))
            if remove_vector is not None
            else old_hash
        )
        return (
            new_hash + Pattern.column_hash(tuple(add_vector))
            if add_vector is not None
            else new_hash
        )
