# Enterprise RAG

## Run the React web chat locally

Set `GROQ_API_KEY` in `.env`. Keep this file private and do not commit API keys.

Install Python dependencies from the project root:

```bash
source /home/bandaru/Desktop/llamaIndex/.venv/bin/activate
pip install -r requirements.txt
```

Start the backend in one terminal:

```bash
cd app
uvicorn api:api --reload
```

In a second terminal, start the React frontend:

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173). Put source PDFs in `data/`; the index is saved in `storage/`. The terminal chat can also be run from the project root with `python app/main.py`.
