import streamlit as st
import pandas as pd
import io
import os

st.set_page_config(page_title="Data Manager", layout="centered")
st.title("📦 Component Data Manager")

# Change this path when switching between local and deployed
base_path = "database/csv"
# base_path = "csv"  # Uncomment this for GitHub/Streamlit deployment

datasets = {
    "Compressor": os.path.join(base_path, "compressor.csv"),
    "Evaporator Coil": os.path.join(base_path, "evaporator_coil.csv"),
    "Condensor Coil": os.path.join(base_path, "codensor_coil.csv"),
    "Blower Motor": os.path.join(base_path, "blower_motor.csv"),
    "Radaitor Motor": os.path.join(base_path, "radaitor_motor.csv"),
    "Air Filter": os.path.join(base_path, "air_filter.csv")
}

for label, path in datasets.items():
    st.subheader(label)
    with st.expander(f"{label} Data"):
        try:
            df = pd.read_csv(path)
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"💾 Save Changes to {label}", key=f"save_{label}"):
                    try:
                        # Remove fully empty rows
                        cleaned_df = edited_df[~edited_df.isnull().all(axis=1)].copy()

                        # Process columns: convert numeric columns, fill others
                        for col in cleaned_df.columns:
                            if pd.api.types.is_numeric_dtype(cleaned_df[col]):
                                cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
                            else:
                                cleaned_df[col] = cleaned_df[col].astype(str).fillna("")

                        cleaned_df.to_csv(path, index=False)
                        st.success(f"{label} data saved.")
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
            st.error(f"Error loading {label} data: {e}")
