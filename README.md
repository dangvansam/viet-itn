<!-- # Vietnamese Inverse Text Normalization API -->
<p align="center">
  <img src="assets/viet-itn-logo.png" style="width: 180px">
  <h1 align="center" style="color: white; font-weight: bold; font-family:roboto">
    <span style="color: white;">VietITN</span>: Vietnamese Inverse Text Normalization API
  </h1>
</p>

<p align="center">
  <a href="https://github.com/dangvansam/viet-itn"><img src="https://img.shields.io/github/stars/dangvansam/viet-itn?style=social"></a>
  <a href="https://pypi.org/project/viet-itn" target="_blank"><img src="https://img.shields.io/pypi/v/viet-itn.svg" alt="PyPI">
  <a href="https://github.com/dangvansam/viet-itn"><img src="https://img.shields.io/badge/Python-3.10-green"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/dangvansam/viet-itn"></a>
  <br>
  <a href="README.md"><img src="https://img.shields.io/badge/README-English-blue"></a>
  <!-- <a href="README_VN.md"><img src="https://img.shields.io/badge/README-Tiếng Việt-red"></a> -->
</p>

**VietITN** is a simple yet powerful REST API for Inverse Text Normalization (ITN) tailored for Vietnamese language, built with FastAPI and Docker. It leverages `pynini` and pre-built grammars to convert spoken-form text into its written form.

---

## ⭐ Features
- 🔁 **Inverse Text Normalization**: Converts spoken Vietnamese into standard written text.
- 🚀 **FastAPI**: Lightweight and modern Python web framework.
- 📦 **Dockerized**: Easily deployable with Docker and Docker Compose.
- 📑 **Interactive API Docs**: Swagger UI automatically available at `/docs`.
- ✅ **Health Check Endpoint**: Keep track of service status via `/health`.

---

## 🛠️ Setup

### 1. Clone the Repository
```bash
git clone https://github.com/dangvansam/viet-itn.git
cd viet-itn
```

### 2. Build & Run with Docker Compose
```bash
docker-compose build
docker-compose up -d
```

### 3. Access the API
Visit: [http://localhost:8000](http://localhost:8000)

---

## 📬 API Usage

### 🔠 Normalize Text
**Endpoint:** `POST /normalize`

**Request Body:**
```json
{
  "text": "ngày ba mươi tháng tư năm một chín bảy năm"
}
```

**Example with curl:**
```bash
curl -X POST "http://localhost:8000/normalize" \
     -H "Content-Type: application/json" \
     -d '{"text": "ngày ba mươi tháng tư năm một chín bảy năm"}'
```

**Response:**
```json
{
  "normalized_text": "ngày 30/4/1975"
}
```

---

### ❤️ Health Check
**Endpoint:** `GET /health`

**Example:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "ok"
}
```

---

### 📚 Interactive Documentation
FastAPI provides built-in Swagger UI. Open your browser and go to:
```
http://localhost:8000/docs
```

---

## 🙏 Acknowledgements
- 🧠 Built on top of `pynini` grammars and inspired by work from the [NLP community](https://github.com/google-research/).
<!-- - ✨ Uses ideas from projects like [VietTTS](https://github.com/dangvansam/viet-tts) and [Vinorm](https://github.com/v-nhandt21/Vinorm). -->

---

## 📜 License
This project is licensed under the **Apache 2.0 License**.

---

## 💬 Contact
- 🌐 Facebook: [fb.com/sam.rngd](https://fb.com/sam.rngd)
- 🐙 GitHub: [dangvansam](https://github.com/dangvansam)
- 📧 Email: dangvansam98@gmail.com