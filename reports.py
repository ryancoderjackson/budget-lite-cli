from __future__ import annotations

from prompts import prompt_month, prompt_type


def view_transactions(transactions: list[dict]) -> None:
    print("\n=== All Transactions ===")
    if not transactions:
        print("No transactions yet.\n")
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

    print()


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

    t_type = prompt_type()  # income or expense

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

    for cat, total in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        print(f"{cat:<15} ${total:.2f}")

    grand_total = sum(totals.values())
    print("-" * 26)
    print(f"{'TOTAL':<15} ${grand_total:.2f}\n")
