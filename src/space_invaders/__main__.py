import click
from space_invaders.matcher import match
from space_invaders.utils import load_pattern, load_radar


@click.command()
@click.option("--pattern", help="query pattern file path", required=True)
@click.option("--radar", help="radar sample file path", required=True)
def main(radar, pattern):
    pattern = load_pattern(pattern)
    print(pattern.hash())
    radar = load_radar(radar)

    results = match(pattern, radar)
    if not results:
        return

    results.sort(key=lambda x: x[0], reverse=False)
    for result in results:
        result[1].print()
        print(f"similarity: {result[0]}\n")


if __name__ == "__main__":
    main()
