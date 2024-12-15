import streamlit as st
import pandas as pd

def show_settings(finance_data, db_file):
    st.header("Settings")
    clear = st.button("Clear All Data")
    if clear:
        try:
            finance_data = pd.DataFrame(columns=["Date", "Category", "Amount", "Notes"])
            finance_data.to_csv(db_file, index=False)  # Save the cleared data to CSV
            st.success("All data cleared!")
        except Exception as e:
            st.error("Failed to clear data.")
            st.write(f"Error details: {e}")
