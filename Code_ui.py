# You are viewing creation of Akansh
import pandas as pd
import streamlit as st
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns  
import warnings
import os

# Suppress Warnings
warnings.filterwarnings("ignore")

# Page Configuration
st.set_page_config(
    page_title="EDA Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Global Theme / CSS Styling
st.markdown(
    """
    <style>
    /* Full-page gradient background */
    .stApp {
        background: linear-gradient(135deg, #0B3D91 0%, #41B3A3 60%, #F5F7FA 100%);
        background-attachment: fixed;
        color: #111827;
    }

    /* Card-like container for main content */
    .main-container {
        background: rgba(255,255,255,0.85);
        border-radius: 18px;
        padding: 24px 24px 24px 24px;
        box-shadow: 0 16px 40px rgba(0,0,0,0.16);
        margin-top: 16px;
    }

    /* Header styling */
    h1, h2, h3, h4 {
        text-align: center;
        color: #0B3140;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-bottom: 6px;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }

    .stSidebar .stButton > button {
        background-color: #0B3D91 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        font-weight: 600;
    }

    .stSidebar .stButton > button:hover {
        background-color: #28A745 !important;
        color: #ffffff !important;
        transform: scale(1.02);
    }

    .stButton>button {
        border-radius: 10px !important;
        font-weight: 600;
    }

    /* File uploader */
    .stFileUploader {
        border-radius: 14px;
        border: 1px solid rgba(0,0,0,0.12);
        padding: 14px;
        background: rgba(245, 247, 250, 0.8);
    }

    /* Table styling */
    .stDataFrame table {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 10px 20px rgba(0,0,0,0.08);
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
<div class='main-container'>
  <h1>Exploratory Data Analysis Dashboard</h1>
  <p style='text-align:center; margin-top: -10px; color: #334155; font-size: 15px;'>Created by Akansh Tyagi</p>
  <h4>Upload your dataset to explore it with charts, heatmaps, and cross-tabulations.</h4>
</div>
""", unsafe_allow_html=True)

# Sidebar Setup
st.sidebar.title("📌 Navigation")
st.sidebar.write("Choose a dataset and a plot type to explore your data.")

# Session State Setup
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if "default_loaded" not in st.session_state:
    st.session_state.default_loaded = False

# File Uploader
with st.sidebar.expander("1) Upload or Load Data", expanded=True):
    file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"], help="CSV or XLSX files only")

    if file is not None:
        file_extenision = os.path.splitext(file.name)[-1].lower()
        try:
            if file_extenision == ".csv":
                sep = st.text_input("CSV separator", ",")
                df = pd.read_csv(file, sep=sep)
            else:
                df = pd.read_excel(file)

            st.session_state.df = df
            st.success("✅ Dataset loaded successfully")
        except Exception as e:
            st.error(f"Error reading file: {e}")

    if st.button("Use Default Dataset") and not st.session_state.default_loaded:
        try:
            df = pd.read_csv("Visadataset.csv")
            st.session_state.df = df
            st.session_state.default_loaded = True
            st.success("✅ Default dataset loaded")
        except Exception as e:
            st.error(f"Error loading default dataset: {e}")

# Dataframe reference
df = st.session_state.df

if not df.empty:
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    st.subheader("Preview of the dataset")
    st.dataframe(df.head(10), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Helper Functions

def outli(se_co):
    va = df[se_co].values
    m = df[se_co].median()
    q1 = np.percentile(df[se_co], 25)
    q3 = np.percentile(df[se_co], 75)
    iqr = q3 - q1
    lb = q1 - (1.5 * iqr)
    ub = q3 + (1.5 * iqr)
    f = df[se_co]
    con = (va < lb) | (va > ub)
    l = np.where(con, m, f)
    return l


def chart(pl, se_co):
    if pl == "bar":
        v = df[se_co].value_counts()
        if len(v) <= 12:
            sns.countplot(data=df, x=se_co, palette="Set2")
            plt.title(se_co, fontsize=16)
            st.pyplot(plt)
            plt.clf()
    elif pl == "pie":
        data = df[se_co].value_counts()
        if len(data) <= 12:
            ke = data.keys()
            va = data.values
            plt.pie(va, labels=ke, autopct="%0.2f%%", radius=1, colors=sns.color_palette("pastel"))
            plt.title(se_co, fontsize=16)
            st.pyplot(plt)
            plt.clf()
    elif pl == "hist":
        df["bal"] = outli(se_co)
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.hist(df[se_co], color="skyblue", edgecolor="black")
        plt.title(f"{se_co} (Before Outliers)", fontsize=14)
        plt.subplot(1, 2, 2)
        plt.hist(df["bal"], color="salmon", edgecolor="black")
        plt.title(f"{se_co} (After Outliers)", fontsize=14)
        st.pyplot(plt)
        plt.clf()
        df.drop("bal", axis=1, inplace=True)
    elif pl == "dist":
        df["bal"] = outli(se_co)
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        sns.histplot(df[se_co], kde=True, color="skyblue")
        plt.title(f"{se_co} (Before Outliers)", fontsize=14)
        plt.subplot(1, 2, 2)
        sns.histplot(df["bal"], kde=True, color="salmon")
        plt.title(f"{se_co} (After Outliers)", fontsize=14)
        st.pyplot(plt)
        plt.clf()
        df.drop("bal", axis=1, inplace=True)
    elif pl == "boxplot":
        df["bal"] = outli(se_co)
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.boxplot(df[se_co])
        plt.title(f"{se_co} (Before Outliers)", fontsize=14)
        plt.subplot(1, 2, 2)
        plt.boxplot(df["bal"])
        plt.title(f"{se_co} (After Outliers)", fontsize=14)
        st.pyplot(plt)
        plt.clf()
        df.drop("bal", axis=1, inplace=True)


def heat():
    cor = df.corr(numeric_only=True)
    plt.figure(figsize=(10, 6))
    sns.heatmap(cor, annot=True, cmap="coolwarm", fmt="0.2f")
    st.pyplot(plt)
    plt.clf()


def cro(se_col1, se_col2):
    df1 = pd.crosstab(df[se_col1], df[se_col2])
    df1.plot(kind="bar", figsize=(10, 6), color=["#41B3A3", "#0B3D91"])
    plt.title(f"Cross Tabulation: {se_col1} vs {se_col2}", fontsize=16)
    plt.tight_layout()
    st.pyplot(plt)
    plt.clf()


# Plot selection
catcol = df.select_dtypes(include="object").columns
numcol = df.select_dtypes(exclude="object").columns

with st.sidebar.expander("2) Choose Plot Type", expanded=True):
    se_op = st.selectbox(
        "Choose Plot Type:",
        ["bar", "pie", "hist", "dist", "boxplot", "heatmap", "crosstab"],
    )

    if se_op == "crosstab":
        se_col1 = st.selectbox("Select Column 1:", catcol)
        se_col2 = st.selectbox("Select Column 2:", catcol)
        se_co = None
    elif se_op in ["bar", "pie"]:
        se_co = st.selectbox("Select Categorical Column:", catcol)
        se_col1 = se_col2 = None
    else:
        se_co = st.selectbox("Select Numerical Column:", numcol)
        se_col1 = se_col2 = None

    st.write("---")
    submit = st.button("Generate Plot")

if submit:
    if df.empty:
        st.error("Please upload a dataset or use the default dataset.")
    else:
        st.markdown("<div class='main-container'>", unsafe_allow_html=True)
        if se_op == "crosstab":
            cro(se_col1, se_col2)
        elif se_op == "heatmap":
            heat()
        else:
            chart(se_op, se_co)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div style='text-align:center; margin-top: 32px; color:#0B3140;'>
        <p>Special Thanks To:</p>
        <p>👨 My Father – Hamendra Tyagi | 👩 My Mother – Shalini Tyagi | 👦 My Brother – Aditya Tyagi</p>
        <p style='font-size:12px; opacity: 0.8;'>Your constant love and encouragement make everything possible 💖</p>
    </div>
    """,
    unsafe_allow_html=True,
)
