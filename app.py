import streamlit as st
from agent import ask_agent

st.title("Sensor Database Query UI")

# Input box for NL query
user_query = st.text_input("Enter your query:", "Show me active sensors")

if user_query:
    # Call your agent
    results = ask_agent(user_query)

    if isinstance(results, str):
        # Error message
        st.error(results)
    else:
        # Display results in a table
        st.write("Query results:")
        st.dataframe(results)
