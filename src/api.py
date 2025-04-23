import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from src.normalize import InverseTextNormalizer

app = FastAPI(
    title="Vietnamese Text Normalization API",
    description="API to perform inverse text normalization for Vietnamese.",
    version="1.0.0"
)

inverse_normalizer = InverseTextNormalizer()

class NormalizationRequest(BaseModel):
    text: str = Field(..., example="ngày ba mươi tháng tư năm một chín bảy năm", description="Text to normalize")

class NormalizationResponse(BaseModel):
    normalized_text: str

@app.post("/normalize", response_model=NormalizationResponse)
async def normalize_endpoint(request: NormalizationRequest):
    normalized = inverse_normalizer.inverse_normalize(request.text)
    return NormalizationResponse(normalized_text=normalized)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
