from __future__ import annotations

import csv
from pathlib import Path

from prompts import (
    prompt_amount,
    prompt_date,
    prompt_nonempty,
    prompt_optional_amount,
    prompt_optional_date,
    prompt_optional_nonempty,
    prompt_optional_type,
    prompt_type,
)
from storage import save_transactions


EXPORT_FILE = Path("transactions.csv")


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


def delete_transaction(transactions: list[dict]) -> None:
    print("\n=== Delete a Transaction ===")
    if not transactions:
        print("No transactions to delete.\n")
        return

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
                print("That number isn't in the list.")
                continue
        except ValueError:
            print("Enter a valid number, or 'c' to cancel.")
            continue

        to_delete = transactions_sorted[idx - 1]

        confirm = input(
            f"Delete '{to_delete.get('description', '')}' on {to_delete.get('date', '')}? (y/n): "
        ).strip().lower()
        if confirm != "y":
            print("Not deleted.\n")
            return

        transactions.remove(to_delete)
        save_transactions(transactions)
        print("🗑️ Deleted!\n")
        return


def edit_transaction(transactions: list[dict]) -> None:
    print("\n=== Edit a Transaction ===")
    if not transactions:
        print("No transactions to edit.\n")
        return

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
        choice = input("Enter the number to edit (or 'c' to cancel): ").strip().lower()
        if choice == "c":
            print("Canceled.\n")
            return

        try:
            idx = int(choice)
            if idx < 1 or idx > len(transactions_sorted):
                print("That number isn't in the list.")
                continue
        except ValueError:
            print("Enter a valid number, or 'c' to cancel.")
            continue

        t = transactions_sorted[idx - 1]

        current_date = str(t.get("date", ""))
        current_type = str(t.get("type", ""))
        current_category = str(t.get("category", ""))
        current_desc = str(t.get("description", ""))
        current_amount = float(t.get("amount", 0) or 0)

        print("\nPress Enter to keep the current value.")
        print(f"Current date       : {current_date}")
        print(f"Current type       : {current_type}")
        print(f"Current category   : {current_category}")
        print(f"Current description: {current_desc}")
        print(f"Current amount     : {current_amount:.2f}\n")

        new_date = prompt_optional_date(current_date)
        new_type = prompt_optional_type(current_type)
        new_category = prompt_optional_nonempty("Category [Enter to keep current]: ", current_category)
        new_desc = prompt_optional_nonempty("Description [Enter to keep current]: ", current_desc)
        new_amount = prompt_optional_amount(current_amount)

        confirm = input("Save changes? (y/n): ").strip().lower()
        if confirm != "y":
            print("Not saved.\n")
            return

        t["date"] = new_date
        t["type"] = new_type
        t["category"] = new_category
        t["description"] = new_desc
        t["amount"] = new_amount

        save_transactions(transactions)
        print("✏️ Updated!\n")
        return


def export_to_csv(transactions: list[dict]) -> None:
    print("\n=== Export to CSV ===")
    if not transactions:
        print("No transactions to export.\n")
        return

    transactions_sorted = sorted(transactions, key=lambda t: str(t.get("date", "")))
    fieldnames = ["date", "type", "category", "description", "amount"]

    try:
        with EXPORT_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for t in transactions_sorted:
                writer.writerow({
                    "date": t.get("date", ""),
                    "type": t.get("type", ""),
                    "category": t.get("category", ""),
                    "description": t.get("description", ""),
                    "amount": t.get("amount", ""),
                })

        print(f"✅ Exported {len(transactions_sorted)} transactions to {EXPORT_FILE}\n")
    except OSError as e:
        print(f"Could not write CSV file: {e}\n")
