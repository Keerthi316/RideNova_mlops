# 🚀 RideNova  
> ⚡ AI-Powered Electric Scooter Price Optimization System

---

## 📌 Overview

**RideNova** is a full-stack AI-driven platform that helps optimize electric scooter pricing using real-world market data.

It not only predicts the **optimal price**, but also:
- 📈 Estimates demand
- 📊 Simulates price vs demand
- 💡 Suggests feature upgrades to increase product value

---

## 🎯 Problem Statement

Pricing electric scooters is complex due to:

- Varying specifications (battery, range, power)
- Competitive market dynamics
- Customer expectations and features

RideNova provides a **data-driven solution** to make smarter pricing and product decisions.

---

## 🧠 Key Features

- 🔍 Web scraping from BikeDekho (Selenium)
- ☁️ Cloud database (MongoDB Atlas)
- 🧹 Data cleaning & feature engineering
- 🤖 ML model using **CatBoost Regressor**
- 📉 Price vs Demand simulation engine
- 💡 Feature upgrade recommendations
- 🖥️ Interactive React dashboard

---

## 🏗️ System Architecture


Web Scraper (Selenium)
↓
MongoDB Atlas
↓
Data Cleaning & Feature Engineering
↓
ML Model (CatBoost)
↓
Simulation Engine
↓
Frontend Dashboard (React)


---

## ⚙️ Tech Stack

### 🔹 Backend & ML
- Python  
- CatBoost  
- Pandas, NumPy  

### 🔹 Scraping
- Selenium  
- Undetected ChromeDriver  

### 🔹 Database
- MongoDB Atlas  

### 🔹 Frontend
- React.js  
- Tailwind CSS  
- Chart.js / Recharts  

---

## 📄 Modules

### 1️⃣ Data Collection
- Scrapes scooter data (price, specs, features)
- Uses XPath-based extraction
- Anti-blocking strategies implemented

---

### 2️⃣ Data Storage
- MongoDB Atlas (`ev_pricing`)
- Collection: `scooters_raw`
- Upsert to prevent duplicates

---

### 3️⃣ Data Cleaning & Feature Engineering
- Converts raw data into ML-ready format
- Engineered features:
  - `efficiency`
  - `price_per_km`
  - `charging_speed`

---

### 4️⃣ Machine Learning (CatBoost)
- Uses **CatBoost Regressor**
- Handles structured data efficiently
- Evaluated using RMSE & R²

---

### 5️⃣ Simulation Engine


User Input
↓
Generate Price Range
↓
Predict Demand
↓
Analyze Feature Impact
↓
Suggest Improvements
↓
Return Results


Outputs:
- 📊 Price vs Demand curve  
- 💰 Optimal price  
- 📈 Profit estimation  

---

### 💡 Feature Optimization (Unique)

RideNova suggests:

> “What features should be added to increase price?”

Example:
- 🔋 Increase battery → +₹12,000  
- 🛑 Add ABS → +₹5,000  
- 🧭 Add Navigation → +₹4,000  

---

### 6️⃣ Frontend Dashboard

- Input scooter specifications  
- View predicted price & demand  
- Visualize demand curve  
- Explore feature upgrade suggestions  

---


Outputs:
- Price vs Demand graph  
- Optimal price  
- Demand estimation  

---

### 💡 Feature Optimization (Unique)

System suggests how to increase price:

Example:
- Increase battery → +₹12,000  
- Add ABS → +₹5,000  
- Add Navigation → +₹4,000  

---

### 6. Frontend

- Input scooter specs  
- View price & demand  
- See demand graph  
- Get feature suggestions  

---

## 📊 Example Output

```json
{
  "recommended_price": 105000,
  "expected_demand": 7200,
  "suggestions": [
    "Increase battery capacity",
    "Add ABS",
    "Add Navigation"
  ]
}

## 🚀 Setup

Clone repo
```bash
git clone https://github.com/your-username/ridenova.git
cd ridenova

##Install dependencies
pip install -r requirements.txt

##Run scraper
python scraper.py

##Train model
python train_model.py

##Run backend
python app.py

## Run frontend
cd frontend
npm install
npm start
