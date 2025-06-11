import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Data", page_icon="📊", layout="centered")

# Make sure the folder exists
os.makedirs("database/csv", exist_ok=True)

def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame()

def save_csv(df, path):
    try:
        df.to_csv(path, index=False)
    except Exception as e:
        st.error(f"❌ Failed to save CSV: {e}")

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

    # ✅ Save edited data
    if st.button(f"💾 Save {label} data", key=f"{label}_save"):
        try:
            if search_term:
                filtered_indices = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)].index
                df.loc[filtered_indices] = edited_df.values
            else:
                df = edited_df

            save_csv(df, path)
            st.success("Changes saved!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Failed to save data: {e}")

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

        # 🧪 Show the row to be added
        st.write("🧪 New row preview:", new_row)

        if st.button(f"➕ Add {label} row", key=f"{label}_add"):
            try:
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_csv(df, path)
                st.success("Row added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to add row: {e}")

# 🗂️ Your datasets
datasets = {
    "Compressor": "database/csv/compressor.csv",
    "Evaporator coil": "database/csv/evaporator_coil.csv",
    "Condensor coil": "database/csv/condensor_coil.csv",
    "Blower motor": "database/csv/blower_motor.csv",
    "Radiator motor": "database/csv/radiator_motor.csv",
    "Air filter": "database/csv/air_filter.csv",
    "Filter dryer receiver": "database/csv/Filter_dryer_receiver.csv",
    "Expension valve": "database/csv/Expension_valve.csv"
}

for label, path in datasets.items():
    display_dataset(label, path)
