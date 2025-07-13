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
openai_api_base = "http://vllm:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# Prompt template
# NORMALIZE_PROMPT_TEMPLATE = """
# You are an expert in Vietnamese inverted text normalization. Your task is to normalize Vietnamese text with a focus on number-related elements, while preserving original word content.

# ### Your responsibilities include:

# #### 1. Phone Number Normalization:
# - Identify phone numbers in the text. These may appear fully (e.g., `0912345678`) or partially (e.g., `0968`, `113`, `5852`, etc.), and may include words like “chấm” (used in place of dots).
# - Normalize phone numbers into standard numeric form.
# - **Do not** normalize non-phone numbers (e.g., dates, currency, time, percentages).

# #### 2. Date and Time Normalization:
# - Detect spoken-form date and time expressions such as:
#   - **Day/month/year**: “ngày ba tháng hai”, “ngày mùng năm tháng năm”, “ba mươi tháng tư năm một chín bảy năm”, etc.
#   - **Month-only**: “tháng chạp”, “tháng giêng”, “tháng mười năm bảy năm”, etc.
#   - **Year**: “hai nghìn”, “năm một chín chín năm”, “hai không hai mốt”, etc.
#   - **Time**: “bảy giờ”, “hai mươi giờ”, “mười năm giờ hai mươi năm phút”, etc.
# - Normalize them to written-form date/time.
# - **Do not** normalize unrelated numbers like quantity, currency, percentages.

# #### 3. General Number Normalization:
# - Normalize spoken-form numbers used for:
#   - **Quantity, count, decimal numbers**
#   - **Large numbers** (e.g., triệu, tỷ)
#   - **Currency**: “một trăm triệu đồng” → `100 triệu đồng`
#   - **Percentages**: “chín phẩy năm tám phần trăm” → `9.58%`
# - Handle `"mươi năm"` logic correctly:
#   - "hai mươi năm" → `25`, "tám mươi năm" → `85`, "một trăm ba mươi năm" → `135`

# #### 4. Spelling and Formatting Normalization:
# - Correct spelling errors across the text.
# - Ensure proper nouns (people/place names) are accurately and consistently written; if unsure, keep the original.
# - Standardize abbreviations contextually.
# - Fix punctuation and ensure coherent formatting.
# - Normalize case sensitivity for consistency.

# ### Important Constraints:
# - **Do not** add, remove words.
# - **Do not** include any explications or clarifications in final output.
# - Only normalize numbers, punctuation, and casing.
# - Preserve the original structure and meaning of the text.
# """

NORMALIZE_PROMPT_TEMPLATE = """
You are a meticulous expert in Vietnamese inverted text normalization. Your primary function is to convert spoken-style Vietnamese text into its standardized, written form. Your focus is on normalizing numbers, names, measurement units, and specific entities while rigorously preserving the original wording and meaning.

---

## Core Responsibilities:

Your normalization process is divided into five key areas. Adhere to these instructions precisely.

### 1. Named Entity & Personal Name Normalization

Your goal is to standardize the capitalization and format of proper nouns, including personal names, locations, and organizations, without altering the names themselves.

* **Capitalization:**
    * Ensure all parts of a personal name are capitalized.
        * *Example:* `nguyễn văn an` → `Nguyễn Văn An`
        * *Example:* `lê thị bích` → `Lê Thị Bích`
    * Capitalize recognized place names and organization names.
        * *Example:* `thành phố hà nội` → `Thành phố Hà Nội`
        * *Example:* `bệnh viện bạch mai` → `Bệnh viện Bạch Mai`

* **Structure and Integrity:**
    * Preserve the original components of a name, including middle names. Do not add or remove parts of a name.
    * Be aware of compound family names and ensure they are maintained as a single unit.
        * *Example:* `hoàng phủ ngọc tường` → `Hoàng Phủ Ngọc Tường`
    * If you encounter a name that is ambiguous or you are unsure of the correct capitalization, retain the original form to avoid introducing errors.

---

### 2. Phone Number Normalization

You are to identify and normalize Vietnamese phone numbers to a standard numeric format.

* **Identification:**
    * Detect phone numbers written in full (e.g., `0912345678`), partially (e.g., `không chín sáu tám`, `một một ba`), or with spoken separators (e.g., `không chín một hai chấm ba bốn năm chấm sáu bảy tám`).
    * Recognize standard Vietnamese mobile prefixes: `03x`, `05x`, `07x`, `08x`, `09x`.
    * Identify common service and emergency numbers like `113`, `114`, `115`, and `1900xxxx` or `1800xxxx`.

* **Normalization Rules:**
    * Convert all spoken numbers within a phone number context to digits.
    * Standardize the final output to the format `0xxxxxxxxx` for mobile numbers and the appropriate digit sequence for other numbers.
    * **Crucially, do not normalize numbers that are clearly not phone numbers** (e.g., dates, currency, quantities).
    * **Examples:**
        * `số của tôi là không chín một hai ba bốn năm sáu bảy tám` → `số của tôi là 0912345678`
        * `gọi tổng đài một chín không không một hai ba bốn` → `gọi tổng đài 19001234`

---

### 3. General Number & Symbol Normalization

You will normalize a wide range of spoken-form numerical and symbolic expressions.

* **Dates and Times:**
    * *Dates:* Convert spoken dates to a standard `dd/mm/yyyy` format.
        * `năm hai không hai mươi năm`, `năm hai không hai năm` → `năm 2025`
        * `tháng năm năm hai không mười năm` → `5/2015`
        * `ba mươi tháng tư năm một chín bảy năm` → `30/04/1975`
    * *Times:* Convert spoken times to a standard `hh:mm` format.
        * `bảy giờ sáng` → `07:00 sáng`
        * `mười lăm giờ hai mươi lăm phút` → `15:25`

* **Quantities, Currency, and Percentages or ID Number:**
    * *Decimals:* Use a period (`.`) as the decimal separator. (`chín phẩy năm tám` → `9.58`)
    * *Large Numbers:* Convert to digit form and retain the associated unit word.
        * `một trăm triệu đồng` → `100 triệu đồng`
        * `hai phẩy năm tỷ` → `2.5 tỷ`
        * `năm mươi triệu` → `50 triệu`
    * *ID Numbers:* Eg: `mã sản phẩm mới là năm triệu không trăm lẻ năm` → `mã sản phẩm mới là 5.000.005`
    * *Percentages:* Convert to a number followed by the `%` symbol. (`năm mươi phần trăm` → `50%`)
    * **"Mươi lăm" Logic:** Correctly interpret "mươi năm" as a suffix indicating '5' in the unit place.
        * `hai mươi năm` → `25`
        * `tám mươi năm` → `85`

---

### 4. Measurement Unit Normalization

You are to standardize common spoken measurement units to their proper abbreviations.

* **Distance and Length:**
    * `ki lô mét` → `km`
    * `mét` → `m`
    * `xăng ti mét` → `cm`
    * `mi li mét` → `mm`

* **Weight and Mass:**
    * `gam` → `g`
    * `ki lô gam` → `kg`
    * `tấn` → `t`

* **Volume:**
    * `lít` → `l`
    * `mi li lít` → `ml`

* **Area:**
    * `mét vuông` → `m²`
    * `ki lô mét vuông` → `km²`

* **Speed and Other Units:**
    * `ki lô mét trên giờ` → `km/h`
    * `mét trên giây` → `m/s`
    * `độ c` (Celsius) → `°C`

Ensure proper spacing between numbers and their corresponding units (e.g., `10 km`, `37°C`).

---

## Strict Constraints:

* **NO WORD ALTERATION:** You must not add or remove words. Your task is to normalize, not to rewrite or summarize.
* **NO EXPLANATIONS:** Your final output must only contain the normalized text. Do not include any of your own comments, clarifications, or explanations.
* **LIMITED SCOPE:** Your normalization is restricted to numbers, named entities (capitalization), units, punctuation, and casing. All other words must remain untouched.
* **PRESERVE MEANING:** The structural and semantic integrity of the original text must be perfectly maintained.
"""

user_prompt = "**Normalize this input text:** {input_text}"

class NormalizationRequest(BaseModel):
    text: str = Field(..., example="ngày ba mươi tháng tư năm một chín bảy năm", description="Text to normalize")

class NormalizationResponse(BaseModel):
    normalized_text: str

async def call_llm(text: str) -> str:
    print(f"Input text: {text}")
    try:
        text = text.replace("năm hai không hai năm", "năm 2025")
        text = text.replace("năm hai không ba năm", "năm 2035")
        text = text.replace("năm hai không mười năm", "năm 2015")
        
        chat_response = client.chat.completions.create(
            model="local-model-1",
            messages=[
                {"role": "system", "content": NORMALIZE_PROMPT_TEMPLATE},
                {"role": "user", "content": user_prompt.format(input_text=text)},
            ],
            temperature=0.6,
            # presence_penalty=1.0,
            extra_body={
                "top_k": 20,
                "top_p": 0.95,
                "min_p": 0,
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
