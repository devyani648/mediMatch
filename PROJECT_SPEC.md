# MediMatch Project Specification for GitHub Copilot

I want to build MediMatch, a medical image semantic search system. Generate the complete project structure and code.

## Project Overview
- **Name:** MediMatch
- **Purpose:** Privacy-first medical image search using semantic embeddings
- **Tech Stack:** FastAPI (Python), PostgreSQL + pgvector, React, standard CLIP model (CPU-optimized)
- **Key Feature:** Search medical images using text queries or upload similar images

## Project Structure

Create this exact folder structure:
```
medimatch/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── medical_case.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── case.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── embedding_service.py
│   │   │   └── search_service.py
│   │   └── routers/
│   │       ├── __init__.py
│   │       └── search.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   ├── components/
│   │   │   ├── SearchBar.jsx
│   │   │   ├── ImageUpload.jsx
│   │   │   ├── CaseGrid.jsx
│   │   │   └── CaseCard.jsx
│   │   └── api/
│   │       └── client.js
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── index.html
├── data_pipeline/
│   ├── quick_dataset.py
│   └── generate_embeddings.py
├── scripts/
│   └── setup_database.sql
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Requirements

### Backend (requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pgvector==0.2.3
python-multipart==0.0.6
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
torch==2.1.0
torchvision==0.16.0
ftfy==6.1.1
pillow==10.1.0
numpy==1.24.3
pandas==2.1.3
tqdm==4.66.1

# Install CLIP separately: pip install git+https://github.com/openai/CLIP.git
```

### Frontend (package.json)
```json
{
  "name": "medimatch-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "postcss": "^8.4.32",
    "autoprefixer": "^10.4.16"
  }
}
```

## Code Generation Instructions

### 1. Backend Configuration (backend/app/config.py)
Generate a settings class using pydantic-settings with:
- database_url (default: postgresql://medimatch:medimatch@localhost:5432/medimatch)
- device (default: "cpu")
- upload_dir, data_dir

### 2. Database Setup (backend/app/database.py)
Generate:
- SQLAlchemy engine and session
- Base declarative class
- get_db() dependency function

### 3. Medical Case Model (backend/app/models/medical_case.py)
Create SQLAlchemy model with:
- id (primary key)
- case_id (unique string)
- age, gender (optional)
- modality (string: xray, ct, mri)
- body_part (string: chest, brain, etc)
- diagnosis (text)
- findings (text, optional)
- clinical_notes (text, optional)
- image_path (string)
- image_url (string, optional)
- image_embedding (vector(512) using pgvector)
- text_embedding (vector(512), optional)
- source (string, default 'custom')
- metadata (JSONB, optional)
- created_at, updated_at (timestamps)

### 4. Pydantic Schemas (backend/app/schemas/case.py)
Create:
- MedicalCaseBase (base fields)
- MedicalCaseCreate (for creating)
- MedicalCaseResponse (for API responses with similarity_score)
- SearchRequest (query: str, image: str, modality: str, body_part: str, limit: int, similarity_threshold: float)
- SearchResponse (results: list, total: int, query_time_ms: float)

### 5. Embedding Service (backend/app/services/embedding_service.py)
**CRITICAL REQUIREMENTS:**
- Use standard CLIP model: `clip.load("ViT-B/32", device="cpu")`
- NOT BiomedCLIP (too slow on CPU)
- Force device to "cpu"
- Methods:
  - encode_text(text: Union[str, List[str]]) -> np.ndarray
  - encode_image(image: Union[PIL.Image, str]) -> np.ndarray (handles base64)
  - Normalize embeddings (divide by L2 norm)
- Singleton pattern with get_embedding_service() function
- Add helpful print statements for loading status

### 6. Search Service (backend/app/services/search_service.py)
Create SearchService class with:
- vector_search() method using SQL with pgvector operators
- Use cosine similarity: `1 - (embedding <=> query_embedding)`
- Support filtering by modality and body_part
- Return results ordered by similarity
- Calculate and return query_time_ms

### 7. Main FastAPI App (backend/app/main.py)
Create FastAPI app with:
- CORS middleware (allow all origins for development)
- Startup event to load embedding service
- Routes:
  - GET / (welcome message)
  - GET /health (health check)
  - POST /api/search (search endpoint using SearchRequest schema)
- Handle both image and text search in same endpoint
- Return SearchResponse with results

### 8. Database Schema (scripts/setup_database.sql)
Generate PostgreSQL script with:
- CREATE EXTENSION vector;
- medical_cases table (matching the SQLAlchemy model)
- HNSW index on image_embedding for fast search
- Helper function search_similar_cases() that takes query_embedding and returns similar cases
- Sample comments showing index creation and performance tuning

### 9. Frontend React App (frontend/src/App.jsx)
Create modern React app with:
- State for: searchResults, loading, error, searchMode ('text' or 'image')
- Header with title "MediMatch" and mode toggle buttons
- Conditional rendering: SearchBar for text mode, ImageUpload for image mode
- CaseGrid to display results
- Loading spinner when searching
- Error display
- Empty state message

### 10. Search Bar Component (frontend/src/components/SearchBar.jsx)
Create form with:
- Text input for query (placeholder: "E.g., pneumonia, bilateral infiltrates...")
- Select for modality (optional: all, xray, ct, mri)
- Select for body_part (optional: all, chest, brain, abdomen)
- Submit button (disabled when loading or empty query)
- Use Tailwind CSS for styling

### 11. Image Upload Component (frontend/src/components/ImageUpload.jsx)
Create component with:
- File input (hidden, triggered by styled div)
- Drag & drop zone with dashed border
- Image preview after upload
- Clear button on preview
- Same filters as SearchBar (modality, body_part)
- Convert file to base64 before sending
- Use Tailwind CSS

### 12. Case Card Component (frontend/src/components/CaseCard.jsx)
Create card displaying:
- Image (if image_url exists)
- Similarity score badge (color-coded: >90% green, >80% blue, >70% yellow)
- Case ID
- Diagnosis (as heading)
- Modality, body_part, age, gender (in grid)
- Findings (truncated with line-clamp-2)
- "View Details" button
- Hover effect
- Use Tailwind CSS

### 13. Case Grid Component (frontend/src/components/CaseGrid.jsx)
Simple grid wrapper:
- CSS Grid with responsive columns (1 on mobile, 2 on md, 3 on lg)
- Maps over cases array to render CaseCard components
- Gap between cards

### 14. API Client (frontend/src/api/client.js)
Create axios client with:
- Base URL from env (VITE_API_URL) or localhost:8000
- search(params) method that POSTs to /api/search
- uploadCase(formData) method (for future use)
- health() method for health check

### 15. Quick Dataset Creator (data_pipeline/quick_dataset.py)
Create script that:
- Generates 20 simple test images (colored squares representing different diagnoses)
- Creates 4 categories: Normal (gray), Pneumonia (blue-ish), Fracture (pink-ish), Tumor (purple-ish)
- 5 examples of each
- Saves images as PNG files (256x256)
- Creates metadata.csv with: case_id, diagnosis, modality, body_part, image_path, age, gender, findings
- Print helpful messages about what was created

### 16. Embedding Generator (data_pipeline/generate_embeddings.py)
Create script that:
- Takes --input CSV path argument
- Loads CLIP model (CPU mode)
- Creates database tables if needed
- Reads CSV with pandas
- For each row:
  - Load image from image_path
  - Generate embedding using embedding service
  - Create MedicalCase object with embedding
  - Save to database
  - Show progress with tqdm
- Print summary (successful/failed counts)
- Handle errors gracefully

### 17. Docker Compose (docker-compose.yml)
Create compose file with:
- postgres service using ankane/pgvector:latest
  - Environment: POSTGRES_USER=medimatch, POSTGRES_PASSWORD=medimatch, POSTGRES_DB=medimatch
  - Port: 5432:5432
  - Volume for data persistence
  - Health check
- backend service (optional, for future)
- frontend service (optional, for future)

### 18. Environment File (backend/.env.example)
Create example with:
- DATABASE_URL
- DEVICE=cpu
- API_HOST, API_PORT
- UPLOAD_DIR, DATA_DIR

### 19. README.md
Create comprehensive README with:
- Project title and description
- Features list
- Quick Start section (with prerequisites)
- Installation steps (backend, frontend, database)
- Usage examples (text search, image search)
- Architecture overview
- Tech stack
- Contributing section
- License (MIT)

### 20. .gitignore
Standard Python + Node.js gitignore:
- __pycache__, *.pyc, venv/, .env
- node_modules/, dist/, build/
- data/, uploads/, *.png, *.jpg
- .DS_Store

## Additional Requirements

### Code Style
- Use type hints in Python
- Add docstrings to all functions
- Use async/await where appropriate in FastAPI
- Modern React with hooks (functional components)
- Clean, readable code with comments

### Error Handling
- Try/catch blocks for file operations
- Proper HTTP status codes in API
- User-friendly error messages
- Database rollback on errors

### Performance
- Batch operations where possible
- Connection pooling for database
- Normalize all embeddings (L2 norm)
- Use HNSW index for vector search

### UI/UX
- Loading states for all async operations
- Empty states with helpful messages
- Responsive design (mobile-friendly)
- Accessible forms (labels, placeholders)
- Modern, clean aesthetic with Tailwind

## Generation Order

Please generate files in this order:
1. Project structure (folders)
2. requirements.txt and package.json
3. Backend config, database, models
4. Backend services (embedding, search)
5. Backend main app and routers
6. Database SQL script
7. Frontend API client
8. Frontend components (in order: CaseCard, CaseGrid, SearchBar, ImageUpload, App)
9. Frontend config files (vite, tailwind)
10. Data pipeline scripts
11. Docker compose
12. Environment files
13. README and .gitignore

## Testing Instructions

After generation, test with:
```bash
# 1. Start PostgreSQL
docker-compose up -d postgres

# 2. Setup database
docker exec -i medimatch-postgres psql -U medimatch -d medimatch < scripts/setup_database.sql

# 3. Create test data
python data_pipeline/quick_dataset.py

# 4. Generate embeddings
python data_pipeline/generate_embeddings.py --input data/test/metadata.csv

# 5. Start backend
cd backend
uvicorn app.main:app --reload

# 6. Start frontend (new terminal)
cd frontend
npm install
npm run dev

# 7. Test at http://localhost:5173
```

## Success Criteria

The project is complete when:
- [ ] All files generated without errors
- [ ] Backend API runs and responds to /health
- [ ] Database schema created successfully
- [ ] 20 test images created and embeddings generated
- [ ] Frontend loads and shows search interface
- [ ] Text search returns results
- [ ] Image upload and search works
- [ ] Results display with similarity scores
- [ ] No console errors

## Notes for Copilot

- Prioritize CPU-friendly code (no GPU required)
- Use standard CLIP, NOT BiomedCLIP
- All vector operations should use pgvector
- Keep code simple and well-commented
- Focus on functionality over optimization initially
- Make it work first, optimize later

---

Generate the complete project now. Start with creating all folders and files, then populate each file with complete, working code. Do not truncate or summarize - provide full implementations for every file.
```

---

## How to Use This with Copilot:

### Method 1: Copilot Chat (Easiest)
1. Open VS Code
2. Open Copilot Chat (Ctrl+Shift+I or Cmd+Shift+I)
3. Paste the entire prompt above
4. Hit Enter
5. Copilot will start generating files one by one

### Method 2: Inline with Comments
1. Create a new file: `PROJECT_SPEC.md`
2. Paste the prompt above
3. Then in Copilot Chat, say: "Read PROJECT_SPEC.md and generate the entire project structure and all files"

### Method 3: Step by Step
If Copilot generates too much at once, break it up:

**First prompt:**
```
Based on PROJECT_SPEC.md, create the backend folder structure and generate:
1. requirements.txt
2. app/config.py
3. app/database.py
4. app/models/medical_case.py
```

**Second prompt:**
```
Now generate the backend services:
1. app/services/embedding_service.py (CPU-optimized CLIP)
2. app/services/search_service.py