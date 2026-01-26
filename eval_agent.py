from autoevals import LLMClassifier
from braintrust import Eval, init_dataset, Score, Prompt
from braintrust.prompt import PromptData
from main import run_agent

def _build_prompt_override(parameters: dict | None, input: dict) -> dict | None:
    if not parameters:
        return None

    main_param = parameters.get("main")
    if main_param is None:
        return None

    if hasattr(main_param, "build"):
        return main_param.build(input=input)

    if isinstance(main_param, dict):
        if "messages" in main_param or isinstance(main_param.get("prompt"), str):
            return main_param

        prompt_data = None
        if isinstance(main_param.get("prompt"), dict):
            prompt_data = main_param
        elif main_param.get("type") == "prompt":
            prompt_data = main_param.get("default")

        if prompt_data:
            prompt_name = main_param.get("name") if isinstance(main_param.get("name"), str) else "main"
            prompt = Prompt.from_prompt_data(prompt_name, PromptData.from_dict_deep(prompt_data))
            return prompt.build(input=input)

    return None

def _attach_playlist_metadata(hooks: dict | None, playlist: dict | None) -> None:
    if hooks is None or playlist is None:
        return

    metadata = None
    if isinstance(hooks, dict):
        metadata = hooks.get("metadata")
        if metadata is None:
            metadata = {}
            hooks["metadata"] = metadata

    if metadata is None:
        return

    metadata.update(
        {
            "playlist_name": playlist.get("playlist_name"),
            "total_tracks": playlist.get("total_tracks"),
            "total_duration_min": playlist.get("total_duration_min"),
            "tracks": playlist.get("songs"),
        }
    )

def task(input: dict, hooks: dict):
    """Run the playlist agent for the dataset input."""
    user_input = input.get("user_request", "")
    parameters = None
    if hooks is not None:
        parameters = getattr(hooks, "parameters", None)
        if parameters is None and isinstance(hooks, dict):
            parameters = hooks.get("parameters")

    prompt_override = _build_prompt_override(parameters, input)

    result = run_agent(user_input, prompt_override=prompt_override)
    result_payload = result.model_dump()
    _attach_playlist_metadata(hooks, result_payload.get("playlist"))
    return result_payload

variety_scorer = LLMClassifier(
    name="Variety",
    prompt_template=(
        "Evaluate playlist variety. Prefer many unique artists and genres. "
        "Return A (high variety), B (medium), or C (low).\n\n"
        "Playlist output:\n{{output}}"
    ),
    choice_scores={"A": 1.0, "B": 0.5, "C": 0.0},
    model="gpt-4o-mini",
)

def playlist_length_scorer(output: dict):
    playlist = output.get("playlist") if isinstance(output, dict) else None
    duration = playlist.get("total_duration_min") if isinstance(playlist, dict) else None
    score = 1.0 if duration is not None and duration <= 30 else 0.0
    return Score(name="PlaylistLength", score=score, metadata={"duration_min": duration})

Eval(
    name="PlaylistGenerator",
    task=task,
    data=init_dataset(project="PlaylistGenerator", name="InputExamples"),
    scores=[variety_scorer, playlist_length_scorer],
    parameters={
        "main": {
            "type": "prompt",
            "name": "Main prompt",
            "default": {
                "prompt": {
                    "type": "chat",
                    "messages": [{"role": "user", "content": "{{input.user_request}}"}],
                },
                "options": {"model": "gpt-4o-mini"},
            },
        },
    },
)
