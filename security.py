import json

import streamlit as st
from cryptography.fernet import Fernet

st.title("Security stuff")

# form = st.form("Encode")
# text = form.text_input("Please enter the text to encode")
# form.form_submit_button(label="Submit")

credentials = {}

text = json.dumps(credentials)
st.text_area(label="Credentials:", value=text)

key = Fernet.generate_key()
st.text_area(label="key generated, save this!:", value=key)

f = Fernet(key)
token: bytes = f.encrypt(str.encode(text))
st.text_area(label=f'Encrypted text with key:', value=f'{token}')

decrypted: bytes = f.decrypt(token)
st.text_area(label=f'decrypted text:', value=decrypted)

decrypted_dict = json.loads(s=bytes.decode(decrypted))
assert decrypted_dict == credentials

