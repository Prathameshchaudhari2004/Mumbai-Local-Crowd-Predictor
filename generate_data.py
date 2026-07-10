# ============================================
# Mumbai Local - Synthetic Data Generator
# Step 1: Data Creation
# ============================================

import pandas as pd
import numpy as np
import random
import os

# Seed set karo taaki har baar same data mile
np.random.seed(42)
random.seed(42)

# ============================================
# STEP 1A: Basic Setup - Stations aur Info
# ============================================

western_line_stations = [
    "Churchgate", "Marine Lines", "Charni Road", "Grant Road",
    "Mumbai Central", "Mahalaxmi", "Lower Parel", "Elphinstone Road",
    "Dadar", "Matunga Road", "Mahim", "Bandra", "Khar Road",
    "Santacruz", "Vile Parle", "Andheri", "Jogeshwari", "Goregaon",
    "Malad", "Kandivali", "Borivali", "Dahisar", "Mira Road",
    "Bhayandar", "Nalasopara", "Vasai Road", "Virar"
]

central_line_stations = [
    "CSMT", "Masjid", "Sandhurst Road", "Byculla", "Chinchpokli",
    "Currey Road", "Parel", "Dadar", "Matunga", "Sion",
    "Kurla", "Vidyavihar", "Ghatkopar", "Vikhroli", "Kanjurmarg",
    "Bhandup", "Nahur", "Mulund", "Thane", "Kalwa",
    "Mumbra", "Diva", "Kopar", "Dombivli", "Thakurli",
    "Kalyan", "Shahad", "Ambivali", "Titwala", "Khadavli"
]

harbour_line_stations = [
    "CSMT", "Sandhurst Road", "Dockyard Road", "Reay Road",
    "Cotton Green", "Sewri", "Vadala Road", "GTB Nagar",
    "Chunabhatti", "Kurla", "Tilak Nagar", "Chembur",
    "Govandi", "Mankhurd", "Vashi", "Sanpada", "Juinagar",
    "Nerul", "Seawoods", "Belapur", "Kharghar", "Panvel"
]

lines_info = {
    "Western":  {"stations": western_line_stations, "base_crowd": 75},
    "Central":  {"stations": central_line_stations, "base_crowd": 70},
    "Harbour":  {"stations": harbour_line_stations, "base_crowd": 55}
}

train_types = ["Fast", "Slow", "Semi-Fast"]
total_coaches = 12

print("✅ Setup complete - Stations loaded")

# ============================================
# STEP 1B: Crowd Logic - Real Patterns
# ============================================

def get_time_multiplier(hour):
    """
    Hour ke hisaab se crowd multiplier decide karo.
    Real Mumbai Local pattern ke basis pe.
    """
    if 7 <= hour <= 10:      # Morning peak
        return random.uniform(0.85, 1.0)
    elif 11 <= hour <= 16:   # Afternoon - low crowd
        return random.uniform(0.30, 0.55)
    elif 17 <= hour <= 21:   # Evening peak
        return random.uniform(0.75, 0.95)
    elif 22 <= hour <= 23:   # Late night
        return random.uniform(0.15, 0.30)
    else:                    # Early morning (before 7)
        return random.uniform(0.10, 0.25)

def get_day_multiplier(day_of_week):
    """
    Day of week ke hisaab se multiplier.
    0 = Monday, 6 = Sunday
    """
    day_multipliers = {
        0: 1.00,   # Monday - highest
        1: 0.95,   # Tuesday
        2: 0.92,   # Wednesday
        3: 0.93,   # Thursday
        4: 0.97,   # Friday - second highest
        5: 0.70,   # Saturday - moderate
        6: 0.45    # Sunday - lowest
    }
    return day_multipliers[day_of_week]

def get_train_multiplier(train_type):
    """
    Fast trains mein zyada crowd hoti hai
    kyunki wo kam stations par rukti hain.
    """
    multipliers = {
        "Fast":      1.15,
        "Semi-Fast": 1.00,
        "Slow":      0.80
    }
    return multipliers[train_type]

def get_coach_multiplier(coach_number):
    """
    Middle coaches zyada crowded hote hain.
    First aur last coach thode khaali hote hain.
    """
    if coach_number in [1, 12]:        # End coaches
        return random.uniform(0.60, 0.75)
    elif coach_number in [2, 11]:      # Near end
        return random.uniform(0.75, 0.85)
    elif coach_number in [3, 4, 9, 10]: # Middle-ish
        return random.uniform(0.85, 0.95)
    else:                               # Middle (5,6,7,8)
        return random.uniform(0.90, 1.00)

def calculate_crowd(base_crowd, time_mult, day_mult, 
                    train_mult, coach_mult, 
                    is_monsoon, is_holiday):
    """
    Sabhi factors mila ke final crowd % nikalo.
    """
    crowd = base_crowd * time_mult * day_mult * train_mult * coach_mult
    
    # Monsoon mein log road se shift hote hain local pe
    if is_monsoon:
        crowd = crowd * 1.18
    
    # Holiday pe crowd kam hoti hai
    if is_holiday:
        crowd = crowd * 0.55
    
    # Random noise add karo (real world mein variation hoti hai)
    noise = random.uniform(-5, 5)
    crowd = crowd + noise
    
    # 0 se 100 ke beech rakho
    crowd = max(5, min(100, crowd))
    
    return round(crowd, 2)

print("✅ Crowd logic functions ready")

# ============================================
# STEP 1C: Data Generation - 50,000 Records
# ============================================

print("\n🔄 Data generate ho raha hai... thoda time lagega")

all_records = []

# 365 days ka data banayenge
for day_offset in range(365):
    
    # Date calculate karo
    from datetime import date, timedelta
    current_date = date(2023, 1, 1) + timedelta(days=day_offset)
    day_of_week  = current_date.weekday()  # 0=Mon, 6=Sun
    month        = current_date.month
    
    # Monsoon months (June to September)
    is_monsoon = 1 if month in [6, 7, 8, 9] else 0
    
    # Holidays (simplified - major ones)
    holiday_dates = [
        date(2023, 1, 26),   # Republic Day
        date(2023, 8, 15),   # Independence Day
        date(2023, 10, 2),   # Gandhi Jayanti
        date(2023, 10, 24),  # Diwali (approx)
        date(2023, 12, 25),  # Christmas
    ]
    is_holiday = 1 if current_date in holiday_dates else 0
    
    # Har line ke liye
    for line_name, line_data in lines_info.items():
        stations   = line_data["stations"]
        base_crowd = line_data["base_crowd"]
        
        # Har ghante ke liye (6 AM se 11 PM)
        for hour in range(6, 24):
            
            # 3 trains per hour per line (approx)
            for train_num in range(3):
                
                # Random stations pick karo
                from_idx = random.randint(0, len(stations) - 3)
                to_idx   = random.randint(from_idx + 1, len(stations) - 1)
                
                station_from = stations[from_idx]
                station_to   = stations[to_idx]
                
                # Train type
                train_type = random.choice(train_types)
                
                # Multipliers calculate karo
                time_mult  = get_time_multiplier(hour)
                day_mult   = get_day_multiplier(day_of_week)
                train_mult = get_train_multiplier(train_type)
                
                # Har coach ke liye record
                for coach in range(1, total_coaches + 1):
                    
                    coach_mult = get_coach_multiplier(coach)
                    
                    crowd_pct = calculate_crowd(
                        base_crowd, time_mult, day_mult,
                        train_mult, coach_mult,
                        is_monsoon, is_holiday
                    )
                    
                    record = {
                        "date":          str(current_date),
                        "day_of_week":   day_of_week,
                        "day_name":      current_date.strftime("%A"),
                        "hour":          hour,
                        "month":         month,
                        "is_monsoon":    is_monsoon,
                        "is_holiday":    is_holiday,
                        "line":          line_name,
                        "station_from":  station_from,
                        "station_to":    station_to,
                        "train_type":    train_type,
                        "coach_number":  coach,
                        "crowd_percent": crowd_pct
                    }
                    
                    all_records.append(record)

print(f"✅ Records generated: {len(all_records):,}")

# ============================================
# STEP 1D: Save to CSV
# ============================================

# Folder banao agar nahi hai
os.makedirs("data", exist_ok=True)

# DataFrame banao
df = pd.DataFrame(all_records)

# CSV save karo
df.to_csv("data/mumbai_local_crowd_data.csv", index=False)

print(f"\n✅ CSV saved: data/mumbai_local_crowd_data.csv")
print(f"📊 Total Rows:    {len(df):,}")
print(f"📋 Total Columns: {len(df.columns)}")
print(f"\n🔍 First 3 rows ka preview:")
print(df.head(3).to_string())
print(f"\n📈 Crowd % Stats:")
print(df["crowd_percent"].describe().round(2))