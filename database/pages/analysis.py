import streamlit as st
import pandas as pd
import os
import altair as alt

st.set_page_config(page_title="📊 Data Visualizer", layout="wide")
st.title("📊 Component Visual Analysis")

base_path = "database/csv"
datasets = {
    "Compressor": os.path.join(base_path, "compressor.csv"),
    "Evaporator Coil": os.path.join(base_path, "evaporator_coil.csv"),
    "Condensor Coil": os.path.join(base_path, "codensor_coil.csv"),
    "Blower Motor": os.path.join(base_path, "blower_motor.csv"),
    "Radaitor Motor": os.path.join(base_path, "radaitor_motor.csv"),
    "Air Filter": os.path.join(base_path, "air_filter.csv")
}

for label, path in datasets.items():
    st.header(f"📌 {label}")
    try:
        df = pd.read_csv(path)

        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        if not numeric_cols:
            st.warning(f"No numeric columns in {label} for visualization.")
            continue

        selected_col = st.selectbox(f"Select numeric column to plot ({label})", numeric_cols, key=label)

        chart = alt.Chart(df.reset_index()).mark_line(point=True).encode(
            x=alt.X("index:O", title="Row Number"),
            y=alt.Y(f"{selected_col}:Q", title=selected_col),
            tooltip=["index", selected_col]
        ).properties(width="container", height=300)

        st.altair_chart(chart, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Error in {label}: {e}")
