# Agents & Decisions: quick reference

The general introduction uses PIM CVL examples for Decisions. Slides 1–15 form the main talk. Slides 16–21 are optional references. Image evidence appears on slide 11 and hosted-environment pricing on slide 20.

Install: `pip install -U openai python-dotenv`. Later examples share slide 5 setup. Supply an authorized key in your root .env. Calls incur usage charges. Run the image code from the project root so its relative image path resolves.

The CVL keys are illustrative. `needs_review` is a workflow fallback, not a CVL value. Printed JSON is draft data, not a vendor-specific PIM update request.

## Slide 1: Agents & Decisions

OpenAI Platform  /  3 November 2026


## Slide 2: A task and a judgment

**Agents:** Work toward a goal through steps and tools.

**Decisions:** Answer a bounded question about supplied evidence.

They can cooperate: one evaluates an input, the other carries out a task.

- [Official reference](https://developers.openai.com/api/docs/guides/agents)
- [Official reference](https://developers.openai.com/api/docs/guides/decisions)

## Slide 3: The building blocks of an agent

01. **Configuration:** Model, instructions and available tools

02. **Session:** Conversation and work across turns

03. **Environment:** Optional compute for commands and files

04. **Events:** Progress, tool activity and results

The managed Agents API runs OpenAI’s harness. Your application supplies tools and policy.

- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/overview)
- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/architecture)

## Slide 4: Ways to create and configure agents

| Approach | How you define it | What persists |
| --- | --- | --- |
| Inline Agents API | agent={model, instructions, …} | Configuration within a session |
| Saved Agents API | client.beta.agents.create(...) | Reusable agent_id |
| Separate Agents SDK | Agent(...) with Runner | An application object + chosen storage |

A compatible saved agent_id can also come from the Platform. Creating one there is optional.

- [Official reference](https://developers.openai.com/api/docs/guides/agents)
- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/configuration)
- [Official reference](https://developers.openai.com/api/docs/guides/agents/quickstart)

## Slide 5: Shared Python setup

```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
DECISION_MODEL = "gpt-6-luna"
AGENT_MODEL = "gpt-6-astra"
EVIDENCE = ("Navy blue jacket. "
            "Suitable for hiking and cycling.")
TASK = (
    "Write and run Python to find the "
    "average of 12, 18 and 24. Explain it."
)
```

Terminal: pip install -U openai python-dotenv. Later snippets reuse this setup.

**Decisions model:** `gpt-6-luna` is currently the only model supported by the Decisions endpoint.

- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/quickstart)
- [Decisions model support](https://developers.openai.com/api/docs/guides/decisions)

## Slide 6: Inline agent: start a task and stream events

```python
with client.beta.agents.sessions.create(
    agent={
        "model": AGENT_MODEL,
        "instructions": "Run code and report the actual output."
    },
    environment={"type": "openai_hosted"},
    input=TASK,
    stream=True,
).with_result_collection() as events:
    for event in events:
        print(event.to_json(indent=None), flush=True)
    result = events.get_final_result()

print(result.output_text)
print(result.session_id)
```

Uses slide 5 setup. Hosted compute adds container charges. See the cost reference on slide 20.

- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/quickstart)
- [Official reference](https://developers.openai.com/api/docs/pricing#tools)
- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/environments/openai-hosted)

## Slide 7: Saved agent: create once and reuse

```python
saved = client.beta.agents.create(
    name="Technical explainer",
    model=AGENT_MODEL,
    instructions="Explain technical issues clearly."
)
session = client.beta.agents.sessions.create(
    agent_id=saved.id,
    environment={"type": "none"},
    input="Explain why a file export might fail."
)

print("name:", saved.name)
print("agent_id:", saved.id)
print("session_id:", session.id)
```

Uses slide 5 setup. Another authorized process can reference the saved agent ID.

- [Official reference](https://developers.openai.com/api/reference/python/resources/beta/subresources/agents/methods/create)
- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/configuration)

The name is for human recognition. Persist `saved.id` for retrieval and session creation. To rename an existing agent: `client.beta.agents.update(agent_id, name="Technical explainer")`.

## Slide 8: Retrieve an agent and a session later

```python
# Replace these with the IDs you persisted.
agent_id = "YOUR_SAVED_AGENT_ID"
session_id = "YOUR_SESSION_ID"

agent = client.beta.agents.retrieve(agent_id)
session = client.beta.agents.sessions.retrieve(
    session_id
)

print(agent.model)
print(agent.instructions)
print(session.status)
```

Uses slide 5 setup. Retrieving a resource does not start another task.

- [Official reference](https://developers.openai.com/api/reference/python/resources/beta/subresources/agents/methods/retrieve)
- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/sessions/manage)

## Slide 9: Decisions: three bounded answer types

**OpenAI reports ~10× faster typed answers than Responses API.** Provider-reported comparison. Actual latency varies with the workload.

| Type | Example question | Main result |
| --- | --- | --- |
| predicate | Is hiking supported by the source? | Probability from 0 to 1 |
| choice | Which base_color CVL key fits? | One supplied CVL key |
| score | How positive is this review? | 0 negative, 1 neutral, 2 positive |

Example: “Easy to use. I love it.” Illustrative score: 1.8 / 2.

CVL = controlled vocabulary list. Single-CVL fields accept one key. Multi-CVL fields accept several.

- [Official reference](https://developers.openai.com/api/docs/guides/decisions)
- [Official reference](https://developers.openai.com/api/reference/resources/decisions/methods/create)

## Slide 10: Single CVL: select one base_color key

```python
d = client.decisions.create(
    model=DECISION_MODEL, input=EVIDENCE,
    questions=[{
        "type": "choice", "name": "base_color",
        "instructions": "Map navy to blue. If unclear use needs_review.",
        "choices": [{"value": v} for v in
                    ["blue", "red", "green", "needs_review"]]
    }]
)
a = d.answers[0]
if a.type == "choice" and a.choice != "needs_review":
    print({"base_color": a.choice})
else:
    print("Review needed")
```

Illustrative draft: base_color = blue. needs_review is a workflow fallback, not a CVL key.

- [Official reference](https://developers.openai.com/api/reference/resources/decisions/methods/create)

## Slide 11: Single CVL: use a photo as evidence

```python
from base64 import b64encode
from pathlib import Path
p = Path("outputs/learning-session/assets")
url = "data:image/png;base64," + b64encode(
    (p / "jacket-evidence.png").read_bytes()).decode()
colors = ["orange", "blue", "black",
          "needs_review"]
d = client.decisions.create(model=DECISION_MODEL,
    input=[dict(role="user", content=[
        dict(type="input_image", image_url=url)])],
    questions=[dict(type="choice", name="base_color",
        instructions="Select jacket color.",
        choices=[{"value": c} for c in colors])])
print(d.answers[0].model_dump())
```

Illustrative draft
base_color = orange

Uses slide 5 setup. The local PNG becomes a base64 image input. Treat the color as a draft.

- [Official reference](https://developers.openai.com/api/docs/guides/decisions)

## Slide 12: Multi-CVL: assess each allowed activity

```python
keys = ["hiking", "running", "cycling"]
d = client.decisions.create(model=DECISION_MODEL, input=EVIDENCE,
    questions=[{
        "type": "predicate", "name": key,
        "instructions": f"Is {key} explicitly listed as a suitable activity?"
    } for key in keys])
selected, review = [], []
for a in d.answers:
    if a.type != "predicate":
        review.append(a.name)
    elif a.probability >= 0.85:
        selected.append(a.name)
    elif a.probability > 0.15:
        review.append(a.name)
print({"activities": selected, "review": review})
```

Illustrative draft: activities = [hiking, cycling]. Thresholds require validation on your data.

- [Official reference](https://developers.openai.com/api/reference/resources/decisions/methods/create)

## Slide 13: Choosing the right amount of automation

01. **Rules:** Exact validation and deterministic checks

02. **Decisions:** Classification, routing and rubric judgments

03. **Agent:** Tasks that need investigation or tools

04. **Application:** Authorization, execution and verification

Use each piece where it helps. A simple task may need only one of them.

- [Official reference](https://developers.openai.com/api/docs/guides/agents)
- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/tools/functions)

## Slide 14: Use cases across different systems

**Support:** Route a request, then investigate it.

**Operations:** Prioritize an alert, then prepare a report.

**PIM:** Classify products and flag conflicting claims. Draft supported content corrections.

Suggested applications. Product claims still need source evidence and authorized review.

- [Official reference](https://developers.openai.com/api/docs/guides/agents)

## Slide 15: What to try after this session

**One small judgment:** Write a Decisions question with clear allowed answers.

**One small task:** Create an agent session, observe it, then retrieve it by ID.

Main session ends here. The appendix contains extra Python examples and source links.


## Slide 16: Reference: predicate and score code

```python
d = client.decisions.create(
    model=DECISION_MODEL, input="Review: Easy to use. I love it.",
    questions=[
        {"type": "predicate", "name": "positive",
         "instructions": "Is the review positive?"},
        {"type": "score", "name": "sentiment",
         "instructions": "Rate the tone of this review.",
         "levels": [
             {"label": "Negative", "description": "An unfavorable opinion."},
             {"label": "Neutral", "description": "Neither positive nor negative."},
             {"label": "Positive", "description": "A favorable opinion."}
         ]}
    ])
print(d.model_dump())
```

Separate review example. Uses slide 5 client and model. CVL mapping uses choice or predicates.

- [Official reference](https://developers.openai.com/api/reference/resources/decisions/methods/create)

## Slide 17: Reference: the separate Agents SDK

```python
# pip install -U openai-agents
from agents import Agent, Runner

agent = Agent(
    name="Technical explainer",
    model="gpt-6-astra",
    instructions="Explain technical issues clearly."
)
# In a notebook, use top-level await.
sdk_result = await Runner.run(
    agent,
    "Why might a file export fail?"
)
print(sdk_result.final_output)
```

This is an alternative runtime. Earlier examples use the managed Agents API.

- [Official reference](https://developers.openai.com/api/docs/guides/agents/quickstart)

## Slide 18: Reference: Decisions through Azure

```python
import os
from openai import OpenAI

azure = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
             + "/openai/v1/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)
d = azure.decisions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    input=EVIDENCE,
    questions=[{"type": "predicate", "name": "hiking",
                "instructions": "Is hiking explicitly listed?"}]
)
print(d.answers[0].model_dump())
```

Uses slide 5 EVIDENCE and environment setup. Confirm Azure regional availability.

- [Official reference](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/decisions)

## Slide 19: Reference: saved work and session cleanup

```python
# Use the session ID returned by slide 6 or slide 7.
session_id = "YOUR_SESSION_ID"
s = client.beta.agents.sessions.retrieve(session_id)
print(s.status)

items = client.beta.agents.sessions.items.list(
    session_id, order="asc", limit=10
)
for item in items:
    print(item.model_dump())

# Save needed artifacts before deleting the session.
# client.beta.agents.sessions.delete(session_id)
```

Uses slide 5 setup. Retrieval inspects work; deletion is intentionally commented out.

- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/sessions)
- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/sessions/manage)

## Slide 20: OpenAI-hosted environment costs

Model tokens + container + separately priced tools

| Size | Memory | USD / 20 minutes / container |
| --- | --- | --- |
| small | 1 GB | $0.03 |
| medium (default) | 4 GB | $0.12 |
| large | 16 GB | $0.48 |

Eligible sessions: per-minute billing, with a five-minute minimum.
Confirm which billing treatment applies to your usage.

Default: medium (4 GB). Select small explicitly for lightweight tasks.
Save artifacts and delete finished sessions. Closing the stream does not cancel work.

Prices checked 3 November 2026. Model usage and separately priced tools are additional.

- [Official reference](https://developers.openai.com/api/docs/pricing#tools)
- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/environments/openai-hosted)

## Slide 21: Official references and hands-on practice

**Agents:** Overview, configuration and Python quickstart Retrieve-agent and session-management references

**Decisions:** Guide and request reference Try predicate, choice and score questions.

**Practice:** Run a small task, save the IDs and retrieve it later. Compare decisions with human-labeled examples.

Official links are in the reference block at the end of each slide’s notes.

- [Official reference](https://developers.openai.com/api/docs/guides/agents)
- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/configuration)
- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/quickstart)
- [Official reference](https://developers.openai.com/api/docs/guides/decisions)
- [Official reference](https://developers.openai.com/api/reference/resources/decisions/methods/create)
- [Official reference](https://developers.openai.com/api/reference/python/resources/beta/subresources/agents/methods/create)
- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/sessions)
- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/architecture)
- [Official reference](https://developers.openai.com/api/docs/guides/agents/quickstart)
- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/tools/functions)
- [Official reference](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/decisions)
- [Official reference](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [Official reference](https://developers.openai.com/api/reference/python/resources/beta/subresources/agents/methods/retrieve)
- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/sessions/manage)
- [Official reference](https://developers.openai.com/api/docs/guides/agents-api/overview)
