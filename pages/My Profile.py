import streamlit as st
import helpers.sidebar
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
from PIL import Image
import base64

from helpers import connection as conn


helpers.sidebar.show()
connection = conn.pgsql_connect()
cur = connection.cursor()


logo = "./images/profile_3135715.png"
image = Image.open(logo)

# Function to convert image to Base64
def get_image_as_base64(path):
    with open(path, "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{data}"
    
	
image_base64 = get_image_as_base64(logo)

st.markdown(f"""
			<a href="/" style="color:white;text-decoration: none;">
				<div style="display:table;margin-top:-15 rem;margin-left:0%; display: flex;">
			  		<img src="{image_base64}" alt="Insurehub Logo" style="width:50px;height:40px;margin-left:750px; flex:2;" </img>
					<span style="padding:10px; flex:2;">Username</span>
				</div>
			</a>
			<br>
				""", unsafe_allow_html=True)

custId = '2DECA7C8-395E-5B44-4A3B-C792143C9F45'

def getProfileDetails(attr):
    cur.execute(f"select {attr} from insurehub.customer where cust_id = '{custId}'")
    return cur.fetchall()[0][0]

def getPhoneDetails(attr):
    cur.execute(f"select phone from insurehub.cust_phone where cust_id = '{custId}'")
    return cur.fetchall()

def updateDbTable(attr, val):
    print(val)
    if attr == 'phone1':
        cur.execute(f"update insurehub.cust_phone SET phone = '{val}' where cust_id = '{custId}' and phone= '{phone_no_1}'")
        connection.commit()
    elif attr == 'phone2':
        if val == '':
            cur.execute(f"delete from insurehub.cust_phone where cust_id = '{custId}' and phone= '{phone_no_2}'")
            connection.commit()
            
        if phone_no_2 == '':
            cur.execute(f"insert into insurehub.cust_phone VALUES ('{custId}','{val}')")
            connection.commit()
        else:
            cur.execute(f"update insurehub.cust_phone SET phone = '{val}' where cust_id = '{custId}' and phone= '{phone_no_2}'")
            connection.commit()
    else:
        cur.execute(f"update insurehub.customer SET {attr} = '{val}' where cust_id = '{custId}'")
        connection.commit()

phone_no = getPhoneDetails('phone')
if len(phone_no) == 1:
    phone_no_1 = phone_no[0][0]
    phone_no_2 = ''
elif len(phone_no) > 1:
    phone_no_1 = phone_no[0][0]
    phone_no_2 = phone_no[1][0]
else:
    phone_no_1 = ''
    phone_no_2 = ''

print("Phone 1 and phone 2 are", phone_no_1, phone_no_2)

profile = {
    "first_name": getProfileDetails('first_name'),
    "last_name": getProfileDetails('last_name'),
    "email": getProfileDetails('email'),
    "dob": getProfileDetails('dob'),
    "address": getProfileDetails('address'),
    "phone1": phone_no_1,
    "phone2": phone_no_2
}

def update_profile(first_name, last_name, email, dob, address, phone1, phone2):
    # Update profile data
    profile["first_name"] = first_name
    updateDbTable("first_name", first_name)
    profile["last_name"] = last_name
    updateDbTable("last_name", last_name)
    profile["email"] = email
    updateDbTable("email", email)
    profile["dob"] = dob
    updateDbTable("dob", dob)
    profile["address"] = address
    updateDbTable("address", address)
    profile["phone1"] = phone1
    updateDbTable("phone1", phone1)
    profile["phone2"] = phone2
    updateDbTable("phone2", phone2)
    st.success("Profile updated successfully!")

# Displaying the profile information
st.header("My Profile")

with st.form("profile_form"):
    first_name = st.text_input("First Name", value=profile["first_name"])
    last_name = st.text_input("Last Name", value=profile["last_name"])
    email = st.text_input("Email", value=profile["email"])
    dob = st.text_input("Date of Birth", value=profile["dob"])
    address = st.text_input("Address", value=profile["address"])
    phone1 = st.text_input("Phone 1", value=profile["phone1"])
    phone2 = st.text_input("Phone 2", value=profile["phone2"])
    
    # Form submission button
    submit_button = st.form_submit_button(label="Update Profile")
    
    if submit_button:
        update_profile(first_name, last_name, email, dob, address, phone1, phone2)