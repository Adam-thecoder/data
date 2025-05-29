import streamlit as st
import pandas as pd

st.set_page_config(
     page_title="Data",
     page_icon="📊",
     layout="centered"
)
st.subheader("Compressor")
data_1 = pd.read_csv("/Users/macbookair/Py/database/csv/compressor.csv")
with st.expander("Data list"):
     st.dataframe(data_1)

st.subheader("Evaporator coil")
data_2 = pd.read_csv("/Users/macbookair/Py/database/csv/evaporator_coil.csv")
with st.expander("Data list"):
     st.dataframe(data_2)

st.subheader("Condensor coil")
data_3 = pd.read_csv("/Users/macbookair/Py/database/csv/codensor_coil.csv")
with st.expander("Data list"):
     st.dataframe(data_3)

st.subheader("Blower motor")
data_4 = pd.read_csv("/Users/macbookair/Py/database/csv/blower_motor.csv")
with st.expander("Data list"):
     st.dataframe(data_4)

st.subheader("Radaitor motor")
data_5 = pd.read_csv("/Users/macbookair/Py/database/csv/radaitor_motor.csv")
with st.expander("Data list"):
     st.dataframe(data_5)

st.subheader("Air filter")
data_6 = pd.read_csv("/Users/macbookair/Py/database/csv/air_filter.csv")
with st.expander("Data list"):
     st.dataframe(data_6)