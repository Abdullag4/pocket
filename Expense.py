import streamlit as st
import pandas as pd

def show_add_expense(finance_data, save_data):
    """
    Display the Add Expense page for the app.
    Allows the user to input expense details and save them to the database.
    """
    st.title("Add Expense")

    # Input form for expense details
    with st.form("expense_form"):
        date = st.date_input("Date")  # Date input
        category = st.selectbox("Category", ["Food", "Clothes", "Electric"])  # Category dropdown
        amount = st.number_input("Amount", min_value=0.01, step=0.01)  # Positive numeric input
        notes = st.text_area("Notes")  # Optional notes
        submit = st.form_submit_button("Add Expense")

        if submit:
            # Create a new expense entry (negative amount for expense)
            new_data = {
                "Date": date,
                "Category": category,
                "Amount": -amount,  # Negative amount for expense
                "Notes": notes,
            }
            # Append new data to the existing finance_data
            finance_data = pd.concat([finance_data, pd.DataFrame([new_data])], ignore_index=True)
            
            # Save the updated data using the provided save_data function
            save_data(finance_data)
            st.success("Expense added successfully!")
