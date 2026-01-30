from __future__ import annotations

from autoevals import LLMClassifier
from braintrust import Eval, Score, init_dataset

from evals.core import (
    PROJECT_NAME,
    VARIETY_PROMPT_TEMPLATE,
    VARIETY_MODEL,
    VARIETY_CHOICE_SCORES,
    compute_playlist_length_score,
)
from main import run_agent
from settings import PROMPT_ENVIRONMENT


def _normalize_user_request(raw_input) -> str:
    # Common Braintrust dataset shapes:
    #   input: "make me a happy playlist"
    #   input: {"user_request": "..."}
    #   input: {"input": "..."}
    if isinstance(raw_input, str):
        return raw_input

    if isinstance(raw_input, dict):
        if isinstance(raw_input.get("user_request"), str):
            return raw_input["user_request"]
        if isinstance(raw_input.get("input"), str):
            return raw_input["input"]

    return ""


def _set_environment_metadata(hooks) -> None:
    # Attach env for debugging; works with dict or object hooks.
    if hooks is None:
        return

    try:
        hooks.metadata = {"environment": PROMPT_ENVIRONMENT}
        return
    except Exception:
        pass

    if isinstance(hooks, dict):
        hooks.setdefault("metadata", {})["environment"] = PROMPT_ENVIRONMENT


def task(input, hooks):
    user_request = _normalize_user_request(input)
    _set_environment_metadata(hooks)

    # No prompt overrides. Always run the "real" agent path.
    return run_agent(user_request)


# --- Scorers ---

variety_scorer = LLMClassifier(
    name="Variety",
    prompt_template=VARIETY_PROMPT_TEMPLATE,
    choice_scores=VARIETY_CHOICE_SCORES,
    model=VARIETY_MODEL,
)


def playlist_length_scorer(output: dict):
    score, metadata = compute_playlist_length_score(output)
    return Score(name="PlaylistLength", score=score, metadata=metadata)


# --- Eval registration ---

Eval(
    name="PlaylistGenerator",
    task=task,
    data=init_dataset(project=PROJECT_NAME, name="InputExamples"),
    scores=[variety_scorer, playlist_length_scorer],
)
