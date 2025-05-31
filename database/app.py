import streamlit as st
import pandas as pd
import os
import time

st.set_page_config(page_title="Data Manager", layout="centered")
st.title("📦 Component Data Manager")

# Define the base path for your CSV files.
# Change this path when switching between local and deployed environments.
# For local development, ensure 'database/csv' directory exists and contains your CSVs.
# For deployment (e.g., on Streamlit Cloud), 'csv' might be the root if files are directly in the repository.
base_path = "database/csv"
# base_path = "csv" # Uncomment this for GitHub/Streamlit deployment

# Check if the base_path directory exists. If not, inform the user and stop execution.
# This is crucial for local development to ensure files can be found.
if not os.path.exists(base_path):
    st.warning(f"Directory '{base_path}' not found. Please create it and place your CSV files there.")
    st.stop() # Stop the app if the directory is missing, as it won't be able to load data.

# Define the datasets, mapping a user-friendly label to its corresponding CSV file path.
datasets = {
    "Compressor": os.path.join(base_path, "compressor.csv"),
    "Evaporator Coil": os.path.join(base_path, "evaporator_coil.csv"),
    "Condensor Coil": os.path.join(base_path, "condensor_coil.csv"),
    "Blower Motor": os.path.join(base_path, "blower_motor.csv"),
    "Radaitor Motor": os.path.join(base_path, "radiator_motor.csv"),
    "Air Filter": os.path.join(base_path, "air_filter.csv")
}

# Initialize Streamlit's session state to store DataFrames.
# This allows the DataFrames to persist across reruns of the script,
# ensuring the `st.data_editor` always displays the most current data.
if 'dataframes' not in st.session_state:
    st.session_state.dataframes = {}

# Iterate through each dataset to create a section for managing its data.
for label, path in datasets.items():
    st.subheader(label)
    with st.expander(f"{label} Data"):
        # --- Data Loading Logic ---
        try:
            # Check if the CSV file for the current component exists.
            if not os.path.exists(path):
                # If the file doesn't exist, create an empty DataFrame.
                st.warning(f"CSV file for {label} not found at '{path}'. Creating an empty one.")
                # Define some default columns for the new empty CSV. Adjust these as needed.
                initial_df = pd.DataFrame(columns=["ID", "Name", "Amount", "Unit", "Description"])
                initial_df.to_csv(path, index=False) # Save the empty DataFrame to create the file.
            else:
                # If the file exists, read its content into a DataFrame.
                initial_df = pd.read_csv(path)

            # Store the loaded (or newly created empty) DataFrame in session state.
            # This ensures that on subsequent reruns, the `st.data_editor` uses
            # the current state of the data from session state, rather than always
            # re-reading the file, which might not yet reflect unsaved edits.
            if label not in st.session_state.dataframes:
                st.session_state.dataframes[label] = initial_df

            # --- Data Editing Form ---
            # Create a Streamlit form for data editing and saving.
            # Using a form ensures that inputs are processed together when the submit button is clicked.
            with st.form(key=f"form_{label}"):
                st.caption("ℹ️ Edit data below and click 'Save Changes' to commit them.")

                # Use st.data_editor to allow interactive editing, adding, and deleting rows.
                # It's initialized with the DataFrame from session state, ensuring consistency.
                # 'num_rows="dynamic"' enables adding new rows at the bottom.
                # 'use_container_width=True' makes the editor responsive to the container width.
                edited_df = st.data_editor(
                    st.session_state.dataframes[label],
                    num_rows="dynamic",
                    use_container_width=True
                )

                # Save button for the form.
                save_clicked = st.form_submit_button(f"💾 Save Changes to {label}")

                # Placeholder for displaying success or error messages.
                # Messages will be displayed here and then cleared.
                success_placeholder = st.empty()

                # --- Save Logic ---
                # This block executes only when the save button is clicked.
                if save_clicked:
                    try:
                        # Clean the edited DataFrame:
                        # 1. Use .dropna(how='all') to remove rows where all values are NaN.
                        #    This effectively handles rows that have been "deleted" by the `st.data_editor`,
                        #    as `st.data_editor` often turns deleted rows into all NaNs.
                        cleaned_df = edited_df.dropna(how='all').copy()

                        # 2. Replace any remaining NaN values (e.g., in partially filled new rows) with empty strings.
                        #    This ensures data consistency when saving to CSV.
                        cleaned_df.fillna("", inplace=True)

                        # Save the cleaned DataFrame back to the CSV file.
                        # `index=False` prevents pandas from writing the DataFrame index as a column in the CSV.
                        cleaned_df.to_csv(path, index=False)

                        # --- CRITICAL FIX FOR PERSISTENCE AND SCROLLBAR ---
                        # Immediately re-read the CSV file after saving.
                        # This ensures that `st.session_state.dataframes[label]` is updated
                        # with the absolute latest data from the file.
                        st.session_state.dataframes[label] = pd.read_csv(path)

                        # Display a success message using the placeholder.
                        success_placeholder.success(f"{label} data saved successfully!")

                        # Wait for a short duration to allow the user to see the message.
                        time.sleep(2)
                        # Clear the success message from the placeholder.
                        success_placeholder.empty()

                        # Force a rerun of the script.
                        # This is essential to make `st.data_editor` re-render with the
                        # newly updated data from `st.session_state`, reflecting the changes immediately.
                        # While it will cause the scrollbar to jump, the data displayed will be correct.
                        st.rerun()

                    except Exception as save_err:
                        # Display an error message if saving fails.
                        st.error(f"Failed to save data: {save_err}")
        except Exception as e:
            # Display an error message if loading data initially fails (e.g., file corruption).
            st.error(f"Error loading {label} data: {e}")
