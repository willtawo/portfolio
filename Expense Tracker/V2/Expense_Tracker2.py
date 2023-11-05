import sqlite3
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import graphviz
from collections import defaultdict

def create_expense_table():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        description TEXT,
        category TEXT,
        subcategory TEXT,
        amount REAL
    )
    ''')
    
    conn.commit()
    conn.close()

def create_budget_table():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        subcategory TEXT,
        amount REAL,
        period TEXT
    )
    ''')

    conn.commit()
    conn.close()

def delete_budget(budget_id):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM budgets WHERE id = ?', (budget_id,))
    conn.commit()
    conn.close()

def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    description = input("Enter description: ")
    category = input("Enter category: ")
    subcategory = input("Enter subcategory: ")
    amount = float(input("Enter amount: "))

    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO expenses (date, description, category, subcategory, amount)
    VALUES (?, ?, ?, ?, ?)
    ''', (date, description, category, subcategory, amount))

    conn.commit()
    conn.close()

    print("Expense added successfully!")

def get_expenses():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()

    conn.close()

    expense_list = []
    for expense in expenses:
        expense_dict = {
            "ID": expense[0],
            "Date": expense[1],
            "Description": expense[2],
            "Category": expense[3],
            "Subcategory": expense[4] if len(expense) > 4 else "",
            "Amount": expense[5] if len(expense) > 5 else 0.0,
        }
        expense_list.append(expense_dict)

    return expense_list


def set_budget():
    category = input("Enter category for the budget: ")
    subcategory = input("Enter subcategory (optional, press Enter to skip): ")
    amount = float(input("Enter budget amount: "))
    period = input("Enter budget period (monthly/weekly): ")

    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO budgets (category, subcategory, amount, period)
    VALUES (?, ?, ?, ?)
    ''', (category, subcategory, amount, period))

    conn.commit()
    conn.close()

    print("Budget set successfully!")

def get_budgets():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM budgets')
    budgets = cursor.fetchall()

    conn.close()

    budget_list = []
    for budget in budgets:
        budget_dict = {
            "ID": budget[0],
            "Category": budget[1],
            "Subcategory": budget[2] if len(budget) > 2 else "",  # Check if subcategory exists
            "Amount": budget[3] if len(budget) > 3 else 0.0,  # Check if amount exists
            "Period": budget[4] if len(budget) > 4 else ""  # Check if period exists
        }
        budget_list.append(budget_dict)

    return budget_list

def view_budgets():
    budgets = get_budgets()

    if not budgets:
        print("No budgets set.")
        return {}

    budget_dict = {}
    for budget in budgets:
        category = budget["Category"]
        amount = budget["Amount"]
        budget_dict[category] = amount

        id = budget["ID"]
        subcategory = budget["Subcategory"]
        period = budget["Period"]
        if isinstance(amount, float):
            amount_str = f"${amount:.2f}"
        else:
            amount_str = str(amount)

        print("{:<5} {:<20} {:<20} {:<10} {:<10}".format(id, category, subcategory, amount_str, period))

    return budget_dict

def view_expenses(expenses):
    if not expenses:
        print("No expenses to display.")
    else:
        print("Expense List:")
        print("{:<5} {:<12} {:<20} {:<15} {:<15} {:<10}".format("ID", "Date", "Description", "Category", "Subcategory", "Amount"))
        print("-" * 80)
        for expense in expenses:
            id = expense["ID"]
            date = expense["Date"]
            description = expense["Description"]
            category = expense["Category"]
            subcategory = expense["Subcategory"]
            amount = expense["Amount"]
            print("{:<5} {:<12} {:<20} {:<15} {:<15} ${:.2f}".format(id, date, description, category, subcategory, amount))


def edit_expense():
    expense_id = int(input("Enter the ID of the expense to edit: "))

    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,))
    expense = cursor.fetchone()

    if not expense:
        print("Expense not found.")
        conn.close()
        return

    print("Current Expense Details:")
    print(f"Date: {expense[1]}")
    print(f"Description: {expense[2]}")
    print(f"Category: {expense[3]}")
    print(f"Subcategory: {expense[4]}")
    print(f"Amount: ${expense[5]:.2f}")

    date = input("Enter new date (YYYY-MM-DD): ")
    description = input("Enter new description: ")
    category = input("Enter new category: ")
    subcategory = input("Enter new subcategory: ")
    amount = float(input("Enter new amount: "))

    cursor.execute('''
    UPDATE expenses
    SET date = ?, description = ?, category = ?, subcategory = ?, amount = ?
    WHERE id = ?
    ''', (date, description, category, subcategory, amount, expense_id))

    conn.commit()
    conn.close()

    print("Expense updated successfully!")

def delete_expense():
    expense_id = int(input("Enter the ID of the expense to delete: "))

    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,))
    expense = cursor.fetchone()

    if not expense:
        print("Expense not found.")
        conn.close()
        return

    print("Expense Details:")
    print(f"Date: {expense[1]}")
    print(f"Description: {expense[2]}")
    print(f"Category: {expense[3]}")
    print (f"Subcategory: {expense[4]}")
    print(f"Amount: ${expense[5]:.2f}")

    confirm = input("Are you sure you want to delete this expense? (yes/no): ")

    if confirm.lower() == "yes":
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()
        print("Expense deleted successfully.")
    else:
        print("Expense deletion canceled.")
        
def generate_report(expenses, budgets):
    if not expenses:
        print("No expenses to generate a report for.")
        return

    print("Expense Report:")
    print("{:<5} {:<12} {:<20} {:<15} {:<15} {:<10}".format("ID", "Date", "Description", "Category", "Subcategory", "Amount"))
    print("-" * 80)

    total_expenses = {}
    
    for expense in expenses:
        id = expense["ID"]
        date = expense["Date"]
        description = expense["Description"]
        category = expense["Category"]
        subcategory = expense["Subcategory"]
        amount = expense["Amount"]
        
        # Update total expenses for the category
        if category in total_expenses:
            total_expenses[category] += amount
        else:
            total_expenses[category] = amount
        
        print("{:<5} {:<12} {:<20} {:<15} {:<15} ${:.2f}".format(id, date, description, category, subcategory, amount))
        
    print("{:<15} {:<20}".format("Category", "Total Expenses"))
    print("-" * 55)
    for category in total_expenses:
        total_expense = total_expenses[category]
        print("{:<15} ${:.2f}".format(category, total_expense))



        
def set_monthly_income_biweekly():
    # Prompt the user for the monthly income amount
    income = float(input("Enter your monthly income amount: "))

    # Calculate the biweekly income by dividing the monthly income by 2
    biweekly_income = income / 2

    # Add the biweekly income to the database
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO budgets (category, subcategory, amount, period)
    VALUES (?, ?, ?, ?)
    ''', ("Income", "Biweekly", biweekly_income, "biweekly"))

    conn.commit()
    conn.close()

    print(f"Biweekly income set successfully: ${biweekly_income:.2f} per biweek.")
    
def view_monthly_income():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    cursor.execute('SELECT amount FROM budgets WHERE category = "Income" AND subcategory = "Biweekly"')
    biweekly_income = cursor.fetchone()

    if not biweekly_income:
        print("Monthly income not set.")
    else:
        monthly_income = biweekly_income[0] * 2  # Assuming biweekly income, you can adjust as needed
        print(f"Monthly Income: ${monthly_income:.2f}")

    conn.close()

    
def view_remaining_budgets(expenses, budgets):
    if not expenses:
        print("No expenses to calculate remaining budget.")
        return

    remaining_budgets = {}

    for expense in expenses:
        category = expense["Category"]
        amount = expense["Amount"]

        # Update remaining budget for the category
        if category in remaining_budgets:
            remaining_budgets[category] -= amount
        else:
            remaining_budgets[category] = -amount

    for category, budget_amount in budgets.items():
        if category in remaining_budgets:
            remaining_budgets[category] += budget_amount
        else:
            remaining_budgets[category] = budget_amount

    print("\nRemaining Budget by Category:")
    print("{:<15} {:<15}".format("Category", "Remaining Budget"))
    print("-" * 30)

    for category, remaining_budget in remaining_budgets.items():
        print("{:<15} ${:.2f}".format(category, remaining_budget))
        
def export_report_to_pdf(expenses, file_name):
    c = canvas.Canvas(file_name, pagesize=letter)

    # Define the report content here
    c.drawString(100, 750, "Expense Report")
    c.drawString(100, 730, "ID  Date       Description                Category   Subcategory   Amount")

    y = 710  # Initial Y coordinate for the content
    for expense in expenses:
        id = expense["ID"]
        date = expense["Date"]
        description = expense["Description"]
        category = expense["Category"]
        subcategory = expense["Subcategory"]
        amount = expense["Amount"]

        content = f"{id}  {date}  {description}  {category}  {subcategory}  {amount}"
        c.drawString(100, y, content)

        y -= 20  # Adjust the Y coordinate for the next line

    c.showPage()
    c.save()

    print(f"Expense report exported to {file_name} successfully.")



def export_report_to_excel(expenses, file_name):
    if not expenses:
        print("No expenses to export.")
        return

    df = pd.DataFrame(expenses)
    df.to_excel(file_name, index=False)

    print(f"Expense report exported to {file_name} successfully.")
    
def view_estimated_monthly_balance(expenses, budgets):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    cursor.execute('SELECT amount FROM budgets WHERE category = "Income" AND subcategory = "Biweekly"')
    biweekly_income = cursor.fetchone()

    if not biweekly_income:
        print("Monthly income not set.")
        conn.close()
        return

    biweekly_income = biweekly_income[0]
    monthly_income = biweekly_income * 2  # Assuming biweekly income, you can adjust as needed

    total_expenses = sum(expense["Amount"] for expense in expenses)
    estimated_monthly_balance = monthly_income - total_expenses

    print(f"Estimated Monthly Income: ${monthly_income:.2f}")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Estimated Monthly Balance: ${estimated_monthly_balance:.2f}")

    conn.close()
    
    
def visualize_expense_distribution_tree(expenses):
    if not expenses:
        print("No expenses to visualize.")
        return

    # Create a hierarchical tree structure using defaultdict
    tree = defaultdict(lambda: defaultdict(float))

    for expense in expenses:
        category = expense["Category"]
        subcategory = expense.get("Subcategory", "None")
        amount = expense["Amount"]
        
        # Update the tree structure with amounts
        tree[category][subcategory] += amount

    # Create a Graphviz graph
    dot = graphviz.Digraph(comment='Expense Distribution', format='png')

    # Traverse the tree and add nodes and edges to the graph
    for category, subcategories in tree.items():
        dot.node(category, label=category)
        for subcategory, amount in subcategories.items():
            dot.node(subcategory, label=f"{subcategory}\n(${amount:.2f})")
            dot.edge(category, subcategory)
            
    # Render and save the graph
    dot.render("expense_distribution_tree")
    print("Expense distribution tree visualization saved as 'expense_distribution_tree.png'")



def main():
    create_expense_table()
    create_budget_table()
    budgets = {}
    
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. Edit Expense")
        print("3. Delete Expense")
        print("4. View Expenses")
        print("5. Generate Report")
        print("6. Visualize Expense Distribution (Tree Diagram)")
        print("7. Export Expense Report to PDF")
        print("8. Export Expense Report to Excel")
        print("9. Set Budget")
        print("10. View Budgets")
        print("11. Delete Budget")
        print("12. Set Monthly Income (Biweekly)")
        print("13. View Monthly Income")
        print("14. View Remaining Budget")
        print("15. View Estimated Monthly Balance")
        print("16. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            edit_expense()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            expenses = get_expenses()
            view_expenses(expenses)
        elif choice == "5":
            expenses = get_expenses()
            generate_report(expenses, budgets)
        elif choice == "6":
            expenses = get_expenses()
            visualize_expense_distribution_tree(expenses)
        elif choice == "7":
            expenses = get_expenses()
            export_report_to_pdf(expenses, "expense_report.pdf")
        elif choice == "8":
            expenses = get_expenses()
            export_report_to_excel(expenses, "expense_report.xlsx")
        elif choice == "9":
            set_budget()
        elif choice == "10":
            view_budgets()
        elif choice == "11":
            budget_id = int(input("Enter the ID of the budget to delete: "))
            delete_budget(budget_id)
            print("Budget deleted successfully.")
        elif choice == "12":
            set_monthly_income_biweekly()
        elif choice == "13":
            view_monthly_income()
        elif choice == "14":
            expenses = get_expenses()
            view_remaining_budgets(expenses, budgets)
        elif choice == "15":
            view_estimated_monthly_balance(expenses, budgets)
        elif choice == "16":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()