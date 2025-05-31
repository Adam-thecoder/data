import streamlit as st
import pandas as pd
import io
import os
import time

st.set_page_config(page_title="Data Manager", layout="centered")
st.title("📦 Component Data Manager")

# Change this path when switching between local and deployed
base_path = "database/csv"
# base_path = "csv" # Uncomment this for GitHub/Streamlit deployment

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
                # Inform the user about editing and saving
                st.caption("ℹ️ Edit data below and click 'Save Changes' to commit them.")

                # Use st.data_editor to allow interactive editing, adding, and deleting rows
                # 'num_rows="dynamic"' enables adding new rows at the bottom
                # 'use_container_width=True' makes the editor responsive to the container width
                edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

                # Save button for the form
                save_clicked = st.form_submit_button(f"💾 Save Changes to {label}")

                # Placeholder for success messages that will disappear after a delay
                success_placeholder = st.empty()

                # Logic to execute when the save button is clicked
                if save_clicked:
                    try:
                        # --- MAIN CHANGE EXPLANATION HERE ---
                        # When rows are deleted in st.data_editor, they are simply not present
                        # in the 'edited_df' returned by the editor.
                        # The following line robustly handles both completely empty new rows
                        # and implicitly handles deleted rows by only keeping rows that are
                        # not entirely NaN (empty).
                        cleaned_df = edited_df[~edited_df.isnull().all(axis=1)].copy()

                        # Replace any remaining NaN values (e.g., in partially filled new rows) with empty strings
                        cleaned_df.fillna("", inplace=True)

                        # Save the cleaned DataFrame back to the CSV file
                        cleaned_df.to_csv(path, index=False)

                        # Display a success message using the placeholder
                        success_placeholder.success(f"{label} data saved.")

                        # Wait for 2 seconds
                        time.sleep(2)

                        # Clear the success message from the placeholder
                        success_placeholder.empty()

                    except Exception as save_err:
                        # Display an error message if saving fails
                        st.error(f"Failed to save data: {save_err}")
        except Exception as e:
            # Display an error message if loading data initially fails
            st.error(f"Error loading {label} data: {e}")
