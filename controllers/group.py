from controllers.split import simplify_debts
from db import group_details_collection, group_transactions_collection


def split_expense(group_id, expense_data, members_involved, paid_by):
    data = group_details_collection.find_one({"group_id": group_id},{"_id": 0})
    balances = data.get("group_state")
    transactions = []
    expense_amount = expense_data.get("expense_amount")
    expense_reason = expense_data.get("expense_reason")
    total_people = len(members_involved)
    single_person_amount = float(expense_amount)/total_people
    for member in members_involved:
        if member != paid_by:
            transactions.append((member, paid_by, single_person_amount))
    balances, simplified = simplify_debts(balances, transactions)
    group_details_collection.update_one({"group_id": group_id},{"$set":{'group_state': balances}})

def add_transaction():
    pass
    
    