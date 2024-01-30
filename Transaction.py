import random
import string

import Database
from User import User


class Transaction:

    def __init__(self, sent_to, received_from, transaction_amount):
        self.transaction_id = "TN-"+randomStringGenerator(6)
        self.sent_to = sent_to
        self.received_from = received_from
        self.transaction_amount = transaction_amount
        self.transaction_time = User.dateFormatter


def getTransaction(transaction_id):
    transaction = Database.getTransaction(transaction_id)
    if transaction:
        return transaction


def getAllTransactions():
    transactions = Database.getTransactions()
    if transactions:
        return transactions


def randomStringGenerator(length):
    value = string.digits
    return ''.join(random.choice(value) for _ in range(length))
