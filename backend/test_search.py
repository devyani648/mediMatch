from app.routers.search import search_endpoint
from app.schemas.case import SearchRequest
from app.database import SessionLocal
import traceback

try:
    db = SessionLocal()
    req = SearchRequest(query="Pneumonia", limit=5)
    result = search_endpoint(req, db)
    print("Success:", result)
except Exception as e:
    print("ERROR:")
    traceback.print_exc()
finally:
    db.close()
