from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path


DATA_FILE = Path("data.json")


# ----------------------------
# File helpers
# ----------------------------

def load_transactions() -> list[dict]:
    if not DATA_FILE.exists():
        return []

    try:
        raw = DATA_FILE.read_text(encoding="utf-8").strip()
        if not raw:
            return []
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_transactions(transactions: list[dict]) -> None:
    DATA_FILE.write_text(json.dumps(transactions, indent=2), encoding="utf-8")


# ----------------------------
# Validation + input helpers
# ----------------------------

def prompt_nonempty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter something (can't be blank).")


def prompt_type() -> str:
    while True:
        value = input("Type (income/expense): ").strip().lower()
        if value in {"income", "expense"}:
            return value
        print("Type must be 'income' or 'expense'.")


def prompt_amount() -> float:
    while True:
        value = input("Amount (e.g., 12.50): ").strip()
        try:
            amount = float(value)
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Please enter a valid number (like 12.50).")


def prompt_date() -> str:
    while True:
        value = input("Date (YYYY-MM-DD) [Enter for today]: ").strip()
        if value == "":
            return datetime.today().strftime("%Y-%m-%d")

        try:
            dt = datetime.strptime(value, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD (example: 2026-02-05).")


# ----------------------------
# Core features
# ----------------------------

def add_transaction(transactions: list[dict]) -> None:
    print("\n=== Add Transaction ===")
    t_date = prompt_date()
    t_type = prompt_type()
    category = prompt_nonempty("Category (e.g., Food, Rent, Gas): ")
    description = prompt_nonempty("Description: ")
    amount = prompt_amount()

    transaction = {
        "date": t_date,
        "type": t_type,
        "category": category,
        "description": description,
        "amount": amount,
    }

    transactions.append(transaction)
    save_transactions(transactions)
    print("✅ Saved!\n")


def view_transactions(transactions: list[dict]) -> None:
    print("\n=== All Transactions ===")
    if not transactions:
        print("No transactions yet.\n")
        return

    # Sort by date (ascending)
    def sort_key(t: dict) -> str:
        return str(t.get("date", ""))

    transactions_sorted = sorted(transactions, key=sort_key)

    # Pretty display
    for i, t in enumerate(transactions_sorted, start=1):
        date = t.get("date", "????-??-??")
        t_type = t.get("type", "?")
        category = t.get("category", "")
        desc = t.get("description", "")
        amount = t.get("amount", 0)

        sign = "+" if t_type == "income" else "-"
        print(f"{i:>3}. {date} | {t_type:<7} | {category:<12} | {desc:<25} | {sign}${amount:.2f}")

    print()  # newline


def summary(transactions: list[dict]) -> None:
    print("\n=== Summary ===")
    income_total = 0.0
    expense_total = 0.0

    for t in transactions:
        t_type = t.get("type")
        amount = float(t.get("amount", 0) or 0)

        if t_type == "income":
            income_total += amount
        elif t_type == "expense":
            expense_total += amount

    net = income_total - expense_total

    print(f"Total Income : ${income_total:.2f}")
    print(f"Total Expense: ${expense_total:.2f}")
    print(f"Net          : ${net:.2f}\n")


def prompt_month() -> str:
    while True:
        value = input("Month (YYYY-MM), e.g. 2026-02: ").strip()
        try:
            datetime.strptime(value, "%Y-%m")
            return value
        except ValueError:
            print("Invalid month. Use YYYY-MM (example: 2026-02).")


def filter_by_month(transactions: list[dict]) -> None:
    print("\n=== Transactions by Month ===")
    if not transactions:
        print("No transactions yet.\n")
        return

    month = prompt_month()
    filtered = [t for t in transactions if str(t.get("date", "")).startswith(month)]

    if not filtered:
        print(f"No transactions found for {month}.\n")
        return

    # Use the same view formatting logic
    filtered_sorted = sorted(filtered, key=lambda t: str(t.get("date", "")))

    for i, t in enumerate(filtered_sorted, start=1):
        date = t.get("date", "????-??-??")
        t_type = t.get("type", "?")
        category = t.get("category", "")
        desc = t.get("description", "")
        amount = float(t.get("amount", 0) or 0)

        sign = "+" if t_type == "income" else "-"
        print(f"{i:>3}. {date} | {t_type:<7} | {category:<12} | {desc:<25} | {sign}${amount:.2f}")

    print()


def category_totals(transactions: list[dict]) -> None:
    print("\n=== Category Totals ===")
    if not transactions:
        print("No transactions yet.\n")
        return

    t_type = prompt_type()

    totals: dict[str, float] = {}
    for t in transactions:
        if t.get("type") != t_type:
            continue
        category = str(t.get("category", "Uncategorized")).strip() or "Uncategorized"
        amount = float(t.get("amount", 0) or 0)
        totals[category] = totals.get(category, 0.0) + amount

    if not totals:
        print(f"No {t_type} transactions to total.\n")
        return

    # Sort categories by total descending
    for cat, total in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        print(f"{cat:<15} ${total:.2f}")

    grand_total = sum(totals.values())
    print("-" * 26)
    print(f"{'TOTAL':<15} ${grand_total:.2f}\n")


def delete_transaction(transactions: list[dict]) -> None:
    print("\n=== Delete a Transaction ===")
    if not transactions:
        print("No transactions to delete.\n")
        return

    # Display current list in a stable order
    transactions_sorted = sorted(transactions, key=lambda t: str(t.get("date", "")))

    for i, t in enumerate(transactions_sorted, start=1):
        date = t.get("date", "????-??-??")
        t_type = t.get("type", "?")
        category = t.get("category", "")
        desc = t.get("description", "")
        amount = float(t.get("amount", 0) or 0)
        sign = "+" if t_type == "income" else "-"
        print(f"{i:>3}. {date} | {t_type:<7} | {category:<12} | {desc:<25} | {sign}${amount:.2f}")

    while True:
        choice = input("Enter the number to delete (or 'c' to cancel): ").strip().lower()
        if choice == "c":
            print("Canceled.\n")
            return

        try:
            idx = int(choice)
            if idx < 1 or idx > len(transactions_sorted):
                print("That number isn’t in the list.")
                continue
        except ValueError:
            print("Enter a valid number, or 'c' to cancel.")
            continue

        to_delete = transactions_sorted[idx - 1]

        confirm = input(f"Delete '{to_delete.get('description', '')}' on {to_delete.get('date', '')}? (y/n): ").strip().lower()
        if confirm != "y":
            print("Not deleted.\n")
            return

        # Remove the matching dict from the original list and save
        transactions.remove(to_delete)
        save_transactions(transactions)
        print("🗑️ Deleted!\n")
        return



# ----------------------------
# CLI loop
# ----------------------------

def menu() -> str:
    print("=== Budget Lite v2 ===")
    print("1) Add transaction")
    print("2) View all transactions")
    print("3) View summary")
    print("4) View transactions by month")
    print("5) Category totals (income/expense)")
    print("6) Delete a transaction")
    print("7) Exit")
    return input("Choose an option (1-7): ").strip()


def main() -> None:
    transactions = load_transactions()

    while True:
        choice = menu()
        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            view_transactions(transactions)
        elif choice == "3":
            summary(transactions)
        elif choice == "4":
            filter_by_month(transactions)
        elif choice == "5":
            category_totals(transactions)
        elif choice == "6":
            delete_transaction(transactions)
        elif choice == "7":
            print("Later, accountant. 👋")
            break
        else:
            print("Pick a number from the menu (1-7).\n")


if __name__ == "__main__":
    main()
