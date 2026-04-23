# RideNova: AI-Driven Price Optimization for Electric Scooters

RideNova is an end-to-end starter project for electric scooter pricing intelligence in the Indian market. It combines Selenium scraping, MongoDB-ready raw storage, feature engineering, machine learning, demand simulation, and a React dashboard.

## What Is Included

- `backend/app/scraper`: BikeDekho scraper using the XPath pattern from your screenshot
- `backend/app/storage`: MongoDB Atlas upsert support
- `backend/app/pipeline`: cleaning and feature engineering
- `backend/app/ml`: price model training and inference
- `backend/app/services`: price-vs-demand simulation and feature recommendations
- `backend/app/main.py`: FastAPI endpoints
- `frontend`: React + Vite dashboard for input, output, graph, and XPath display

## Architecture

```text
Web Scraper (Selenium)
        ↓
Raw Data Storage (MongoDB Atlas)
        ↓
Data Cleaning & Feature Engineering
        ↓
ML Model Layer
   ├── Price Prediction
   └── Demand Modeling
        ↓
Simulation Engine
        ↓
Frontend Dashboard (React)
```

## XPath Strategy Used

These selectors are already wired into the scraper:

- Bike container: `//li[@data-type='autofitmobile']`
- Bike name: `.//a[contains(@class, 'model-name')]`
- Price: `.//div[contains(@class,'price')]`
- Link: `.//a[contains(@class, 'model-name')]`

Detail extraction is handled with label-based XPath lookups so the scraper is more robust when page layouts shift.

## Backend Setup

From the project root:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API runs at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### API Endpoints

- `GET /health`
- `POST /train`
- `POST /predict`
- `POST /simulate`

### Example Request

```json
{
  "battery_kwh": 3.5,
  "range_km": 140,
  "charging_time_hr": 5.0,
  "motor_power_kw": 5.5,
  "weight_kg": 112,
  "abs": 1,
  "navigation": 1,
  "cruise_control": 0,
  "traction_control": 0,
  "rating": 4.3,
  "review_count": 980,
  "sentiment_score": 0.47,
  "target_margin": 0.18
}
```

## Scraper Setup

If you want to scrape BikeDekho and push records to MongoDB Atlas:

1. Copy `.env.example` to `.env`
2. Add your `MONGO_URI`
3. Run:

```powershell
cd backend
python run_scraper.py
```

`run_scraper.py` opens the listing page, extracts links with the screenshot XPath selectors, visits detail pages, and upserts records when MongoDB is configured.

## Frontend Setup

From [frontend](C:\Users\Kalyani\Downloads\project\RideNova\frontend):

```powershell
cmd /c npm install
cmd /c npm run dev
```

Frontend runs at [http://127.0.0.1:5173](http://127.0.0.1:5173) and is already configured to call the FastAPI backend.

## Sample Data

A starter dataset is included at [sample_scooters.csv](C:\Users\Kalyani\Downloads\project\RideNova\backend\app\data\sample_scooters.csv) so the ML pipeline works even before live scraping is connected.

## Notes

- `xgboost` is included as an optional candidate model; if unavailable, training still works with the other regressors.
- The demand model is currently a simulation-oriented heuristic on top of the value score and predicted price.
- The project is structured so you can later swap in real demand history, sentiment analysis, and more marketplaces like ZigWheels.
