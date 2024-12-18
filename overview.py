import streamlit as st
import pandas as pd

def apply_styles(finance_data):
    try:
        # Ensure Amount column is numeric
        finance_data["Amount"] = pd.to_numeric(finance_data["Amount"], errors="coerce")
        finance_data = finance_data.dropna(subset=["Amount"])  # Remove rows with invalid Amounts
        styled_data = finance_data.style.highlight_max(axis=0)
        return styled_data
    except Exception as e:
        st.error("Error applying styles to data.")
        st.write(f"Error details: {e}")
        return finance_data

def show_overview(finance_data):
    st.header("Overview")

    if finance_data.empty:
        st.warning("No data available.")
        return

    try:
        # Ensure proper data types
        finance_data["Amount"] = pd.to_numeric(finance_data["Amount"], errors="coerce")
        finance_data.dropna(subset=["Amount"], inplace=True)

        # Display the data
        st.dataframe(finance_data)
    except Exception as e:
        st.error("Error displaying overview table.")
        st.write(f"Error details: {e}")
