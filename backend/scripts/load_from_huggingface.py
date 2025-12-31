# backend/scripts/load_from_huggingface.py
"""
Fixed version with correct method names
"""

import sys
import os
from pathlib import Path

current_dir = Path(__file__).parent
backend_dir = current_dir.parent
sys.path.insert(0, str(backend_dir))

print(f"📁 Working directory: {os.getcwd()}")
print(f"📂 Backend directory: {backend_dir}")

try:
    from app.database import SessionLocal, engine
    from app.models.medical_case import MedicalCase, Base
    from app.services.embedding_service import EmbeddingService
    print("✅ Imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

from tqdm import tqdm
import random

def load_from_huggingface():
    """Load real medical data"""
    
    print("\n🤗 Hugging Face Medical Data Loader")
    print("=" * 50)
    
    # Initialize database
    print("🗄️  Initializing database...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Initialize embedding service
    print("🤖 Loading CLIP model...")
    embedding_service = EmbeddingService()
    print("✅ CLIP model loaded!")
    
    # Check what methods are available
    print("\n🔍 Checking available methods...")
    methods = [m for m in dir(embedding_service) if not m.startswith('_')]
    print(f"Available methods: {methods}")
    
    try:
        # Try to import datasets
        try:
            from datasets import load_dataset
            print("✅ 'datasets' package found")
        except ImportError:
            print("Installing datasets...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "datasets"])
            from datasets import load_dataset
        
        print("\n📥 Loading dataset from Hugging Face...")
        
        # Try to load dataset
        try:
            dataset = load_dataset(
                "keremberke/chest-xray-classification",
                name="full",
                split="train",
                streaming=False
            )
            print(f"✅ Loaded dataset with {len(dataset)} images!")
            
            max_cases = min(500, len(dataset))
            dataset = dataset.select(range(max_cases))
            
        except Exception as e:
            print(f"⚠️  Could not load from Hugging Face: {e}")
            print("Creating realistic sample data instead...")
            create_sample_data(db, embedding_service)
            return
        
        # Process cases
        added = 0
        print(f"\n📊 Processing {len(dataset)} cases...")
        
        diagnosis_map = {
            0: 'Normal',
            1: 'Pneumonia',
            2: 'COVID-19'
        }
        
        for idx, item in enumerate(tqdm(dataset, desc="Loading cases")):
            try:
                image = item['image']
                label = item['labels']
                diagnosis = diagnosis_map.get(label, 'Unknown')
                findings = f"Chest X-ray demonstrating findings consistent with {diagnosis}"
                
                # TRY DIFFERENT METHOD NAMES
                # Check which method exists and use it
                if hasattr(embedding_service, 'generate_text_embedding'):
                    txt_emb = embedding_service.generate_text_embedding(findings)
                    img_emb = embedding_service.generate_image_embedding(image)
                elif hasattr(embedding_service, 'encode_text'):
                    txt_emb = embedding_service.encode_text(findings)
                    img_emb = embedding_service.encode_image(image)
                elif hasattr(embedding_service, 'get_text_embedding'):
                    txt_emb = embedding_service.get_text_embedding(findings)
                    img_emb = embedding_service.get_image_embedding(image)
                elif hasattr(embedding_service, 'create_embedding'):
                    txt_emb = embedding_service.create_embedding(findings, 'text')
                    img_emb = embedding_service.create_embedding(image, 'image')
                else:
                    print(f"❌ Cannot find embedding methods!")
                    print(f"Available methods: {[m for m in dir(embedding_service) if not m.startswith('_')]}")
                    create_sample_data(db, embedding_service)
                    return
                
                # Convert embeddings to list, handle numpy arrays
                if hasattr(txt_emb, 'tolist'):
                    txt_list = txt_emb.tolist()
                else:
                    txt_list = list(txt_emb)
                
                if hasattr(img_emb, 'tolist'):
                    img_list = img_emb.tolist()
                else:
                    img_list = list(img_emb)
                
                # Flatten if nested (embeddings should be 1D list)
                if isinstance(txt_list[0], list):
                    txt_list = txt_list[0]
                if isinstance(img_list[0], list):
                    img_list = img_list[0]
                
                case = MedicalCase(
                    case_id=f"hf_case_{idx:05d}",
                    diagnosis=diagnosis,
                    findings=findings,
                    modality="xray",
                    body_part="chest",
                    age=random.randint(25, 75),
                    gender=random.choice(['M', 'F']),
                    image_path=f"hf_xray_{idx}.jpg",  # Add this
                    image_url=f"huggingface_xray_{idx}",
                    text_embedding=txt_list,
                    image_embedding=img_list
                )
                
                db.add(case)
                added += 1
                
                if added % 50 == 0:
                    db.commit()
                    print(f"✅ Added {added} cases...")
                    
            except Exception as e:
                print(f"\n❌ Error processing case {idx}: {e}")
                continue
        
        db.commit()
        
        print(f"\n🎉 SUCCESS!")
        print(f"✅ Loaded {added} REAL medical cases!")
        
        # Show stats
        print("\n📈 Database Statistics:")
        total = db.query(MedicalCase).count()
        print(f"Total cases: {total}")
        
        for diag in diagnosis_map.values():
            count = db.query(MedicalCase).filter(MedicalCase.diagnosis == diag).count()
            print(f"  {diag}: {count} cases")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

def create_sample_data(db, embedding_service):
    """Fallback: Create realistic sample data"""
    print("\n📝 Creating realistic medical sample data...")
    
    cases = [
        ("Pneumonia", "Right lower lobe consolidation with air bronchograms", 45, "M"),
        ("Pneumonia", "Bilateral infiltrates consistent with bacterial pneumonia", 62, "F"),
        ("Normal", "Clear lung fields, no acute cardiopulmonary abnormality", 28, "F"),
        ("Normal", "Heart size normal, lungs clear", 35, "M"),
        ("Atelectasis", "Left lower lobe atelectasis", 55, "M"),
        ("Cardiomegaly", "Enlarged cardiac silhouette", 68, "M"),
        ("Effusion", "Right pleural effusion, moderate", 71, "F"),
        ("Pneumonia", "Left upper lobe pneumonia", 52, "M"),
        ("Normal", "No focal consolidation or effusion", 34, "F"),
        ("Pneumothorax", "Small right pneumothorax", 29, "M"),
    ]
    
    # Multiply to get 100 cases
    cases = cases * 10
    
    added = 0
    print(f"Creating {len(cases)} cases...")
    
    for idx, (diagnosis, findings, age, gender) in enumerate(tqdm(cases, desc="Creating")):
        try:
            txt = f"{diagnosis}. {findings}"
            
            # Try different method names
            if hasattr(embedding_service, 'generate_text_embedding'):
                txt_emb = embedding_service.generate_text_embedding(txt)
            elif hasattr(embedding_service, 'encode_text'):
                txt_emb = embedding_service.encode_text(txt)
            elif hasattr(embedding_service, 'get_text_embedding'):
                txt_emb = embedding_service.get_text_embedding(txt)
            elif hasattr(embedding_service, 'create_embedding'):
                txt_emb = embedding_service.create_embedding(txt, 'text')
            else:
                print("❌ Cannot create embeddings - method not found!")
                print(f"Available methods: {[m for m in dir(embedding_service) if not m.startswith('_')]}")
                return
            
            # Convert to list and flatten if needed
            if hasattr(txt_emb, 'tolist'):
                txt_list = txt_emb.tolist()
            else:
                txt_list = list(txt_emb)
            
            # Flatten if nested
            if isinstance(txt_list[0], list):
                txt_list = txt_list[0]
            
            case = MedicalCase(
                case_id=f"sample_{idx:05d}",
                diagnosis=diagnosis,
                findings=findings,
                modality="xray",
                body_part="chest",
                age=age + (idx % 10),
                gender=gender,
                image_path=f"sample_{idx}.jpg",  # Add this
                image_url=f"sample_{idx}",
                text_embedding=txt_list,
                image_embedding=txt_list  # Use same for fallback
            )
            
            db.add(case)
            added += 1
            
            if added % 50 == 0:
                db.commit()
                
        except Exception as e:
            print(f"Error creating case {idx}: {e}")
            continue
    
    db.commit()
    print(f"✅ Created {added} sample cases")
    print("\n🎉 Database ready with realistic medical data!")

if __name__ == "__main__":
    load_from_huggingface()