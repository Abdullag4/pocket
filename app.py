def save_data(finance_data):
    """Saves the finance data to the database file."""
    finance_data.to_csv(db_file, index=False)

# Page Routing
if menu == "Overview":
    st.title("Overview")
    st.dataframe(finance_data.style.highlight_max(axis=0))
elif menu == "Add Expense":
    show_add_expense(finance_data, save_data)  # Pass the save_data function
elif menu == "Add Income":
    show_add_income(finance_data, save_data)  # Pass the save_data function
elif menu == "Settings":
    show_settings(finance_data, db_file)
