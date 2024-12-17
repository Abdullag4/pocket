from style import apply_styles
import streamlit as st

def show_overview(finance_data):
    st.header("Overview")
    try:
        # Convert numerical columns to integers
        for col in finance_data.select_dtypes(include=['float', 'int']).columns:
            finance_data[col] = finance_data[col].astype(int)

        # Display the table with styles
        st.dataframe(apply_styles(finance_data))
    except Exception as e:
        st.error("Error displaying overview table.")
        st.write(f"Error details: {e}")
