from __future__ import annotations

from actions import add_transaction, delete_transaction, edit_transaction, export_to_csv
from reports import category_totals, filter_by_month, summary, view_transactions
from storage import load_transactions


def menu() -> str:
    print("=== Budget Lite (Phase B) ===")
    print("1) Add transaction")
    print("2) View all transactions")
    print("3) View summary")
    print("4) View transactions by month")
    print("5) Category totals (income/expense)")
    print("6) Delete a transaction")
    print("7) Edit a transaction")
    print("8) Export to CSV")
    print("9) Exit")
    return input("Choose an option (1-9): ").strip()


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
            edit_transaction(transactions)
        elif choice == "8":
            export_to_csv(transactions)
        elif choice == "9":
            print("Later, accountant. 👋")
            break
        else:
            print("Pick a number from the menu.\n")


if __name__ == "__main__":
    main()
