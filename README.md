# agent-core

Shared orchestration utilities for LangGraph services: confidence-gated loops, compiled eval graphs, evaluation scoring, run artifacts, retrieval helpers, and text completion when configured.

## Features

- Loop policy (`decide_loop`, `weighted_confidence`, `run_confidence_loop`)
- LangGraph eval loop compiler (`run_eval_loop_graph`)
- Multi-source merge helpers (`merge_ranked_results`, `chain_nodes`)
- Text evaluation (`score_text_answer`)
- Run artifacts (`summary.json`, `REPORT.md`, `trace.json`)
- Wikipedia summary fetch for research augmentation
- OpenAI-compatible completion when `LLM_API_KEY` is configured

## Install

```bash
pip install "agent-core @ git+https://github.com/milos-plavsic/agent-core.git@v1.2.0"
```

Depends on [ml-core](https://github.com/milos-plavsic/ml-core).

## Configuration

| Variable | Purpose |
|----------|---------|
| `LLM_API_KEY` | API key for chat completion |
| `LLM_BASE_URL` | Provider base URL (default OpenAI-compatible) |
| `LLM_MODEL` | Model id (default `gpt-4o-mini`) |

`OPENAI_API_KEY`, `OPENAI_BASE_URL`, and `OPENAI_MODEL` are accepted as aliases.

## Usage

```python
from agent_core import decide_loop, fetch_wikipedia_summary, run_confidence_loop

wiki = fetch_wikipedia_summary("retrieval augmented generation")
```

## License

MIT
