import json
import logging

import streamlit as st
from cryptography.fernet import Fernet

ENCRYPTED_CREDENTIALS_NAME = "ENCRYPTED_CREDENTIALS"
ENCRYPTED_CREDENTIALS = b'gAAAAABiH_vkh2bB4JaTsJPIgnC8-Zfc2abcWw7P6JeekqcZyGwD9XiHG8eVzo3zzyPiC3dCCCXs_BaG9aNyGmUd7fKXr_a5acXHXdAViBhfISVKOpalrw23gfhfd5svo70USj_eKe7fMUYEBVJ6k0n2SvY46yoVBExWe__QhvpXTQHqVP7hVFK3DT2eUjmqXSvQu3A4TQwIuue6ktAXDv9vOB_uveo1FoS-1GMG0hcl1zjyhYYu38-KbyzbvEgPJpopP3zfA-9bfjKKoetSO3oegb2nDsnZOKPSmRmuHKf1_Z_MNwX8NHsN0JiATo1qQBb7-yQv9la7o23HLCZT0z77fv1nham72VefKCLrGZDH6R7XRqwa16Gxf43Ec4yVGR28w0uhVO2Fdmd6CSSNeYem8nndapAgYOZWYRyZo0qWLgl618CVFs4pX1InS_9C1ngggB9rX1-U56RhwxxACP31ebVyg2dQd6EFteqnG1m06ZqNKAH4F_S_R20X8oYYcl25vq0wqJBq0gh3AdNZ0V2ijrc8SWZIcrRrSDGtKdsR88y52IvHnrc7MIfdbGE9__-YT4Xc6uOI_13SyfNYNA884PhxIkwYBZaw3gWdVsc6P8BIqAg_OVvCyUF3sWzbl7XgkYILy0U1g9CmN9EyP-tKlpqJfkgQoSkC8AxRtRmrhbCNVtt7Bc59c-HPFtRVQBxN70Ey4Vz0C3NyourUS-dqFgPAvqyyD2HS47UmP83YXvJMzi54P_4e9LHQUrFNTlihHu1fS6bbmBgyH16r5O5uwpNXoOCoPtME_GtSCRGdKc30mg2fdaJyFPdI07z16uyEHKnpxGOkWm2fUa-C6nRmG2AvgIX3ffxNm2ekvv7Rw-XZC-2EDJ18al5McIHqXSIkOUDs9YXqUoUEQQqYQR0Nk43bNtRpevkz4wewlwk51yY9PvGjtqZv-6KKFzlfCS1q4aAaVQO5KejXR-RlfXxSFlyRa8v-Rk4XBV0RA1pTSUoK3hPCitB8J6d6gfjtqaqDRwxNLLzwxXbvkCcipq8vHeGX9C8COKob-EIu0izFxK_r1Qlm_rYNi-zB63Yofs5EcNdiDC5xCIs3_BXJfKHE7PVGWQ9eQFEAZP0fkQQhmCxu2b5xC59IxKl9pb4OTrU9DYbmxyWyEaaV9SlYMUfT3EQhYevGWwI68nIZ-AQqqihvZaF-ptezau0gY76R6ZoSJQUyY9LcsfYZ0Qp82UFzGC0ufkMm0hJGGShBbfNVhlviRRUHTf6FIjhKIXt2LlLkmi8lnes2wADa54z1eT6f2RH3xO8lzmnqO8oXLXcLZPyw1lg2JcsGin31yHMwXRWtKawd5KiL31LVCTbzNZEuMOwm4b1Khs2_MX_1QClVlySuAlhWKasfdNR5ycLJo-hVl_HB-MiEwZ9-5QnxWTIK78NAxTTHKUGj4Yq9PHXB7zoQaljyGM-DHanNxylbPN_c0g1tsckrkzjjuuPmJg5Bd6fa5UK78vQB3p0V6MsvY8DKQEg2BWaT83k_GsTtdmJ35o2J6KRwJC0MfdkUxZpnMNkby58l6GgzBcamx28lp9zW2IKxR5xNwqJjXQ7Fvu_SumRDYn-xIwEt-bmVjqSEiKxX2NSd0a9xadi6F0EoKHqRKgz61W7p8u9QQdxIFqs58x7VacEA5Ct0Ln_OzVSBttI5R5m7j3hcNyZf-xpEKps3Kf-vnls3lOdRsN_gLbZztLWFEFEwNjVZDmDGzCsYXpmF3XMSywqgjN6CefjVJACt2rUR4cvuZr9qJOLCvnrnPXdp8gFCqeGQHWYBJLi7mBcvHATDXTzpu5pz9yTYFesR4r5LBkujcG1uLQz_sW0VT24nAxX38yM9zO01Ynk5WKLGjvmD5X2Gy7anz_Z0fAU1fDKualu8z7jwuAm2q-J3erkwje8oHj7fCStpte8aKni1bqFmKRqW4ltcy-H3F4nMXGOcshe8LRrgAfAuKU2mIvq5t1HC9kBHic9bKtcN1TkaB4WLuld0nANlsj-C5efU9Kypa0-DHoJLRrlvR5YsRv_3Ss-xjRNsbWVVyyhbMof06yXoHDvrdJuL8pJF2xR65Mrqbvflrc4P4zTNBaxaBtFQn0lgmkntuAqeInh5VhLplc15JFLFk8_XruhCy7ky2SboZJrt5pZvy2SqhWmKchg2y6zuf-GfWyGGgBLIwfuhFsf5lAdlTxBfOtsq_ROT-YJjWYWY-i2lZ3fNNh6qOoSH2qeFl8-N_RMboREjvf-x5zhLqG-2TbhNMU3j3FyJY4cdHlL1srfr8zS1RLJHwVMKMEne5X2qZ6Wzo3HinvSFXF9e5vgTa9ryF2UBDiR0wZvqX3v7FeK6BKKd0t_QXTMv-rqRCjQHZdwaTP4Ro7v5lGVvYlzUB4VYumHQTw58hXEddt0UjI2kVIA3KZgebI_IFDsw0TDyjVPHMWQkHzmqT1_JYBvzBnTk5PWENlk8FDoKQkZClY9CvU3VeKqkDJK62t-9yZLuWXSBH42EXOM5yAtKFi0fEijz_GzQSgfUVecz01PpjR3nsOx33aDdd4SHT8F7Ak5Xkrlo6v81WoMOLv11UFDG0l2qlczkwUqypA1VHNT0OZilYuPwu9pTtvxGvDOD_bPVaLaUSwfnH_MS4GuJ7y5TZuaWSk-ZN2HJIjBv8tpVKM7Ej0u6LN_8z9SCEjIfBXMFvRPYuamqMoybxUPBHIFzrrbkuaSi2kmsz4spqP3bQUNH9yf0tvzK9QTm2rlXC9DIMvF1f8omDmboI4MBjLHH90y_iF7x0InUgSWolPxCnEB3RHQw7ukEwe2ATbVfRCzqqej9KyeIbHiJ-TfQ43wP0vBSg6Vp-GKxw-iaIRsA36ISdPZzUXmhrSnYS1JYwd2zbhl36M6B6tiEhgGt1jTdze_nOiMjIWWOOAsDdmQC78qKM9vH-01fNKdA785IIsj-YMTgKBo-0H9kbqMpjVFJR5ZD7mXOq5tbYcWqArCr_d_EZH3KT9_UJG3ydp8uY30hU-PPOCagAHCYp0gaUysI_GrP0Em2mWGFniQpLcvzNoD6rZF8ScUrcoSe13QWXbXM5gOXptw4iqzlhGCaG-kBp4iRxWlBP54yLV86UxnJfHs-Inl54dRl2GigbD3j'
# Credentials are obtained from this tutorial: https://docs.gspread.org/en/latest/oauth2.html
# They look like this:
# credentials = {
#     "type": "service_account",
#     "project_id": "api-project-XXX",
#     "private_key_id": "2cd … ba4",
#     "private_key": "-----BEGIN PRIVATE KEY-----\nNrDyLw … jINQh/9\n-----END PRIVATE KEY-----\n",
#     "client_email": "473000000000-yoursisdifferent@developer.gserviceaccount.com",
#     "client_id": "473 … hd.apps.googleusercontent.com",
# }
def get_credentials(key: str) -> dict[str, str]:
    if ENCRYPTED_CREDENTIALS_NAME in st.secrets:
        logging.warning(f'Getting credentials from secrets')
        raw_credentials = str.encode(st.secrets[ENCRYPTED_CREDENTIALS_NAME])
    else:
        logging.warning(f'Getting credentials from code')
        raw_credentials = ENCRYPTED_CREDENTIALS

    f = Fernet(key)

    decrypted: bytes = f.decrypt(raw_credentials)

    return json.loads(s=bytes.decode(decrypted))