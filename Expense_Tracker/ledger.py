from decimal import Decimal, ROUND_HALF_UP, getcontext
from collections import defaultdict
from typing import List, Dict
from models import Expense, Settlement, Participant

getcontext().prec = 28

class Ledger:
    def __init__(self, participants: List[Participant]=None, expenses: List[Expense]=None):
        self.participants = participants or []
        self.expenses = expenses or []

    def add_expense(self, expense: Expense):
        self.expenses.append(expense)

    def compute_balances(self) -> Dict[str, Decimal]:
        """
        Returns net balance per participant id:
         - positive => they should receive money
         - negative => they owe money
        """
        balances = defaultdict(Decimal)
        for e in self.expenses:
            amt = Decimal(e.amount)
            n = Decimal(len(e.split_between))
            share = (amt / n).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            # payer receives full amount then owes their share if included
            balances[e.payer_id] += amt
            for pid in e.split_between:
                balances[pid] -= share
        # normalize to 2 decimals
        for k in list(balances.keys()):
            balances[k] = balances[k].quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return dict(balances)

    def settle_debts_greedy(self) -> List[Settlement]:
        """
        Greedy algorithm:
         - sort debtors (negative) and creditors (positive)
         - match largest debtor to largest creditor repeatedly
        Produces minimal number of transactions for practical group sizes.
        """
        balances = self.compute_balances()
        debtors = []
        creditors = []
        for pid, bal in balances.items():
            if bal < 0:
                debtors.append([pid, -bal])  # amount they owe as positive
            elif bal > 0:
                creditors.append([pid, bal])
        debtors.sort(key=lambda x: x[1], reverse=True)
        creditors.sort(key=lambda x: x[1], reverse=True)

        settlements: List[Settlement] = []
        i = j = 0
        while i < len(debtors) and j < len(creditors):
            d_id, d_amt = debtors[i]
            c_id, c_amt = creditors[j]
            transfer = min(d_amt, c_amt).quantize(Decimal("0.01"))
            settlements.append(Settlement(from_id=d_id, to_id=c_id, amount=transfer))
            d_amt -= transfer
            c_amt -= transfer
            if d_amt == 0:
                i += 1
            else:
                debtors[i][1] = d_amt
            if c_amt == 0:
                j += 1
            else:
                creditors[j][1] = c_amt
        return settlements
