<!-- Copilot / AI agent instructions for MediMatch -->

Purpose
- Provide concise, actionable guidance for AI coding agents working on this repo.

Big picture
- Backend: FastAPI app at `backend/app/main.py` exposing `/api/search` (see `routers/search.py`).
- Embeddings: CLIP-based service in `backend/app/services/embedding_service.py` (singleton via `get_embedding_service`).
- Storage: PostgreSQL + `pgvector` extension; SQLAlchemy models in `backend/app/models/medical_case.py` (image_embedding: `Vector(512)`).
- Search: Vector search implemented in `backend/app/services/search_service.py` using the pgvector `<=>` operator; similarity computed as `1 - distance`.
- Frontend: Vite + React in `frontend/`; API client uses `VITE_API_URL` (see `frontend/src/api/client.js`).
- Data pipeline: `data_pipeline/generate_embeddings.py` creates embeddings and inserts rows; `data_pipeline/quick_dataset.py` creates synthetic data.

Key developer workflows
- Start DB (with pgvector): `docker-compose up -d postgres` (see root `docker-compose.yml`).
- Initialize schema: run `scripts/setup_database.sql` inside the DB container.
- Create test data + embeddings:
  - `python data_pipeline/quick_dataset.py`
  - `python data_pipeline/generate_embeddings.py --input data/test/metadata.csv`
- Run backend (dev): `cd backend && uvicorn app.main:app --reload` (FastAPI app host/port controlled by `backend/app/config.py`).
- Run frontend (dev): `cd frontend && npm install && npm run dev`.

Project-specific patterns & gotchas
- Embedding model is heavyweight. Use `get_embedding_service()` (singleton) — do not recreate the model per-request.
- `encode_image` accepts a base64 string or PIL Image. The search endpoint will call `encode_image` when `image` is provided in `SearchRequest` (base64 string expected).
- `SearchService.vector_search` constructs raw SQL using SQLAlchemy `text()` and relies on pgvector accepting a Python list for parameter `:q`.
- Similarity is returned as `1 - (image_embedding <=> :q)`. Client-facing responses attach `similarity_score` (float).
- Database model uses `pgvector.sqlalchemy.Vector(512)` — embedding dimension is 512 throughout the codebase.

Where to look when changing behavior
- To change routing or add endpoints: add router in `backend/app/routers/` and include it in `backend/app/main.py`.
- To change embedding model or device defaults: edit `backend/app/config.py` (`device`) and `embedding_service.py` as needed.
- To alter search ranking/filters: edit `backend/app/services/search_service.py` (SQL generation and filter placement).
- To add ingestion pipelines or batch jobs: follow `data_pipeline/generate_embeddings.py` (uses SQLAlchemy `Session` and `Base.metadata.create_all`).

Testing / Debugging tips for agents
- Reuse the test dataset flow: `quick_dataset.py` + `generate_embeddings.py` to produce reproducible inputs.
- For DB-related issues, inspect SQL generated in `search_service.py` and test queries directly in psql (container).
- To reproduce frontend API errors locally, set `VITE_API_URL` (e.g. `http://localhost:8000`) when running Vite.

Conventions
- Filenames and modules under `backend/app/` follow typical FastAPI + SQLAlchemy layout: `routers/`, `services/`, `models/`, `schemas/`.
- Keep embeddings as plain Python lists before inserting into pgvector columns (see `generate_embeddings.py`).

When you are unsure
- Prefer reading the service files above before changing model loading or SQL. If a change affects model loading, ensure it remains a singleton.
- Ask about environment specifics (GPU availability, DB host) before switching `device` to `cuda`.

If you update this file
- Preserve the structure above and only add short notes referencing concrete files. Keep guidance actionable and repository-specific.
