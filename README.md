# Budget Lite (CLI)

A lightweight personal finance tracker built in Python.  
Users can record income and expenses, view summaries, filter by month, and export transactions to CSV.

This project represents the CLI foundation of a larger web-based budgeting system.

---

## Why This Project

This project was built to strengthen file handling, modular architecture, and CRUD logic in Python before transitioning the application into a Django web app.

---

## Features

- Add income and expense transactions
- Edit existing transactions
- Delete transactions
- View all transactions (sorted by date)
- Filter transactions by month (YYYY-MM)
- View summary (total income, total expenses, net)
- View category totals (income or expense)
- Export transactions to CSV
- Persistent storage using JSON file handling
- Modular architecture (storage, prompts, reports, actions)

---

## Project Structure
budget-lite-cli/
│
├── budget.py # Main entry point / CLI loop
├── storage.py # JSON load/save logic
├── prompts.py # Input validation helpers
├── reports.py # Reporting + summaries
├── actions.py # CRUD operations + export
├── data.json # Local storage file
└── .gitignore

---

## How to Run

Clone the repository:

```bash
git clone https://github.com/ryancoderjackson/budget-lite-cli.git
cd budget-lite-cli
# Run the application
python budget.py