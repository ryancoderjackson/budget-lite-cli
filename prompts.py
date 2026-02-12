from __future__ import annotations

from datetime import datetime


# ----------------------------
# Required prompts (create mode)
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
    """Date in YYYY-MM-DD. Enter defaults to today."""
    while True:
        value = input("Date (YYYY-MM-DD) [Enter for today]: ").strip()
        if value == "":
            return datetime.today().strftime("%Y-%m-%d")

        try:
            dt = datetime.strptime(value, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD (example: 2026-02-05).")


def prompt_month() -> str:
    """Month in YYYY-MM."""
    while True:
        value = input("Month (YYYY-MM), e.g. 2026-02: ").strip()
        try:
            datetime.strptime(value, "%Y-%m")
            return value
        except ValueError:
            print("Invalid month. Use YYYY-MM (example: 2026-02).")


# ----------------------------
# Optional prompts (edit mode)
# ----------------------------

def prompt_optional_nonempty(prompt: str, current: str) -> str:
    value = input(prompt).strip()
    return value if value else current


def prompt_optional_type(current: str) -> str:
    while True:
        value = input("Type (income/expense) [Enter to keep current]: ").strip().lower()
        if value == "":
            return current
        if value in {"income", "expense"}:
            return value
        print("Type must be 'income' or 'expense'.")


def prompt_optional_amount(current: float) -> float:
    while True:
        value = input("Amount (e.g., 12.50) [Enter to keep current]: ").strip()
        if value == "":
            return float(current)
        try:
            amount = float(value)
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Please enter a valid number (like 12.50).")


def prompt_optional_date(current: str) -> str:
    while True:
        value = input("Date (YYYY-MM-DD) [Enter to keep current]: ").strip()
        if value == "":
            return current
        try:
            dt = datetime.strptime(value, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD (example: 2026-02-05).")
