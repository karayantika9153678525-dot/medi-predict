import streamlit as st
import requests
import sqlite3
import hashlib
import pickle
import numpy as np

st.set_page_config(
    page_title="Multiple Disease Prediction System",
    page_icon="🩺",
    layout="wide"
)

# ---------- DATABASE ----------
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

# ---------- LOAD MODELS ----------
with open("Models/diabetes_model.pkl", "rb") as f:
    diabetes_model = pickle.load(f)

with open("Models/diabetes_scaler.pkl", "rb") as f:
    diabetes_scaler = pickle.load(f)

with open("Models/heart_disease_model.pkl", "rb") as f:
    heart_model = pickle.load(f)

with open("Models/heart_scaler.pkl", "rb") as f:
    heart_scaler = pickle.load(f)

# ---------- AUTH ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup_user(username, password):
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )
    return cursor.fetchone()

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "messages" not in st.session_state:
    st.session_state.messages = [
        ("bot", "Hello 👋 I'm your AI Health Assistant. How can I help you today?")
    ]

# ---------- LOGIN PAGE ----------
def login_page():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
    }

    header {
        visibility: hidden;
    }

    .login-card {
        max-width: 460px;
        margin: auto;
        margin-top: 70px;
        padding: 35px;
        border-radius: 25px;
        background: rgba(255,255,255,0.25);
        backdrop-filter: blur(18px);
        box-shadow: 0px 20px 45px rgba(0,0,0,0.25);
        border: 1px solid rgba(255,255,255,0.4);
    }

    .logo-box {
        background: rgba(255,255,255,0.85);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
    }

    .login-title {
        font-size: 34px;
        font-weight: 900;
        color: #111827;
    }

    .login-subtitle {
        color: #374151;
        font-size: 15px;
    }

    label {
        color: white !important;
        font-weight: 700 !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: white !important;
        font-weight: bold;
    }

    .stTextInput input {
        background: white !important;
        color: #111827 !important;
        border-radius: 10px !important;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #4f46e5, #9333ea);
        color: white !important;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    st.markdown("""
    <div class="logo-box">
        <div class="login-title">🩺 MEDI PREDICT</div>
        <div class="login-subtitle">AI Powered Health Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if username == "" or password == "":
                st.warning("Please fill all fields")
            elif login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        new_username = st.text_input("Create Username", key="signup_username")
        new_password = st.text_input("Create Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

        if st.button("Create Account"):
            if new_username == "" or new_password == "" or confirm_password == "":
                st.warning("Please fill all fields")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            elif signup_user(new_username, new_password):
                st.success("Account created successfully. Now login.")
            else:
                st.error("Username already exists")

    st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    login_page()
    st.stop()

# ---------- MAIN CSS ----------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: #071126;
}

.sidebar-title {
    color: white;
    font-size: 28px;
    font-weight: bold;
    padding: 20px 0;
}

.sidebar-subtitle {
    color: #b8c4d6;
    font-size: 14px;
    margin-bottom: 35px;
}

.health-box {
    margin-top: 40px;
    background: #101b2d;
    color: white;
    text-align: center;
    padding: 20px;
    border-radius: 12px;
}

.main-title {
    font-size: 36px;
    font-weight: 800;
    color: #101827;
}

.subtitle {
    color: #6b7280;
    font-size: 15px;
    margin-bottom: 25px;
}

.form-box {
    background: white;
    padding: 35px;
    border-radius: 15px;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.08);
}

.chat-header {
    background: linear-gradient(135deg, #4f46e5, #6d48d9);
    color: white;
    padding: 22px;
    border-radius: 14px 14px 0 0;
    font-weight: bold;
    font-size: 20px;
}

.chat-box {
    background: white;
    height: 420px;
    border: 1px solid #e5e7eb;
    padding: 18px;
    overflow-y: auto;
}

.bot-message {
    background: #eef0f4;
    color: #111827;
    padding: 13px;
    border-radius: 12px;
    margin-bottom: 12px;
    width: fit-content;
    max-width: 90%;
}

.user-message {
    background: #4f46e5;
    color: white;
    padding: 13px;
    border-radius: 12px;
    margin-left: auto;
    margin-bottom: 12px;
    width: fit-content;
    max-width: 90%;
}

/* Sidebar radio menu */
[data-testid="stSidebar"] .stRadio {
    background: white;
    padding: 18px;
    border-radius: 8px;
}

[data-testid="stSidebar"] .stRadio label {
    color: #111827 !important;
    font-weight: 600;
    padding: 8px;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    margin-bottom: 12px;
}

.stButton > button {
    width: 100%;
    background-color: #f3f4f6;
    border: none;
    padding: 10px;
}

.stButton > button:hover {
    background-color: #4f46e5;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown('<div class="sidebar-title">🩺 MEDI PREDICT</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">AI Health Dashboard</div>', unsafe_allow_html=True)

    st.success(f"Logged in as {st.session_state.username}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    page = st.radio(
        "Navigation",
        [
            "🩸 Diabetes Prediction",
            "♡ Heart Disease Prediction",
            "🧮 BMI Calculator",
            "🍎 Diet Recommendation",
            "ⓘ About Project"
        ],
        label_visibility="collapsed"
    )

    st.markdown("""
    <div class="health-box">
        🌿 Stay Healthy,<br>Stay Happy
    </div>
    """, unsafe_allow_html=True)

# ---------- MAIN LAYOUT ----------
left, right = st.columns([3.2, 1])

with left:
    st.markdown('<div class="main-title">Multiple Disease Prediction System</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI Based System to Predict Multiple Diseases and Provide Health Assistance</div>', unsafe_allow_html=True)

    search = st.text_input("", placeholder="Search or ask anything...")

    st.markdown('<div class="form-box">', unsafe_allow_html=True)

    # ---------- DIABETES PAGE ----------
    if page == "🩸 Diabetes Prediction":
        st.markdown("## 🩸 Diabetes Prediction Using ML")
        st.write("Enter patient details below:")

        c1, c2, c3 = st.columns(3)

        with c1:
            pregnancies = st.number_input("Pregnancies", min_value=0, value=1)
            skin = st.number_input("Skin Thickness", min_value=0, value=20)
            dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, value=0.30)

        with c2:
            glucose = st.number_input("Glucose Level", min_value=0, value=95)
            insulin = st.number_input("Insulin Level", min_value=0, value=85)
            age = st.number_input("Age", min_value=1, value=25)

        with c3:
            bp = st.number_input("Blood Pressure", min_value=0, value=70)
            bmi = st.number_input("BMI", min_value=0.0, value=24.00)

        if st.button("Predict Diabetes"):
            input_data = np.array([[pregnancies, glucose, bp, skin, insulin, bmi, dpf, age]])
            scaled_data = diabetes_scaler.transform(input_data)
            prediction = diabetes_model.predict(scaled_data)

            try:
                probability = diabetes_model.predict_proba(scaled_data)[0][1] * 100
                st.info(f"Prediction confidence: {probability:.2f}%")
            except:
                pass

            if prediction[0] == 1:
                st.error("⚠️ The patient is likely to have diabetes.")
            else:
                st.success("✅ The patient is not likely to have diabetes.")

    # ---------- HEART PAGE ----------
    elif page == "♡ Heart Disease Prediction":
        st.markdown("## ❤️ Heart Disease Prediction Using ML")
        st.write("Enter patient details below:")

        c1, c2, c3 = st.columns(3)

        with c1:
            heart_age = st.number_input("Age", min_value=1, max_value=120, value=45)
            sex = st.selectbox("Sex", ["Female", "Male"])
            cp = st.selectbox("Chest Pain Type", [0, 1, 2, 3])
            trestbps = st.number_input("Resting Blood Pressure", min_value=50, value=120)

        with c2:
            chol = st.number_input("Cholesterol", min_value=100, value=200)
            fbs = st.selectbox("Fasting Blood Sugar > 120", [0, 1])
            restecg = st.selectbox("Rest ECG", [0, 1, 2])
            thalach = st.number_input("Maximum Heart Rate", min_value=50, value=150)

        with c3:
            exang = st.selectbox("Exercise Induced Angina", [0, 1])
            oldpeak = st.number_input("Oldpeak", min_value=0.0, value=1.0)
            slope = st.selectbox("Slope", [0, 1, 2])
            ca = st.selectbox("Major Vessels", [0, 1, 2, 3, 4])
            thal = st.selectbox("Thal", [0, 1, 2, 3])

        if st.button("Predict Heart Disease"):
            sex_value = 1 if sex == "Male" else 0

            heart_input = np.array([[
                heart_age, sex_value, cp, trestbps, chol, fbs,
                restecg, thalach, exang, oldpeak, slope, ca, thal
            ]])

            scaled_heart = heart_scaler.transform(heart_input)
            heart_prediction = heart_model.predict(scaled_heart)

            try:
                heart_probability = heart_model.predict_proba(scaled_heart)[0][1] * 100
                st.info(f"Prediction confidence: {heart_probability:.2f}%")
            except:
                pass

            if heart_prediction[0] == 1:
                st.error("⚠️ The patient is likely to have heart disease.")
            else:
                st.success("✅ The patient is not likely to have heart disease.")

    # ---------- BMI PAGE ----------
    elif page == "🧮 BMI Calculator":
        st.markdown("## 🧮 BMI Calculator")

        height = st.number_input("Height in cm", min_value=50.0, value=160.0)
        weight = st.number_input("Weight in kg", min_value=10.0, value=55.0)

        if st.button("Calculate BMI"):
            bmi_value = weight / ((height / 100) ** 2)

            st.success(f"Your BMI is {bmi_value:.2f}")

            if bmi_value < 18.5:
                st.warning("You are underweight.")
            elif 18.5 <= bmi_value < 25:
                st.success("You have normal weight.")
            elif 25 <= bmi_value < 30:
                st.warning("You are overweight.")
            else:
                st.error("You are obese.")

    # ---------- DIET PAGE ----------
    elif page == "🍎 Diet Recommendation":
        st.markdown("## 🍎 Diet Recommendation")

        goal = st.selectbox(
            "Choose your goal",
            ["Diabetes Friendly Diet", "Heart Healthy Diet", "Weight Loss Diet", "General Healthy Diet"]
        )

        if goal == "Diabetes Friendly Diet":
            st.info("Eat whole grains, vegetables, dal, lean protein, nuts, and avoid sugary drinks.")
        elif goal == "Heart Healthy Diet":
            st.info("Eat fruits, vegetables, oats, fish/lean protein, nuts, and reduce oily/fried foods.")
        elif goal == "Weight Loss Diet":
            st.info("Focus on calorie control, protein, vegetables, fruits, and avoid junk food.")
        else:
            st.info("Eat balanced meals with carbs, protein, vegetables, fruits, and enough water.")

    # ---------- ABOUT PAGE ----------
    elif page == "ⓘ About Project":
        st.markdown("## ⓘ About Project")
        st.write("""
        **Medi Predict** is an AI-based multiple disease prediction system.

        Features:
        - Diabetes prediction using ML
        - Heart disease prediction using ML
        - BMI calculator
        - Diet recommendation
        - AI health assistant chatbot
        - Login and signup system
        """)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- CHATBOT ----------
with right:
    st.markdown('<div class="chat-header">🤖 AI Health Assistant<br><small>Always here to help</small></div>', unsafe_allow_html=True)

    st.markdown('<div class="chat-box">', unsafe_allow_html=True)

    for sender, msg in st.session_state.messages:
        if sender == "bot":
            st.markdown(f'<div class="bot-message">{msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="user-message">{msg}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    user_msg = st.text_input("Type your message...", key="chat_input")

    if st.button("Send"):
        if user_msg:
            st.session_state.messages.append(("user", user_msg))

            try:
                response = requests.post(
                    "http://127.0.0.1:8001/chat",
                    json={"question": user_msg}
                )

                if response.status_code == 200:
                    bot_reply = response.json()["response"]
                else:
                    bot_reply = "Server error. Please check FastAPI."

            except:
                bot_reply = "FastAPI is not running. Start backend first."

            st.session_state.messages.append(("bot", bot_reply))
            st.rerun()