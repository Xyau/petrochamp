from toml import dumps, load, loads
import streamlit as st
credentials = {}

toml = dumps(credentials)

st.text_area(label="Toml:", value=toml)

dic = loads(toml)
st.text(dic)