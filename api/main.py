"""Local DislocPred inference service for the portfolio demo.

Research use only. This endpoint does not return diagnoses or treatment advice.
"""
from base64 import b64encode
from pathlib import Path
from time import perf_counter

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO

MODEL_PATH = Path(__file__).parent / "models" / "best11.pt"
app = FastAPI(title="DislocPred Portfolio Service", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "POST"], allow_headers=["*"])
model = YOLO(str(MODEL_PATH), task="pose")

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": MODEL_PATH.exists(), "model": MODEL_PATH.name, "purpose": "research prototype"}

@app.post("/analyze")
async def analyze(image: UploadFile = File(...)):
    if image.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(415, "Upload a PNG, JPEG, or WebP image.")
    payload = await image.read()
    if len(payload) > 16 * 1024 * 1024:
        raise HTTPException(413, "Maximum image size is 16 MB.")
    frame = cv2.imdecode(np.frombuffer(payload, np.uint8), cv2.IMREAD_COLOR)
    if frame is None:
        raise HTTPException(400, "The uploaded file could not be read as an image.")
    started = perf_counter()
    result = model.predict(frame, conf=0.25, verbose=False)[0]
    overlay = result.plot(labels=False, boxes=False)
    encoded_ok, encoded = cv2.imencode(".jpg", overlay, [cv2.IMWRITE_JPEG_QUALITY, 90])
    if not encoded_ok:
        raise HTTPException(500, "Could not render model overlay.")
    groups = 0 if result.keypoints is None else len(result.keypoints)
    return {"overlay": "data:image/jpeg;base64," + b64encode(encoded).decode(), "landmarks_detected": groups, "inference_ms": round((perf_counter() - started) * 1000), "disclaimer": "Research prototype only; not for diagnosis or treatment."}
