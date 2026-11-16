# 🌱 Smart Circular Economy Platform (EcoCircle)

Full-stack, AI-driven circular economy platform to buy, sell, repair, reuse, donate & recycle products with multi-phase sustainability intelligence.

## ⚡ Tech Stack
- **Frontend**: HTML5, Vanilla JavaScript (SPA Fetch Router), Tailwind CSS
- **Maps**: Leaflet.js + OpenStreetMap (100% Free, no frontend API key needed!)
- **Backend**: Python 3.11+, Flask (RESTful API), Flask-SocketIO (WebSockets with `eventlet`)
- **Database**: SQLite with SQLAlchemy ORM (`backend/instance/circular_economy.db`)
- **AI & ML Engine (4-Phase Architecture)**:
  - **Phase 1 (Vision Detection)**: CLIP (Category & Material Classifier), YOLOv8 (Damage Detector), EasyOCR (Brand/Model Reader)
  - **Phase 2 (Scoring & Valuation)**: LCA Carbon Estimator + GBR (M5), XGBoost Resale Pricing (M6), XGBoost Eco-Trend Predictor (M7)
  - **Phase 3 (Semantic Matching)**: Sentence-BERT (M8 semantic NGO donation matcher)
  - **Phase 4 (Synthesis)**: Google Gemini 3.8 Flash Multimodal API

---

## 🧠 How It Works — 4-Phase AI Pipeline

EcoCircle analyzes every product through a **4-phase multimodal AI pipeline** that runs locally (Phase 1–3) + cloud (Phase 4). Here's the flow:

### Phase 1 — Vision Detection (Local Models)
When you upload a photo (or describe an item), four models run in parallel:

| Model | Purpose | Output |
|-------|---------|--------|
| **CLIP Category Classifier** (M1) | Zero-shot product categorization | `electronics`, `clothing`, `furniture`, `mobile`, `laptop`, `appliance`, `vehicle`, `books`, `sports`, `other` |
| **YOLOv8 Damage Detector** (M2) | Detects cracks, dents, wear, missing parts | `damage_severity: minimal|moderate|severe`, bounding boxes, confidence |
| **EasyOCR Text Extractor** (M3) | Reads brand, model numbers, labels from image | Extracted text → brand/model identification |
| **CLIP Material Classifier** (M4) | Zero-shot material/fabric detection | `plastic`, `metal`, `glass`, `wood`, `cotton`, `polyester`, `leather`, `ceramic`, `composite`, `other` |

**Result:** Structured product fingerprint — category, material, damage level, brand — without any cloud call.

---

### Phase 2 — Scoring & Valuation (Local ML Models)
Uses the Phase 1 outputs + user inputs (weight, age, condition, purchase price) to compute:

| Model | Input | Output |
|-------|-------|--------|
| **Carbon Estimator** (M5) | category, material, weight, condition, action (reuse/recycle/repair) | `carbon_saved_kg` (LCA + GBR), emission factor, trees/car equivalents, citation |
| **Resale Valuation** (M6) | category, brand, age, condition, original price | `estimated_resale_inr`, confidence interval, depreciation % |
| **Eco-Trend Predictor** (M7) | user's history, category diversity, activity streak | 30-day forecast, trend direction, top driver |

---

### Phase 3 — NGO Semantic Matcher (Local)
When you choose **Donate**, Sentence-BERT embeddings match your item's description against a curated NGO database:

- **Model:** `all-MiniLM-L6-v2` (384-dim embeddings)
- **Database:** 15+ verified Indian NGOs (Goonj, TechForAll India, Clothes Box Foundation, etc.)
- **Output:** Top 3 NGOs with semantic similarity scores, contact info, accepted categories

---

### Phase 4 — Gemini Multimodal Synthesis (Cloud)
All structured data from Phases 1–3 is sent to **Google Gemini 3.8 Flash** with a system prompt to produce a human-readable report:

```json
{
  "eco_score_reason": "2-3 sentences explaining sustainability score...",
  "repair_tips": "3 numbered steps with INR cost estimates (if Repair) or 'N/A'",
  "recommendation_text": "Plain-language recommendation mentioning resale price / carbon saving",
  "eco_insight": "One surprising environmental fact with a number"
}
```

This synthesis is what the user sees on the **AI Engine** page — natural language, not raw numbers.

---

## 📱 User Journey — Step-by-Step Procedure

### 1. **Landing Page** (`/`)
- 3D interactive globe (React + Three.js) showing global circular economy stats
- Click **"Get Started"** → redirects to login

### 2. **Authentication** (`/login.html`)
- **Register:** Name, email, password + optional **face descriptor** (128-dim vector from browser Face-API.js)
- **Login:** Email/password **or** Face Unlock (Euclidean distance < 0.6 match)
- JWT token stored in `localStorage`, auto-attached to all API calls

### 3. **Dashboard** (`/dashboard.html`)
- **Stats cards:** Eco Score, Carbon Saved (kg), Items Donated/Sold, Login Streak, Badge
- **Leaderboard:** Top 10 users by Eco Score
- **Eco-Trend Chart:** 30-day forecast from XGBoost model (M7)
- **Activity Feed:** Real-time via Socket.IO (new donations, sales, repairs)
- **Quick Actions:** Analyze Item, Donate, Sell, Repair, Recycle

### 4. **AI Vision Analysis** (`/ai-engine.html`)
**The core feature — upload a photo, get full sustainability report:**

1. Click **"Upload Photo"** or drag-drop an image
2. (Optional) Add description: *"3-year-old Dell laptop, screen has minor scratch, battery lasts 2hrs, paid ₹50,000"*
3. Fill/confirm: Category, Material, Condition, Weight (kg), Age (years), Purchase Price
4. Click **"Analyze"** → shows loading spinner while pipeline runs:
   - Phase 1: CLIP + YOLOv8 + OCR + Material CLIP (~2-5s)
   - Phase 2: Carbon + Resale + Eco-Trend (<1s)
   - Phase 3: NGO match (if donation relevant) (<1s)
   - Phase 4: Gemini synthesis (~3-8s)
5. **Results displayed:**
   - **Category & Material** (with confidence)
   - **Damage Assessment** (severity + visual summary)
   - **Carbon Impact** (kg CO₂ saved by reuse/recycle)
   - **Resale Estimate** (₹ range + depreciation %)
   - **Recommendation** (Repair / Resell / Donate / Recycle / Keep Using)
   - **Gemini Synthesis** (natural-language report with eco_insight, repair_tips)
   - **Nearby Facility Hint** (e-waste recycler, donation center, repair shop)

### 5. **My Items** (`/products.html`)
- CRUD for your personal inventory
- Each item shows: lifecycle stage (In Use → Listed → Donated/Sold/Recycled/Repaired), AI analysis attached
- Actions: **Edit**, **Analyze** (re-run AI), **Donate**, **Sell**, **Repair**, **Recycle**, **Delete**

### 6. **Donate** (`/donate.html`)
- Browse verified NGOs (from Phase 3 database)
- Filter by category, location
- Click **"Donate to this NGO"** → creates donation record, updates dashboard stats, notifies NGO (simulated)

### 7. **Marketplace** (`/marketplace.html`)
- List items for resale (uses M6 valuation as suggested price)
- Browse other users' listings
- Contact seller via in-app messaging (simulated)

### 8. **Repair & Recycling** (`/repair.html`, `/recycling.html`)
- Find nearby repair shops / recycling centers (LocationIQ geocoding if API key set)
- Book repair, track status
- Recycling: generates certificate with carbon saved

### 9. **Map View** (`/map.html`)
- Leaflet.js + OpenStreetMap
- Markers: NGOs, Repair shops, Recycling centers, User listings
- Click marker → details + directions

### 10. **Profile & Settings** (`/profile.html`)
- Edit name, location, avatar
- Toggle **Face Unlock** on/off
- View badge progression (Newcomer → Eco Warrior → Circular Champion)
- Download personal impact report (PDF)

---

## 📁 Project Structure
```
smart-circular-economy/
├── frontend/
│   ├── pages/          → All HTML pages (dashboard, ai-engine, map, donate, marketplace, repair, recycling, profile, admin)
│   ├── css/            → Design system & stylesheets
│   ├── js/             → Modular JS (api.js, config.js, nav.js)
│   └── assets/         → Landing page React build & assets
├── backend/
│   ├── app.py          → Flask entry point & WebSocket engine
│   ├── routes/         → RESTful API routes (ai, auth, donate, ngo, marketplace, repair, recycling, etc.)
│   ├── models/         → SQLAlchemy database models (user, product, listing, ngo, repair, recycling, eco)
│   ├── ml/             → 4-Phase ML pipeline, models & trained artifacts
│   ├── instance/       → circular_economy.db (active SQLite DB)
│   ├── audit_all_phases.py → Phase 1-4 audit & health check script
│   └── .env.example    → Environment variable template
├── start.bat           → Quick start for Windows
├── start.sh            → Quick start for Linux / macOS
└── README.md
```

---

## 🔑 Environment Configuration (`backend/.env`)

Copy `backend/.env.example` to `backend/.env` and configure:

```ini
# Required: Flask session & JWT secret
SECRET_KEY=any_random_secret_string_here

# Google Gemini API Key (for Phase 4 AI Vision Analysis & Synthesis)
# Free at: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.8-flash

# Optional: LocationIQ API Key (for backend geocoding / nearby facility lookup)
# Free at: https://locationiq.com/register
LOCATIONIQ_API_KEY=your_locationiq_api_key_here

# Optional: Carbon Interface API Key (for real-time emissions data)
# Free at: https://www.carboninterface.com/users/sign_up
CARBON_API_KEY=your_carbon_api_key_here
```

> **Note on Maps:** The frontend interactive map uses Leaflet.js and OpenStreetMap tiles. **No Google Maps API key is required!**

---

## 🚀 How to Run

### Quick Start (Windows)
Double-click `start.bat` (or run `./start.bat` from terminal).

### Quick Start (Linux / macOS)
```bash
chmod +x start.sh
./start.sh
```

### Manual Run
```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open your browser at: **http://localhost:5000/**

---

## 📸 Screenshots

> **Note:** Screenshots to be added manually. Placeholder filenames:
>
> - `screenshots/01_landing_page.png` — Landing Page with 3D interactive globe
> - `screenshots/02_login_page.png` — Login/Register with Face Unlock
> - `screenshots/03_dashboard.png` — Dashboard with stats, leaderboard, eco-trend
> - `screenshots/04_ai_engine.png` — AI Vision Analysis page

---

## 🧪 Testing the ML Pipeline
To verify all 4 phases of the AI/ML pipeline:
```bash
cd backend
python audit_all_phases.py
```
This tests CLIP, YOLOv8, EasyOCR, Material Classifier, Carbon LCA model, XGBoost resale valuation, Sentence-BERT NGO matcher, and Gemini 3.8 Flash synthesis.

---

## 🚢 Deployment

### Local Production (Windows/Linux/macOS)
```bash
cd backend
# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Set production env vars (in backend/.env)
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_RELOAD=False
AUTO_OPEN_BROWSER=false

# Run with a production WSGI server
# Option A: waitress (Windows-friendly)
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app

# Option B: gunicorn (Linux/macOS)
gunicorn --bind 0.0.0.0:5000 --workers 4 --threads 2 app:app
```

### Docker Deployment
```dockerfile
# Dockerfile (create at project root)
FROM python:3.11-slim

WORKDIR /app

# System deps for ML libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY . .

# Don't copy .env - mount at runtime
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False
ENV PORT=5000

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "app:app"]
```

```bash
# Build & run (with .env mounted)
docker build -t ecocircle .
docker run -d -p 5000:5000 --name ecocircle \
  -v $(pwd)/backend/.env:/app/backend/.env:ro \
  ecocircle
```

### Cloud Deployment (Render / Railway / Fly.io)
1. **Repository:** Push to GitHub (already done)
2. **Build command:** `pip install -r backend/requirements.txt`
3. **Start command:** `gunicorn --bind 0.0.0.0:$PORT --workers 4 --threads 2 app:app`
4. **Environment variables** (set in platform dashboard):
   - `SECRET_KEY` = random 32+ char string
   - `GEMINI_API_KEY` = your Google AI Studio key
   - `GEMINI_MODEL` = `gemini-3.8-flash`
   - `LOCATIONIQ_API_KEY` = (optional) your LocationIQ key
   - `CARBON_API_KEY` = (optional) your Carbon Interface key
   - `FLASK_ENV` = `production`
   - `FLASK_DEBUG` = `false`
   - `PORT` = provided by platform

### Persistence Notes
- **SQLite** (`backend/instance/circular_economy.db`) is file-based — use a **persistent volume** on cloud platforms
- **ML artifacts** (`backend/ml/artifacts/*.pkl`) are committed and read-only
- **Uploads** (`backend/uploads/`) need persistent storage for user images

### Health Check
```bash
curl https://your-domain.com/api/health
# → {"message":"EcoCircle API running 🌿","status":"ok"}

curl https://your-domain.com/api/ai/models/health
# → {"phase1_available": true, "models": {...}, "warmup": {...}}
```

---

## 🔮 Future Scope

### AI/ML Enhancements
- **Video Analysis:** Extend Phase 1 to process video uploads (frame sampling + temporal damage tracking)
- **Fine-tuned CLIP:** Domain-adapt CLIP on circular-economy product images for higher category accuracy
- **Damage Segmentation:** Replace YOLOv8 bounding boxes with instance segmentation (Mask R-CNN / SAM) for pixel-level damage masks
- **Multi-modal Embeddings:** Joint image+text embeddings (ImageBind / CLIP) for richer Phase 3 NGO matching
- **Carbon Model v2:** Incorporate regional grid emission factors, transport distance, end-of-life scenarios
- **Resale Time-to-Sell:** Predict not just price but expected days-on-market using survival analysis
- **Anomaly Detection:** Flag suspicious listings (stolen goods, misrepresented condition) via isolation forests

### Platform Features
- **Mobile App:** React Native / Flutter wrapper with offline-first sync (camera + local Phase 1 inference via ONNX)
- **Community Verification:** Peer-review system for donations/resale — users vouch for condition authenticity
- **Circular Credits:** Tokenized eco-credits (ERC-20 on Polygon) redeemable for discounts, NGO donations, or carbon offsets
- **B2B Marketplace:** Bulk listing API for repair shops, recyclers, refurbishers to source inventory
- **ESG Reporting:** Admin dashboard with org-level carbon avoidance, waste diversion, circularity metrics
- **AR Try-Before-Buy:** WebXR viewer for furniture/clothing — place items in your space via phone camera

### Infrastructure & Scale
- **PostgreSQL + PostGIS:** Replace SQLite for production multi-user concurrency + geospatial queries
- **Redis Cache:** Cache Phase 1–3 results by image hash (perceptual hash) for instant repeat analyses
- **Message Queue (Celery + Redis/RabbitMQ):** Offload heavy ML inference to worker pool; WebSocket progress updates
- **Model Serving (Triton / TorchServe / BentoML):** Dedicated inference endpoints with batching, GPU autoscaling
- **Vector DB (Qdrant / Pinecone / pgvector):** Semantic search over NGO descriptions, product embeddings
- **Observability:** OpenTelemetry traces, Prometheus metrics, Grafana dashboards for latency/error rates

### Data & Partnerships
- **Open Product Database:** Crowdsource verified brand/model/weight/specs — improve OCR + valuation accuracy
- **NGO API Integration:** Real-time capacity APIs (Goonj, etc.) — auto-match only when NGO has space
- **Logistics Partnerships:** Integrate Delhivery/Shadowfax/India Post APIs for pickup scheduling + carbon accounting
- **Government Schemes:** Link to EPR (Extended Producer Responsibility) portals, Swachh Bharat credits

### Research Directions
- **Life-Cycle Assessment (LCA) Automation:** Auto-generate ISO 14040-compliant LCA reports from product data
- **Circular Design Assistant:** Generative AI (Gemini/Stable Diffusion) suggests redesign for repairability/recyclability
- **Behavioral Nudges:** A/B test gamification (streaks, badges, social comparison) on long-term circular habits
- **Policy Simulation:** Agent-based model of city-wide circular flows — optimize collection routes, facility placement

---

*Contributions welcome! Open an issue or PR to discuss any of these directions.*
