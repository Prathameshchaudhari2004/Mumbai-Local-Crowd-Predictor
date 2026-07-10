<div align="center">

# 🚆 Mumbai Local Crowd Predictor

### *Because guessing which train to board shouldn't be a daily gamble.*

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-189AB4?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=FF6B35&center=true&vCenter=true&width=600&lines=AI-Powered+Train+Crowd+Prediction;Right+Train.+Right+Coach.+Right+Time.;Built+for+7.5+Million+Daily+Commuters+%F0%9F%9A%86" alt="Typing SVG" />

</div>

---

## 😤 The Problem (That Every Mumbaikar Knows)

You're standing at Borivali station. It's 8:45 AM. Three trains are about to arrive.

- **Which one will be less crowded?**
- **Which coach should you stand in front of?**
- **Is it worth waiting 7 minutes for the next one?**

Right now? You just *guess*. And you're almost always wrong.

> 7.5 million people travel Mumbai Local every single day — more than the entire population of London. Yet not one of them has access to real-time crowd intelligence. This project changes that.

---

## 💡 What This Project Does

An end-to-end **Machine Learning system** that predicts crowd levels across Mumbai Local trains — so passengers can make smarter travel decisions before even reaching the platform.

```
You enter  →  Source Station + Destination + Travel Time
You get    →  Which train to take + Which coach to board
```

### Three Core Features

| Feature | What it does |
|--------|-------------|
| 🚆 **Train Recommendation** | Predicts crowd % for upcoming trains and recommends the least crowded one |
| 🚃 **Coach Advisor** | Shows crowd prediction for all 12 coaches — so you stand at the right spot |
| 📊 **Analytics Dashboard** | Interactive visualizations of crowd patterns by hour, day, season & route |

---

## 🛠️ Tech Stack

```
Data Generation  →  Python (NumPy, Pandas)
ML Models        →  Scikit-learn, XGBoost
Web App          →  Streamlit
Visualizations   →  Plotly
Model Storage    →  Joblib (.pkl files)
```

---

## 🤖 Machine Learning Pipeline

### Dataset
- **7,09,560 rows** of synthetic crowd data
- Generated using real Mumbai Local domain knowledge:
  - Rush hour patterns (8–10 AM, 6–9 PM)
  - Day-of-week trends (Monday highest, Sunday lowest)
  - Monsoon effect (+18% crowd during June–September)
  - Fast vs Slow train behavior
  - Coach-wise distribution patterns

> *Real crowd data from Mumbai Railway is not publicly available. Synthetic data generation is a standard ML practice — used by companies like Netflix, Tesla, and major healthcare AI systems when real data is restricted or unavailable.*

### Models Trained & Compared

| Model | R² Score | MAE |
|-------|----------|-----|
| Linear Regression | Baseline | — |
| Decision Tree | — | — |
| **Random Forest** ✅ | **90%+** | **~3-4%** |
| Gradient Boosting | — | — |
| XGBoost | — | — |

> Best model selected automatically based on R² Score — no manual guessing.

### Key Insights from EDA
- 🕐 **Peak Hours:** 8 AM and 7 PM are the most crowded
- 📅 **Busiest Day:** Monday (start of work week)
- 🚆 **Fast Trains** are 15% more crowded than Slow trains
- 🌧️ **Monsoon** adds ~18% extra crowd (people avoid roads)
- 🚃 **Coaches 5–8** are most crowded; **Coach 1 & 12** are best

---

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/Prathameshchaudhari2004/mumbai-local-crowd-predictor.git
cd mumbai-local-crowd-predictor
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate the Dataset
```bash
python generate_data.py
```

### 4. Train the ML Model
Open and run all cells in:
```
ml_model_training.ipynb
```

### 5. Launch the Web App
```bash
streamlit run app.py
```

Open your browser → `http://localhost:8501`

---

## 📁 Project Structure

```
mumbai-local-crowd-predictor/
│
├── 📂 data/
│   └── mumbai_local_crowd_data.csv     # 7 Lakh+ records
│
├── 📂 model/
│   ├── crowd_model.pkl                  # Trained ML model
│   ├── encoders.pkl                     # Label encoders
│   └── feature_columns.pkl             # Feature order
│
├── 📓 generate_data.py                  # Synthetic data generation
├── 📓 eda_analysis.ipynb               # Exploratory Data Analysis
├── 📓 ml_model_training.ipynb          # Model training & comparison
├── 🌐 app.py                           # Streamlit web application
├── 📋 requirements.txt
├── 🚫 .gitignore
└── 📖 README.md
```

---

## 📊 App Preview

```
🏠 Home            →  Project overview + key stats
🚆 Train Advisor   →  Enter route & time → get recommendations
🚃 Coach Advisor   →  See all 12 coaches crowd prediction
📊 Analytics       →  Interactive charts & crowd patterns
```

---

## 🎯 Why This Project Matters

Mumbai Local is not just a train. It's the lifeline of an entire city.

Every day, people get injured in the rush. Shirts get torn. Productivity drops. Mental health suffers. And all of it — because **no one knows which train will be less crowded**.

This project is a small step toward fixing that with data and machine learning.

---

## 🔮 Future Scope

- [ ] Real-time data integration via Railway APIs
- [ ] Mobile-friendly PWA version
- [ ] CCTV-based Computer Vision crowd detection
- [ ] WhatsApp bot for crowd alerts
- [ ] Integration with Google Maps for end-to-end journey planning

---

## 👨‍💻 About the Author

**Prathamesh Chaudhari**
B.Tech Information Technology — NMIMS University (Class of 2027)

Passionate about building ML systems that solve real-world problems —
not just ones that look good in Jupyter notebooks.

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Prathameshchaudhari2004)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/YOUR_LINKEDIN)

---

<div align="center">

*If this helped you think about Mumbai Local differently — give it a ⭐*

**Right Train. Right Coach. Right Time. 🚆**

</div>
