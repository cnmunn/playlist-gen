# Braintrust Sales Engineer Technical Screen

## Background

You are preparing to deliver a 40-minute discovery and demo to a potential customer – **Bryan, the Vice President of Engineering at Spotify**. You have already met with **Phil, Director of Engineering** a week ago to have a high level discussion about Braintrust. Spotify is working to roll out an LLM-based playlist generation service and is concerned about quality of the generated playlists.

In the first meeting, you learned the following challenges her team is facing:

| Challenge | Details |
|-----------|---------|
| **Comparing models** | The team currently uses primarily OpenAI models, but wants to evaluate Gemini and Claude as potential alternatives. Do they get higher quality? Save money? |
| **Iteration speed** | Currently, when they make a change to the app, a developer runs a script that tries out LLM inputs from a Google Sheet with input, output, and a couple scores they've developed. From there, they manually review the results but it doesn't feel that significant—more vibes-based than anything else. |
| **Involving PMs** | The team is looking to enable PMs to do experimentation with prompts and models as well, to save engineering time and get more people involved. |
| **Production logging & monitoring** | Tracking uptime, latency, duration, etc. is still important, but what they really care about is: How are users interacting with the product? Where are we underperforming or failing? |

Bryan is open to Braintrust but is also evaluating other competitive tools, or just building the tool internally.

---

## Your Task

Using this repo as a stand-in for Spotify's playlist generation agent, prepare a 40-minute discovery and demo for Bryan.

### Required Deliverables

1. **Instrument this repo with the Braintrust SDK** and send several traces to Braintrust
   - Traces should capture the agent's LLM calls and tool usage

2. **Create Experiments** with the following scoring functions:
   - **Variety** (LLM-as-a-judge): Evaluate whether the playlist has good artist/genre diversity
   - **PlaylistLength**: Playlist should be under 30 minutes total

3. **Slide Presentation** to speak through. Slides will be delivered to you but you can trim the deck down to only what you need.

### Bonus Points

- Incorporate **Online Scoring** into your demo (running evals on production traces)
- Incorporate **Remote Evals** to show how Product Managers could iterate with agents.

---

## Runbook

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key
- Braintrust account and API key

### Setup

```bash
# Clone the repo and navigate to it
cd playlist-gen

# Install dependencies
uv sync

# Create a .env file with your API keys
echo "OPENAI_API_KEY=your-openai-key" >> .env
echo "BRAINTRUST_API_KEY=your-braintrust-key" >> .env

# Run the agent
uv run python main.py
```

### Using the Agent

Once running, you can interact with the agent:

```
Playlist Generator Agent
Type 'quit' to exit

What kind of playlist would you like? > upbeat workout music
```

The agent will:
1. Search the mock catalog for matching songs
2. Select appropriate tracks
3. Create a named playlist

Try a few different requests to generate traces:
- "Create a chill playlist for studying"
- "I need motivational music for a morning run"
- "Make me a sad songs playlist"
- "Happy road trip vibes"

### Agent Output Structure

The agent returns structured Pydantic models:

```python
class Song(BaseModel):
    title: str
    artist: str

class Playlist(BaseModel):
    playlist_name: str
    songs: list[Song]
    total_tracks: int
    total_duration_min: float

class ToolCall(BaseModel):
    tool: str
    arguments: dict
    result: dict | list

class AgentResult(BaseModel):
    playlist: Playlist | None   # The created playlist (if any)
    response: str               # The assistant's final response
    tool_calls: list[ToolCall]  # Log of all tool calls made
```

---

## Tips for Success

### Show the Flywheel

The most compelling demo tells a story of continuous improvement:

1. **Production traces** → See a real user interaction in Braintrust
2. **Identify an issue** → Maybe the playlist was too long, or lacked variety
3. **Bring to dataset** → Add that trace to an offline eval dataset
4. **Tweak the agent** → Adjust the prompt, switch models, etc.
5. **Run an eval** → See if your change improved or regressed quality
6. **Ship with confidence** → Deploy knowing you've measured the impact

This flywheel is the core value prop. Don't just show features, show the workflow.

### Keep It Accessible

Remember Braintrust's dual audience:

- **AI Engineers** care about SDK integration, programmatic evals, CI/CD
- **PMs and domain experts** care about no-code experimentation, readable results, quick iteration

Bryan mentioned wanting to involve PMs. Show how Braintrust makes that possible—prompt playground, readable eval results, no-code scoring setup.

**Don't make the demo overly technical.** Show what customers can *do* with Braintrust, not what Braintrust can *do*.

### Use Loop

Braintrust's GenAI assistant, **Loop**, can help with:
- Writing scoring functions
- Analyzing eval results
- Debugging traces
- Explaining failures

Sprinkle Loop usage throughout your demo to show how it accelerates workflows for both engineers and non-engineers.

### Address Bryan's Concerns Directly

| His concern | How Braintrust helps |
|-------------|---------------------|
| Model comparison | Side-by-side experiments with same dataset, cost tracking |
| Vibes-based evaluation | Structured scoring functions, LLM-as-judge, quantitative results |
| PM involvement | No-code prompt iteration, readable dashboards |
| Production monitoring | Tracing, online evals, alerting on quality regressions |

### Time Management

You have 40 minutes. A suggested structure (it does not have to be this rigid):
- **10 min**: Introductions, slide deck (this will be given to you. You do not have to use the whole thing), clarification
- **25 min**: Showing the "flywheel", diving into how different parts of Braintrust would fit into Spotify's workflow, further discovery
- **5 min**: Next steps

---

## Resources

- [Braintrust Docs](https://www.braintrust.dev/docs): Overall documentation for using Braintrust
- [Braintrust Youtube Channel](https://www.youtube.com/@BraintrustData): Great for getting an understanding of different features of Braintrust
- [Evals 101 Library](https://github.com/philhetzel/braintrust-evals-101/tree/main/py): Some basic eval examples (README includes a Loom link for an "Anatomy of an Eval" explainer)
- [Braintrust Demo](https://www.loom.com/share/ffadc8d0e1964d8e958f2fba65ec7f78): An (older) demo of Braintrust features to give a sense of the correct level of detail

Good luck!
