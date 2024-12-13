import streamlit as st
import pandas as pd

def show_add_income(finance_data, save_data):
    st.title("Add Income")

    with st.form("income_form"):
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Investment", "Salary"])
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        notes = st.text_area("Notes")
        submit = st.form_submit_button("Add Income")

        if submit:
            try:
                new_data = {
                    "Date": date,
                    "Category": category,
                    "Amount": amount,
                    "Notes": notes,
                }
                finance_data = pd.concat([finance_data, pd.DataFrame([new_data])], ignore_index=True)
                save_data(finance_data)
                st.success("Income added successfully!")
            except Exception as e:
                st.error("Failed to add income.")
                st.write(f"Error details: {e}")
