import json

import streamlit as st
from cryptography.fernet import Fernet

st.title("Security stuff")

# form = st.form("Encode")
# text = form.text_input("Please enter the text to encode")
# form.form_submit_button(label="Submit")

credentials = {
}

text = json.dumps(credentials)

key = Fernet.generate_key()
st.text(body=f'key used, save this!: {key}')
f = Fernet(key)

token: bytes = f.encrypt(str.encode(text))
st.info(f'encrypted text:')
st.text_area(f'{token}')

decrypted: bytes = f.decrypt(token)
st.text(f'decrypted text: {decrypted}')

decrypted_dict = json.loads(s=bytes.decode(decrypted))
#
assert decrypted_dict == credentials