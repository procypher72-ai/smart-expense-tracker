import os
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CATEGORIES = ["Food", "Transport", "Utilities", "Entertainment"]


class ExpenseTracker:
    def __init__(self, filename="expenses.csv"):
        self.filename = filename
        self.data = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename):
            self.data = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
            return

        try:
            df = pd.read_csv(self.filename)

            # Data cleaning: handle missing values and invalid rows
            df = df.dropna(subset=["Date", "Amount", "Category"])
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
            df = df[df["Amount"] > 0]
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df = df.dropna(subset=["Date"])
            df["Category"] = df["Category"].astype(str).str.strip()

            self.data = df.sort_values(by="Date").reset_index(drop=True)
        except Exception as e:
            print(f"Error loading file: {e}")
            self.data = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])

    def save_data(self):
        export_df = self.data.copy()
        export_df["Date"] = export_df["Date"].dt.strftime("%Y-%m-%d")
        export_df.to_csv(self.filename, index=False)

    def add_expense(self, date, amount, category, description):
        parsed_date = pd.to_datetime(date)
        new_row = pd.DataFrame([{
            "Date": parsed_date,
            "Amount": float(amount),
            "Category": category,
            "Description": description
        }])

        self.data = pd.concat([self.data, new_row], ignore_index=True)
        self.data = self.data.sort_values(by="Date").reset_index(drop=True)
        self.save_data()
        print("Expense added successfully.")

    def get_summary(self):
        if self.data.empty:
            print("No expenses recorded yet.")
            return {}

        # Calculations using NumPy arrays
        amounts = np.array(self.data["Amount"].values, dtype=float)
        total_expense = float(np.sum(amounts))
        avg_expense = float(np.mean(amounts))
        count = len(amounts)

        summary = {
            "total": total_expense,
            "average": avg_expense,
            "count": count
        }

        print("\n--- Expense Summary ---")
        print(f"Total Transactions : {count}")
        print(f"Total Spent        : ${total_expense:,.2f}")
        print(f"Average Expense    : ${avg_expense:,.2f}")

        # Category totals using Pandas & NumPy
        cat_group = self.data.groupby("Category")["Amount"].sum()
        cat_totals = np.array(cat_group.values)
        cat_names = cat_group.index.tolist()

        print("\nCategory-wise Breakdown:")
        for name, val in zip(cat_names, cat_totals):
            print(f"  {name:<15}: ${val:,.2f}")

        return summary

    def filter_expenses(self, condition):
        if self.data.empty:
            return self.data

        filtered = self.data.copy()

        if isinstance(condition, dict):
            if "category" in condition and condition["category"]:
                cat = condition["category"].lower()
                filtered = filtered[filtered["Category"].str.lower() == cat]

            if "start_date" in condition and condition["start_date"]:
                filtered = filtered[filtered["Date"] >= pd.to_datetime(condition["start_date"])]

            if "end_date" in condition and condition["end_date"]:
                filtered = filtered[filtered["Date"] <= pd.to_datetime(condition["end_date"])]

            if "min_amount" in condition and condition["min_amount"] is not None:
                filtered = filtered[filtered["Amount"] >= float(condition["min_amount"])]

            if "max_amount" in condition and condition["max_amount"] is not None:
                filtered = filtered[filtered["Amount"] <= float(condition["max_amount"])]

        elif isinstance(condition, str):
            filtered = filtered[filtered["Category"].str.lower() == condition.lower()]

        return filtered

    def generate_report(self):
        if self.data.empty:
            print("No expense data available to generate report.")
            return

        amounts = np.array(self.data["Amount"].values, dtype=float)
        total_spending = np.sum(amounts)

        print("\n" + "=" * 45)
        print("         FINANCIAL SUMMARY REPORT")
        print("=" * 45)
        print(f"Total Spending       : ${total_spending:,.2f}")
        print(f"Average Spending     : ${np.mean(amounts):,.2f}")
        print(f"Highest Expense      : ${np.max(amounts):,.2f}")
        print(f"Lowest Expense       : ${np.min(amounts):,.2f}")
        print("-" * 45)

        # Spending percentage by category using NumPy array operations
        cat_spending = self.data.groupby("Category")["Amount"].sum()
        cat_array = np.array(cat_spending.values)
        percentages = (cat_array / total_spending) * 100

        print("Spending Percentage by Category:")
        for category, amount, pct in zip(cat_spending.index, cat_array, percentages):
            print(f"  {category:<14}: ${amount:>8.2f} ({pct:>5.1f}%)")

        top_category = cat_spending.idxmax()
        top_cat_amount = cat_spending.max()
        print(f"\nTop Spending Category: {top_category} (${top_cat_amount:,.2f})")

        # Monthly aggregation
        temp_df = self.data.copy()
        temp_df["Month"] = temp_df["Date"].dt.strftime("%Y-%m")
        monthly_grouped = temp_df.groupby("Month")["Amount"].sum()
        monthly_avg_spending = np.mean(monthly_grouped.values)

        print(f"Monthly Average Spending: ${monthly_avg_spending:,.2f}")
        top_month = monthly_grouped.idxmax()
        print(f"Top Spending Period     : {top_month} (${monthly_grouped[top_month]:,.2f})")

        print("\nMonthly Breakdown:")
        for month, val in monthly_grouped.items():
            print(f"  {month} : ${val:,.2f}")
        print("=" * 45)

    def plot_category_bar(self):
        if self.data.empty:
            print("No data available to plot.")
            return

        cat_data = self.data.groupby("Category")["Amount"].sum().reset_index()

        plt.figure(figsize=(8, 5))
        sns.barplot(data=cat_data, x="Category", y="Amount", hue="Category", palette="Blues_d", legend=False)
        plt.title("Total Expenses by Category", fontsize=14, pad=12)
        plt.xlabel("Category", fontsize=11)
        plt.ylabel("Total Amount ($)", fontsize=11)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.show()

    def plot_trend_line(self):
        if self.data.empty:
            print("No data available to plot.")
            return

        daily_trend = self.data.groupby(self.data["Date"].dt.date)["Amount"].sum().reset_index()

        plt.figure(figsize=(10, 5))
        plt.plot(daily_trend["Date"], daily_trend["Amount"], marker="o", color="#2b5c8f", linewidth=2)
        plt.title("Spending Trends Over Time", fontsize=14, pad=12)
        plt.xlabel("Date", fontsize=11)
        plt.ylabel("Daily Spending ($)", fontsize=11)
        plt.xticks(rotation=45)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()

    def plot_category_pie(self):
        if self.data.empty:
            print("No data available to plot.")
            return

        cat_totals = self.data.groupby("Category")["Amount"].sum()

        plt.figure(figsize=(7, 7))
        colors = sns.color_palette("pastel")[0:len(cat_totals)]
        plt.pie(
            cat_totals.values,
            labels=cat_totals.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=colors,
            wedgeprops={"edgecolor": "white", "linewidth": 1.5}
        )
        plt.title("Proportional Spending Distribution by Category", fontsize=14, pad=12)
        plt.tight_layout()
        plt.show()

    def plot_amount_histogram(self):
        if self.data.empty:
            print("No data available to plot.")
            return

        plt.figure(figsize=(8, 5))
        sns.histplot(self.data["Amount"], bins=8, kde=True, color="#3470a3")
        plt.title("Frequency of Expense Amounts", fontsize=14, pad=12)
        plt.xlabel("Expense Amount ($)", fontsize=11)
        plt.ylabel("Frequency", fontsize=11)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.show()


def get_validated_date():
    while True:
        date_input = input("Enter date (YYYY-MM-DD) [Leave empty for today]: ").strip()
        if not date_input:
            return datetime.now().strftime("%Y-%m-%d")
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            return date_input
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def get_validated_amount():
    while True:
        val = input("Enter amount: ").strip()
        try:
            amount = float(val)
            if amount > 0:
                return amount
            print("Amount must be greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a numerical value.")


def get_validated_category():
    while True:
        print("\nAvailable Categories:")
        for idx, cat in enumerate(CATEGORIES, start=1):
            print(f"  {idx}. {cat}")
        choice = input("Select category number or type name: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]

        for cat in CATEGORIES:
            if cat.lower() == choice.lower():
                return cat

        print("Invalid category selected. Please choose from the list.")


def display_expenses_table(df):
    if df.empty:
        print("No matching expenses found.")
        return

    print("\n" + "-" * 72)
    print(f"{'Date':<12} | {'Category':<15} | {'Amount ($)':<10} | {'Description'}")
    print("-" * 72)
    for _, row in df.iterrows():
        date_str = row["Date"].strftime("%Y-%m-%d") if isinstance(row["Date"], pd.Timestamp) else str(row["Date"])
        print(f"{date_str:<12} | {row['Category']:<15} | {row['Amount']:>10.2f} | {row['Description']}")
    print("-" * 72)


def main():
    tracker = ExpenseTracker("expenses.csv")

    while True:
        print("\n==============================")
        print("   SMART EXPENSE TRACKER")
        print("==============================")
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. View Summary (Total & Avg)")
        print("4. Filter Expenses")
        print("5. Generate Financial Report")
        print("6. Data Visualizations")
        print("7. Exit")

        choice = input("\nEnter choice (1-7): ").strip()

        if choice == "1":
            date = get_validated_date()
            category = get_validated_category()
            amount = get_validated_amount()
            desc = input("Enter short description: ").strip()
            tracker.add_expense(date, amount, category, desc)

        elif choice == "2":
            display_expenses_table(tracker.data)

        elif choice == "3":
            tracker.get_summary()

        elif choice == "4":
            print("\nFilter by:")
            print("1. Category")
            print("2. Date Range")
            print("3. Amount Range")
            f_choice = input("Select option (1-3): ").strip()

            condition = {}
            if f_choice == "1":
                cat = get_validated_category()
                condition["category"] = cat
            elif f_choice == "2":
                start_d = input("Enter start date (YYYY-MM-DD): ").strip()
                end_d = input("Enter end date (YYYY-MM-DD): ").strip()
                condition["start_date"] = start_d
                condition["end_date"] = end_d
            elif f_choice == "3":
                min_a = input("Enter minimum amount (leave blank for none): ").strip()
                max_a = input("Enter maximum amount (leave blank for none): ").strip()
                if min_a:
                    condition["min_amount"] = float(min_a)
                if max_a:
                    condition["max_amount"] = float(max_a)

            results = tracker.filter_expenses(condition)
            display_expenses_table(results)

        elif choice == "5":
            tracker.generate_report()

        elif choice == "6":
            print("\nSelect Visualization:")
            print("1. Bar Chart (Expenses by Category)")
            print("2. Line Graph (Spending Trends Over Time)")
            print("3. Pie Chart (Spending Distribution)")
            print("4. Histogram (Frequency of Amounts)")
            v_choice = input("Enter choice (1-4): ").strip()

            if v_choice == "1":
                tracker.plot_category_bar()
            elif v_choice == "2":
                tracker.plot_trend_line()
            elif v_choice == "3":
                tracker.plot_category_pie()
            elif v_choice == "4":
                tracker.plot_amount_histogram()
            else:
                print("Invalid visualization choice.")

        elif choice == "7":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
