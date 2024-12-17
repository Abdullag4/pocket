import streamlit as st
import pandas as pd
from style import apply_styles

def show_add_expense(finance_data, db_file):
    st.header("Add Expense")
    
    # Input form
    with st.form(key="expense_form"):
        date = st.date_input("Date")
        category = st.text_input("Category")
        amount = st.number_input("Amount (Negative for expenses)", min_value=-1_000_000.0, max_value=0.0, value=0.0)
        notes = st.text_area("Notes")
        submit = st.form_submit_button("Add Expense")

    if submit:
        # Add new data
        new_data = {"Date": date, "Category": category, "Amount": amount, "Notes": notes}
        finance_data = pd.concat([finance_data, pd.DataFrame([new_data])], ignore_index=True)

        # Save updated data
        finance_data.to_csv(db_file, index=False)
        st.success("Expense added successfully!")

    # Defensive check and styled display
    try:
        st.dataframe(apply_styles(finance_data))  # Styled display
    except Exception as e:
        st.error("Failed to apply styles.")
        st.write(f"Error details: {e}")
        st.write(finance_data)  # Show raw data for debugging

    return finance_data
