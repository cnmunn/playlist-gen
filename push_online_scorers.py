from typing import Any

import braintrust
from pydantic import BaseModel

from evals.core import (
    PROJECT_NAME,
    VARIETY_PROMPT_TEMPLATE,
    VARIETY_MODEL,
    VARIETY_CHOICE_SCORES,
    VARIETY_PASS_THRESHOLD,
    PLAYLIST_LENGTH_PASS_THRESHOLD,
    compute_playlist_length_score,
)

project = braintrust.projects.create(name=PROJECT_NAME)


class PlaylistLengthParams(BaseModel):
    input: Any | None = None
    output: Any | None = None
    expected: Any | None = None
    metadata: dict | None = None


def handler(
    input: Any | None = None,
    output: Any | None = None,
    expected: Any | None = None,
    metadata: dict | None = None,
):
    score, metadata_payload = compute_playlist_length_score(output)
    return {
        "name": "PlaylistLength",
        "score": score,
        "metadata": metadata_payload,
    }


project.scorers.create(
    name="PlaylistLength",
    slug="playlist-length",
    description="Score 1 if playlist duration is <= 30 minutes, else 0.",
    parameters=PlaylistLengthParams,
    handler=handler,
    if_exists="replace",
    metadata={"__pass_threshold": PLAYLIST_LENGTH_PASS_THRESHOLD},
)


project.scorers.create(
    name="Variety",
    slug="playlist-variety",
    description="Evaluate whether the playlist has good artist and genre diversity.",
    messages=[
        {
            "role": "user",
            "content": VARIETY_PROMPT_TEMPLATE,
        }
    ],
    model=VARIETY_MODEL,
    use_cot=False,
    choice_scores=VARIETY_CHOICE_SCORES,
    if_exists="replace",
    metadata={"__pass_threshold": VARIETY_PASS_THRESHOLD},
)
