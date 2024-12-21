import streamlit as st
import pandas as pd

def show_add_income(finance_data, db_file):
    st.header("Add Income")

    # Input fields for adding income
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Salary", "Business", "Investments", "Gifts", "Others"])
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    notes = st.text_area("Notes")

    # Add button
    if st.button("Add Income"):
        try:
            # Ensure the date is saved as a string
            formatted_date = date.strftime("%Y-%m-%d")

            # Create a new row with Type as "Income"
            new_data = pd.DataFrame({
                "Date": [formatted_date],
                "Category": [category],
                "Amount": [amount],
                "Notes": [notes],
                "Type": ["Income"]  # Automatically set as "Income"
            })

            # Append to the existing data
            finance_data = pd.concat([finance_data, new_data], ignore_index=True)

            # Save to file
            finance_data.to_csv(db_file, index=False)

            st.success("Income added successfully!")
            st.dataframe(finance_data)  # Display updated table
        except Exception as e:
            st.error("Failed to add income.")
            st.write(f"Error details: {e}")

    return finance_data
