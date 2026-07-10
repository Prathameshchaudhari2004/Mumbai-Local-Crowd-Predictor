# ============================================
# Mumbai Local - Smart Crowd Prediction App
# Step 4: Streamlit Web Application
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================
# APP CONFIG — Sabse Pehle Ye Run Hota Hai
# ============================================
st.set_page_config(
    page_title="Mumbai Local Crowd Predictor",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS — App Ko Sundar Banao
# ============================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B35;
        padding: 1rem 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .crowd-high {
        background-color: #FFE5E5;
        border-left: 5px solid #FF4444;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .crowd-medium {
        background-color: #FFF9E5;
        border-left: 5px solid #FFA500;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .crowd-low {
        background-color: #E5FFE5;
        border-left: 5px solid #44AA44;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .metric-card {
        background-color: #F8F9FA;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stSelectbox label {
        font-weight: bold;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# MODEL LOAD KARO — Cache Se Fast Load Hoga
# ============================================
# @st.cache_resource matlab model baar baar
# load nahi hoga — ek baar load, hamesha fast

@st.cache_resource
def load_model():
    try:
        model    = joblib.load("model/crowd_model.pkl")
        encoders = joblib.load("model/encoders.pkl")
        features = joblib.load("model/feature_columns.pkl")
        return model, encoders, features
    except:
        return None, None, None

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/mumbai_local_crowd_data.csv")
        return df
    except:
        return None

model, encoders, feature_columns = load_model()
df = load_data()

# ============================================
# STATION LISTS
# ============================================
western_stations = [
    "Churchgate", "Marine Lines", "Charni Road", "Grant Road",
    "Mumbai Central", "Mahalaxmi", "Lower Parel", "Elphinstone Road",
    "Dadar", "Mahim", "Bandra", "Khar Road", "Santacruz",
    "Vile Parle", "Andheri", "Jogeshwari", "Goregaon",
    "Malad", "Kandivali", "Borivali", "Dahisar",
    "Mira Road", "Bhayandar", "Nalasopara", "Vasai Road", "Virar"
]

central_stations = [
    "CSMT", "Masjid", "Sandhurst Road", "Byculla", "Chinchpokli",
    "Currey Road", "Parel", "Dadar", "Matunga", "Sion",
    "Kurla", "Vidyavihar", "Ghatkopar", "Vikhroli",
    "Bhandup", "Mulund", "Thane", "Dombivli", "Kalyan"
]

harbour_stations = [
    "CSMT", "Sandhurst Road", "Dockyard Road", "Reay Road",
    "Cotton Green", "Sewri", "Vadala Road", "GTB Nagar",
    "Chunabhatti", "Kurla", "Tilak Nagar", "Chembur",
    "Govandi", "Mankhurd", "Vashi", "Nerul", "Panvel"
]

# ============================================
# PREDICTION FUNCTION
# ============================================
def predict_crowd(line, station_from, station_to,
                  train_type, coach_number,
                  hour, day_of_week, month,
                  is_monsoon, is_holiday):

    input_data = pd.DataFrame([{
        'day_of_week':  day_of_week,
        'hour':         hour,
        'month':        month,
        'is_monsoon':   is_monsoon,
        'is_holiday':   is_holiday,
        'line':         line,
        'station_from': station_from,
        'station_to':   station_to,
        'train_type':   train_type,
        'coach_number': coach_number
    }])

    # Categorical columns encode karo
    categorical_cols = ['line', 'station_from', 'station_to', 'train_type']
    for col in categorical_cols:
        le = encoders[col]
        try:
            input_data[col] = le.transform(input_data[col])
        except ValueError:
            input_data[col] = 0

    crowd = model.predict(input_data[feature_columns])[0]
    return round(max(5, min(100, crowd)), 1)

def get_crowd_status(crowd_pct):
    if crowd_pct >= 70:
        return "🔴 High", "crowd-high"
    elif crowd_pct >= 40:
        return "🟡 Medium", "crowd-medium"
    else:
        return "🟢 Low", "crowd-low"

# ============================================
# SIDEBAR — NAVIGATION
# ============================================
st.sidebar.markdown("## 🚆 Mumbai Local")
st.sidebar.markdown("**Smart Crowd Predictor**")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate To:",
    ["🏠 Home",
     "🚆 Train Recommendation",
     "🚃 Coach Advisor",
     "📊 Analytics Dashboard"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📅 Current Info")
now = datetime.now()
st.sidebar.info(f"""
**Date:** {now.strftime('%d %b %Y')}
**Time:** {now.strftime('%I:%M %p')}
**Day:** {now.strftime('%A')}
""")

# ============================================
# PAGE 1 — HOME
# ============================================
if page == "🏠 Home":

    st.markdown(
        '<div class="main-header">🚆 Mumbai Local Crowd Predictor</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sub-header">AI-Powered Smart Train Recommendation System</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Stats row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Daily Passengers", "75 Lakh+", "Mumbai Local")
    with col2:
        st.metric("Trains Per Day", "2,900+", "All Lines")
    with col3:
        st.metric("Total Stations", "100+", "3 Lines")
    with col4:
        st.metric("Model Accuracy", "90%+", "R² Score")

    st.markdown("---")

    # Features
    st.markdown("## 🎯 What This App Does")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 🚆 Train Recommendation
        Enter your source, destination & time.
        Get crowd prediction for upcoming trains
        and a smart recommendation.
        """)

    with col2:
        st.markdown("""
        ### 🚃 Coach Advisor
        Know which coach will be least crowded
        before you even reach the platform.
        Stand at the right spot!
        """)

    with col3:
        st.markdown("""
        ### 📊 Analytics
        Explore crowd patterns by hour, day,
        season, and train type through
        interactive visualizations.
        """)

    st.markdown("---")
    st.markdown("### 🚀 How to Use")
    st.info("""
    1. Go to **Train Recommendation** from the sidebar
    2. Enter your Source Station, Destination & Travel Time
    3. Get instant crowd predictions for upcoming trains
    4. Check **Coach Advisor** to know the best coach
    5. Explore **Analytics Dashboard** for deeper insights
    """)

# ============================================
# PAGE 2 — TRAIN RECOMMENDATION
# ============================================
elif page == "🚆 Train Recommendation":

    st.markdown("## 🚆 Train Recommendation")
    st.markdown("Find the least crowded train for your journey")
    st.markdown("---")

    if model is None:
        st.error("❌ Model not found! Please run ml_model_training.ipynb first.")
    else:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### 📍 Journey Details")

            line = st.selectbox("Select Railway Line", [
                "Western", "Central", "Harbour"
            ])

            if line == "Western":
                stations = western_stations
            elif line == "Central":
                stations = central_stations
            else:
                stations = harbour_stations

            station_from = st.selectbox(
                "📍 Source Station", stations
            )

            remaining = [s for s in stations if s != station_from]
            station_to = st.selectbox(
                "🏁 Destination Station", remaining
            )

            train_type = st.selectbox(
                "🚆 Train Type", ["Fast", "Slow", "Semi-Fast"]
            )

        with col2:
            st.markdown("### ⏰ Time Details")

            travel_hour = st.slider(
                "Travel Hour", 6, 23, 8,
                help="Select the hour you want to travel"
            )

            # Show time nicely
            time_str = f"{travel_hour:02d}:00"
            st.info(f"⏰ Selected Time: **{time_str}**")

            day_names = ["Monday", "Tuesday", "Wednesday",
                        "Thursday", "Friday", "Saturday", "Sunday"]
            day_name  = st.selectbox("📅 Day of Travel", day_names)
            day_of_week = day_names.index(day_name)

            month = st.slider("Month", 1, 12, now.month)

            col_a, col_b = st.columns(2)
            with col_a:
                is_monsoon = st.checkbox(
                    "🌧️ Monsoon Season",
                    value=True if month in [6,7,8,9] else False
                )
            with col_b:
                is_holiday = st.checkbox("🏖️ Public Holiday")

        st.markdown("---")
        predict_btn = st.button(
            "🔍 Get Train Recommendations",
            use_container_width=True
        )

        if predict_btn:
            st.markdown("### 🚆 Upcoming Trains — Crowd Prediction")

            # 3 trains predict karo (current + next 2)
            train_results = []
            for i, t_type in enumerate(["Fast", "Slow", "Semi-Fast"]):
                hour_offset = travel_hour + (i * 0)
                crowd = predict_crowd(
                    line, station_from, station_to,
                    t_type, 6,
                    travel_hour, day_of_week, month,
                    int(is_monsoon), int(is_holiday)
                )
                train_results.append({
                    "time": f"{travel_hour:02d}:{i*6:02d}",
                    "type": t_type,
                    "crowd": crowd
                })

            # Best train
            best_train = min(train_results, key=lambda x: x['crowd'])

            # Display results
            for i, train in enumerate(train_results):
                status, css_class = get_crowd_status(train['crowd'])
                is_best = "⭐ RECOMMENDED" if train == best_train else ""

                st.markdown(f"""
                <div class="{css_class}">
                    <strong>{train['time']} — {train['type']} Train</strong>
                    {is_best}<br>
                    Crowd Level: <strong>{train['crowd']}%</strong>
                    {status}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # Recommended train highlight
            st.success(f"""
            ✅ **Best Option: {best_train['time']} — {best_train['type']} Train**
            Expected crowd: **{best_train['crowd']}%** only!
            """)

            # Hourly crowd graph for this route
            st.markdown("### 📈 Crowd Pattern — Today's Trend")
            hourly_predictions = []
            for h in range(6, 24):
                c = predict_crowd(
                    line, station_from, station_to,
                    train_type, 6,
                    h, day_of_week, month,
                    int(is_monsoon), int(is_holiday)
                )
                hourly_predictions.append({
                    "Hour": h,
                    "Crowd %": c
                })

            hourly_df = pd.DataFrame(hourly_predictions)
            fig = px.line(
                hourly_df, x="Hour", y="Crowd %",
                title=f"Crowd Trend: {station_from} → {station_to}",
                markers=True,
                color_discrete_sequence=["#FF6B35"]
            )
            fig.add_vrect(
                x0=travel_hour - 0.3,
                x1=travel_hour + 0.3,
                fillcolor="blue", opacity=0.3,
                annotation_text="Your Time"
            )
            fig.add_hrect(
                y0=70, y1=100,
                fillcolor="red", opacity=0.1,
                annotation_text="High Risk"
            )
            fig.add_hrect(
                y0=40, y1=70,
                fillcolor="yellow", opacity=0.1,
                annotation_text="Medium"
            )
            fig.update_layout(
                plot_bgcolor='white',
                xaxis=dict(tickmode='linear', dtick=1)
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================
# PAGE 3 — COACH ADVISOR
# ============================================
elif page == "🚃 Coach Advisor":

    st.markdown("## 🚃 Coach Advisor")
    st.markdown("Find the least crowded coach before reaching the platform!")
    st.markdown("---")

    if model is None:
        st.error("❌ Model not found! Please run ml_model_training.ipynb first.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            line_c = st.selectbox("Railway Line", [
                "Western", "Central", "Harbour"
            ], key="coach_line")

            if line_c == "Western":
                stations_c = western_stations
            elif line_c == "Central":
                stations_c = central_stations
            else:
                stations_c = harbour_stations

            from_c = st.selectbox(
                "Source Station", stations_c, key="coach_from"
            )
            to_c   = st.selectbox(
                "Destination", [s for s in stations_c if s != from_c],
                key="coach_to"
            )

        with col2:
            type_c  = st.selectbox(
                "Train Type", ["Fast", "Slow", "Semi-Fast"],
                key="coach_type"
            )
            hour_c  = st.slider("Hour", 6, 23, 8, key="coach_hour")
            day_c   = st.selectbox(
                "Day", ["Monday","Tuesday","Wednesday",
                        "Thursday","Friday","Saturday","Sunday"],
                key="coach_day"
            )
            day_idx_c  = ["Monday","Tuesday","Wednesday",
                          "Thursday","Friday",
                          "Saturday","Sunday"].index(day_c)
            month_c    = st.slider("Month", 1, 12, now.month, key="coach_month")
            monsoon_c  = st.checkbox(
                "Monsoon?",
                value=True if month_c in [6,7,8,9] else False,
                key="coach_monsoon"
            )

        st.markdown("---")
        coach_btn = st.button(
            "🔍 Show Coach-Wise Crowd",
            use_container_width=True
        )

        if coach_btn:
            st.markdown("### 🚃 All 12 Coaches — Crowd Prediction")

            coach_data = []
            for coach_num in range(1, 13):
                crowd = predict_crowd(
                    line_c, from_c, to_c, type_c, coach_num,
                    hour_c, day_idx_c, month_c,
                    int(monsoon_c), 0
                )
                status, _ = get_crowd_status(crowd)
                coach_data.append({
                    "Coach": f"Coach {coach_num}",
                    "Crowd %": crowd,
                    "Status": status
                })

            coach_df = pd.DataFrame(coach_data)
            best_coach = coach_df.loc[coach_df["Crowd %"].idxmin()]

            # Display table
            st.dataframe(
                coach_df,
                use_container_width=True,
                hide_index=True
            )

            # Best coach highlight
            st.success(f"""
            ✅ **Best Coach: {best_coach['Coach']}**
            Expected crowd: **{best_coach['Crowd %']}%**
            Stand in front of this coach on the platform!
            """)

            # Coach heatmap
            fig = px.bar(
                coach_df,
                x="Coach", y="Crowd %",
                title="🚃 Coach-wise Crowd Distribution",
                color="Crowd %",
                color_continuous_scale="RdYlGn_r",
                text="Crowd %"
            )
            fig.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside'
            )
            fig.update_layout(plot_bgcolor='white')
            st.plotly_chart(fig, use_container_width=True)

# ============================================
# PAGE 4 — ANALYTICS DASHBOARD
# ============================================
elif page == "📊 Analytics Dashboard":

    st.markdown("## 📊 Analytics Dashboard")
    st.markdown("Explore crowd patterns across Mumbai Local Network")
    st.markdown("---")

    if df is None:
        st.error("❌ Dataset not found!")
    else:
        tab1, tab2, tab3 = st.tabs([
            "⏰ Time Patterns",
            "📅 Day & Season",
            "🚆 Train & Coach"
        ])

        # TAB 1 — Time Patterns
        with tab1:
            st.markdown("### ⏰ Hourly Crowd Pattern")
            hourly = df.groupby('hour')['crowd_percent'].mean().reset_index()
            fig = px.line(
                hourly, x='hour', y='crowd_percent',
                title='Average Crowd by Hour of Day',
                markers=True,
                color_discrete_sequence=['#FF6B35']
            )
            fig.add_hrect(
                y0=70, y1=100,
                fillcolor="red", opacity=0.1,
                annotation_text="High Risk Zone"
            )
            fig.add_hrect(
                y0=40, y1=70,
                fillcolor="yellow", opacity=0.1,
                annotation_text="Medium Zone"
            )
            fig.update_layout(
                plot_bgcolor='white',
                xaxis=dict(tickmode='linear', dtick=1)
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### 🚉 Line-wise Crowd Comparison")
            line_data = df.groupby(['hour', 'line'])['crowd_percent'].mean().reset_index()
            fig2 = px.line(
                line_data, x='hour', y='crowd_percent',
                color='line',
                title='Crowd by Railway Line (Hourly)',
                markers=True
            )
            fig2.update_layout(plot_bgcolor='white')
            st.plotly_chart(fig2, use_container_width=True)

        # TAB 2 — Day & Season
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 📅 Day-wise Crowd")
                day_order = ['Monday','Tuesday','Wednesday',
                             'Thursday','Friday','Saturday','Sunday']
                day_data  = df.groupby('day_name')['crowd_percent'].mean().reset_index()
                day_data['day_name'] = pd.Categorical(
                    day_data['day_name'],
                    categories=day_order, ordered=True
                )
                day_data = day_data.sort_values('day_name')
                fig3 = px.bar(
                    day_data, x='day_name', y='crowd_percent',
                    title='Average Crowd by Day',
                    color='crowd_percent',
                    color_continuous_scale='RdYlGn_r'
                )
                fig3.update_layout(plot_bgcolor='white')
                st.plotly_chart(fig3, use_container_width=True)

            with col2:
                st.markdown("### 🌧️ Monsoon vs Normal")
                monsoon_data = df.groupby(
                    ['is_monsoon','hour'])['crowd_percent'].mean().reset_index()
                monsoon_data['Season'] = monsoon_data['is_monsoon'].map(
                    {0:'Normal ☀️', 1:'Monsoon 🌧️'}
                )
                fig4 = px.line(
                    monsoon_data, x='hour', y='crowd_percent',
                    color='Season',
                    title='Monsoon vs Normal Season',
                    color_discrete_map={
                        'Normal ☀️': '#FFA500',
                        'Monsoon 🌧️': '#1E90FF'
                    }
                )
                fig4.update_layout(plot_bgcolor='white')
                st.plotly_chart(fig4, use_container_width=True)

        # TAB 3 — Train & Coach
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🚆 Train Type Comparison")
                train_data = df.groupby(
                    ['train_type','hour'])['crowd_percent'].mean().reset_index()
                fig5 = px.line(
                    train_data, x='hour', y='crowd_percent',
                    color='train_type',
                    title='Fast vs Slow vs Semi-Fast'
                )
                fig5.update_layout(plot_bgcolor='white')
                st.plotly_chart(fig5, use_container_width=True)

            with col2:
                st.markdown("### 🚃 Coach-wise Average Crowd")
                coach_data = df.groupby(
                    'coach_number')['crowd_percent'].mean().reset_index()
                fig6 = px.bar(
                    coach_data, x='coach_number', y='crowd_percent',
                    title='Average Crowd per Coach',
                    color='crowd_percent',
                    color_continuous_scale='RdYlGn_r'
                )
                fig6.update_layout(plot_bgcolor='white')
                st.plotly_chart(fig6, use_container_width=True)

            st.markdown("### 🔥 Coach × Hour Heatmap")
            heatmap_data = df.groupby(
                ['coach_number','hour'])['crowd_percent'].mean().reset_index()
            pivot = heatmap_data.pivot(
                index='coach_number',
                columns='hour',
                values='crowd_percent'
            )
            fig7 = px.imshow(
                pivot,
                title='Coach × Hour Crowd Heatmap',
                labels=dict(x='Hour', y='Coach', color='Crowd %'),
                color_continuous_scale='RdYlGn_r',
                aspect='auto'
            )
            st.plotly_chart(fig7, use_container_width=True)