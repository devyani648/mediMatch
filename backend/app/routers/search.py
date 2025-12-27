from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from typing import List
from sqlalchemy.orm import Session

from ..schemas.case import SearchRequest, SearchResponse, MedicalCaseResponse
from ..database import get_db
from ..services.embedding_service import get_embedding_service
from ..services.search_service import SearchService

router = APIRouter()


@router.post("/api/search", response_model=SearchResponse)
def search_endpoint(req: SearchRequest, db: Session = Depends(get_db)):
    svc = get_embedding_service(device="cpu")

    if not req.query and not req.image:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="query or image required")

    if req.image:
        emb = svc.encode_image(req.image)
    else:
        emb = svc.encode_text(req.query)

    # emb is numpy array (N, dim) or (1, dim)
    if emb.ndim == 2:
        q = emb[0].tolist()
    else:
        q = emb.tolist()

    search_svc = SearchService(db)
    res = search_svc.vector_search(
        query_embedding=q,
        limit=req.limit,
        modality=req.modality,
        body_part=req.body_part,
        similarity_threshold=req.similarity_threshold,
    )

    results = []
    for r in res["results"]:
        item = MedicalCaseResponse(
            id=r.get("id"),
            case_id=r.get("case_id"),
            age=r.get("age"),
            gender=r.get("gender"),
            modality=r.get("modality"),
            body_part=r.get("body_part"),
            diagnosis=r.get("diagnosis"),
            findings=r.get("findings"),
            clinical_notes=r.get("clinical_notes"),
            image_path=r.get("image_path"),
            image_url=r.get("image_url"),
            source=r.get("source"),
            metadata=r.get("metadata"),
            similarity_score=float(r.get("similarity", 0.0)),
        )
        results.append(item)

    return SearchResponse(results=results, total=res["total"], query_time_ms=res["query_time_ms"])
