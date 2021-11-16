import time
from pathlib import Path

from pytest import mark
from space_invaders.matcher import match
from space_invaders.utils import load_pattern, load_radar


@mark.parametrize(
    "test_samples",
    [
        [
            (47, 0.875, (1, 74, 8, 84)),
            (46, 1.0, (12, 85, 19, 95)),
            (38, 0.9090909090909091, (13, 60, 20, 70)),
        ]
    ],
)
def test_a(test_samples):
    path = Path(__file__).parent / "res"
    radar = load_radar(path / "radar_sample")
    pattern = load_pattern(path / "pattern_sample_1")
    start_time = time.time()
    results = match(pattern, radar)
    total_time = time.time() - start_time
    print("--- %s seconds ---" % total_time)
    for i in range(len(results)):
        result = results[i]
        test_sample = test_samples[i]
        assert result[2] == test_sample[0]
        assert result[0] == test_sample[1]
        assert (
            result[1].top_left.tuple() + result[1].bottom_right.tuple()
            == test_sample[2]
        )

    assert len(results) == 3


@mark.parametrize(
    "test_samples",
    [
        [
            (31, 0.8035714285714286, (0, 18, 6, 25)),
            (34, 0.875, (0, 42, 7, 49)),
            (38, 0.84375, (15, 35, 22, 42)),
            (39, 0.859375, (28, 16, 35, 23)),
            (37, 0.859375, (41, 82, 48, 89)),
            (27, 0.925, (45, 17, 49, 24)),
        ]
    ],
)
def test_b(test_samples):
    path = Path(__file__).parent / "res"
    radar = load_radar(path / "radar_sample")
    pattern = load_pattern(path / "pattern_sample_2")

    start_time = time.time()
    results = match(pattern, radar)
    total_time = time.time() - start_time
    print("--- %s seconds ---" % total_time)
    for i in range(len(results)):
        result = results[i]
        test_sample = test_samples[i]

        assert result[2] == test_sample[0]
        assert result[0] == test_sample[1]
        assert (
            result[1].top_left.tuple() + result[1].bottom_right.tuple()
            == test_sample[2]
        )

    assert len(results) == 6
