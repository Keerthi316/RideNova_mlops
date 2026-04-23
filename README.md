# 🚀 RideNova: AI-Powered EV Price Optimization

RideNova is an end-to-end MLOps project designed to scrape, analyze, and predict the market value of electric scooters in the Indian market. It utilizes machine learning to provide accurate price estimations based on technical specifications and market features.

---

## 🏗️ System Architecture

1.  **Data Acquisition**: A robust scraper using Selenium and BeautifulSoup to extract real-time data from automotive portals.
2.  **Feature Engineering**: Data cleaning and enrichment pipeline that calculates performance metrics and usage classifications.
3.  **Inference Engine**: A FastAPI-based backend serving a pre-trained **CatBoost** regression model.
4.  **User Interface**: A modern, responsive web frontend for interactive price prediction.

---

## 📂 Project Structure

```text
RideNova_mlops/
├── backend/
│   ├── main.py                 # FastAPI Prediction Service
│   ├── catboost_model.pkl      # Trained CatBoost Regressor
│   └── model_columns.pkl       # Feature alignment metadata
├── frontend/
│   ├── ev-landing.html         # Project Landing Page
│   └── ev-price-predictor.html # Interactive Prediction UI
├── newscraper.py               # Selenium-based Web Scraper
├── features.py                 # Data Cleaning & Feature Engineering
└── final_scooters.xlsx         # Raw Dataset
```

---

## 🛠️ Tech Stack

-   **Backend**: Python, FastAPI, Joblib
-   **Machine Learning**: CatBoost, Pandas, Scikit-learn
-   **Web Scraping**: Selenium, BeautifulSoup4
-   **Frontend**: HTML5, CSS3 (Syne & DM Sans typography), Vanilla JavaScript

---

## 🚀 Getting Started

### 1. Environment Setup
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn pandas catboost selenium beautifulsoup4 openpyxl joblib
```

### 2. Data Collection & Processing
To refresh the dataset and process features:
```bash
python newscraper.py   # Scrapes latest data to electric_scooters.csv
python features.py     # Cleans and engineers features for the model
```

### 3. Running the Backend
Start the FastAPI server:
```bash
cd backend
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### 4. Launching the Frontend
Simply open `frontend/ev-landing.html` in your browser. Ensure the backend is running to enable real-time predictions in the `ev-price-predictor.html` page.

---

## 🧠 Model Features

The prediction model evaluates several key parameters:
-   **Performance**: Battery Capacity (kWh), Range (km), Top Speed (kmph).
-   **Physical**: Motor Power (kW), Vehicle Weight (kg), Load Capacity.
-   **Convenience**: Under-seat Storage, USB Charging, Anti-theft Alarm.
-   **Derived**: Performance Score, Usage Type, Power-to-Weight ratio.

---

## 📊 Future Roadmap
- [ ] Integration with MongoDB Atlas for persistent storage.
- [ ] Automated model retraining pipeline (MLflow).
- [ ] Containerization with Docker for cloud deployment.
- [ ] Enhanced demand simulation engine.
