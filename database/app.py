import streamlit as st
import pandas as pd
import io
import os
import time

st.set_page_config(page_title="Data Manager", layout="centered")
st.title("📦 Component Data Manager")

# Change this path when switching between local and deployed
base_path = "database/csv"

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
            # Read the CSV data into a DataFrame
            df = pd.read_csv(path)

            # Create a Streamlit form for data editing and saving
            with st.form(key=f"form_{label}"):
                st.caption("ℹ️ Edit data below and click 'Save Changes' to commit them.")

                # Use st.data_editor to allow interactive editing, adding, and deleting rows
                edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

                # Save button for the form
                save_clicked = st.form_submit_button(f"💾 Save Changes to {label}", disabled=st.session_state.get(f"save_in_progress_{label}", False))

                # Placeholder for success messages that will disappear after a delay
                success_placeholder = st.empty()

                # Logic to execute when the save button is clicked
                if save_clicked:
                    st.session_state[f"save_in_progress_{label}"] = True  # Disable the button
                    try:
                        cleaned_df = edited_df.dropna(how='all').copy()
                        cleaned_df.fillna("", inplace=True)
                        cleaned_df.to_csv(path, index=False)

                        success_placeholder.success(f"{label} data saved.")
                        time.sleep(2)
                        success_placeholder.empty()

                    except Exception as save_err:
                        st.error(f"Failed to save data: {save_err}")
                    finally:
                        st.session_state[f"save_in_progress_{label}"] = False  # Re-enable the button
        except Exception as e:
            st.error(f"Error loading {label} data: {e}")
