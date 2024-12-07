import streamlit as st
import pandas as pd

# App title
st.title("Monthly Finance Manager")

# Sidebar
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Menu", ["Overview", "Add Expense", "Add Income", "Settings"])

# Initialize data with sample entries if empty
if "finance_data" not in st.session_state:
    sample_data = [
        {"Date": "2024-12-01", "Type": "Income", "Category": "Salary", "Amount": 2000, "Notes": "Monthly salary"},
        {"Date": "2024-12-03", "Type": "Expense", "Category": "Food", "Amount": -150, "Notes": "Groceries shopping"},
        {"Date": "2024-12-05", "Type": "Expense", "Category": "Electric", "Amount": -50, "Notes": "Utility bill"},
        {"Date": "2024-12-07", "Type": "Expense", "Category": "Clothes", "Amount": -100, "Notes": "Winter jacket"},
        {"Date": "2024-12-10", "Type": "Income", "Category": "Investment", "Amount": 500, "Notes": "Stock dividends"}
    ]
    st.session_state["finance_data"] = pd.DataFrame(sample_data)

finance_data = st.session_state["finance_data"]

# Overview Page
if menu == "Overview":
    st.header("Overview")
    if not finance_data.empty:
        st.subheader("Transaction History")
        st.dataframe(finance_data)

        st.subheader("Summary")
        total_income = finance_data[finance_data["Type"] == "Income"]["Amount"].sum()
        total_expenses = finance_data[finance_data["Type"] == "Expense"]["Amount"].sum()
        balance = total_income + total_expenses

        st.write(f"**Total Income:** ${total_income}")
        st.write(f"**Total Expenses:** ${abs(total_expenses)}")
        st.write(f"**Balance:** ${balance}")
    else:
        st.info("No transactions available yet. Use the menu to add income or expenses.")

# Add Expense Page
elif menu == "Add Expense":
    st.header("Add Expense")
    with st.form("expense_form"):
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Clothes", "Electric"])
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        notes = st.text_area("Notes (optional)")
        submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_data = {
            "Date": date.strftime("%Y-%m-%d"),
            "Type": "Expense",
            "Category": category,
            "Amount": -amount,
            "Notes": notes
        }
        finance_data = finance_data.append(new_data, ignore_index=True)
        st.session_state["finance_data"] = finance_data
        st.success("Expense added successfully!")

# Add Income Page
elif menu == "Add Income":
    st.header("Add Income")
    with st.form("income_form"):
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Salary", "Investment"])
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        notes = st.text_area("Notes (optional)")
        submitted = st.form_submit_button("Add Income")

    if submitted:
        new_data = {
            "Date": date.strftime("%Y-%m-%d"),
            "Type": "Income",
            "Category": category,
            "Amount": amount,
            "Notes": notes
        }
        finance_data = finance_data.append(new_data, ignore_index=True)
        st.session_state["finance_data"] = finance_data
        st.success("Income added successfully!")

# Settings Page
elif menu == "Settings":
    st.header("Settings")
    clear = st.button("Clear All Data")
    if clear:
        st.session_state["finance_data"] = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Notes"])
        st.success("All data cleared!")

