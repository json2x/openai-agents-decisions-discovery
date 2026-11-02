# OpenAI Agents & Decisions Discovery

A hands-on learning project for OpenAI's managed Agents API, the separate Agents SDK, and the Decisions API. Includes a 10–15 minute knowledge-sharing presentation, presenter scripts, and executable Python examples.

## Learning materials

| Material | Purpose |
| --- | --- |
| [Slide companion notebook](agents_decisions_slide_showcase.ipynb) | Main showcase, with sections mapped to the slides |
| [PowerPoint presentation](agents-decisions-learning-session.pptx) | 21 editable slides with speaker notes; 15 main slides and 6 reference slides |
| [Quick reference](outputs/learning-session/quick-guide.md) | Copyable slide examples and documentation links |
| [Presenter script](outputs/learning-session/speaker-script.md) | Spoken script for each slide |
| [Slide content](outputs/learning-session/slides.json) | Text, code examples, source links, and notes used in the presentation |
| [Earlier demo notebook](agents_decisions_demo.ipynb) | Original lab with additional PIM examples |

The main notebook demonstrates inline and saved managed agents, named agents, full JSON event streaming, retrieval across Python instances, and explicit cleanup. Decisions examples cover a single controlled vocabulary list (CVL), a multi-value CVL, image evidence, and sentiment scoring. Optional sections demonstrate the separate Agents SDK and Azure Decisions. PIM examples prepare draft values and do not write to a live PIM system.

## Setup

Use Python 3.10 or later. Python 3.12 is a suitable starting point. Clone the repository, then create an isolated environment.

### Windows PowerShell

```powershell
git clone https://github.com/json2x/openai-agents-decisions-discovery.git
cd openai-agents-decisions-discovery
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python -m jupyterlab
```

### macOS / Linux

```bash
git clone https://github.com/json2x/openai-agents-decisions-discovery.git
cd openai-agents-decisions-discovery
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
.venv/bin/python -m jupyterlab
```

Edit `.env` and set `OPENAI_API_KEY`. Select the project's `.venv` as your notebook kernel. The requirements install both `openai` (managed API and Decisions) and `openai-agents` (imported as `agents`). Existing environment variables take precedence over `.env`.

## Run the showcase

1. Open `agents_decisions_slide_showcase.ipynb` and run its setup cells.
2. Enable only the desired `RUN_*` switches in its controls cell.
3. Run the matching sections in order. The saved-agent example reuses persisted IDs when available.
4. Use the notebook's explicit cleanup lists to delete demo resources when you no longer need them.

All live calls are disabled in the committed notebooks. Enabling them incurs API usage charges; the hosted agent demonstration also uses billable container compute. The notebook explains those costs. OpenAI model/feature access and API-key permissions are required. The Azure section needs separate Azure credentials and a supported deployment.

The main examples use `gpt-6-luna` for Decisions because it is currently the endpoint's only supported model. Agents use `gpt-6-astra` to follow OpenAI's quickstart; that is a demonstration choice. Evaluate supported agent models for your own quality, latency, and cost requirements. Documentation and pricing were reviewed on 3 November 2026 and can change.

Agent/session IDs are saved locally in `.agents_decisions_showcase_state.json`. Your `.env`, `.venv`, saved outputs, local notebook backups, resource state, and private slide-build files are excluded from Git. Never place an API key directly in notebook code.

## Checks before sharing changes

Clear notebook outputs and execution counts, and return all `RUN_*` switches to `False`. Then run:

```bash
python scripts/check_notebooks.py
```

The same check runs on GitHub pushes and pull requests. It checks notebook syntax, sharing defaults, and the bundled image without executing API calls. It does not establish live service availability or model quality. Dependency installation and SDK imports were checked locally; Decisions response handling was also exercised with mocked responses.

## Official references

- [Managed Agents API](https://developers.openai.com/api/docs/guides/agents-api/overview)
- [Agents API configuration](https://developers.openai.com/api/docs/guides/agents-api/configuration)
- [Agents SDK quickstart](https://developers.openai.com/api/docs/guides/agents/quickstart)
- [Decisions API](https://developers.openai.com/api/docs/guides/decisions)
- [Azure OpenAI Decisions](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/decisions)
- [OpenAI pricing](https://developers.openai.com/api/docs/pricing)

The illustration assets are AI-generated examples. The jacket image is included so the image-evidence notebook section works after cloning.
