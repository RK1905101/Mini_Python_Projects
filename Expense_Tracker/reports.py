from rich.console import Console
from rich.table import Table
from tabulate import tabulate
from decimal import Decimal
from typing import Dict, List
from models import Participant, Expense, Settlement

console = Console()

def print_balances(participants: List[Participant], balances: Dict[str, Decimal]):
    table = Table(title="Net Balances")
    table.add_column("Name", style="bold")
    table.add_column("Balance", justify="right")
    id_to_name = {p.id: p.name for p in participants}
    for pid, bal in balances.items():
        table.add_row(id_to_name.get(pid, pid), f"{bal:.2f}")
    console.print(table)

def text_summary(participants: List[Participant], balances: Dict[str, Decimal]) -> str:
    id_to_name = {p.id: p.name for p in participants}
    rows = []
    for pid, bal in balances.items():
        rows.append([id_to_name.get(pid, pid), f"{bal:.2f}"])
    return tabulate(rows, headers=["Name", "Net Balance"], tablefmt="github")

def print_settlements(settlements: List[Settlement], participants: List[Participant]):
    table = Table(title="Settlement Plan (who pays whom)")
    table.add_column("From")
    table.add_column("To")
    table.add_column("Amount", justify="right")
    id_to_name = {p.id: p.name for p in participants}
    for s in settlements:
        table.add_row(id_to_name.get(s.from_id, s.from_id), id_to_name.get(s.to_id, s.to_id), f"{s.amount:.2f}")
    console.print(table)
