from collections import defaultdict
def simplify_debts(balances, transactions):
    # Calculate net balances for each person
    for payer, payee, amount in transactions:
        balances[payer] -= amount
        balances[payee] += amount
   
    # Separate creditors and debtors
    creditors = sorted([(p, b) for p, b in balances.items() if b > 0], key=lambda x: -x[1])
    debtors = sorted([(p, b) for p, b in balances.items() if b < 0], key=lambda x: x[1])
   
    simplified_transactions = []
   
    # Settle debts
    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debtor, debt = debtors[i]
        creditor, credit = creditors[j]
       
        settled_amount = min(-debt, credit)
        simplified_transactions.append((debtor, creditor, settled_amount))
       
        # Update balances
        debtors[i] = (debtor, debt + settled_amount)
        creditors[j] = (creditor, credit - settled_amount)
       
        # Move to the next debtor or creditor if settled
        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1
   
    return balances, simplified_transactions