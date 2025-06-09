import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Data", page_icon="📊", layout="centered")

def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame()

def save_csv(df, path):
    df.to_csv(path, index=False)

def display_dataset(label, path):
    st.subheader(label)

    df = load_csv(path)

    if df.empty:
        st.warning("No data found or CSV is empty.")
        return

    # 🔍 Search bar
    search_term = st.text_input(f"Search in {label}", key=f"{label}_search")
    if search_term:
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    else:
        filtered_df = df

    # ✍️ Editable data table
    with st.expander("📋 Data list"):
        edited_df = st.data_editor(
            filtered_df,
            num_rows="dynamic",
            use_container_width=True,
            key=f"{label}_editor"
        )

    # ✅ Save edited data (applies to entire dataset, not just filtered)
    if st.button(f"💾 Save {label} data", key=f"{label}_save"):
        # Re-map edited rows to original df if a search term was used
        if search_term:
            mask = df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)
            df.loc[mask] = edited_df.values
        else:
            df = edited_df

        save_csv(df, path)
        st.success("Changes saved!")

    # ➕ Add new row
    with st.expander("➕ Add new row"):
        new_row = {}
        for col in df.columns:
            dtype = df[col].dtype
            input_key = f"{label}_new_{col}"

            if dtype == "int64":
                new_row[col] = st.number_input(f"{col}", step=1, key=input_key)
            elif dtype == "float64":
                new_row[col] = st.number_input(f"{col}", format="%.2f", key=input_key)
            else:
                new_row[col] = st.text_input(f"{col}", key=input_key)

        if st.button(f"➕ Add {label} row", key=f"{label}_add"):
            try:
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_csv(df, path)
                st.success("Row added successfully! Refresh to see it.")
            except Exception as e:
                st.error(f"Failed to add row: {e}")

# 🗂️ Your datasets
datasets = {
    "Compressor": "database/csv/compressor.csv",
    "Evaporator coil": "database/csv/evaporator_coil.csv",
    "Condensor coil": "database/csv/condensor_coil.csv",
    "Blower motor": "database/csv/blower_motor.csv",
    "Radiator motor": "database/csv/radiator_motor.csv",
    "Air filter": "database/csv/air_filter.csv",
    "Filter dryer receiver": "database/csv/Filter_dryer_receiver.csv",
    "Expension valve":"database/csv/Expension_valve.csv"
}

for label, path in datasets.items():
    display_dataset(label, path)
