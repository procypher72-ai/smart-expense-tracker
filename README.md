# Smart Expense Tracker Application

A Python-based command-line expense tracker application that helps users log, manage, and analyze daily expenses with data visualization.

---

## Features

- **Expense Input & Validation**: Add expenses with date, amount, category, and description. Validates date format, positive amounts, and predefined categories.
- **Data Management**: Uses Pandas for loading, cleaning, filtering, and persisting records in `expenses.csv`.
- **Calculations & Metrics**: Uses NumPy for numerical operations including totals, averages, and spending percentages.
- **Reporting**: Generates summary reports detailing total expenditure, category breakdown, monthly averages, and top spending categories/periods.
- **Visualizations**: Matplotlib and Seaborn graphs:
  - Bar Chart: Total expenses by category
  - Line Graph: Daily spending trends over time
  - Pie Chart: Proportional spending distribution by category
  - Histogram: Distribution and frequency of expense amounts

---

## Dataset Structure

The project stores records in `expenses.csv` with the following columns:

| Column | Format / Description | Example |
| :--- | :--- | :--- |
| `Date` | YYYY-MM-DD | 2024-01-05 |
| `Amount` | Positive floating point number | 45.50 |
| `Category` | Food, Transport, Utilities, Entertainment | Food |
| `Description` | Short text note | Groceries at supermarket |

---

## Prerequisites & Installation

Ensure you have Python 3.8+ installed. Install the required libraries using pip:

```bash
pip install numpy pandas matplotlib seaborn
```

---

## Running the Application

Execute the Python script from the project folder:

```bash
python expense_tracker.py
```

### Menu Options

1. **Add New Expense**: Prompts for date, category, amount, and description with input validation.
2. **View All Expenses**: Displays all recorded transactions in a formatted table.
3. **View Summary**: Displays total transaction count, total spending, average expense, and category totals.
4. **Filter Expenses**: Filter by Category, Date Range (start and end dates), or Amount range.
5. **Generate Financial Report**: Displays high-level analytics, category percentage share, top categories, and monthly averages.
6. **Data Visualizations**: Select and view Bar, Line, Pie, or Histogram plots.
7. **Exit**: Saves any changes and terminates the application.
