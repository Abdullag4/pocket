import streamlit as st
import pandas as pd

def show_manage_data(finance_data, db_file):
    st.title("Manage Data")

    # Display the current data
    st.header("Current Financial Data")
    if finance_data.empty:
        st.info("No data available to manage.")
        return

    st.dataframe(finance_data)

    # Provide an option to select and delete rows
    st.subheader("Delete Records")
    indices_to_delete = st.multiselect(
        "Select rows to delete by index:",
        finance_data.index.tolist()
    )

    if st.button("Delete Selected Records"):
        if indices_to_delete:
            finance_data.drop(indices_to_delete, inplace=True)
            save_data(finance_data, db_file)
            st.success(f"Deleted {len(indices_to_delete)} record(s). Please refresh the page to see the updated data.")
        else:
            st.warning("No records selected for deletion.")

# Function to save updated data back to the file
def save_data(finance_data, db_file):
    finance_data.to_csv(db_file, index=False)
