# Multi-Agent Research Assistant

Run from the workspace root:

```bash
pip install -r day5/multi_agent_research_assistant/requirements.txt
python -m day5.multi_agent_research_assistant.main
```

Set `GROQ_API_KEY` and `DATABASE_URL` in `day5/multi_agent_research_assistant/.env` before running.
Create the PostgreSQL database first, for example:

```bash
createdb research_assistant
```

The workflow fans out to three researchers, combines their findings, reviews and
revises the report, pauses for human approval, and stores checkpoints in PostgreSQL.

## React frontend

Install the Python API dependencies, then start the backend from the workspace root:

```bash
python -m uvicorn day5.multi_agent_research_assistant.api:app --reload --port 8000
```

In another terminal, install and start the React app:

```bash
cd day5/multi_agent_research_assistant/frontend
npm install
npm run dev
```
