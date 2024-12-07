import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# App title
st.title("Monthly Finance Manager")

# File path for the database CSV
db_file = "database.csv"

# Load data from CSV if it exists; otherwise, create an empty DataFrame
if os.path.exists(db_file):
    finance_data = pd.read_csv(db_file)
else:
    finance_data = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Notes"])

# Sidebar
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Menu", ["Overview", "Add Expense", "Add Income", "Settings"])

# Overview Page
if menu == "Overview":
    st.header("Financial Overview")
    
    if not finance_data.empty:
        st.subheader("Transaction History")
        st.dataframe(finance_data.style.highlight_max(axis=0))

        # Generate summary for income and expenses
        st.subheader("Summary")
        total_income = finance_data[finance_data["Type"] == "Income"]["Amount"].sum()
        total_expenses = finance_data[finance_data["Type"] == "Expense"]["Amount"].sum()
        balance = total_income + total_expenses

        st.write(f"**Total Income:** ${total_income:,.2f}")
        st.write(f"**Total Expenses:** ${abs(total_expenses):,.2f}")
        st.write(f"**Balance:** ${balance:,.2f}")

        # Visualization: Pie chart for income vs. expenses
        st.subheader("Financial Breakdown")
        fig, ax = plt.subplots()
        labels = ['Income', 'Expenses']
        sizes = [total_income, abs(total_expenses)]
        colors = ['lightgreen', 'lightcoral']
        explode = (0.1, 0.1)
        
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        ax.axis('equal')
        st.pyplot(fig)
        
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
        finance_data.to_csv(db_file, index=False)  # Save to CSV
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
        finance_data.to_csv(db_file, index=False)  # Save to CSV
        st.success("Income added successfully!")

# Settings Page
elif menu == "Settings":
    st.header("Settings")
    clear = st.button("Clear All Data")
    if clear:
        finance_data = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Notes"])
        finance_data.to_csv(db_file, index=False)  # Save the cleared data to CSV
        st.success("All data cleared!")
