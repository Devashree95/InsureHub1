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


st.title('My Goals!')