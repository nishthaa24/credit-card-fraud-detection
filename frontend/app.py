import streamlit as st
import json
import requests as re
import os
os.environ['CURL_CA_BUNDLE'] = ''

st.title("Credit Card Fraud Detection Web App")

st.image("image.png")


st.sidebar.header('Input Features of The Transaction')

sender_name = st.sidebar.text_input("""Input Sender ID""")
receiver_name = st.sidebar.text_input("""Input Receiver ID""")
step = st.sidebar.slider("""Number of Hours it took the Transaction to complete: """)
types = st.sidebar.subheader(f"""
                 Enter Type of Transfer Made:\n\n\n\n
                 0 for 'Cash In' Transaction\n 
                 1 for 'Cash Out' Transaction\n 
                 2 for 'Debit' Transaction\n
                 3 for 'Payment' Transaction\n  
                 4 for 'Transfer' Transaction\n""")
types = st.sidebar.selectbox("",(0,1,2,3,4))
x = ''
if types == 0:
    x = 'Cash in'
if types == 1:
    x = 'Cash Out'
if types == 2:
    x = 'Debit'
if types == 3:
    x = 'Payment'
if types == 4:
    x =  'Transfer'
    
amount = st.sidebar.number_input("Amount in $",min_value=0, max_value=110000)
oldbalanceorg = st.sidebar.number_input("""Original Balance Before Transaction was made""",min_value=0, max_value=110000)
newbalanceorg= st.sidebar.number_input("""New Balance After Transaction was made""",min_value=0, max_value=110000)
oldbalancedest= st.sidebar.number_input("""Old Balance""",min_value=0, max_value=110000)
newbalancedest= st.sidebar.number_input("""New Balance""",min_value=0, max_value=110000)
isflaggedfraud = st.sidebar.selectbox("""Specify if this was flagged as Fraud by your System: """,(0,1))


if st.button("Detection Result"):
    values = {
    "step": step,
    "types": types,
    "amount": amount,
    "oldbalanceorig": oldbalanceorg,
    "newbalanceorig": newbalanceorg,
    "oldbalancedest": oldbalancedest,
    "newbalancedest": newbalancedest,
    "isflaggedfraud": isflaggedfraud
    }


    st.write(f"""### These are the transaction details:\n
    Sender ID: {sender_name}
    Receiver ID: {receiver_name}
    1. Number of Hours it took to complete: {step}\n
    2. Type of Transaction: {x}\n
    3. Amount Sent: {amount}\n
    4. Sender Previous Balance Before Transaction: {oldbalanceorg}\n
    5. Sender New Balance After Transaction: {newbalanceorg}\n
    6. Recepient Balance Before Transaction: {oldbalancedest}\n
    7. Recepient Balance After Transaction: {newbalancedest}\n
    8. System Flag Fraud Status: {isflaggedfraud}
                """)

    res = re.post(f"http://backend.docker:8000/predict/",json=values)
    json_str = json.dumps(res.json())
    resp = json.loads(json_str)
    
    if sender_name=='' or receiver_name == '':
        st.write("Error! Please input Transaction ID or Names of Sender and Receiver!")
    else:
        st.write(f"""### The '{x}' transaction that took place between {sender_name} and {receiver_name} is {resp[0]}.""")









