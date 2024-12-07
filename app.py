import streamlit as st
import pandas as pd
import os
from Expense import show_add_expense
from Income import show_add_income
from Setting import show_settings

# App title
st.title("Monthly Finance Manager")

# File path for the database CSV
db_file = "database.csv"

# Load data from CSV if it exists; otherwise, create an empty DataFrame
if os.path.exists(db_file):
    finance_data = pd.read_csv(db_file)
else:
    finance_data = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Notes"])

# Sidebar navigation
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
        import matplotlib.pyplot as plt
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
    show_add_expense(finance_data, db_file)

# Add Income Page
elif menu == "Add Income":
    show_add_income(finance_data, db_file)

# Settings Page
elif menu == "Settings":
    show_settings(finance_data, db_file)
