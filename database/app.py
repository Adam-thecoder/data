import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Data", page_icon="📊", layout="centered")

# Helper function to load and save CSVs
def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame()

def save_csv(df, path):
    df.to_csv(path, index=False)

# Reusable function for each dataset section
def display_dataset(label, path):
    st.subheader(label)
    df = load_csv(path)

    # Editable data table
    with st.expander("Data list"):
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    # Section to add a new row
    with st.expander("Add new row"):
        if df.empty:
            st.info("CSV must have at least one column to add rows.")
        else:
            new_row = {}
            for col in df.columns:
                dtype = df[col].dtype
                unique_key = f"{label}_{col}"
                if dtype == "int64":
                    new_row[col] = st.number_input(col, step=1, key=unique_key)
                elif dtype == "float64":
                    new_row[col] = st.number_input(col, format="%.2f", key=unique_key)
                else:
                    new_row[col] = st.text_input(col, key=unique_key)

            if st.button(f"Add new {label.lower()} row"):
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_csv(df, path)
                st.success("Row added! Refresh the page to see changes.")

    # Save edited data
    if st.button(f"Save {label.lower()} data"):
        save_csv(edited_df, path)
        st.success("Changes saved to CSV.")

# List of datasets to manage
datasets = {
    "Compressor": "database/csv/compressor.csv",
    "Evaporator coil": "database/csv/evaporator_coil.csv",
    "Condensor coil": "database/csv/condensor_coil.csv",
    "Blower motor": "database/csv/blower_motor.csv",
    "Radaitor motor": "database/csv/radiator_motor.csv",
    "Air filter": "database/csv/air_filter.csv"
}

# Display all dataset sections
for label, path in datasets.items():
    display_dataset(label, path)
