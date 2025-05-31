import streamlit as st
import pandas as pd
import os
import time

st.set_page_config(page_title="Data Manager", layout="centered")
st.title("📦 Component Data Manager")

# Set base path
base_path = "database/csv"

datasets = {
    "Compressor": os.path.join(base_path, "compressor.csv"),
    "Evaporator Coil": os.path.join(base_path, "evaporator_coil.csv"),
    "Condensor Coil": os.path.join(base_path, "condensor_coil.csv"),
    "Blower Motor": os.path.join(base_path, "blower_motor.csv"),
    "Radaitor Motor": os.path.join(base_path, "radiator_motor.csv"),
    "Air Filter": os.path.join(base_path, "air_filter.csv")
}

# Store save status
if "last_saved_label" not in st.session_state:
    st.session_state.last_saved_label = None
if "saved_time" not in st.session_state:
    st.session_state.saved_time = 0

for label, path in datasets.items():
    st.subheader(label)
    with st.expander(f"{label} Data"):
        try:
            df = pd.read_csv(path)

            with st.form(key=f"form_{label}"):
                #st.caption("ℹ️ Add or delete rows. Click 'Save Changes' to apply them.")
                edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
                save_clicked = st.form_submit_button(f"💾 Save Changes to {label}")

                if save_clicked:
                    try:
                        cleaned_df = edited_df.dropna(how="all").copy()
                        cleaned_df.fillna("", inplace=True)
                        cleaned_df.reset_index(drop=True, inplace=True)

                        cleaned_df.to_csv(path, index=False)
                        st.session_state.last_saved_label = label
                        st.session_state.saved_time = time.time()
                    except Exception as save_err:
                        st.error(f"Failed to save data: {save_err}")

        except Exception as e:
            st.error(f"Error loading {label} data: {e}")

    # Show success message for 3 seconds after save
    if (
        st.session_state.last_saved_label == label
        and time.time() - st.session_state.saved_time < 3
    ):
        st.success(f"{label} data saved.")
