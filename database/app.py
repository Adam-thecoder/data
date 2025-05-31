import streamlit as st
import pandas as pd
import io
import os

st.set_page_config(page_title="Data Manager", layout="centered")
st.title("📦 Component Data Manager")

# Define the base path for CSV files
# Change this path when switching between local and deployed
base_path = "database/csv" 
# base_path = "csv"  # Uncomment this for GitHub/Streamlit deployment

# Ensure the base directory exists
os.makedirs(base_path, exist_ok=True)

datasets = {
    "Compressor": os.path.join(base_path, "compressor.csv"),
    "Evaporator Coil": os.path.join(base_path, "evaporator_coil.csv"),
    "Condensor Coil": os.path.join(base_path, "condensor_coil.csv"),  # Fixed typo
    "Blower Motor": os.path.join(base_path, "blower_motor.csv"),
    "Radiator Motor": os.path.join(base_path, "radiator_motor.csv"),  # Fixed typo
    "Air Filter": os.path.join(base_path, "air_filter.csv")
}

for label, path in datasets.items():
    st.subheader(label)
    with st.expander(f"{label} Data"):
        df = pd.DataFrame()
        try:
            if os.path.exists(path):
                df = pd.read_csv(path)
            else:
                st.info(f"'{label}' CSV not found. Creating an empty dataset.")
                df = pd.DataFrame({"No": [], "Item Name": [], "Amount": []})

            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"💾 Save Changes to {label}", key=f"save_{label}"):
                    try:
                        cleaned_df = edited_df.copy()

                        # Fill only non-numeric columns with empty strings
                        for col in cleaned_df.columns:
                            if not pd.api.types.is_numeric_dtype(cleaned_df[col]):
                                cleaned_df[col] = cleaned_df[col].fillna("")

                        # Optional: Drop rows missing important numeric values (like 'Amount')
                        if "Amount" in cleaned_df.columns:
                            cleaned_df = cleaned_df[cleaned_df["Amount"].notna()]

                        cleaned_df.to_csv(path, index=False)
                        st.success(f"{label} data saved successfully!")
                    except Exception as save_err:
                        st.error(f"Failed to save data: {save_err}")

            with col2:
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    edited_df.to_excel(writer, index=False, sheet_name=label[:31]) 
                buffer.seek(0)

                st.download_button(
                    label="⬇️ Download as Excel",
                    data=buffer,
                    file_name=f"{label.replace(' ', '_').lower()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"download_{label}"
                )
        except Exception as e:
            st.error(f"Error loading or processing {label} data: {e}")



