import streamlit as st
import pandas as pd
from style import apply_styles

def show_add_income(finance_data, db_file):
    st.header("Add Income")

    # Input form
    with st.form(key="income_form"):
        date = st.date_input("Date")
        category = st.text_input("Category")
        amount = st.number_input("Amount (Positive for income)", min_value=0.0, max_value=1_000_000.0, value=0.0)
        notes = st.text_area("Notes")
        submit = st.form_submit_button("Add Income")

    if submit:
        # Add new data
        new_data = {"Date": date, "Category": category, "Amount": amount, "Notes": notes}
        finance_data = pd.concat([finance_data, pd.DataFrame([new_data])], ignore_index=True)

        # Save updated data
        finance_data.to_csv(db_file, index=False)
        st.success("Income added successfully!")

    # Defensive check and styled display
    try:
        st.dataframe(apply_styles(finance_data))  # Styled display
    except Exception as e:
        st.error("Failed to apply styles.")
        st.write(f"Error details: {e}")
        st.write(finance_data)  # Show raw data for debugging

    return finance_data
