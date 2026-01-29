import json
from typing import Any

PROJECT_NAME = "PlaylistGenerator"

VARIETY_PROMPT_TEMPLATE = (
    "Evaluate playlist variety. Prefer many unique artists and genres. "
    "Return A (high variety), B (medium), or C (low).\n\n"
    "Playlist output:\n{{output}}"
)
VARIETY_MODEL = "gpt-4o-mini"
VARIETY_CHOICE_SCORES = {"A": 1.0, "B": 0.5, "C": 0.0}
VARIETY_PASS_THRESHOLD = 0.5

PLAYLIST_LENGTH_THRESHOLD_MIN = 30
PLAYLIST_LENGTH_PASS_THRESHOLD = 1.0


def _coerce_dict(value: Any) -> dict | None:
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            return None
    return value if isinstance(value, dict) else None


def compute_playlist_length_score(output: Any) -> tuple[float, dict]:
    payload = _coerce_dict(output)
    playlist = _coerce_dict(payload.get("playlist")) if payload else None
    duration = playlist.get("total_duration_min") if playlist else None
    duration_min = float(duration) if isinstance(duration, (int, float)) else None
    score = 1.0 if duration_min is not None and duration_min <= PLAYLIST_LENGTH_THRESHOLD_MIN else 0.0
    reason = None
    if payload is None:
        reason = "output_not_dict"
    elif playlist is None:
        reason = "playlist_not_dict"
    elif duration_min is None:
        reason = "duration_missing"
    return score, {"duration_min": duration_min, "reason": reason}
