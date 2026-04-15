import requests
import streamlit as st

def send_code(code):
    response = requests.get(f"http://192.168.4.1/code?code={code}")
    print(response.text)

message = st.text_input("Enter the code / complex you want to send")
# send_code("ALERT")
# send_code("READY")
# send_code("WARN")
if st.button('Send'):
    send_code(message)