import streamlit as st
import pandas as pd

def show_add_expense(finance_data, db_file):
    st.header("Add Expense")

    # Input fields for adding expense
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Transport", "Rent", "Utilities", "Others"])
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    notes = st.text_area("Notes")

    # Add button
    if st.button("Add Expense"):
        try:
            # Ensure the date is saved as a string
            formatted_date = date.strftime("%Y-%m-%d")

            # Create a new row with Type as "Expense"
            new_data = pd.DataFrame({
                "Date": [formatted_date],
                "Category": [category],
                "Amount": [amount],
                "Notes": [notes],
                "Type": ["Expense"]  # Automatically set as "Expense"
            })

            # Append to the existing data
            finance_data = pd.concat([finance_data, new_data], ignore_index=True)

            # Save to file
            finance_data.to_csv(db_file, index=False)

            st.success("Expense added successfully!")
            st.dataframe(finance_data)  # Display updated table
        except Exception as e:
            st.error("Failed to add expense.")
            st.write(f"Error details: {e}")

    return finance_data
