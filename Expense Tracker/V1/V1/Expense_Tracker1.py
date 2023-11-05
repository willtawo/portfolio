import sqlite3
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
#########################################################################################
def create_expense_table():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        description TEXT,
        category TEXT,
        amount REAL
    )
    ''')
    
    conn.commit()
    conn.close()
############################################################################################

def create_budget_table():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        amount REAL,
        period TEXT
    )
    ''')

    conn.commit()
    conn.close()
############################################################################################
def add_expense():
    # Prompt the user for expense details
    date = input("Enter date (YYYY-MM-DD): ")
    description = input("Enter description: ")
    category = input("Enter category: ")
    amount = float(input("Enter amount: "))

    # Add the expense to the database
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO expenses (date, description, category, amount)
    VALUES (?, ?, ?, ?)
    ''', (date, description, category, amount))

    conn.commit()
    conn.close()

    print("Expense added successfully!")

############################################################################################

def get_expenses():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    
    conn.close()
    
    # Convert the list of tuples to a list of dictionaries
    expense_list = []
    for expense in expenses:
        expense_dict = {
            "Date": expense[1],
            "Description": expense[2],
            "Category": expense[3],
            "Amount": expense[4]
        }
        expense_list.append(expense_dict)

    return expense_list

############################################################################################
def set_budget():
    category = input("Enter category for the budget: ")
    amount = float(input("Enter budget amount: "))
    period = input("Enter budget period (monthly/weekly): ")

    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO budgets (category, amount, period)
    VALUES (?, ?, ?)
    ''', (category, amount, period))

    conn.commit()
    conn.close()

    print("Budget set successfully!")
###############################################################################################
def get_budgets():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM budgets')
    budgets = cursor.fetchall()

    conn.close()

    return budgets
###########################################################################################
def view_expenses(expenses):
    if not expenses:
        print("No expenses to display.")
    else:
        print("Expense List:")
        print("{:<12} {:<20} {:<15} {:<10}".format("Date", "Description", "Category", "Amount"))
        print("-" * 57)
        for expense in expenses:
            date = expense["Date"]
            description = expense["Description"]
            category = expense["Category"]
            amount = expense["Amount"]
            print("{:<12} {:<20} {:<15} ${:<10.2f}".format(date, description, category, amount))
            
############################################################################################

def generate_report(expenses):
    print("Generate Report:")
    print("1. Expense Summary by Category")
    print("2. Filter Expenses by Date Range")
    
    choice = input("Enter your choice (1/2): ")
    
    if choice == "1":
        expense_summary_by_category(expenses)
    elif choice == "2":
        filter_expenses_by_date_range(expenses)
    else:
        print("Invalid choice. Please enter 1 or 2.")
############################################################################################

def expense_summary_by_category(expenses):
    category_summary = {}
    
    for expense in expenses:
        category = expense["Category"]
        amount = expense["Amount"]
        if category in category_summary:
            category_summary[category] += amount
        else:
            category_summary[category] = amount
    
    if not category_summary:
        print("No expenses to summarize.")
    else:
        print("Expense Summary by Category:")
        for category, total_amount in category_summary.items():
            print(f"{category}: ${total_amount:.2f}")
############################################################################################

def filter_expenses_by_date_range(expenses):
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    
    filtered_expenses = []
    
    for expense in expenses:
        date = expense["Date"]
        if start_date <= date <= end_date:
            filtered_expenses.append(expense)
    
    if not filtered_expenses:
        print("No expenses found within the specified date range.")
    else:
        print("Expenses within Date Range:")
        view_expenses(filtered_expenses)  # Reuse the view_expenses function
############################################################################################
       
def visualize_expense_distribution(expenses):
    category_summary = {}

    for expense in expenses:
        category = expense["Category"]
        amount = expense["Amount"]
        if category in category_summary:
            category_summary[category] += amount
        else:
            category_summary[category] = amount

    if not category_summary:
        print("No expenses to visualize.")
        return

    # Create a pie chart to visualize expense distribution by category
    labels = category_summary.keys()
    sizes = category_summary.values()
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution by Category')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

############################################################################################
def export_report_to_pdf(expenses, filename):
    if not expenses:
        print("No expenses to export.")
        return

    # Create a PDF document
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Expense Report")

    y = 720
    for expense in expenses:
        y -= 20
        c.drawString(100, y, f"Date: {expense['Date']}")
        c.drawString(200, y, f"Description: {expense['Description']}")
        c.drawString(350, y, f"Category: {expense['Category']}")
        c.drawString(450, y, f"Amount: ${expense['Amount']:.2f}")

    c.save()
    print(f"Expense report exported as '{filename}' (PDF).")
#############################################################################################
def export_report_to_excel(expenses, filename):
    if not expenses:
        print("No expenses to export.")
        return

    # Create a DataFrame from the expense data
    df = pd.DataFrame(expenses)

    # Create an Excel writer and save the DataFrame to an Excel file
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Expense Report', index=False)

    # Close the Excel writer and print a success message
    writer.save()
    print(f"Expense report exported as '{filename}' (Excel).")
############################################################################################
def view_budgets():
    budgets = get_budgets()
    
    if not budgets:
        print("No budgets set.")
        return
    
    print("Budgets:")
    print("{:<20} {:<10} {:<10}".format("Category", "Amount", "Period"))
    print("-" * 45)
    
    for budget in budgets:
        category = budget[1]
        amount = budget[2]
        period = budget[3]
        print("{:<20} ${:<10.2f} {:<10}".format(category, amount, period))

############################################################################################

def edit_expense():
    # Prompt the user for the ID of the expense to edit
    expense_id = int(input("Enter the ID of the expense to edit: "))

    # Retrieve the current details of the expense from the database
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
    print(f"Amount: ${expense[4]:.2f}")

    # Prompt the user to update the expense details
    date = input("Enter new date (YYYY-MM-DD): ")
    description = input("Enter new description: ")
    category = input("Enter new category: ")
    amount = float(input("Enter new amount: "))

    # Update the expense details in the database
    cursor.execute('''
    UPDATE expenses
    SET date = ?, description = ?, category = ?, amount = ?
    WHERE id = ?
    ''', (date, description, category, amount, expense_id))

    conn.commit()
    conn.close()

    print("Expense updated successfully!")
    
###########################################################################################

def delete_expense():
    # Prompt the user for the ID of the expense to delete
    expense_id = int(input("Enter the ID of the expense to delete: "))

    # Retrieve the current details of the expense from the database
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
    print(f"Amount: ${expense[4]:.2f}")

    # Ask for confirmation before deleting the expense
    confirm = input("Are you sure you want to delete this expense? (yes/no): ")

    if confirm.lower() == "yes":
        # Delete the expense from the database
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()
        print("Expense deleted successfully.")
    else:
        print("Expense deletion canceled.")

############################################################################################
def main():
    create_expense_table()  # Initialize the database
    create_budget_table()  # Create the budgets table
    
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Generate Report")
        print("4. Visualize Expense Distribution")
        print("5. Export Expense Report to PDF")
        print("6. Export Expense Report to Excel")
        print("7. Set Budget")
        print("8. View Budget")
        print("9. Edit Expense")
        print("10. Delete Expense")
        print("11. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            expenses = get_expenses()  # Retrieve expenses from the database
            view_expenses(expenses)
        elif choice == "3":
            expenses = get_expenses()  # Retrieve expenses from the database
            generate_report(expenses)
        elif choice == "4":
            expenses = get_expenses()  # Retrieve expenses from the database
            visualize_expense_distribution(expenses)
        elif choice == "5":
            expenses = get_expenses()  # Retrieve expenses from the database
            export_report_to_pdf(expenses, "expense_report.pdf")
        elif choice == "6":
            expenses = get_expenses()  # Retrieve expenses from the database
            export_report_to_excel(expenses, "expense_report.xlsx")
        elif choice == "7":
            set_budget()
        elif choice == "8":
            view_budgets()
        elif choice == "9":
            edit_expense()
        elif choice == "10":
            delete_expense()
        elif choice == "11":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()




