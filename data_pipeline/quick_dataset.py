"""Create a small synthetic dataset of colored square images and metadata CSV."""
from PIL import Image
from pathlib import Path
import csv


def make_square(color, path):
    img = Image.new("RGB", (256, 256), color)
    img.save(path)


def main():
    out_dir = Path("data/test")
    out_dir.mkdir(parents=True, exist_ok=True)

    categories = {
        "Normal": (200, 200, 200),
        "Pneumonia": (100, 150, 240),
        "Fracture": (240, 180, 200),
        "Tumor": (160, 100, 200),
    }

    rows = []
    i = 1
    for label, color in categories.items():
        for j in range(5):
            case_id = f"case_{i:03d}"
            filename = f"{case_id}.png"
            path = out_dir / filename
            make_square(color, path)
            row = {
                "case_id": case_id,
                "diagnosis": label,
                "modality": "xray",
                "body_part": "chest",
                "image_path": str(path),
                "age": str(30 + (i % 20)),
                "gender": "F" if (i % 2 == 0) else "M",
                "findings": f"Synthetic {label} example",
            }
            rows.append(row)
            i += 1

    csv_path = out_dir / "metadata.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["case_id", "diagnosis", "modality", "body_part", "image_path", "age", "gender", "findings"]) 
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"Created {len(rows)} images in {out_dir}")
    print(f"Metadata CSV at {csv_path}")


if __name__ == "__main__":
    main()
