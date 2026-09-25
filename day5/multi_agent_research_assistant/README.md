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
