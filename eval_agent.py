from math import nan
from autoevals import LLMClassifier
from braintrust import Eval, init_dataset, Score
from answer import run_agent

#This is the function you are avaluating (we import it from main.py and use `input` from a Braintrust dataset to experiment)
def task(input: dict, hooks: dict):
    user_input = input.get("user_request")
    return run_agent(user_input)

#TODO Create LLM as a judge to define a higher score for a higher variety playlist
variety_scorer = LLMClassifier(

)

#TODO
def playlist_length_scorer(output: dict):
    score = nan #complete scoring logic
    return Score(name = "PlaylistLength", score = score)

Eval(
    name="PlaylistGenerator",
    task=task,
    data=init_dataset(project="PlaylistGenerator", name="InputExamples"), #TODO you'll need to create a dataset. Run a comple traces to populate the logs page and then "add to dataset"
    scores=[variety_scorer, playlist_length_scorer]
    #TODO to would be great to implement Remote Evals if possible
)
