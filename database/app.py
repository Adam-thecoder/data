import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Data Manager", layout="centered")
st.title("📦 Component Data Manager")

# Change this path when switching between local and deployed
base_path = "database/csv"
# base_path = "csv"  # Uncomment this for GitHub/Streamlit deployment

datasets = {
    "Compressor": os.path.join(base_path, "compressor.csv"),
    "Evaporator Coil": os.path.join(base_path, "evaporator_coil.csv"),
    "Condensor Coil": os.path.join(base_path, "condensor_coil.csv"),
    "Blower Motor": os.path.join(base_path, "blower_motor.csv"),
    "Radaitor Motor": os.path.join(base_path, "radiator_motor.csv"),
    "Air Filter": os.path.join(base_path, "air_filter.csv")
}

for label, path in datasets.items():
    st.subheader(label)
    with st.expander(f"{label} Data"):
        try:
            df = pd.read_csv(path)

            with st.form(key=f"form_{label}"):
                #st.caption("ℹ️ You can add or delete rows below. Click 'Save Changes' to commit all edits.")
                edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
                save_clicked = st.form_submit_button(f"💾 Save Changes to {label}")

                if save_clicked:
                    try:
                        # Ensure deletions are saved by dropping fully empty rows and resetting index
                        cleaned_df = edited_df.dropna(how='all').copy()
                        cleaned_df.fillna("", inplace=True)
                        cleaned_df.reset_index(drop=True, inplace=True)

                        # Overwrite the CSV with the cleaned data
                        cleaned_df.to_csv(path, index=False)
                        st.success(f"{label} data saved.")
                    except Exception as save_err:
                        st.error(f"Failed to save data: {save_err}")

        except Exception as e:
            st.error(f"Error loading {label} data: {e}")
