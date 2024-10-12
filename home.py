import streamlit as st
from auth import check_password  # Import the password check

st.set_page_config(page_title="Crypto Market Project")


# Apply the password check
if not check_password():
    st.stop()  # Stop rendering the page if password is incorrect
    
# Home Page Content
st.image("whenlambo.jpg", caption="", use_column_width=True)
