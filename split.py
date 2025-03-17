from collections import defaultdict
balances = defaultdict(int)
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

# Example transactions
transactions = [
    ('A', 'B', 20),
    ('B', 'C', 30),
    ('C', 'A', 25),
]

balances, simplified = simplify_debts(balances, transactions)



new_transactions = [    
    ('A', 'B', 15),
    ('B', 'C', 10),
    ('C', 'A', 35),
    ('A', 'B', 50),
    ('B', 'C', 40),
    ('C', 'A', 45),
    ('A', 'B', 60)]

balances, simplified = simplify_debts(balances, new_transactions)

print("Simplified transactions:")
for debtor, creditor, amount in simplified:
    print(f"{debtor} pays {creditor} ${amount}")