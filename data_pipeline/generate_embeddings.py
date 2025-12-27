"""Generate embeddings from CSV and insert into database."""
import argparse
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import numpy as np

from backend.app.config import settings
from backend.app.services.embedding_service import get_embedding_service
from backend.app.models.medical_case import MedicalCase
from backend.app.database import Base


def main(input_csv: str):
    print("Loading CLIP embedding service (CPU)...")
    svc = get_embedding_service(device=settings.device)

    engine = create_engine(settings.database_url, future=True)
    Base.metadata.create_all(bind=engine)

    df = pd.read_csv(input_csv)
    success = 0
    fail = 0

    with Session(engine) as session:
        for idx, row in df.iterrows():
            try:
                img_path = row["image_path"]
                from PIL import Image

                img = Image.open(img_path).convert("RGB")
                emb = svc.encode_image(img)
                if emb.ndim == 2:
                    vec = emb[0].tolist()
                else:
                    vec = emb.tolist()

                mc = MedicalCase(
                    case_id=row["case_id"],
                    age=str(row.get("age", "")),
                    gender=str(row.get("gender", "")),
                    modality=row.get("modality", "xray"),
                    body_part=row.get("body_part", "chest"),
                    diagnosis=row.get("diagnosis", ""),
                    findings=row.get("findings", ""),
                    image_path=row["image_path"],
                    image_embedding=vec,
                )
                session.add(mc)
                session.commit()
                success += 1
            except Exception as e:
                print(f"Failed {row.get('case_id')}: {e}")
                session.rollback()
                fail += 1

    print(f"Finished: success={success}, failed={fail}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", dest="input", required=True)
    args = parser.parse_args()
    main(args.input)
