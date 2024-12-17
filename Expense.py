from style import apply_styles
import pandas as pd
import streamlit as st

def show_add_expense(finance_data, db_file):
    st.header("Add Expense")
    with st.form("expense_form"):
        date = st.date_input("Date")
        category = st.text_input("Category")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        notes = st.text_area("Notes")
        submit = st.form_submit_button("Add Expense")
    
    if submit:
        new_data = pd.DataFrame([{"Date": date, "Category": category, "Amount": amount, "Notes": notes}])
        finance_data = pd.concat([finance_data, new_data], ignore_index=True)

        # Save to CSV
        finance_data.to_csv(db_file, index=False)

        # Ensure "Amount" is integer
        finance_data["Amount"] = finance_data["Amount"].astype(int)

        st.success("Expense added successfully!")
        st.dataframe(apply_styles(finance_data))  # Display updated table

    return finance_data
