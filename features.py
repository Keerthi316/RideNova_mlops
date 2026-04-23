import pandas as pd
import os

# ==============================
# FILE PATHS
# ==============================
INPUT_FILE = "final_scooters.xlsx"

# ==============================
# LOAD DATA
# ==============================
df = pd.read_excel(INPUT_FILE)

print("Columns in dataset:", df.columns.tolist())

# ==============================
# CLEAN DATA
# ==============================

# Remove unwanted columns like 'Unnamed: 2'
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# Columns to convert to numeric
numeric_cols = [
    "range_km",
    "motor_power_kw",
    "top_speed_kmph",
    "battery_kwh",
    "charging_time_hr",
    "weight_kg",
    "rating",
    "load_carrying_capacity",
    "review_count",
    "price"
]

# Convert to numeric safely
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Fill only numeric columns with 0
df[numeric_cols] = df[numeric_cols].fillna(0)

# ==============================
# FEATURE ENGINEERING
# ==============================

# Performance score
df["performance_score"] = (
    df["range_km"] * 0.4 +
    df["motor_power_kw"] * 20 +
    df["top_speed_kmph"] * 0.3
).round(2)

# Usage type (vectorized - faster)
df["usage_type"] = 4  # default = long ride

df.loc[df["range_km"] < 180, "usage_type"] = 3
df.loc[df["range_km"] < 100, "usage_type"] = 2
df.loc[df["motor_power_kw"] > 6, "usage_type"] = 1

# ==============================
# SAVE FILE (ROBUST)
# ==============================

paths_to_try = [
    "final_scooters_updated.xlsx",
    "output.xlsx",
    r"C:\Users\Keerthi\Desktop\final_scooters_updated.xlsx"
]

saved = False

for path in paths_to_try:
    try:
        df.to_excel(path, index=False)
        print(f"✅ File saved successfully at: {path}")
        saved = True
        break
    except PermissionError:
        print(f"❌ Permission denied for: {path}")

if not saved:
    print("\n🚨 ERROR: Could not save file anywhere.")
    print("👉 Close Excel / Run as Administrator / Change folder")

# ==============================
# DEBUG INFO
# ==============================

print("\nData types after cleaning:\n", df.dtypes)
print("\nPreview:\n", df.head())