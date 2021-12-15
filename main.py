from typing import Optional
from urllib.parse import unquote
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from pyotp import TOTP
from src.config import config
from src.database import Database
from src.layout import CustomLayout, CodeText, set_page_config, display_image
from src.utils import get_time_process, format_code, QRCodeDecoder


# Load config
set_page_config(title=config.application_name)
code_text = CodeText()

# Connect to to database
if 'db' not in st.session_state:
    st.session_state['db'] = Database()

# Setup auto refresh every second
ping = st_autorefresh(
    interval=1000,
    key='counterkey'
)


def sidebar():

    # Text input to get QR Code's image
    input_url: str = st.sidebar.text_input(
        label="QR Code image URL or OTP Auth URL:",
        placeholder="http:// or https:// or otpauth://"
    )

    # Add to the database when the user click the button
    if st.sidebar.button('Import'):
        otp_url: Optional[str] = None

        # If an QR code image is given, process it
        if input_url.startswith('http'):
            otp_url = QRCodeDecoder.from_url(input_url).content

        # If a direct otpauth url is given, decode it
        elif input_url.startswith('otpauth'):
            otp_url = unquote(input_url)

        # Add to the database
        st.session_state['db'].add(otp_url)


def content():

    # Display application header
    st.title(config.application_name)
    time: float = get_time_process()
    st.progress(time)

    # Display all codes from the database
    database: Database = st.session_state['db']
    for authenticator in database:
        st.markdown("""---""")

        # Get a code
        otp: TOTP = authenticator.otp
        code: str = otp.now()

        cols = st.columns((1, 4, 2, 1))

        # Display code's logo
        with cols[0]:
            display_image(authenticator.image)

        # Display code
        with cols[1]:
            st.container()
            st.write(f"{otp.issuer} ({otp.name})")
            code_text.write(format_code(code))

        # Delete button
        with cols[3]:
            if st.button("Delete", key=otp.secret):
                database.delete(otp.secret)


# Apply layout and display content
CustomLayout.apply()
sidebar()
content()
