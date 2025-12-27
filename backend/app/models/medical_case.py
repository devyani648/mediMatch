from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

from ..database import Base


class MedicalCase(Base):
    __tablename__ = "medical_cases"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String, unique=True, nullable=False, index=True)
    age = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    modality = Column(String, nullable=False)
    body_part = Column(String, nullable=False)
    diagnosis = Column(Text, nullable=False)
    findings = Column(Text, nullable=True)
    clinical_notes = Column(Text, nullable=True)
    image_path = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    image_embedding = Column(Vector(512), nullable=False)
    text_embedding = Column(Vector(512), nullable=True)
    source = Column(String, default="custom")
    metadata = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now(), server_default=func.now())
