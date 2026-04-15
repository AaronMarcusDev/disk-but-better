import requests
import streamlit as st

def send_code(code):
    response = requests.get(f"http://192.168.4.1/code?code={code}")
    print(response.text)

st.title("Send LED code by hand")
st.text("Mainly for debugging purposes.")

message = st.text_input("Enter the code / complex you want to send")
# send_code("ALERT")
# send_code("READY")
# send_code("WARN")
if st.button('Send'):
    send_code(message)
    
st.text("You can also reset the LED strip in one go:")
    
if st.button('Reset LEDs'):
    i = 0
    while i < 10:
        send_code('WARN')
        i += 1