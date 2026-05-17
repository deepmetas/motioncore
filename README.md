```markdown
# MotionCore · AI Dance Analysis

MotionCore is a dance analysis system based on video pose estimation and Large Language Model (LLM).  
After uploading two videos, the system automatically extracts 3D skeleton sequences, generates a streaming analysis report with audio alignment, and provides a synchronized dual-video comparison player.  
It supports multiple languages (Chinese / English) and multiple LLM providers (OpenAI / DeepSeek / Gemma4).

---

## 🎬 demo video


https://github.com/user-attachments/assets/5e08d1fc-d04f-4354-b4ad-cfb2fbf8b0a0



https://github.com/user-attachments/assets/17fb303f-2b61-48b7-bff5-9a01973a77d0


---

## ✨ Features

- ✅ Dual video upload (A: user action, B: reference instruction)
- ✅ Real-time skeleton keypoint overlay (MediaPipe)
- ✅ Streaming AI training report (SSE)
- ✅ Automatic audio alignment + synchronized dual-video playback
- ✅ Chat-style interface with copyable reports
- ✅ Chinese / English interface and report language switching
- ✅ Supports OpenAI, DeepSeek, and Gemma4 LLMs
- ✅ Processing progress bar with time estimation

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| Backend | FastAPI (Python) |
| Pose Estimation | MediaPipe Pose |
| Audio Alignment | MoviePy + NumPy |
| LLM Integration | OpenAI SDK (compatible with DeepSeek / Ollama) |
| Computer Vision | OpenCV, Ultralytics (YOLO) |
| Environment Variables | python-dotenv |

---

## 📦 Installation & Configuration

### 1. Clone the repository

```bash
git clone https://github.com/deepmetas/motioncore.git
cd motioncore
```

### 2. Create a virtual environment (recommended)

```bash
# Windows
conda create -n motion python=3.10 -y
conda activate motion
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

A `.env.example` template is provided in the project root. Copy it to `.env` and fill in the required values:

```bash
cp .env.example .env
```

Open `.env` and choose your LLM provider, then provide the corresponding API key:

```ini
# LLM: openai / deepseek / gemma4
LLM_PROVIDER=deepseek

# OpenAI
OPENAI_API_KEY=sk-xxxxxx
OPENAI_MODEL=gpt-4.1-mini

# DeepSeek (recommended for users in China)
DEEPSEEK_API_KEY=sk-xxxxxx
DEEPSEEK_MODEL=deepseek-v4-pro

# Gemma 4 (or other OpenAI compatible models, such as running Gemma through Ollama)
# You need to provide base_url and api_key (if available)
GEMMA_API_KEY=ollama
GEMMA_BASE_URL=http://localhost:11434/v1
GEMMA_MODEL=gemma2:9b
```

### 5. Start the service

```bash
python main.py
```

Visit `http://127.0.0.1:8000` to use the dance analysis tool.

---

## 🚀 Usage

1. Open the dance analysis page and upload **two videos** by clicking or dragging:
   - **Video A**: Your action video
   - **Video B**: Reference instruction video
2. The system automatically processes the videos and extracts skeleton data, then starts AI analysis once processing is complete.
3. The analysis report is displayed in a streaming style word by word, and you can click "Stop" at any time to interrupt.
4. After the report finishes, a **dual-video synchronized comparison player** will appear at the bottom of the chat area with audio aligned, allowing you to play both videos simultaneously and compare the differences.

---

## 📂 Project Structure

```
motioncore/
├── main.py                 # Main entry point
├── .env.example            # Environment variable template
├── requirements.txt        # Dependency list
├── README.md               # Project documentation
├── web/                    # Dance analysis application
│   ├── api/
│   │   ├── app.py          # FastAPI endpoints
│   │   ├── client.py       # LLM streaming client
│   │   ├── prompts_zh.py   # Chinese prompt
│   │   └── prompts_en.py   # English prompt
│   └── h5/
│       ├── index.html      # Frontend page
│       └── favicon.ico
└── outputs/                # Runtime generated: uploaded videos, JSON, conversation logs
```

---

## 🌐 Language Switching

A `中文 / English` button is located in the top-right corner of the frontend. Clicking it changes both the UI text and the language of the AI analysis report simultaneously.  
In English mode, the system instruction forces the model to respond in English.

---

## 🔌 API Endpoints (Summary)

| Method | Path                  | Description                             |
| ------ | --------------------- | --------------------------------------- |
| POST   | `/upload`             | Upload video, returns task_id           |
| GET    | `/stream/{task_id}`   | MJPEG video stream (during processing)  |
| GET    | `/progress/{task_id}` | Query processing progress               |
| GET    | `/status/{task_id}`   | Get completion status and download link |
| POST   | `/analyze/stream`     | Streaming analysis (SSE)                |
| GET    | `/audio-offset`       | Calculate audio alignment offset        |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
