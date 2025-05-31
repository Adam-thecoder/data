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

            # Put editor and save button in a form
            with st.form(key=f"form_{label}"):
                st.caption("ℹ️ Add new rows below and click 'Save Changes' to commit them.")
                edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
                save_clicked = st.form_submit_button(f"💾 Save Changes to {label}")

                if save_clicked:
                    try:
                        # Drop fully empty rows, keep partially filled ones
                        cleaned_df = edited_df[~edited_df.isnull().all(axis=1)].copy()
                        cleaned_df.fillna("", inplace=True)  # Replace NaNs with empty string
                        cleaned_df.to_csv(path, index=False)
                        st.success(f"{label} data saved.")
                    except Exception as save_err:
                        st.error(f"Failed to save data: {save_err}")

            # # Download button (can be outside the form)
            # buffer = io.BytesIO()
            # with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            #     edited_df.to_excel(writer, index=False, sheet_name=label[:31])
            # buffer.seek(0)

            # st.download_button(
            #     label="⬇️ Download as Excel",
            #     data=buffer,
            #     file_name=f"{label.replace(' ', '_').lower()}.xlsx",
            #     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            #     key=f"download_{label}"
            # )

        except Exception as e:
            st.error(f"Error loading {label} data: {e}")

