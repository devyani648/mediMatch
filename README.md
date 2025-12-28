# 🏥 MediMatch - AI-Powered Medical Case Search Platform

> Semantic search engine for medical imaging using CLIP embeddings and vector similarity

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

## 📋 Overview

MediMatch is an intelligent medical case retrieval system that enables healthcare professionals to search for similar medical cases using natural language queries or medical images. Built with state-of-the-art AI technology, it uses OpenAI's CLIP model for semantic understanding and pgvector for efficient similarity search.

### ✨ Key Features

- 🔍 **Multi-Modal Search**: Search using text descriptions or medical images
- 🧠 **Semantic Understanding**: CLIP embeddings capture clinical meaning, not just keywords
- ⚡ **Fast Vector Search**: pgvector extension provides millisecond query times
- 🎯 **Advanced Filtering**: Filter by modality (X-ray, CT, MRI), body part, age, gender
- 📊 **Similarity Scoring**: Ranked results with confidence scores
- 🎨 **Modern UI**: Clean, responsive interface built with React
- 🔌 **RESTful API**: Well-documented API with interactive Swagger UI

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   React UI      │────────▶│   FastAPI        │────────▶│  PostgreSQL     │
│   (Frontend)    │  HTTP   │   (Backend)      │  SQL    │  + pgvector     │
│   Port: 5173    │         │   Port: 8000     │         │  Port: 5432     │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                    │
                                    ▼
                            ┌──────────────────┐
                            │  CLIP Model      │
                            │  (Embeddings)    │
                            └──────────────────┘
```

### Tech Stack

**Frontend:**
- React + Vite
- Modern ES6+ JavaScript
- Responsive CSS

**Backend:**
- FastAPI (Python 3.10+)
- SQLAlchemy ORM
- Pydantic for validation
- OpenAI CLIP (ViT-B/32)
- PyTorch

**Database:**
- PostgreSQL 14+
- pgvector extension for vector similarity search

**Infrastructure:**
- Docker & Docker Compose
- Uvicorn ASGI server

## 🚀 Quick Start

### Prerequisites

- Docker Desktop
- Python 3.10+
- Node.js 16+
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/devyani648/mediMatch.git
cd mediMatch
```

2. **Start the database**
```bash
docker-compose up -d
```

3. **Set up the backend**
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Linux/Mac

pip install -r requirements.txt
```

4. **Start the backend server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. **Set up the frontend** (in a new terminal)
```bash
cd frontend
npm install
npm run dev
```

6. **Access the application**
- Frontend: http://localhost:5173
- API Documentation: http://localhost:8000/docs
- API: http://localhost:8000

## 📖 Usage

### Text-Based Search

1. Enter a clinical query like "Pneumonia" or "chest x-ray with consolidation"
2. Optionally filter by modality or body part
3. Click "Search" to find similar cases
4. View results ranked by similarity score

### Image-Based Search

1. Click the "Image" tab
2. Upload a medical image (X-ray, CT, MRI)
3. The system will find visually and clinically similar cases
4. Compare findings and diagnoses

### API Usage

```python
import requests

# Text search
response = requests.post(
    "http://localhost:8000/api/search",
    json={
        "query": "Pneumonia",
        "limit": 5,
        "modality": "xray",
        "body_part": "chest"
    }
)

results = response.json()
print(f"Found {results['total']} cases in {results['query_time_ms']:.2f}ms")
```

## 🎯 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/search` | POST | Search for similar medical cases |
| `/docs` | GET | Interactive API documentation |
| `/health` | GET | Service health status |

### Request Schema

```json
{
  "query": "string (optional)",
  "image": "base64_string (optional)",
  "limit": 10,
  "modality": "xray|ct|mri (optional)",
  "body_part": "chest|head|abdomen (optional)",
  "similarity_threshold": 0.0
}
```

### Response Schema

```json
{
  "results": [
    {
      "id": 1,
      "case_id": "case_001",
      "diagnosis": "Pneumonia",
      "findings": "Consolidation in right lower lobe",
      "modality": "xray",
      "body_part": "chest",
      "age": 45,
      "gender": "M",
      "similarity_score": 0.87
    }
  ],
  "total": 5,
  "query_time_ms": 145.2
}
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://medimatch:medimatch@localhost:5432/medimatch
DEVICE=cpu  # or 'cuda' for GPU
API_HOST=0.0.0.0
API_PORT=8000
```

### Database Configuration

The `docker-compose.yml` file configures PostgreSQL with pgvector:

```yaml
services:
  postgres:
    image: ankane/pgvector:latest
    environment:
      POSTGRES_DB: medimatch
      POSTGRES_USER: medimatch
      POSTGRES_PASSWORD: medimatch
    ports:
      - "5432:5432"
```

## 📊 Performance

- **Average Query Time**: ~150-200ms
- **Embedding Generation**: ~100ms per text query
- **Database Size**: Scales to millions of vectors
- **Concurrent Users**: Supports 100+ simultaneous searches

## 🧪 Testing

### Test the API

```bash
cd backend
python test_search.py
```

### Test with curl

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Pneumonia","limit":5}'
```

### Test with PowerShell

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/search" `
  -Method Post `
  -Body '{"query":"Pneumonia","limit":5}' `
  -ContentType "application/json"
```

## 📁 Project Structure

```
mediMatch/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration settings
│   │   ├── database.py          # Database connection
│   │   ├── models/              # SQLAlchemy models
│   │   │   └── medical_case.py
│   │   ├── schemas/             # Pydantic schemas
│   │   │   └── case.py
│   │   ├── routers/             # API routes
│   │   │   └── search.py
│   │   └── services/            # Business logic
│   │       ├── embedding_service.py
│   │       └── search_service.py
│   ├── requirements.txt
│   └── docker-compose.yml
│
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── App.jsx             # Main application
│   │   └── main.jsx            # Entry point
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 🛠️ Development

### Adding New Features

1. Create a new branch
```bash
git checkout -b feature/new-feature
```

2. Make your changes and commit
```bash
git add .
git commit -m "Add: Description of new feature"
```

3. Push and create a pull request
```bash
git push origin feature/new-feature
```

### Running in Development Mode

Both frontend and backend support hot-reload:
- Backend: `uvicorn --reload` automatically restarts on code changes
- Frontend: Vite dev server hot-reloads React components

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL container is running
docker ps

# Restart the container
docker-compose restart

# View logs
docker logs medimatch-postgres-1
```

### Port Already in Use

```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (Windows)
taskkill /PID <PID> /F
```

### CLIP Model Not Loading

Ensure you have enough RAM (minimum 4GB) and PyTorch is properly installed:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

## 🔮 Future Enhancements

- [ ] Multi-language support for international medical terms
- [ ] DICOM file format support
- [ ] Real-time collaborative annotations
- [ ] Integration with PACS systems
- [ ] Advanced analytics dashboard
- [ ] User authentication and role-based access
- [ ] Export results to PDF/Excel
- [ ] Mobile application
- [ ] Integration with real medical datasets (MIMIC-CXR, ChestX-ray14)
- [ ] GPU acceleration for faster embeddings

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

**Devyani** - [@devyani648](https://github.com/devyani648)

Project Link: [https://github.com/devyani648/mediMatch](https://github.com/devyani648/mediMatch)

## 🙏 Acknowledgments

- [OpenAI CLIP](https://github.com/openai/CLIP) for the embedding model
- [pgvector](https://github.com/pgvector/pgvector) for efficient vector similarity search
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- Medical imaging community for inspiration and support

## 📊 Statistics

- **Development Time**: 2 weeks
- **Lines of Code**: ~2,000+
- **Test Coverage**: In Progress
- **Performance**: Sub-200ms query times

---

**Built with ❤️ for healthcare professionals**

*Making medical knowledge more accessible through AI*
