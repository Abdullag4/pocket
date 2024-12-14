import streamlit as st
import pandas as pd

def show_add_income(finance_data, save_data):
    """
    Display the Add Income page for the app.
    Allows the user to input income details and save them to the database.
    """
    st.title("Add Income")

    # Input form for income details
    with st.form("income_form"):
        date = st.date_input("Date")  # Date input
        category = st.selectbox("Category", ["Investment", "Salary"])  # Category dropdown
        amount = st.number_input("Amount", min_value=0.01, step=0.01)  # Positive numeric input
        notes = st.text_area("Notes")  # Optional notes
        submit = st.form_submit_button("Add Income")

        if submit:
            # Create a new income entry
            new_data = {
                "Date": date,
                "Category": category,
                "Amount": amount,  # Positive amount for income
                "Notes": notes,
            }
            # Append new data to the existing finance_data
            finance_data = pd.concat([finance_data, pd.DataFrame([new_data])], ignore_index=True)
            
            # Save the updated data using the provided save_data function
            save_data(finance_data)
            st.success("Income added successfully!")
