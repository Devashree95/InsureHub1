import streamlit as st
from PIL import Image
import base64
import uuid

from helpers import connection as conn
from helpers.Insurehub_Login import login_snippet

if "user_logged_in" not in st.session_state or not st.session_state.user_logged_in:
    st.toast("You need to login to access this page.")
    user_logged_in = login_snippet(key="buy_or_renew_login")


if st.session_state.user_logged_in:
    connection = conn.pgsql_connect()
    cur = connection.cursor()


    logo = "./images/profile_3135715.png"
    image = Image.open(logo)

    # Function to convert image to Base64
    def get_image_as_base64(path):
        with open(path, "rb") as image_file:
            data = base64.b64encode(image_file.read()).decode()
            return f"data:image/jpeg;base64,{data}"
        
    def get_base64_of_file(path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()
        
    def set_background_from_local_file(path):
        base64_string = get_base64_of_file(path)
        # CSS to utilize the Base64 encoded string as a background
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_string}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    
    def get_agent_id(email):
        query = f"SELECT agent_id FROM insurehub.relationship_manager WHERE email = '{email}'"
        cur.execute(query)
        custId = cur.fetchall()
        return custId[0][0]
        
    set_background_from_local_file('./images/login_background.png')
        
        
    image_base64 = get_image_as_base64(logo)

    st.markdown(f"""
                <a href="/" style="color:white;text-decoration: none;">
                    <div style="display:table;margin-top:-15 rem;margin-left:0%; display: flex;">
                        <img src="{image_base64}" alt="Insurehub Logo" style="width:50px;height:40px;margin-left:750px; flex:2;" </img>
                        <span style="padding:10px; flex:2;">{st.session_state['username']}</span>
                    </div>
                </a>
                <br>
                    """, unsafe_allow_html=True)

    #agent_id = '0381AA78-BF6A-8C7E-23B7-36728C8C43D5'
    if st.session_state['role'] == 'agent':
        agent_id = get_agent_id(st.session_state['username'])
        custid = str(uuid.uuid4()).upper()
    else:
        agent_id = ''

    def fetch_customers():
        query = f"SELECT * FROM insurehub.customer where agent_id = '{agent_id}'"  
        cur.execute(query)
        customers = cur.fetchall()
        return customers

    def delete_customer(customer_id):
        query = f"DELETE FROM insurehub.customer WHERE cust_id = '{customer_id}' "  
        cur.execute(query)
        connection.commit()

    def add_customer(fname, lname, email, dob, address):
        query = f"INSERT INTO insurehub.customer VALUES ('{custid}', '{fname}' , '{lname}', '{email}', '{dob}', '{address}', '{agent_id}' )"
        cur.execute(query)
        connection.commit()

    if st.session_state['role'] == 'agent':
        st.title("🖋️Customer Management")

        # Add customer form
        with st.form("add_customer"):
            st.write("Add a new customer")
            fname = st.text_input("First Name")
            lname = st.text_input("Last Name")
            email = st.text_input("Email")
            dob = st.date_input("Date of Birth")
            address = st.text_input("Address")

            submit_button = st.form_submit_button("➕Add Customer")

            if submit_button:
                add_customer(fname, lname, email, dob, address)
                st.success("Customer added successfully!")
                st.rerun()

        # Display existing customers
        st.title("📒Existing Accounts:")

        customers = fetch_customers()
        for customer in customers:
            with st.expander(f"👨‍💼Customer :  {customer[1]} {customer[2]}"):
                st.write(f"🔹Id: {customer[0]}") 
                st.write(f"🔹Email: {customer[3]}")  
                st.write(f"🔹Date of Birth: {customer[4]}") 
                st.write(f"🔹Address: {customer[5]}") 

                if st.button("🗑️Remove Account", key=f"delete_{customer[0]}"):
                    delete_customer(customer[0])
                    st.rerun()

        st.title("📊Statistics")
        st.write("Total number of customers under management: ", len(customers))
        
        min_coverage_query = f"SELECT MIN(po.tot_coverage_amt) AS min_coverage_amount FROM insurehub.customer cu JOIN insurehub.purchases p ON cu.cust_id = p.cust_id JOIN insurehub.policy po ON p.policy_id = po.policy_id WHERE cu.agent_id = '{agent_id}'"
        cur.execute(min_coverage_query)
        min_coverage = cur.fetchone()[0]
        st.write("Minimum coverage amount: ", min_coverage)

        max_coverage_query = f"SELECT MAX(po.tot_coverage_amt) AS max_coverage_amount FROM insurehub.customer cu JOIN insurehub.purchases p ON cu.cust_id = p.cust_id JOIN insurehub.policy po ON p.policy_id = po.policy_id WHERE cu.agent_id = '{agent_id}'"
        cur.execute(max_coverage_query)
        max_coverage = cur.fetchone()[0]
        st.write("Maximum coverage amount: ", max_coverage)

        avg_coverage_query = f"SELECT AVG(po.tot_coverage_amt) AS avg_coverage_amount FROM insurehub.customer cu JOIN insurehub.purchases p ON cu.cust_id = p.cust_id JOIN insurehub.policy po ON p.policy_id = po.policy_id WHERE cu.agent_id = '{agent_id}'"
        cur.execute(avg_coverage_query)
        avg_coverage = cur.fetchone()[0]
        st.write("Average coverage amount: ", avg_coverage)

        total_policies_query = f"SELECT COUNT(p.policy_id) AS total_policies FROM insurehub.customer cu JOIN insurehub.purchases p ON cu.cust_id = p.cust_id WHERE cu.agent_id = '{agent_id}'"
        cur.execute(total_policies_query)
        total_policies = cur.fetchone()[0]
        st.write("Total number of policies under management: ", total_policies)

        sum_coverage_query = f"SELECT SUM(po.tot_coverage_amt) AS sum_coverage_amount FROM insurehub.customer cu JOIN insurehub.purchases p ON cu.cust_id = p.cust_id JOIN insurehub.policy po ON p.policy_id = po.policy_id WHERE cu.agent_id = '{agent_id}'"
        cur.execute(sum_coverage_query)
        sum_coverage = cur.fetchone()[0]
        st.write("Total coverage amount under management: ", sum_coverage)

    else:
        st.warning("You don't have access to this page.")