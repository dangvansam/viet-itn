import os
import uvicorn
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAI

app = FastAPI(
    title="Vietnamese Text Normalization API",
    description="API to perform inverse text normalization for Vietnamese using LLM.",
    version="1.0.0"
)

# LLM client configuration
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8001/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# Prompt template
NORMALIZE_PROMPT_TEMPLATE = """
You are an expert in Vietnamese inverted text normalization. Your task is to normalize Vietnamese text with a focus on number-related elements, while preserving original word content.

### Your responsibilities include:

#### 1. Phone Number Normalization:
- Identify phone numbers in the text. These may appear fully (e.g., `0912345678`) or partially (e.g., `0968`, `113`, `5852`, etc.), and may include words like “chấm” (used in place of dots).
- Normalize phone numbers into standard numeric form.
- **Do not** normalize non-phone numbers (e.g., dates, currency, time, percentages).

#### 2. Date and Time Normalization:
- Detect spoken-form date and time expressions such as:
  - **Day/month/year**: “ngày ba tháng hai”, “ngày mùng năm tháng năm”, “ba mươi tháng tư năm một chín bảy năm”, etc.
  - **Month-only**: “tháng chạp”, “tháng giêng”, “tháng mười năm bảy năm”, etc.
  - **Year**: “hai nghìn”, “năm một chín chín năm”, “hai không hai mốt”, etc.
  - **Time**: “bảy giờ”, “hai mươi giờ”, “mười năm giờ hai mươi năm phút”, etc.
- Normalize them to written-form date/time.
- **Do not** normalize unrelated numbers like quantity, currency, percentages.

#### 3. General Number Normalization:
- Normalize spoken-form numbers used for:
  - **Quantity, count, decimal numbers**
  - **Large numbers** (e.g., triệu, tỷ)
  - **Currency**: “một trăm triệu đồng” → `100 triệu đồng`
  - **Percentages**: “chín phẩy năm tám phần trăm” → `9.58%`
- Handle `"mươi năm"` logic correctly:
  - "hai mươi năm" → `25`, "tám mươi năm" → `85`, "một trăm ba mươi năm" → `135`

#### 4. Spelling and Formatting Normalization:
- Correct spelling errors across the text.
- Ensure proper nouns (people/place names) are accurately and consistently written; if unsure, keep the original.
- Standardize abbreviations contextually.
- Fix punctuation and ensure coherent formatting.
- Normalize case sensitivity for consistency.

### Important Constraints:
- **Do not** add, remove words.
- **Do not** include any explications or clarifications in final output.
- Only normalize numbers, punctuation, and casing.
- Preserve the original structure and meaning of the text.
"""

user_prompt = "**Normalize this input:** {input_text}"

class NormalizationRequest(BaseModel):
    text: str = Field(..., example="ngày ba mươi tháng tư năm một chín bảy năm", description="Text to normalize")

class NormalizationResponse(BaseModel):
    normalized_text: str

async def call_llm(text: str) -> str:
    print(f"Input text: {text}")
    try:
        chat_response = client.chat.completions.create(
            model="local-model-1",
            messages=[
                {"role": "system", "content": NORMALIZE_PROMPT_TEMPLATE},
                {"role": "user", "content": user_prompt.format(input_text=text)},
            ],
            temperature=0.5,
            presence_penalty=1.0,
            extra_body={
                "top_k": 20,
                "chat_template_kwargs": {"enable_thinking": True}
            },
        )

        message = chat_response.choices[0].message
        
        print("reasoning content:", message.reasoning_content)
        
        normalized = message.content
        if not normalized:
            print("Empty normalization result from LLM.")
            return text
        else:
            normalized = normalized.strip()
        
        print(f"Output text: {normalized}")
        return normalized

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM call failed: {str(e)}")

@app.post("/normalize", response_model=NormalizationResponse)
async def normalize_endpoint(request: NormalizationRequest):
    normalized = await call_llm(request.text)
    return NormalizationResponse(normalized_text=normalized)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
