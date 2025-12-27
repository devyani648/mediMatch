# MediMatch

MediMatch is a privacy-first medical image semantic search system that lets you search medical images using text queries or by uploading a similar image. This scaffold includes a FastAPI backend, a React + Vite frontend, data pipeline scripts, and database setup for PostgreSQL + pgvector.

Quick start (development):

1. Start PostgreSQL with pgvector:

```powershell
docker-compose up -d postgres
```

2. Create database schema:

```powershell
docker exec -i <container> psql -U medimatch -d medimatch < scripts/setup_database.sql
```

3. Create test data and embeddings:

```powershell
python data_pipeline/quick_dataset.py
python data_pipeline/generate_embeddings.py --input data/test/metadata.csv
```

4. Start backend:

```powershell
cd backend
uvicorn app.main:app --reload
```

5. Start frontend:

```powershell
cd frontend
npm install
npm run dev
```

See `PROJECT_SPEC.md` for detailed requirements and testing instructions.
