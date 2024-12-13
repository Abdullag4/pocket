def show_add_expense(finance_data, save_data):
    st.title("Add Expense")

    with st.form("expense_form"):
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Clothes", "Electric"])
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        notes = st.text_area("Notes")
        submit = st.form_submit_button("Add Expense")

        if submit:
            new_data = {
                "Date": date,
                "Category": category,
                "Amount": -amount,  # Negative for expenses
                "Notes": notes,
            }
            finance_data = pd.concat([finance_data, pd.DataFrame([new_data])], ignore_index=True)
            save_data(finance_data)  # Save data using the passed function
            st.success("Expense added successfully!")
