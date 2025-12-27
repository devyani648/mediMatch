from typing import Union, List
import numpy as np
import torch
from PIL import Image
import io
import base64

import clip


class EmbeddingService:
    def __init__(self, device: str = "cpu"):
        print(f"Loading CLIP model on device={device}...")
        self.device = device
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        self.model.eval()
        print("CLIP model loaded.")

    def _to_numpy(self, tensor: torch.Tensor) -> np.ndarray:
        arr = tensor.detach().cpu().numpy()
        return arr

    def _normalize(self, vec: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vec, axis=1, keepdims=True) if vec.ndim == 2 else np.linalg.norm(vec)
        norms = np.where(norms == 0, 1, norms)
        return vec / norms

    def encode_text(self, text: Union[str, List[str]]) -> np.ndarray:
        if isinstance(text, str):
            texts = [text]
        else:
            texts = text
        with torch.no_grad():
            tokens = clip.tokenize(texts).to(self.device)
            embeddings = self.model.encode_text(tokens)
            embeddings = embeddings.cpu().numpy()
            embeddings = self._normalize(embeddings)
        return embeddings

    def encode_image(self, image: Union[Image.Image, str]) -> np.ndarray:
        # Accept PIL image or base64 string
        if isinstance(image, str):
            # assume base64
            header, _, data = image.partition(",")
            raw = base64.b64decode(data)
            image = Image.open(io.BytesIO(raw)).convert("RGB")
        elif not isinstance(image, Image.Image):
            raise ValueError("Unsupported image input")

        img_t = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            embeddings = self.model.encode_image(img_t)
            embeddings = embeddings.cpu().numpy()
            embeddings = self._normalize(embeddings)
        return embeddings


_svc: EmbeddingService | None = None


def get_embedding_service(device: str = "cpu") -> EmbeddingService:
    global _svc
    if _svc is None:
        _svc = EmbeddingService(device=device)
    return _svc
