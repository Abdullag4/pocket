import streamlit as st
import pandas as pd

def show_add_income(finance_data, save_data):
    st.title("Add Income")

    # Input fields for new income
    date = st.date_input("Date")
    category = st.text_input("Category")
    amount = st.number_input("Amount", min_value=0.0)
    notes = st.text_area("Notes")

    if st.button("Add Income"):
        new_data = {
            "Date": str(date),  # Ensure date is stored as string
            "Category": category,
            "Amount": float(amount),  # Store income as positive values
            "Notes": notes,
        }

        # Add new income to the DataFrame
        finance_data = pd.concat([finance_data, pd.DataFrame([new_data])], ignore_index=True)

        # Save updated data
        save_data(finance_data)
        st.success("Income added successfully!")
        st.dataframe(finance_data)
