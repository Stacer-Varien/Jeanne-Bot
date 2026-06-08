"""Local GIF catalog used by the reaction commands."""

import json
from pathlib import Path
from random import choice


CATALOG_PATH = Path(__file__).with_name("reaction_gifs.json")

with CATALOG_PATH.open(encoding="utf-8") as catalog_file:
    REACTION_GIFS: dict[str, list[str]] = json.load(catalog_file)


def get_reaction_gif(action: str) -> str:
    """Return a random archived GIF URL for a reaction action."""
    try:
        gifs = REACTION_GIFS[action]
    except KeyError as error:
        raise ValueError(f"No GIF catalog exists for reaction {action!r}") from error

    if not gifs:
        raise ValueError(f"The GIF catalog for reaction {action!r} is empty")
    return choice(gifs)
