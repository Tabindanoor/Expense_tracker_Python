import csv
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt

# Constants
EXPENSES_FILE = 'expenses.csv'
CATEGORIES = ['Food', 'Transportation', 'Entertainment', 'Utilities', 'Other']

# Function to add an expense
def add_expense(date, category, amount):
    with open(EXPENSES_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount])
    print(f"Expense added: {date}, {category}, ${amount}")

# Function to load expenses into a DataFrame
def load_expenses():
    try:
        df = pd.read_csv(EXPENSES_FILE, names=['Date', 'Category', 'Amount'])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Category', 'Amount'])

# Function to view all expenses in CLI
def view_expenses_cli():
    df = load_expenses()
    if df.empty:
        print("No expenses found.")
    else:
        print(df.to_string(index=False))

# Function to generate summary report in CLI
def generate_report_cli():
    df = load_expenses()
    if df.empty:
        print("No expenses to summarize.")
        return
    
    summary = df.groupby('Category')['Amount'].sum()
    total = df['Amount'].sum()
    
    print("Expense Summary:")
    for category, amount in summary.items():
        print(f"{category}: ${amount:.2f}")
    print(f"Total: ${total:.2f}")

    summary.plot(kind='bar', title='Expenses by Category')
    plt.ylabel('Amount ($)')
    plt.xlabel('Category')
    plt.show()

# CLI Interface
def cli_interface():
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Generate Report")
        print("4. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            category = input(f"Enter category ({', '.join(CATEGORIES)}): ")
            amount = input("Enter amount: $")
            try:
                amount = float(amount)
                add_expense(date, category, amount)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        elif choice == '2':
            view_expenses_cli()
        elif choice == '3':
            generate_report_cli()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# GUI Interface
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # Style Configuration
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 12), padding=10)
        self.style.configure('TButton', font=('Helvetica', 12), padding=5)
        self.style.configure('TEntry', padding=10, relief='solid', borderwidth=1)
        self.style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'), foreground='blue')
        self.style.configure('Treeview', font=('Helvetica', 10), rowheight=25)
        
        self.root.configure(bg='#f0f0f0')

        # Date Input
        self.date_label = ttk.Label(root, text="Date (YYYY-MM-DD):")
        self.date_label.pack(pady=5)
        self.date_entry = ttk.Entry(root)
        self.date_entry.pack(pady=5)

        # Category Input
        self.category_label = ttk.Label(root, text="Category:")
        self.category_label.pack(pady=5)
        self.category_entry = ttk.Entry(root)
        self.category_entry.pack(pady=5)

        # Amount Input
        self.amount_label = ttk.Label(root, text="Amount:")
        self.amount_label.pack(pady=5)
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.pack(pady=5)

        # Add Expense Button
        self.add_button = ttk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.pack(pady=10)

        # View Expenses Button
        self.view_button = ttk.Button(root, text="View Expenses", command=self.view_expenses)
        self.view_button.pack(pady=10)

        # Generate Report Button
        self.report_button = ttk.Button(root, text="Generate Report", command=self.generate_report)
        self.report_button.pack(pady=10)

        # Treeview for displaying expenses
        self.expenses_tree = ttk.Treeview(root, columns=('Date', 'Category', 'Amount'), show='headings')
        self.expenses_tree.heading('Date', text='Date')
        self.expenses_tree.heading('Category', text='Category')
        self.expenses_tree.heading('Amount', text='Amount')
        self.expenses_tree.pack(pady=20)

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        if date and category and amount:
            try:
                amount = float(amount)
                add_expense(date, category, amount)
                messagebox.showinfo("Success", "Expense added successfully")
                self.date_entry.delete(0, tk.END)
                self.category_entry.delete(0, tk.END)
                self.amount_entry.delete(0, tk.END)
                self.view_expenses()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")
        else:
            messagebox.showerror("Error", "All fields are required")

    def view_expenses(self):
        df = load_expenses()
        for row in self.expenses_tree.get_children():
            self.expenses_tree.delete(row)
        for index, row in df.iterrows():
            self.expenses_tree.insert('', 'end', values=(row['Date'], row['Category'], row['Amount']))

    def generate_report(self):
        df = load_expenses()
        if df.empty:
            messagebox.showinfo("Info", "No expenses to summarize")
            return
        
        summary = df.groupby('Category')['Amount'].sum()
        total = df['Amount'].sum()
        
        summary_text = "Expense Summary:\n"
        for category, amount in summary.items():
            summary_text += f"{category}: ${amount:.2f}\n"
        summary_text += f"Total: ${total:.2f}"

        messagebox.showinfo("Expense Summary", summary_text)

        # Plotting the summary
        summary.plot(kind='bar', title='Expenses by Category')
        plt.ylabel('Amount ($)')
        plt.xlabel('Category')
        plt.show()

# Main function to choose between CLI and GUI
def main():
    while True:
        print("Choose Interface:")
        print("1. Command-Line Interface (CLI)")
        print("2. Graphical User Interface (GUI)")
        print("3. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            cli_interface()
        elif choice == '2':
            root = tk.Tk()
            app = ExpenseTrackerApp(root)
            root.mainloop()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
